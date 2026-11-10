# Market Pilot MCP

Market Pilot MCP is a Model Context Protocol (MCP) server for maintaining a structured journal of trading research and activity. It gives models a way to record and reference observations, proposals, reviews, decisions, and orders.

The journal preserves the evidence, reasoning, and outcomes behind trading activity, providing context that can be revisited as new information becomes available.

## Contents

- [Journal Entry](#journal-entry)
- [Observation](#observation)
- [Proposal](#proposal)
- [Review](#review)
- [Decision](#decision)
- [Order](#order)

## Journal Entry

### What is it?

A journal entry is a database entry that can later be referenced by the model. It provides a log of all actions taken on behalf of the trader

### Types of journal entries

| Entry Type                  | Purpose                                   |
| --------------------------- | ----------------------------------------- |
| [OBSERVATION](#observation) | Record a fact, event, or finding          |
| [PROPOSAL](#proposal)       | Suggest an action based on observations   |
| [REVIEW](#review)           | Reassess an existing idea or position     |
| [DECISION](#decision)       | Record what was decided and why           |
| [ORDER](#order)             | Record an order and its execution details |

### Observation

An observation records a specific finding and the evidence supporting it. It provides the factual basis for research, proposals, reviews, and decisions. Interpretation is stored separately so readers can distinguish a reported fact from an inference.

#### Fields

| Field                        | What it captures                                                                               |
| ---------------------------- | ---------------------------------------------------------------------------------------------- |
| `symbol_id`                  | The instrument the observation concerns                                                        |
| `title`                      | A short description of the finding                                                             |
| `category`                   | Earnings, valuation, price, volume, news, business operations, or another defined category     |
| `statement`                  | The specific finding, including attribution when a source reports a claim                      |
| `observed_at`                | When the event occurred or a point-in-time measurement applied; optional for period-based data |
| `period_start`, `period_end` | The reporting or measurement period, when applicable                                           |
| `sources`                    | Source references, URLs, publication dates, retrieval times, and supporting excerpts           |
| `metrics`                    | Optional structured measurements with names, values, units, currencies, and comparison periods |
| `interpretation`             | Optional explanation or calculation describing why the finding might matter                    |
| `limitations`                | Missing context, uncertainty, qualifications, or data-quality concerns                         |
| `supersedes_entry_id`        | An earlier observation corrected or replaced by this one                                       |
| `status`                     | Active, superseded, or retracted                                                               |

#### Related Tools

| Tool                  | Parameters                                                                                                                       | Purpose                                                               |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `create_observation`  | `ticker, title, category, statement, sources, observed_at?, period_start?, period_end?, metrics?, interpretation?, limitations?` | Record a sourced finding and its applicable time or period            |
| `get_observation`     | `observation_id`                                                                                                                 | Retrieve an observation, sources, and any correction reference        |
| `list_observations`   | `ticker?, category?, status?, observed_from?, observed_to?, limit?, cursor?`                                                     | Find observations by instrument, category, status, or applicable date |
| `correct_observation` | `observation_id, replacement, reason`                                                                                            | Create a validated replacement and preserve the earlier record        |
| `retract_observation` | `observation_id, reason`                                                                                                         | Mark a finding as withdrawn while preserving its history              |

### Proposal

A proposal describes an action under consideration and the reasoning behind it. It connects evidence to a thesis, identifies counterarguments and risks, and defines when the idea should be reconsidered.

#### Fields

| Field                     | What it captures                                                              |
| ------------------------- | ----------------------------------------------------------------------------- |
| `symbol_id`               | The instrument under consideration                                            |
| `title`                   | A short description                                                           |
| `proposed_action`         | Research, watch, buy, reduce, or exit                                         |
| `thesis`                  | Why the action might make sense                                               |
| `evidence`                | Supporting observations and source references                                 |
| `counterarguments`        | Evidence against the thesis                                                   |
| `risks`                   | Main uncertainties and potential downsides                                    |
| `invalidation_conditions` | What would make the thesis no longer hold                                     |
| `action_details`          | Optional structured scope, sizing, price conditions, or research deliverables |
| `review_at`               | When to revisit it                                                            |
| `expires_at`              | Optional deadline after which the proposal is stale                           |
| `supersedes_proposal_id`  | An optional earlier proposal replaced by this revised idea                    |
| `status`                  | Draft, pending review, accepted, rejected, or expired                         |

#### Related Tools

| Tool                       | Parameters                                                                                                                                                                  | Purpose                                                               |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `create_proposal`          | `ticker, title, proposed_action, thesis, evidence?, counterarguments?, risks?, invalidation_conditions?, action_details?, review_at?, expires_at?, supersedes_proposal_id?` | Create a draft idea linked to its supporting evidence                 |
| `get_proposal`             | `proposal_id`                                                                                                                                                               | Retrieve the proposal, evaluated revisions, evidence, and decisions   |
| `list_proposals`           | `ticker?, status?, proposed_action?, review_due_before?, limit?, cursor?`                                                                                                   | Find proposals by instrument, lifecycle state, action, or review date |
| `update_proposal`          | `proposal_id, expected_revision, changes`                                                                                                                                   | Edit an eligible proposal while detecting conflicting updates         |
| `record_proposal_decision` | `proposal_id, expected_revision, outcome, rationale, decided_by, conditions?, evidence_entry_ids?, review_entry_id?`                                                        | Create a linked decision and update the proposal's status             |

### Review

A review reassesses existing journal entries using current evidence. It can evaluate a proposal before a decision, revisit an earlier thesis, or assess an order's outcome. A review documents findings and recommendations; a separate decision records the chosen action.

#### Fields

| Field               | What it captures                                                              |
| ------------------- | ----------------------------------------------------------------------------- |
| `symbol_id`         | The instrument being reviewed                                                 |
| `title`             | A short description of the review                                             |
| `target_entry_ids`  | The proposals, observations, decisions, or orders being assessed              |
| `review_trigger`    | Scheduled review, new evidence, a changed condition, or a manual request      |
| `as_of`             | The cutoff time for evidence considered                                       |
| `findings`          | What changed or was learned                                                   |
| `evidence`          | Supporting and contradictory observations or source references                |
| `thesis_assessment` | Supported, weakened, invalidated, inconclusive, or not applicable             |
| `recommendation`    | Suggested follow-up, such as more research, a revised proposal, or a decision |
| `limitations`       | Unresolved questions or gaps in the review                                    |
| `next_review_at`    | Optional date for another review                                              |
| `status`            | Draft or completed                                                            |

#### Related Tools

| Tool              | Parameters                                                                                                                                         | Purpose                                                    |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| `create_review`   | `ticker, title, target_entry_ids, review_trigger, as_of, findings?, evidence?, thesis_assessment?, recommendation?, limitations?, next_review_at?` | Start a review of existing journal entries                 |
| `get_review`      | `review_id`                                                                                                                                        | Retrieve the review, targets, and evidence                 |
| `list_reviews`    | `ticker?, target_entry_id?, status?, review_trigger?, limit?, cursor?`                                                                             | Find reviews for an instrument or a specific journal entry |
| `update_review`   | `review_id, changes`                                                                                                                               | Add findings and evidence to a draft review                |
| `complete_review` | `review_id, findings, thesis_assessment, recommendation?, limitations?, next_review_at?`                                                           | Finalize the assessment and preserve its conclusions       |

### Decision

A decision records an explicit outcome for a proposal, the reasoning behind it, and any conditions attached to it. It preserves what was evaluated and who made the decision. An accepted research or watch proposal may require no order.

#### Fields

| Field                    | What it captures                                                    |
| ------------------------ | ------------------------------------------------------------------- |
| `symbol_id`              | The instrument concerned, inherited from the proposal               |
| `title`                  | A short description of the outcome                                  |
| `proposal_id`            | The proposal being decided                                          |
| `proposal_revision`      | The exact revision evaluated                                        |
| `proposal_snapshot`      | The evaluated proposal content and action details                   |
| `outcome`                | Accept, reject, or defer                                            |
| `rationale`              | Why this outcome was chosen                                         |
| `conditions`             | Prerequisites, limits, or scope attached to an accepted action      |
| `evidence_entry_ids`     | Journal entries supporting the decision                             |
| `review_entry_id`        | An optional completed review informing it                           |
| `decided_by`             | The person or process responsible for the decision, with provenance |
| `decided_at`             | When the decision was made                                          |
| `supersedes_decision_id` | An earlier decision replaced by this one                            |

#### Related Tools

| Tool                       | Parameters                                                                                                                      | Purpose                                                                     |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| `record_proposal_decision` | `proposal_id, expected_revision, outcome, rationale, decided_by, conditions?, evidence_entry_ids?, review_entry_id?`            | Record an outcome against the evaluated proposal revision                   |
| `get_decision`             | `decision_id`                                                                                                                   | Retrieve the decision, evaluated proposal snapshot, and supporting evidence |
| `list_decisions`           | `ticker?, proposal_id?, outcome?, decided_from?, decided_to?, limit?, cursor?`                                                  | Find decisions and inspect their history                                    |
| `supersede_decision`       | `decision_id, expected_current_decision_id, outcome, rationale, decided_by, conditions?, evidence_entry_ids?, review_entry_id?` | Record a replacement decision while preserving the original                 |

### Order

An order records a submitted trade instruction and its execution lifecycle. It links the resulting activity back to an accepted decision. One decision may lead to several orders, and one order may have several fills.

The tools below record order activity. A future broker integration can add submission and cancellation capabilities with their own explicit execution behavior.

#### Fields

| Field                       | What it captures                                                                |
| --------------------------- | ------------------------------------------------------------------------------- |
| `symbol_id`                 | The instrument being traded                                                     |
| `title`                     | A short description of the order                                                |
| `decision_id`               | The accepted decision supporting the order                                      |
| `broker`, `account_ref`     | Where the order was placed; account references should avoid storing credentials |
| `broker_order_id`           | An optional external identifier used to reconcile imported activity             |
| `side`                      | Buy or sell                                                                     |
| `quantity`                  | The requested number of units, stored as a positive decimal                     |
| `order_type`                | Market, limit, stop, or stop-limit                                              |
| `limit_price`, `stop_price` | Prices required by the selected order type                                      |
| `currency`                  | The quote/settlement currency used by the order record                          |
| `time_in_force`             | The order duration policy, such as day or good-till-cancelled                   |
| `status`                    | Submitted, partially filled, filled, cancelled, rejected, or expired            |
| `submitted_at`              | When the order was submitted                                                    |
| `fills`                     | Execution quantities, prices, fees, and execution times                         |
| `filled_quantity`           | Total executed quantity, derived from fills                                     |
| `average_fill_price`        | Quantity-weighted execution price, derived from fills                           |
| `notes`                     | Optional execution context or discrepancies                                     |

#### Related Tools

| Tool                  | Parameters                                                                                                                                                        | Purpose                                                                           |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `record_order`        | `decision_id, title, broker, account_ref, side, quantity, order_type, currency, time_in_force, submitted_at, broker_order_id?, limit_price?, stop_price?, notes?` | Record an order submitted under an accepted decision                              |
| `get_order`           | `order_id`                                                                                                                                                        | Retrieve order details, fills, execution totals, and status history               |
| `list_orders`         | `ticker?, decision_id?, broker?, account_ref?, status?, submitted_from?, submitted_to?, limit?, cursor?`                                                          | Find orders by instrument, decision, execution venue, or lifecycle state          |
| `record_order_fill`   | `order_id, quantity, price, executed_at, external_fill_id?, fee_amount?, fee_currency?`                                                                           | Record an execution and update the derived fill totals                            |
| `record_order_status` | `order_id, status, event_at, source, reason?`                                                                                                                     | Record broker/manual status changes, including cancellation, rejection, or expiry |
