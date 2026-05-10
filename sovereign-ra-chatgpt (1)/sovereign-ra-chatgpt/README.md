# Sovereign RA Engine v4.0

A ChatGPT-style local AI gateway for Resolution Assurance. The user experience is designed to feel like a normal modern assistant, with one visible difference: every answer is passed through RA Refinery and labelled **Verified**, **Partially Verified**, **Not Verified**, or **Insufficient Evidence**.

## What v4 adds

- Resolution Assurance colour system: wine, burgundy, gold, cream.
- ChatGPT-style layout: left chat rail, centered messages, bottom composer, quick provider switcher.
- Hosted model wiring: OpenAI, Anthropic, and Ollama.
- Browsing candidates, WordPress REST retrieval, RA graph search, approved local files.
- Live retrieval panel showing what the engine is fetching and checking.
- File attachment flow: uploaded text files are anchored into the local RA graph.
- Apps & tools panel showing connected tools and privacy mode.
- Local JavaScript code sandbox for safe quick calculations/snippets.
- Stricter RA Refinery: high-impact claims such as valuations are downgraded unless strongly supported.
- Hash-chained audit log.
- Ownership guard remains on by default.

## Run

1. Extract the ZIP.
2. Double-click `ONE CLICK SETUP - CREATE DESKTOP ICON.bat` once.
3. Use the `Sovereign RA Engine` desktop icon.

Or run manually:

```bat
cd /d path\to\sovereign-ra-chatgpt
START.bat
```

Open: http://localhost:3030

## Privacy modes

- **Airgap**: local graph/files only; no external calls.
- **Hybrid verified**: best default; uses enabled tools as candidates and verifies through RA Refinery.
- **Full capability**: hosted tools allowed for maximum capability.
- **Evidence lockdown**: no external calls; preservation mode.

## Important rule

Hosted AI output is never final truth. It is draft material. RA Refinery checks it against approved evidence before the user sees the answer status.
