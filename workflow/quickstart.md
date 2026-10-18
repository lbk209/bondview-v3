# Bondview-v3 — User Quickstart

For the underlying architecture and role boundaries, see the [workflow overview](README.md). This file describes **what you do**, not Bernie's internal engineering procedure.

## 1. Roles at a glance

- **Archie (A), Chat:** Your design discussion and independent technical-review partner.
- **Bernie (B), Work:** Executes an approved assignment and coordinates actual subagents when available.
- **Carrie (C):** Bernie's fixed-income reviewer; **Dennis (D):** Bernie's developer. You do not manually launch these children.

**Archie ↔ Bernie transfers are user-mediated.** You generally transfer only a short prompt or GitHub document/PR reference, not a full transcript.

## 2. Before your first implementation assignment

Run the **one-time** [Work Prerequisites](work_prerequisites.md) assignment. That document contains its own short user instructions **and the complete prompt to paste into one new Work session**. Do not separately launch the internal validation and conditional repository-setup steps. Do not start financial implementation merely because the prerequisites pass.

## 3. Starting an ordinary Bernie assignment

1. In Chat, settle the objective, scope, design authority, numerical acceptance criteria, and permitted discretion with Archie. Clearly distinguish **accepted requirements** from provisional ideas in `docs/`.
2. Open a Work session for Bernie. Supply the concise assignment prompt or GitHub link/revision prepared with Archie. Reference `AGENTS.md`, [`work_supervisor_contract.md`](work_supervisor_contract.md), and [`work_handoff_output_contract.md`](work_handoff_output_contract.md).
3. Specify whether Bernie is authorized to implement immediately or must first return an understanding review for your approval. Where the approval gate applies, explicitly authorize implementation after reviewing that understanding.
4. Bernie handles coding, economic challenge, corrections, and validation internally. Respond only to required platform permissions, material reserved decisions, and genuine blockers. Do not create new user-facing stages for ordinary internal workstreams.

## 4. Reviewing an assignment

1. Read **Bernie's final human-readable summary** in the relevant GitHub PR description (and final Work response). PR comments are also concise and link to technical evidence.
2. Supply Archie the **PR URL or run ID**. Archie reads the detailed report under `reports/`, actual code/tests, and evidence under `artifacts/work_runs/<run_id>/`.
3. Decide whether to approve, request a focused follow-up, or defer a reserved design decision. Bernie's `PASS` is a completion claim, **not** your final acceptance.

If no PR was possible, Bernie must explain that in Work and give all available results without inventing GitHub links. **Special case:** a failure during the isolated prerequisite validation prohibits GitHub access, so the failure report is delivered in Work only.

## 5. File boundaries

`docs/` = financial design; `workflow/` = user/Archie-owned operating instructions; `reports/` = Bernie's durable technical reports; `artifacts/work_runs/` = verification evidence. The Git workflow and write restrictions are specified in `AGENTS.md`. Bernie does not independently rewrite `docs/` or `workflow/` as an implementation byproduct.
