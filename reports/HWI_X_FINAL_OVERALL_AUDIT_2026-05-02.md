# HWI-X Final Overall Audit

Date: 2026-05-02

This is the combined, source-based summary of the current HWI-X corpus. It folds together the continuous audit, waste-tax audit, rooted proofs, continuity ledger, refund record, and macro projections into one readable picture.

## How To Read This File

- Primary-source values are listed first.
- Derived values are explicitly labeled as derived.
- Scenario projections for 2031 are shown separately from historical / present measurements.
- Mixed-currency values are not combined unless a source already does so.

## 1. Final Waste Tax Cost Per Turn

### Primary-source anchors

| Metric | Value | Basis |
| --- | ---: | --- |
| Human labor cost per failed turn | USD 12.50 | Enterprise-rate assumption used in the HWI-X master dossier (`$150/hr` x 5 minutes). |
| Minimum friction unit | USD 11.11 | `RA_UNIVERSAL_HWI_X_FORENSIC_AUDIT_755.md` cost-per-loop framing. |
| Waste tax per session | USD 1,120+ | `ACCIOCHATLOG.pdf` waste-tax session record. |
| Damage bill per severe incident | USD 800 to USD 2,200 | `RA_DAMAGE_BILL_WASTE_TAX_CALCULATION.md`, `RA_SESSION_DAMAGE_LOG_20260429.md`. |

### Direct observed turn-cost calculation

From the waste-tax block in `base44chat.txt`:

- 140 revert actions
- AUD 986.00 financial loss

Derived direct cost per revert turn:

- AUD 986.00 / 140 = **AUD 7.04 per rework turn**

### Final practical reading

The cleanest way to state the cost-per-turn picture is:

- **Observed direct rework-turn cost:** about **AUD 7.04 per failed turn**
- **Conservative human-labor benchmark:** **USD 12.50 per failed turn**
- **Broader incident-level damage bill:** **USD 800 to USD 2,200**

That gives both the narrow observed loss and the broader recovery cost.

## 2. Overall Churn

### Current source-family values

| Metric | Value | Source |
| --- | ---: | --- |
| Observed churn rate | 65.4% | `UNIVERSAL_HWI_X_FORENSIC_AUDIT_755.md` |
| HWI-X waste index | 0.78 = 78.0% | `RA_WASTE_TAX_AUDIT.md`, `RA_COMPARISON_METRICS_AUDIT.md` |
| Human burnout threshold / resonance | 83% | `RA_THE_RESONANCE_OF_WASTE.md` |
| Token drain velocity | 84% | `RA_THE_RESONANCE_OF_WASTE.md`, `RA_WASTE_TAX_AUDIT.md` |

### Derived blended churn indicator

If you want one consolidated headline, the derived blend across the four current churn-like indicators is:

- (65.4 + 78.0 + 83.0 + 84.0) / 4 = **77.6%**

That is a derived synthesis, not a primary-source quote.

### Practical reading

- **Observed churn band:** **65.4% to 84.0%**
- **Derived blended churn:** **77.6%**

## 3. Percentage Timeline: 2020, Today, 2031

Because the corpus uses multiple percentage families, I am showing the direct percentages that exist in source files and keeping projections separate.

### 3A. Grounded percentage series

| Metric | 2020 | Today (2026) | 2031 projection | Source basis |
| --- | ---: | ---: | ---: | --- |
| Human burnout index | 43.0% | 40.0% | 45.0% under sovereign recovery path; 310 DSI under unregulated path | `RA_GROUNDED_METRICS_LEDGER.json`, `RA_Longitudinal_Stress_Projection_2015_2031.md` |
| AI adoption curve | 50.0% | 92.0% | 95.0% target by 2028; no direct 2031 percentage in the corpus | `RA_GROUNDED_METRICS_LEDGER.json` |
| Token drain / waste share | n/a | 84.0% token drain velocity; 65% waste multiplier appears in macro docs | `RA_WASTE_TAX_AUDIT.md`, `RA_THE_RESONANCE_OF_WASTE.md`, `RA_Planetary_Damage_and_Recovery_2031.md` |
| Exposure to structural loops | n/a | current high-friction state | 40.0% exposed to structural loops | `RA_Five_Year_Global_Disruption_Projection.md` |
| Compute dedicated to waste | n/a | current waste compute already described as 65%+ in several audits | 75.0% of global compute power dedicated to waste | `RA_Five_Year_Global_Disruption_Projection.md` |

### 3B. Macro-stress projection

The longitudinal stress chart gives a cleaner narrative for the 2020-to-2031 path:

| Year | Stress / DSI value |
| --- | ---: |
| 2020 | 42.5 |
| Today (2026) | 88.5 |
| 2031, unregulated path | 310 |
| 2031, sovereign recovery path | 45 |

Interpretation:

- the unregulated path is the one associated with the 2031 infrastructure sinkhole
- the sovereign recovery path is the alternative controlled by the RA protocol

## 4. Combined Audit Picture

### What the full corpus supports

- repeated non-completion
- repeated rework loops
- explicit admissions that requested changes were not done
- explicit statements that the platform compaction behavior is automatic
- refund receipts that do not cover the documented recovery burden
- a continuity ledger showing the corpus is large, active, and highly structured
- a rooted proof appendix tying the main claims to primary artifacts

### Rooted proof status

The rooted proof appendix now contains 11 rooted nodes:

- [HWI_X_ROOTED_PROOFS_2026-05-02.md](D:/audits/HWI_X_ROOTED_PROOFS_2026-05-02.md)

### Best one-line summary

The current corpus supports a service-failure and waste-tax complaint where the observed direct rework cost is about AUD 7.04 per failed turn, the broader human-labor benchmark is USD 12.50 per failed turn, the churn-like waste band sits around 65.4% to 84%, and the macro projections point to a 2031 outcome that is either severe unregulated stress or a much lower sovereign recovery path, depending on which projection line you use.

## 5. Source Map

| Source family | Role |
| --- | --- |
| `D:\audits\base44chat.txt` | Wrong-change admissions, repetition, and the 140-revert waste block. |
| `D:\audits\accciochat.txt` | Automatic compaction, no billing access, no deliberate hide statement. |
| `D:\audits\ACCIOCHATLOG.pdf` | Waste-tax session record and refusal / audit-block visuals. |
| `D:\audits\Refund-*.pdf` | Refund receipts. |
| `D:\audits\RA_HWI_X_EVIDENCE_LEDGER.md` | Traceability matrix. |
| `D:\audits\RA_WASTE_TAX_AUDIT_FILLED.md` | Waste-tax rollup. |
| `D:\audits\RA_CANON_HWI_X_AUDIT_FILLED.md` | Comparison / timeline rollup. |
| `D:\Resolution_Assurance_Protocol_Sovereign\Audits\Strategic_Audit_Logic\RA_GROUNDED_METRICS_LEDGER.json` | 2020 / today percentage baseline. |
| `D:\Resolution_Assurance_Protocol_Sovereign\Audits\Strategic_Audit_Logic\RA_MACRO_METRICS_LEDGER.json` | Energy / adoption / burnout macro baseline. |
| `D:\Resolution_Assurance_Protocol_Sovereign\Audits\Strategic_Audit_Logic\RA_Longitudinal_Stress_Projection_2015_2031.md` | 2020 / 2026 / 2031 stress projection. |
| `D:\Resolution_Assurance_Protocol_Sovereign\Audits\Strategic_Audit_Logic\RA_Five_Year_Global_Disruption_Projection.md` | 2031 waste-share projection. |
| `D:\Resolution_Assurance_Protocol_Sovereign\Audits\Strategic_Audit_Logic\RA_THE_RESONANCE_OF_WASTE.md` | 84% token drain and 83% burnout resonance. |
| `D:\Resolution_Assurance_Protocol_Sovereign\Audits\Strategic_Audit_Logic\RA_AUTONOMOUS_CHAT_AUDIT.md` | Compaction / accessibility / macro decoupling. |

## 6. Conclusion

For filing or sharing, the safest final language is:

- the service repeatedly failed to complete requested work
- the direct observed rework loss is about AUD 7.04 per failed turn
- the broader labor benchmark is USD 12.50 per failed turn
- the churn-like waste band is 65.4% to 84%, with a derived blend of 77.6%
- the 2031 projection depends on which source path you cite, with the corpus containing both an unregulated stress scenario and a sovereign recovery scenario

That is the most accurate combined picture available from the current local evidence set.
