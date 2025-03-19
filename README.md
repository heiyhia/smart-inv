# 📈 股票数据分析系统

一个基于 Streamlit 的股票数据分析系统，可以查询和分析股票的历史行情数据。

## 功能特点

- 支持输入股票代码和时间区间进行查询
- 显示完整的股票日线数据，包括：
  - 基本行情：开盘价、收盘价、最高价、最低价等
  - 技术指标：M3、M5、M10、M20、M50、M120等均线
  - 成交指标：成交量、量比、换手率等
- 支持自定义显示列
- 数据来源：Tushare API

## 使用前准备

1. 注册 [Tushare Pro](https://tushare.pro/) 账号并获取 token
2. 在项目根目录创建 `.env` 文件，添加你的 token：
   ```
   TUSHARE_TOKEN=your_token_here
   ```

## 安装和运行

1. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

2. 运行应用：
   ```bash
   streamlit run streamlit_app.py
   ```

## 使用说明

1. 在输入框中输入股票代码（如：000001.SZ）
2. 选择查询的起始日期和结束日期
3. 选择要显示的数据列
4. 点击查询按钮获取数据

## 数据说明

- 股票代码格式：
  - 沪市A股：`600xxx.SH`、`601xxx.SH`、`603xxx.SH`
  - 深市A股：`000xxx.SZ`、`002xxx.SZ`、`300xxx.SZ`
- 数据更新频率：每日收盘后更新
- 历史数据范围：最近10年

## 技术栈

- Python
- Streamlit
- Tushare API
- Pandas
- NumPy
