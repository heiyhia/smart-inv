# 股票数据查询系统

一个简单的股票数据查询系统，可以查询指定股票在特定时间范围内的行情数据。

## 功能特点

- 支持输入股票代码和时间区间进行查询
- 显示完整的股票日线数据，包括价格、成交量等信息
- 自动计算各项移动平均线指标(M3, M5, M10, M20, M50, M120)
- 支持按列排序
- 响应式设计，适配各种屏幕尺寸
- 部署在Cloudflare上，访问快速稳定

## 使用方法

1. 在输入框中输入股票代码（如：000001）
2. 选择起始日期和结束日期
3. 点击查询按钮获取数据
4. 可以点击表格标题栏进行排序

## 技术栈

- 纯JavaScript实现
- 使用Tushare API获取数据
- Cloudflare Workers部署

## 部署说明

1. 克隆本仓库
2. 安装 Wrangler CLI:
   ```bash
   npm install -g @cloudflare/wrangler
   ```
3. 登录到 Cloudflare:
   ```bash
   wrangler login
   ```
4. 修改 wrangler.toml:
   - 填写你的 Cloudflare account_id
   - 确认 TUSHARE_TOKEN 设置正确
5. 部署 Worker:
   ```bash
   wrangler publish
   ```
6. 修改 config.js 中的 API_URL 为你的 Worker URL
7. 部署前端文件到你的网站服务器或 Cloudflare Pages

## 注意事项

- 确保 Cloudflare Worker 的 URL 在 config.js 中配置正确
- Tushare API Token 已通过 Cloudflare Worker 环境变量安全存储
- 建议在生产环境中限制 CORS 的 Access-Control-Allow-Origin 为特定域名 