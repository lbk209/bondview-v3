# Bondview-v3 — Work Collaboration Overview

**Purpose:** Explain the full operating arrangement and point to its authoritative detailed instructions. This is a map, not a new contract or a substitute for approved financial design.

## 1. Why the workflow exists

Bondview-v3 supports practical decisions about **Korean-listed U.S. bond ETFs**, grounded in established fixed-income methods, observed market data, and actual ETF exposures. Its architecture and examples under `docs/` remain subject to critical review; their mere existence does not authorize implementation.

The workflow separates economical, independent **design and acceptance in Chat** from **implementation and verification in Work**. It is deliberately light on user-facing handoffs and does not require the user to supervise every internal coding or review iteration.

## 2. People, responsibility, and authority

| Role | Responsibility | Boundary |
|---|---|---|
| **You** | Approve assignments, reserved decisions, and final acceptance | Manually transfer a brief specification/reference to Bernie and a result reference to Archie |
| **Archie (A), Chat** | Design, challenge assumptions, define accepted requirements, independently review Bernie's results | Does not silently authorize changes to financial design or supervise Work subagents |
| **Bernie (B), Work** | Orchestrate authorized work, verify real outputs, resolve in-scope objections, integrate and report | Must not silently redesign accepted economic requirements |
| **Carrie (C), Work subagent** | Review fixed-income logic, ETF exposure mapping, and decision usefulness | Reports to Bernie; does not directly approve the design |
| **Dennis (D), Work subagent** | Implement and test against the accepted task | Reports to Bernie; does not determine financial policy |

Names describe *roles*, not preinstalled agent accounts or proof that the current Work environment can spawn subagents. If necessary tools or permissions are unavailable, Bernie must say so rather than simulate delegation.

## 3. Normal end-to-end lifecycle

1. **Design:** You and Archie assess proposals, identify accepted scope and decision-support requirements, and specify concrete acceptance criteria.
2. **Handoff:** You give Bernie a concise Work assignment with paths/revisions of accepted documents. This is a manual trigger; GitHub can carry the referenced source material.
3. **Authorization:** When the assignment requires a separate understanding review, Bernie presents it before implementation and you authorize execution. Otherwise a sufficiently explicit authorized assignment proceeds directly.
4. **Execution:** Bernie delegates to Dennis and Carrie, inspects the actual files and calculations, runs or verifies tests, and iterates within the approved scope and limits.
5. **Completion:** Bernie publishes detailed results and evidence through the authorized GitHub branch/PR process where feasible. **Every PR description and PR comment is a concise, human-readable explanation**, linking to detailed findings rather than embedding logs or long analyses.
6. **Independent review:** You give Archie the relevant PR link or run ID; Archie reviews the report, code, calculations, objections, and evidence. **Bernie's PASS does not constitute Archie/user acceptance.**

A financial topic (duration, curve, currency, credit, ETF implementation) does **not** automatically require its own user-facing assignment. Bernie can coordinate internal workstreams in a single approved task. Return to Archie/user for material unapproved design choices, genuine blockers, substantial deliverables requiring review, and final acceptance.

## 4. One-time readiness prerequisite

Before financial implementation, perform **one Work Prerequisites assignment** using [`work_prerequisites.md`](work_prerequisites.md). It has two *internal*, conditional parts:

- **Subagent validation:** A real Dennis–Carrie delegation, code/test/review/follow-up/revision sequence in a disposable workspace. **No access to GitHub or the Bondview repository** during this part.
- **Repository setup:** Only after validation passes, verify GitHub access and establish genuine `reports/` and `artifacts/work_runs/` outputs through the authorized Git process.

The user launches this once. No extra user handoff is required between the two parts; platform consent remains mandatory where requested. If validation fails, **do not access GitHub**: Bernie reports failure directly in Work. Passing prerequisites does not approve later financial-model implementation.

## 5. Repository areas and reporting

| Location | Owner / purpose |
|---|---|
| `AGENTS.md` | Stable repository-level engineering, Git, and safety conventions |
| `docs/` | User/Archie's financial-design archive; no Bernie-generated material |
| `workflow/` | User/Archie's instructions, including this overview, quickstart, prerequisites, and contracts |
| `reports/` | Bernie's **detailed**, durable per-assignment technical and review reports |
| `artifacts/work_runs/<run_id>/` | Bernie-created manifest and focused evidence/examples; avoid committing large caches or irrelevant logs |
| `src/`, `tests/` | Actual implementation and reproducible tests when needed |

For repository-changing work, use `AGENTS.md`'s session/task branch → PR workflow. PR **descriptions and comments summarize for humans** (outcome, changes, caveats, next action, links); `reports/` and `artifacts/` preserve the technical depth Archie needs. If GitHub access or PR creation is unavailable, do not invent a PR: give a truthful Work response and identify which durable outputs could not be published. Exact output rules: [`work_handoff_output_contract.md`](work_handoff_output_contract.md).

## 6. Document map and precedence

| Document | Audience / job |
|---|---|
| [`quickstart.md`](quickstart.md) | **You:** shortest path to start Bernie and return results to Archie |
| [`work_prerequisites.md`](work_prerequisites.md) | **You and Bernie:** one-time instructions plus the full ready-to-paste, self-contained Work prompt |
| [`work_supervisor_contract.md`](work_supervisor_contract.md) | **Bernie:** delegation, checks, authority, iteration and stopping rules |
| [`work_handoff_output_contract.md`](work_handoff_output_contract.md) | **Archie, you, and Bernie:** what the task specifies and what evidence/results Bernie delivers |

The accepted task and specifically accepted v3 financial-design decisions govern economic behavior. `AGENTS.md` governs baseline repository operations; the supervisor and handoff contracts elaborate orchestration and deliverables. The prerequisite prompt takes precedence for its isolated initial test. This overview and quickstart are explanatory: if they disagree with a detailed contract, correct the inconsistency rather than silently adopting a new rule.
