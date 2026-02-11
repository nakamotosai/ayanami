# Persistent Child Agent Workflow Skill

## Skill overview
This skill captures the full workflow for standing up a **persistent/always-on child agent** under the OpenClaw umbrella. It codifies the actions you routinely repeat when creating a workspace, copying the parent core files, defining agent-specific rules, applying bindings, and preparing gateway configuration patches.

### What you get
- `scripts/create-persistent-child-agent.sh` – scaffolds a workspace, copies the core files (AGENTS/SOUL/USER/MEMORY/TOOLS), and drops policy/binding/gateway templates.
- `templates/agent-rules.md` – a ready-to-edit rulebook for the child agent.
- `templates/bindings.yaml` – binding scaffold for telegram and HTTP channels.
- `templates/gateway-config.patch` – patch template to register the agent with the gateway config.

## Workflow summary
1. **Define agent metadata** – pick a name (for example `chii-always-on`), decide on a workspace root, and optionally allow re-using an existing directory.
2. **Run the scaffolding script** – `./skills/persistent-child-agent-workflow/scripts/create-persistent-child-agent.sh <name> [options]`. This performs:
   - Workspace creation with directories for scripts, config, policies, and bindings.
   - Core file copy from the repository root so child agents inherit AGENTS/SOUL/USER/MEMORY/TOOLS context.
   - Template placement for rules, bindings, and gateway patch.
3. **Edit the agent-specific files** – update `policies/agent-rules.md`, `bindings/bindings.yaml`, and `config/gateway-config.patch` with real identifiers (workspace path, telegram IDs, etc.).
4. **Integrate with gateway** – apply the patch via `git apply templates/gateway-config.patch` or manually merge into your gateway manifest. Adjust the `agents.*.workspace` path to the real workspace location.
5. **Launch the agent** – start it via the parent orchestration (e.g., `openclaw agent spawn ...`) referencing the new workspace, ensuring the gateway sees the new binding and config.

## Script usage
```bash
cd /home/ubuntu/.openclaw/workspace
./skills/persistent-child-agent-workflow/scripts/create-persistent-child-agent.sh chii-always-on \
  --workspace-root /home/ubuntu/.openclaw/persistent \
  --allow-existing
```
- `--workspace-root` overrides where the child workspace is created.
- `--allow-existing` skips the "already exists" guard when you just need to refresh templates.
- The created workspace contains a `README.md`, copies of AGENTS/SOUL/USER/MEMORY/TOOLS, and directories for scripts, config, policies, and bindings.

## Template fill-in guidance
| Template | Description | Fields to replace |
| --- | --- | --- |
| `agent-rules.md` | Guardrails for the always-on agent's behavior | Replace generic policies with your team's expectations (e.g., authorized channels, logging cadence).
| `bindings.yaml` | Defines inbound/outbound bindings | Fill `{{TELEGRAM_ID}}`, `{{TELEGRAM_ID_BACKUP}}`, `{{AGENT_NAME}}`.
| `gateway-config.patch` | Example `git apply` patch to register the agent with the gateway | Replace `{{AGENT_NAME}}`, `{{WORKSPACE_PATH}}`, and binding references.

## Peer ID formatting (new lesson)
- Always store channel peer IDs as **strings** in `bindings.yaml`/`openclaw.json` (e.g., `"-1003700261569"`). The gateway schema rejects numeric values and will fail validation if you accidentally write bare numbers. Convert any integers inserted by scripts before saving and rerun the sync script to rewrite the config.

## Reference files
See `REFERENCES.md` for a curated list of relevant docs, scripts, and config files.
