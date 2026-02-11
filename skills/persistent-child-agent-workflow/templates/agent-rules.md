# Persistent Child Agent Rules

1. **Availability** – Keep `heartbeat` enabled and ensure the agent reports health to the gateway every 60 seconds.
2. **Bindings** – Limit outbound bindings to pre-approved channels listed in `bindings/bindings.yaml`.
3. **Commands** – Accept only `status`, `pause`, `resume`, `restart`, `shutdown`. All other commands should be rejected with a polite explanation.
4. **Data Guardrails** – Never persist secrets in plaintext. Use the parent agent's vault or config store.
5. **Logging** – Write structured JSON logs into `logs/always-on.log` and rotate daily.
