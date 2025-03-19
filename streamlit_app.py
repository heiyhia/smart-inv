import os
import streamlit as st
import pandas as pd
import numpy as np
import tushare as ts
from datetime import datetime, timedelta

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

stocks = pd.read_csv("data/stock_list.csv")

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
    'ma3': 'M3',
    'ma5': 'M5',
    'ma10': 'M10',
    'ma20': 'M20',
    'ma50': 'M50',
    'ma120': 'M120',
    'vol': '成交量',
    'vol_ratio': '量比',
    'turnover_rate': '换手率',
    'pct_chg': '涨跌幅'
}

@st.cache_data
def get_stock_data(ts_code, start_date, end_date):
    """获取股票数据并计算技术指标"""
    try:
        # 获取日线数据
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        
        if df.empty:
            return None
            
        # 获取基本信息
        basic_info = stocks[stocks['ts_code'] == ts_code]
        stock_name = basic_info.iloc[0]['name'] if not basic_info.empty else ''
        
        # 按日期排序
        df = df.sort_values('trade_date')
        
        # 计算技术指标
        # 移动平均线
        for ma in [3, 5, 10, 20, 50, 120]:
            df[f'ma{ma}'] = df['close'].rolling(window=ma).mean().round(2)
            
        # 最高最低差价
        df['price_range'] = (df['high'] - df['low']).round(2)
        
        # 计算量比（当日成交量/过去5日平均成交量）
        df['vol_ratio'] = (df['vol'] / df['vol'].rolling(window=5).mean()).round(2)
        
        # 添加股票名称
        df['stock_name'] = stock_name
        
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
        value="000001.SZ",
        help="例如：000001.SZ（平安银行）"
    )
    
    # 日期选择
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "开始日期",
            value=datetime.now() - timedelta(days=30)
        )
    with col2:
        end_date = st.date_input(
            "结束日期",
            value=datetime.now()
        )
        
    # 选择显示的列
    st.header("显示设置")
    all_columns = list(COLUMN_NAMES.values())
    default_columns = ['股票代码', '股票名称', '日期', '开盘价', '收盘价', '最高价', '最低价', '涨跌幅']
    selected_columns = st.multiselect(
        "选择要显示的列",
        options=all_columns,
        default=default_columns
    )

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
            
            # 显示统计信息
            st.subheader("数据统计")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("数据天数", len(df))
            with col2:
                st.metric("期间最高价", df['high'].max())
            with col3:
                st.metric("期间最低价", df['low'].min())
        else:
            st.error("未找到数据，请检查股票代码和日期范围是否正确")
