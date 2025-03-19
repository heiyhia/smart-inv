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

2. 部署 Cloudflare Worker:
   ```bash
   cd worker
   npm install -g @cloudflare/wrangler
   wrangler login
   ```

3. 修改 worker/wrangler.toml:
   - 填写你的 Cloudflare account_id
   - 确认 TUSHARE_TOKEN 设置正确

4. 部署 Worker:
   ```bash
   wrangler deploy
   ```
   部署成功后，你会获得一个 Worker URL，类似：
   https://stock-data-api.xxx.workers.dev

5. 修改前端配置:
   - 打开 frontend/config.js
   - 将 API_URL 更新为你的 Worker URL

6. 部署前端文件:
   可以选择以下任一方式：
   - 部署到 Cloudflare Pages
   - 部署到任何静态网站托管服务
   - 直接在本地打开 index.html 文件

## 本地开发

1. 启动 Worker 开发服务器:
   ```bash
   cd worker
   wrangler dev
   ```
   这会启动一个本地开发服务器，并提供一个本地测试 URL

2. 更新前端配置:
   - 临时修改 frontend/config.js 中的 API_URL 为本地 Worker URL
   - 直接打开 frontend/index.html 进行测试

## 注意事项

- 确保 worker.js 和 wrangler.toml 在同一目录下
- 部署前确认 wrangler.toml 中的配置正确
- 本地开发时使用 `wrangler dev` 进行测试
- 生产环境部署使用 `wrangler deploy`

- 确保 Cloudflare Worker 的 URL 在 config.js 中配置正确
- Tushare API Token 已通过 Cloudflare Worker 环境变量安全存储
- 建议在生产环境中限制 CORS 的 Access-Control-Allow-Origin 为特定域名 