# [RA.CANON.7.0] SIGNAL FABRIC NORMALISATION MAP (SFNM)

Date: 2026-04-22
Canon version: 7.0
Governance lock ref: RA-LIC-STD-001
Governance lock status: active
Storage purge TTL hours: 72

## Canonical Tables

| order | table_name | canonical_shape | governing_layer | primary_key |
| --- | --- | --- | --- | --- |
| 1 | source_catalog | active_source | ingestion_layer | source_id |
| 2 | signal_ledger | active_source | orchestration_layer | signal_id |
| 3 | forecast_event | anchored_event | nsde_predictor | event_id |
| 4 | resolved_fact | rooted_fact | anchoring_layer | fact_id |
| 5 | continuity_ledger | anchored_event | continuity_ledger | run_id |

## Counter Normalisation

| order | counter_name | definition |
| --- | --- | --- |
| 1 | active_source | An ingestable source that is currently eligible to emit accepted evidence in the active cadence window. |
| 2 | rooted_fact | A fact promoted through the resolved-fact layer with corroboration, continuity, freshness, and contradiction thresholds satisfied. |
| 3 | rooted_proof | A proofstamp row with a stable hash and seal-ready or higher-trust state. |
| 4 | anchored_event | A time-sealed event row bound to the canon cycle clock and the continuity ledger. |

## Governance Lock Propagation

| layer | lock_ref | status |
| --- | --- | --- |
| ingestion_layer | RA-LIC-STD-001 | active |
| orchestration_layer | RA-LIC-STD-001 | active |
| anchoring_layer | RA-LIC-STD-001 | active |
| nsde_predictor | RA-LIC-STD-001 | active |
| continuity_ledger | RA-LIC-STD-001 | active |

## NSDE Activation

| field | value |
| --- | --- |
| activation_threshold | 0.05 |
| activation_formula | delta_expected_entities_minus_delta_observed_entities_over_continuity_window |
| predictor_state | monitor_or_predictor |

## Storage Alignment

| field | value |
| --- | --- |
| storage_purge_ttl_hours | 72 |
| raw_retention_alignment | 72h_ttl_target |

## Normalisation Rules

- Active Source, Rooted Fact, Rooted Proof, and Anchored Event are the canonical counter definitions for the sealed telemetry stack.
- The forecast_event table is the first-class predictor surface for NSDE and the other operational predictors.
- The 5-table schema is the minimum universal map for sealed audits.
