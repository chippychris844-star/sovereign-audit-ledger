# Sovereign RA Engine v3.2

ChatGPT-style local RA assistant with Resolution Assurance colours, RA Refinery verification, local-private storage, hosted model support, WordPress REST retrieval, opt-in file access, and tamper-evident audit logs.

## One-click start

1. Extract the ZIP.
2. Double-click `ONE CLICK SETUP - CREATE DESKTOP ICON.bat` once.
3. Use the `Sovereign RA Engine` desktop icon.

## What is wired

- OpenAI hosted drafting, if an OpenAI key is present.
- Anthropic hosted drafting, if an Anthropic key is present.
- Ollama local drafting, if Ollama is running.
- WordPress REST API retrieval for posts/pages, if WordPress site URL and application password/API token are present.
- RA knowledge graph retrieval.
- Opt-in file search/read/write inside allowed folders only.
- Live retrieval trace showing graph, files, WordPress, web, hosted/local model, and RA Refinery steps.
- Verified / Partially Verified / Not Verified / Insufficient Evidence badges.
- Local settings storage in `data/private/settings.json`.
- Hash-chained audit log in `logs/sovereign_audit.jsonl`.

## API key discovery

On startup, `START.bat` runs `scripts/connect_keys.mjs --startup`. It scans D: and common folders for local files containing:

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `WORDPRESS_SITE_URL` or `WP_SITE_URL`
- `WORDPRESS_USERNAME` or `WP_USERNAME`
- `WORDPRESS_API_KEY`, `WORDPRESS_APPLICATION_PASSWORD`, `WP_API_KEY`, or `WP_APP_PASSWORD`

Raw secrets are not displayed in the UI. Only masked values are shown.

## Settings

Open Settings inside the app to enable or test:

- Hosted provider
- OpenAI/Anthropic/Ollama models
- WordPress site/user/app password
- Web candidates
- WordPress candidates
- Local graph
- Opt-in file access and file writes
- Retrieval process visibility
- Parallel retrieval for lower lag

## Privacy model

Airgap and Evidence Lockdown modes do not call external hosted services. Hybrid Verified and Full Capability can call hosted tools when enabled. Hosted output is always draft-only and must pass through RA Refinery before display.


## v3.3 Ownership Guard / Lawful Data Gate

This build adds a strict local provenance layer so retrieved data is not blindly used. Before any draft answer is created, the engine classifies every retrieved item as owned, public candidate, needs review, or blocked. In strict mode, only locally anchored RA graph nodes, files inside user-approved folders, and WordPress/web results from approved owned domains are allowed. Unapproved items are quarantined and excluded from the answer.

Use Settings > Run ownership audit to review stored graph/chat/audit evidence. This tool cannot give legal advice or certify provider-side legality, but it helps keep the local engine from mixing in data that is not yours or not approved by you.
