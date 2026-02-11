# 2026-02-10 Skills Memory

## mcporter-mcp Skill Updates
**Modification Date**: 2026-02-10
**Version**: Enhanced with strict formatting rules

### New Features Added:
1. **News Output Standardization**
   - Title format: `### N. **News Title**`
   - Content format: `- **Type**: Content` (no extra line breaks)
   - Separation: Only one empty line between news items

2. **Format Enforcement Rules**
   - No line breaks between title and content
   - No extra empty lines within single news item
   - Strict adherence to specified bullet point format
   - Consistent across all search results

3. **searxng JSON API Priority**
   - Primary search method for all news queries
   - Standard implementation: `curl -s "http://127.0.0.1:8765/search?q=关键词&format=json" | head -50`
   - Error handling and fallback mechanisms

### User Requirements Implemented:
- Compact news format without unnecessary line breaks
- Direct delivery via Telegram as preferred method
- Consistent formatting across all search results
- Evidence-based reporting with source attribution

### Files Modified:
- `/home/ubuntu/.openclaw/workspace/skills/mcporter-mcp/SKILL.md`
- Added comprehensive format section under "📝 News Output Standard Format"

### Testing Results:
- Bitcoin news search: 5 results with perfect formatting compliance
- AI industry news search: 5 results with perfect formatting compliance
- User feedback: Format approved as cleaner and more readable

### Future Considerations:
- Monitor user satisfaction with current formatting
- Adjust format rules based on future feedback
- Continue prioritizing searxng JSON API for searches
- Maintain documentation updates as workflows evolve