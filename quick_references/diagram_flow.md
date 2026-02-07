# Diagram Crafter Quick Reference

## When to use
- Visualize Learner's workflows or the knowledge hub pipeline for easy sharing.
- Turn Mermaid/flowchart text into PNG diagrams you can send back to主人 or embed into reports.

## Steps
1. Create a Mermaid diagram definition somewhere (e.g., `/tmp/learner-flow.mmd`):
   ```mmd
   graph TD
     A[Learner Trigger] --> B[Fetch sources]
     B --> C[Generate cards + reports]
     C --> D[Sync knowledge hub]
   ```
2. Render it:
   ```bash
   ./skills/diagram-crafter/scripts/render_diagram.sh -i /tmp/learner-flow.mmd -o /tmp/learner-flow.png
   ```
3. Send `/tmp/learner-flow.png` back to you or store it alongside the skill output.

## Pro tip
- Learner can include the Mermaid text in the skill output (cards/reports) then run this script to auto-build the diagram and share the PNG.
- Or skip local Chrome by calling `skills/learner-docs/scripts/render_diagram_remote.py --mermaid=<file> --output=<png>`; it posts to Kroki and saves the PNG in `skills/learner-docs/reports/` so other agent can fetch the asset.
- Mention `diagram-crafter quick reference` whenever you want me to generate a diagram for you.
