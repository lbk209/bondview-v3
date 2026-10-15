# Bondview-v3 — User Quickstart: Alisa and Branson

**Prepared:** 2026-10-15  
**Status:** Proposed user reference (not an agent contract)  
**Repository:** https://github.com/lbk209/bondview-v3

## People and responsibilities

| Alias | Name | Role | What you do |
|---|---|---|---|
| A | **Alisa** | Designer — this Chat conversation | Agree on design and review final Work results |
| B | **Branson** | Orchestrator — ChatGPT Work | Start the approved task; receive one consolidated result |
| C | **Clara** | Fixed-Income Reviewer — Branson's subagent | No manual setup or direct interaction |
| D | **Devon** | Developer — Branson's subagent | No manual setup or direct interaction |

**You manually transfer assignments and results between Alisa and Branson.** Branson creates/manages Clara and Devon if your Work environment supports real subagents; these names are role labels, not preinstalled agents.

## Start S0 — once

1. Open **ChatGPT Work → New session** (web is sufficient). Select a capable reasoning model; **Medium** effort is adequate for the operational test. Use GPT-6 / Medium if offered; model choices vary by account and Work surface. Extra plugins and the desktop app are **not required** for S0; GitHub is already connected, but Work must independently verify access during setup.
2. Open `workflow/bondview_v3_s0_work_assignment_20261015_v02.md` yourself and paste **the entire ready-to-paste prompt** into the new Work session. No need to pre-create Clara or Devon, attach `docs/`, or ask Branson to read the Bondview repository before the smoke test.
3. **Do not launch S0-B separately.** Branson internally runs the isolated subagent test (S0-A). Only if it passes, Branson proceeds to repository/report-folder setup (S0-B) in the same assignment. Required platform approvals may still appear.
4. Bring Branson's **single final S0 report, evidence and PR links** back to Alisa for review. **Do not start financial implementation** merely because S0 completes.

For future financial assignments, Alisa supplies the accepted specification and scope. Branson may divide the approved task into Duration, Curve, Credit, FX, coding and review workstreams **internally**; each is **not** automatically a separate user-facing stage. A manual understanding/authorization check is used when specified by the approved handoff.

## Where files belong

- `docs/`: your/Alisa's financial design archive; no Branson-generated documents.
- `workflow/`: user/Alisa-approved instructions; Branson reads, not writes generated reports.
- `reports/`: Branson's consolidated reports.
- `artifacts/work_runs/`: evidence, manifests, examples, unique filenames.
- `AGENTS.md`: root Git and engineering rules. Repository changes use branches and PRs, not direct writes to `main`.

**If S0 fails:** Return Branson's PARTIAL/BLOCKED output to Alisa. Do not assume the exact subagent workflow works without demonstrated evidence. Work may not expose exact per-agent token usage; report 'not exposed' when necessary.
