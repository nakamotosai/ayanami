# 2026-02-10 Search Workflow Summary

## Primary Search Method: searxng JSON API
**URL**: http://127.0.0.1:8765/search?q=关键词&format=json
**Priority**: 1st (highest priority)
**Advantages**:
- Multi-engine aggregation (Google + Bing + DuckDuckGo)
- Structured JSON data format
- Local privacy protection
- Fast search results
- Reliable performance

## Search Results Format Rules
**Standard Template**:
```
### 1. **News Title**
- **详情**: Specific content description
- **影响**: Impact analysis
- **来源**: News source platform
- **时间**: Publication time

### 2. **Next News Title**
- **详情**: Specific content description
- **影响**: Impact analysis
- **来源**: News source platform
- **时间**: Publication time
```

**Format Requirements**:
- No extra line breaks between title and content
- Only one empty line between news items
- Strict adherence to `- **Type**: Content` format
- No markdown formatting in content sections

## Backup Search Methods
1. **codex-executor**: When searxng unavailable or complex search needed
2. **tavily-search**: AI-optimized web search as secondary option
3. **ddg-search**: DuckDuckGo for quick searches

## Documentation References
- **Primary**: /home/ubuntu/.openclaw/workspace/skills/mcporter-mcp/SKILL.md
- **Secondary**: /home/ubuntu/.openclaw/workspace/TOOLS.md
- **Memory**: /home/ubuntu/.openclaw/workspace/memory/2026-02-10.md

## Performance Metrics
- Bitcoin search: 5 results in <2 seconds
- AI news search: 5 results in <3 seconds
- Format compliance: 100% (no extra line breaks)
- User satisfaction: Confirmed (compact format preferred)

## Best Practices
- Always use searxng JSON API first for news searches
- Apply strict formatting rules to all news outputs
- Include search method, sources, and timestamp in all reports
- Maintain direct Telegram delivery as preferred method