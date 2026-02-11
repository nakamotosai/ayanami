---
name: structured-markdown-doc
description: "When the user asks for a Markdown (.md) document, automatically collect the sections, craft structured Markdown, save it to a workspace file, and send the file back without further prompting."
---

# Markdown Output Workflow

1. **Clarify scope**: If the request does not include headings/sections/data, ask for the purpose, required tables/checklists, and desired tone/length. Confirm the preferred file name (default `structured-summary.md`).

2. **Write the document**:
   - Use the latest persona/context (SOUL rules, user preferences, ongoing project updates).
   - Organize output with sensible headings, numbered lists, tables, etc. Include metadata (title + short intro) when helpful.
   - Keep each section concise but informative; avoid fluff and repeat only what the user needs.

3. **Save and attach**:
   - Save the Markdown to `workspace/<user-specified-name>.md` (default `structured-summary.md`) ensuring the content matches the final response.
   - When replying, send a brief note referencing the attachment and mention how to convert to other formats if needed (Pandoc/Word).

4. **Follow-up**:
   - Mention in the reply that the file is attached and remind the user about conversion options.
   - Write a short sentence to `memory/YYYY-MM-DD.md` noting the document delivered.
   - Keep tone aligned with SOUL (playful, brief, honest).

Use this skill whenever the user explicitly requests a Markdown file or says "need an MD/doc"; do not trigger when the user only wants inline text unless they add the file requirement. Always include the attachment before closing the turn.