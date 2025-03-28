import os
import streamlit as st
import pandas as pd
import numpy as np
import tushare as ts
from datetime import datetime, timedelta
import easyquotation as eq
import pytz

# 设置页面配置
st.set_page_config(
    page_title="数据分析系统",
    page_icon="📈",
    layout="wide"
)

# 设置 Tushare Token
token = st.secrets["TUSHARE_TOKEN"]
ts.set_token(token)
pro = ts.pro_api()

# 页面标题
st.title("📈 数据分析系统")
st.write(
    """
    这是一个数据分析系统，可以查询和分析股票的历史行情数据。数据来源于 Tushare Pro。
    """
)

stocks = pd.read_csv("data/stock_list.csv", dtype={'ts_code': str, 'symbol': str})

# 定义列名映射
COLUMN_NAMES = {
    'ts_code': '股票代码',
    'stock_name': '股票名称',
    'trade_date': '日期',
    'open': '开盘价',
    'close': '收盘价',
    'high': '最高价',
    'low': '最低价',
    'price_range': '最高最低差价',
    'amplitude': 'T涨幅差',
    'pct_chg': '涨跌幅%',
    'ma3': 'M3',
    'ma5': 'M5',
    'ma10': 'M10',
    'ma20': 'M20',
    'ma30': 'M30',
    'ma50': 'M50',
    'ma120': 'M120',
    'vol': '成交量',
    'vol_ratio': '量比',
    'turnover_rate': '换手率',
    'macd_hist': 'MACD柱状图'
}

def calculate_macd(df, fast=12, slow=26, signal=9):
    """计算MACD指标
    
    Args:
        df: DataFrame, 包含收盘价数据的DataFrame
        fast: int, 快线周期，默认12
        slow: int, 慢线周期，默认26
        signal: int, 信号线周期，默认9
        
    Returns:
        DataFrame: 添加了MACD指标的DataFrame
    """
    # 计算快线和慢线的EMA
    exp1 = df['close'].ewm(span=fast, adjust=False).mean()
    exp2 = df['close'].ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    
    # 计算信号线
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    
    # 计算MACD柱状图
    hist = macd - signal_line
    
    # 添加到DataFrame
    df['macd'] = macd.round(2)
    df['macd_signal'] = signal_line.round(2)
    df['macd_hist'] = hist.round(2)
    
    return df

def get_today_quote(ts_code):
    """获取当日行情数据
    
    Args:
        ts_code: str, 股票代码(格式: 000001.SZ)
        
    Returns:
        dict: 当日行情数据，如果市场未收盘则返回 None
    """
    # 转换 ts_code 为 easyquotation 格式 (000001.SZ -> 000001)
    code = ts_code.split('.')[0]
    
    # 获取当前时间(使用中国时区)
    tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(tz)
    
    # 如果是交易日且在15:00后
    if now.weekday() < 5 and now.hour >= 15:
        try:
            qq = eq.use('tencent')
            quote = qq.real(code)[code]
            
            # 转换为与 tushare 相同的格式
            today_data = {
                'ts_code': ts_code,
                'trade_date': now.strftime('%Y%m%d'),
                'open': quote['open'],
                'high': quote['high'],
                'low': quote['low'],
                'close': quote['now'],  # 现价即收盘价
                'vol': quote['volume'] / 100,  # 转换为手
                'amount': quote['成交额(万)'] * 10000,  # 转换为元
                'pct_chg': quote['涨跌(%)'],
                'turnover_rate': quote['turnover']
            }
            return today_data
        except Exception as e:
            st.warning(f"获取当日行情失败: {str(e)}")
            return None
    return None

@st.cache_data
def get_stock_data(ts_code, start_date, end_date):
    """获取股票数据并计算技术指标"""
    try:
        if not ts_code.endswith('.SZ') and not ts_code.endswith('.SH'):
            ts_code = stocks[stocks['symbol'] == ts_code].iloc[0]['ts_code']
        # 获取日线数据
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        
        if df.empty:
            return None
            
        # 获取基本信息
        basic_info = stocks[stocks['ts_code'] == ts_code]
        stock_name = basic_info.iloc[0]['name'] if not basic_info.empty else ''
        
        # 按日期降序排序
        df = df.sort_values('trade_date', ascending=True)
        
        # 计算技术指标
        # 移动平均线
        for ma in [3, 5, 10, 20, 30, 50, 120]:
            df[f'ma{ma}'] = df['close'].rolling(window=ma).mean().round(2)
            
        # 最高最低差价
        df['price_range'] = (df['high'] - df['low']).round(2)
        
        # 计算量比（当日成交量/过去5日平均成交量）
        df['vol_ratio'] = (df['vol'] / df['vol'].rolling(window=5).mean()).round(2)
        
        # 计算T幅度差 (收盘价 - 开盘价)
        df['amplitude'] = (df['close'] - df['open']).round(2)
        
        # 涨跌幅保留2位小数
        df['pct_chg'] = df['pct_chg'].round(2)
        
        # 计算MACD指标
        df = calculate_macd(df)
        
        # 添加股票名称
        df['stock_name'] = stock_name

        df = df.sort_values('trade_date', ascending=False)
        
        return df
    except Exception as e:
        st.error(f"获取数据时发生错误: {str(e)}")
        return None

# 创建侧边栏输入
with st.sidebar:
    st.header("查询参数")
    
    # 股票代码输入
    stock_code = st.text_input(
        "股票代码",
        value="000839.SZ",
        help="000839.SZ（中信国安）"
    )
    
    # 日期选择
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "开始日期",
            value=datetime.now() - timedelta(days=90)  # 增加默认天数以确保有足够数据计算MACD
        )
    with col2:
        end_date = st.date_input(
            "结束日期",
            value=datetime.now()
        )
        
    # 选择显示的列
    st.header("显示设置")
    all_columns = list(COLUMN_NAMES.values())
    default_columns = ['股票代码', '股票名称', '日期', '开盘价', '收盘价', '最高价', '最低价', 
                      'T涨幅差', '涨跌幅%', 'MACD柱状图', 'M5', 'M10', 'M20',
                      '最高最低差价']
    selected_columns = st.multiselect(
        "选择要显示的列",
        options=all_columns,
        default=default_columns
    )
    
    # MACD参数设置
    st.header("MACD参数设置")
    macd_fast = st.slider("快线周期", min_value=5, max_value=30, value=12)
    macd_slow = st.slider("慢线周期", min_value=10, max_value=50, value=26)
    macd_signal = st.slider("信号线周期", min_value=3, max_value=20, value=9)

# 查询按钮
if st.sidebar.button("查询"):
    if not stock_code:
        st.error("请输入代码")
    else:
        # 转换日期格式
        start_date_str = start_date.strftime("%Y%m%d")
        end_date_str = end_date.strftime("%Y%m%d")
        
        # 获取数据
        with st.spinner("正在获取数据..."):
            df = get_stock_data(stock_code, start_date_str, end_date_str)
            
        if df is not None and not df.empty:
            # 使用自定义MACD参数重新计算MACD (如果参数与默认值不同)
            if macd_fast != 12 or macd_slow != 26 or macd_signal != 9:
                df = calculate_macd(df, fast=macd_fast, slow=macd_slow, signal=macd_signal)
                
            # 重命名列
            df_display = df.copy()
            for old_name, new_name in COLUMN_NAMES.items():
                if old_name in df_display.columns:
                    df_display = df_display.rename(columns={old_name: new_name})
            
            # 选择要显示的列
            df_display = df_display[selected_columns]
            
            # 显示数据表格
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True
            )
            
            # 显示MACD图表
            st.subheader("MACD图表")
            
            # 准备图表数据 (使用原始日期顺序)
            chart_data = df.sort_values('trade_date', ascending=True).copy()
            chart_data['trade_date'] = pd.to_datetime(chart_data['trade_date'])
            
            # 创建图表
            fig_macd = {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "MACD",
                        "x": chart_data['trade_date'],
                        "y": chart_data['macd'],
                        "line": {"color": "blue"}
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "信号线",
                        "x": chart_data['trade_date'],
                        "y": chart_data['macd_signal'],
                        "line": {"color": "red"}
                    },
                    {
                        "type": "bar",
                        "name": "柱状图",
                        "x": chart_data['trade_date'],
                        "y": chart_data['macd_hist'],
                        "marker": {
                            "color": chart_data['macd_hist'].apply(
                                lambda x: 'red' if x > 0 else 'green'
                            )
                        }
                    }
                ],
                "layout": {
                    "title": f"{stock_code} MACD指标 ({macd_fast},{macd_slow},{macd_signal})",
                    "xaxis": {"title": "日期"},
                    "yaxis": {"title": "值"},
                    "legend": {"x": 0, "y": 1.1, "orientation": "h"},
                    "height": 400,
                }
            }
            
            st.plotly_chart(fig_macd, use_container_width=True)
            
            # 显示统计信息
            st.subheader("数据统计")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("数据天数", len(df))
            with col2:
                st.metric("期间最高价", df['high'].max())
            with col3:
                st.metric("期间最低价", df['low'].min())
            with col4:
                # 显示最新的MACD柱状图值，正值表示看涨，负值表示看跌
                latest_hist = df.iloc[0]['macd_hist']
                st.metric("最新MACD柱状图", f"{latest_hist:.2f}", 
                         delta="看涨信号" if latest_hist > 0 else "看跌信号")
        else:
            st.error("未找到数据，请检查股票代码和日期范围是否正确")
