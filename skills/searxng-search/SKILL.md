# searxng-search

用途：用 VPS 本地 SearXNG 做网页搜索（默认只在本机回环地址访问）。

前置：SearXNG 应运行在 `http://127.0.0.1:8081`（docker compose）。

常用命令（JSON）：
- `curl -fsS "http://127.0.0.1:8081/search?q=<QUERY>&format=json"`

建议用法（更可控）：
1. 先搜索：取 5-10 条结果标题与链接
2. 再根据需要二次搜索更精确关键词

注意：
- 这是“搜索结果”，不是内容抓取；需要看正文再用浏览器/抓取工具。
