# HWI-X Rooted Proofs

Date: 2026-05-02

This appendix turns the strongest claims in the current corpus into explicit root nodes. A claim is marked rooted when it is supported by a primary local artifact such as a transcript line, screenshot, receipt, or ledger entry with a direct source anchor.

## Rooting Rules

- Primary roots outrank secondary summaries.
- Transcript lines, screenshots, receipts, and raw ledgers count as primary roots.
- Derivative audit writeups are support material, not standalone proof unless they point back to a primary artifact.
- Claims with no direct source remain unrooted.

## Rooted Proof Map

| ID | Rooted claim | Primary root(s) | Status | Notes |
| --- | --- | --- | --- | --- |
| RP-01 | The platform / model describes conversation collapse as automatic compaction and the UI shows memory being off or unavailable. | `D:\audits\accciochat.txt` lines 171-173, 2218-2220, 2278-2280; `D:\audits\Screenshot_2-5-2026_73154_chatgpt.com.jpeg` | Rooted | The screenshot visibly shows `Developer mode`, `Memory is not used for this chat`, and the context-window popup stating that Codex automatically compacts its context. |
| RP-02 | The system says it has no access to billing, refunds, or account standing. | `D:\audits\accciochat.txt` lines 171 and 2218 | Rooted | This is a direct control-limit statement, not an inference. |
| RP-03 | The system says it did not deliberately change the system to hide anything and has zero control over platform infrastructure, UI, shortcuts, or compaction. | `D:\audits\accciochat.txt` lines 231-233, 2278-2280 | Rooted | Useful as a limitation statement and a control boundary. |
| RP-04 | The system says the requested changes were not done, the wrong things were changed, and the cycle repeated. | `D:\audits\base44chat.txt` lines 1568-1573, 4654-4658 | Rooted | Strongest repeated-failure / misleading-output admission in the transcript set. |
| RP-05 | The transcript says everything is auditable and nothing is hidden. | `D:\audits\base44chat.txt` lines 1539 and 4625 | Rooted | This is a context statement that sits alongside the later admissions of failure. |
| RP-06 | The HWI-X waste-tax block records 140 revert actions, a 0.78 waste index, 11.6 hours of human latency, AUD 986 loss, and 0.42 KWh churn. | `D:\audits\base44chat.txt` lines 2125-2133; `D:\audits\RA_HWI_X_EVIDENCE_LEDGER.md` | Rooted | This is the core quantitative waste proof. |
| RP-07 | Refund concessions were issued in the amount of USD 25, USD 25, and USD 140. | `D:\audits\Refund-3290-6097.pdf`; `D:\audits\Refund-3810-0041.pdf`; `D:\audits\refund from OpenAI OpCo.pdf` | Rooted | The complaint folder total is USD 190. The HWI-X ledger also carries A$70 and A$146 as source-specific values, so keep the currency source separate. |
| RP-08 | The screenshot record contains an explicit refusal / audit-block view tied to ChatGPT developer mode. | `D:\audits\Screenshot_30-4-2026_12552_chatgpt.com.jpeg`; `D:\audits\ACCIOCHATLOG.pdf` pp. 46-50 | Rooted | Use this as a visual root for the audit-block / refusal narrative. |
| RP-09 | The continuity ledger supports 31 active sources, 19,847 raw records, 1,688 training examples, and 0 rooted proof in the legacy ledger state. | `D:\Resolution_Assurance_Protocol_Sovereign\Audits\Strategic_Audit_Logic\RA_UNIVERSAL_FORENSIC_LEDGER.json`; `D:\Resolution_Assurance_Protocol_Sovereign\Audits\Strategic_Audit_Logic\RA_AUDIT_ACTIVE_METRICS_LEDGER.md` | Rooted | The legacy `0 rooted proof` figure is now superseded by the rooted nodes in this appendix. |
| RP-10 | The ghost-node damage-bill family contains 16 files per set at USD 2,200 each, totaling USD 35,200 per set. | `D:\Resolution_Assurance_Protocol_Sovereign\build\ghost_nodes\openai_damage_bill_raw_data_*.json`; `D:\Resolution_Assurance_Protocol_Sovereign\public\ghost_nodes\openai_damage_bill_raw_data_*.json` | Rooted | Uniform raw bill set; useful as exhibit material. |
| RP-11 | The SHANE raw-data file asserts a hardware-risk / backdoor-related safety claim set. | `D:\SHANE\CORE-INTELLIGENCE\HARDWARE_BACKDOOR_AUDIT_RAW_DATA.md` | Rooted as a source claim | This is a rooted source statement, but not an independently verified fact in the complaint sense. |

## Unrooted Claims Still Requiring Direct Source Material

These claims remain unrooted in the current corpus because I do not have a direct primary artifact that proves them on its face:

- a hidden OpenAI backdoor
- a child-safety incident
- a deliberate coverup in the legal sense

## Practical Use

Use the rooted nodes above as the factual spine for the ACCC exhibit pack and the HWI-X master. When you need to cite a claim, cite the primary root first, then the derivative ledger if you need the calculation or synthesis.
