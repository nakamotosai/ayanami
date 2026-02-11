---
name: diagram-crafter
description: Render Mermaid/flowchart diagrams to PNG so you can visualize any workflow or knowledge map quickly.
---

# Diagram Crafter Skill

## Overview
This skill lets you turn Mermaid or DOT flowchart descriptions into PNG/PNG images using the globally installed `@mermaid-js/mermaid-cli` (`mmdc`). You can feed Learner a flowchart text and get a visual asset ready for sharing.

## Usage
1. Save your Mermaid definition into a `.mmd` file (Learner can generate one programmatically or you can paste it). Example:
   ```bash
   cat <<'EOF' > /tmp/learner-flow.mmd
   graph TD
     A[Start] --> B{Fetch docs}
     B --> C[Summary]
   EOF
   ```
2. Run the renderer:
   ```bash
   ./skills/diagram-crafter/scripts/render_diagram.sh -i /tmp/learner-flow.mmd -o /tmp/learner-flow.png
   ```
3. The PNG will appear at the path you specified. Share it, embed it, or send it back to the user.

## Integration
Learner can call this script after [`skills/learner-docs`] cards or reports are ready to visualize the workflow. Just feed the Mermaid text, run the script, and send back the generated PNG for quick confirmation.
