# Python consumers for reorganized labels.yaml

The four affected Python consumers now use the authoritative YAML hierarchy on `codex/session/261026_1000`. Focused verification passed. No financial calculation, classification, data acquisition, storage, or public function signature changed.

## Authority and repository state

- Assignment: directly execute the user's presentation-configuration compatibility task; no subagents or Bernie workflow.
- Authorized source/session: `codex/session/261026_1000`, revision `693bf09c32607705d1bc926258d0dfad00ef67b1` (`generalize labels.yaml`). Read `AGENTS.md` and `src/bondview/config/labels.yaml` from this revision before editing.
- Initial working tree was clean; local HEAD matched the fetched session revision. Recent commits and local/remote branches were inspected, with fetch/prune and live `ls-remote` verification. Only `main` and the authorized session branch existed remotely before this task.
- Task branch: `codex/task/261027_1352_labels_consumers`, created from the authorized session branch.
- Existing final review PR: [#36](https://github.com/lbk209/bondview-v3/pull/36), from the session branch into `main`, verified open and unmerged before implementation. Reuse this PR; do not create a duplicate or merge it.
- Local Git metadata writes and remote Git operations required sandbox escalation. Fetch and branch creation succeeded; no user work was stashed, discarded, or bypassed.

## Changed source files

| File | Necessary change |
| --- | --- |
| `src/bondview/presentation/treasury_curve.py` | Read N/A, not-applicable text, units and tenor names from `common`; read Treasury-specific labels from `analyses.treasury_curve`. Use `percent_2dp` and `bp_signed_0dp` for levels, changes and interpretation. Existing private/public function signatures remain intact. |
| `src/bondview/plotting/treasury_curve.py` | Read shared tenor names from `common.tenors` and all plot text from `analyses.treasury_curve.plot`. Preserve data selection, trace values/styles, gaps and layout settings. |
| `src/bondview/presentation/widgets.py` | Read date labels from `widgets.dates`; preserve date defaults and widget behavior. |
| `src/bondview/data/fred.py` | Read report templates from `data.fred`; preserve report contents and all data-management behavior. |

Inspected all tracked Python files under `src/`, including direct `load_labels()` calls, YAML/path references, callers and display wrappers. These four files contain all affected consumers. `labels.py` already loads the YAML mapping without assuming a hierarchy and needs no change. Analysis and utility modules have no label dependency. No aliases, flattening, compatibility layer, or new dependency was added.

The supplied YAML determines the terminology and precision: percent levels have two decimals and basis points have an explicit sign and zero decimals. For example, the synthetic comparison displays `3.56%`, `+7 bp`, and `+116 bp`. Earlier test expectations of `+7.00 bp` or older movement wording are not the authoritative presentation contract.

`labels.yaml`, `AGENTS.md`, `docs/`, `workflow/`, notebooks, tests, analysis code and utilities are unchanged from the source revision. Existing ignored notebook checkpoint files are not package sources; they were left untouched and excluded from the tracked-source scan. No YAML inconsistency blocked operation.

## Verification and observed results

Executed in the project's existing Poetry environment: Python 3.12.1, environment `bondview-v3-trCSYVBi-py3.12`. All fixtures are synthetic and offline; none represents a new market retrieval or investment judgment.

1. `poetry run python -m py_compile src/bondview/presentation/treasury_curve.py src/bondview/plotting/treasury_curve.py src/bondview/presentation/widgets.py src/bondview/data/fred.py artifacts/work_runs/261027_labels_consumers_1352/verify_labels.py` — passed.
2. `poetry run python artifacts/work_runs/261027_labels_consumers_1352/verify_labels.py` — passed all nine verification groups. The script is retained as reproducible run evidence without editing test files.
3. `git diff --check` — passed.
4. `poetry run python -m unittest discover -s tests -v` — failed at discovery with three module-import errors both before and after the source edits. See the separate limitation below.

The focused script checks:

- Exact table names, headers, endpoint formats, positive/negative/zero basis-point formatting, unavailable values, not-applicable text and complete interpretation text. Hand-checkable numeric changes remain `[84, 116, 103, 32, -13]` bp; displayed segment changes are `+32 bp` and `-13 bp`.
- Thirteen movement cases spanning bear, bull, twist, parallel, unchanged, short-only and long-only wording; upward/inverted/flat configurations; downward, tied, unchanged and tolerance-aware interpretations.
- Each of six individual missing endpoint observations and a comparison where no tenor has paired endpoint observations. N/A/partial/no-data text resolves correctly without altering the numerical results.
- Plot titles, axes, legend, trace names, hover template, three line styles, trace dates/values, missing gaps and selected-period slicing. Both `show_yield_history()` and `show_curve_results()` wrappers work with their display calls intercepted.
- Date defaults and actual `DateRangePicker` construction, descriptions and selected values.
- Exact multiline `FredDataManager.report()` output after loading a temporary CSV: provenance, loaded dates, row count, path, source units/frequency, missing counts and snapshot qualification. Reporting leaves the snapshot bytes unchanged.
- Separate temporary nested YAML customization across all four consumers, including shared units and tenors, and rereading changes without module reload. The repository YAML is never edited.
- AST comparison of every function signature in the four files against the authorized source, plus a tracked-source scan for obsolete root lookups and old `units.percent`/`units.bp` keys.
- Protected paths and financial results remain unchanged.

## Existing tests and limitations

The existing suite imports `date_picker_defaults` from `bondview.presentation.treasury_curve`; the authorized source instead defines it in `bondview.presentation.widgets` and does not re-export it. `test_treasury_curve` therefore fails to import, which also prevents `test_fred` and `test_notebook` from importing their shared fixture. The same error was observed before editing. This task does not restore an obsolete import, edit tests, or claim that the full suite passed. Other stale expectations visible in the test source include old flat YAML paths, basis-point precision, older wording, exact-date endpoint behavior and plot behavior; these tests could not execute through the import failure.

No live FRED request, fresh-kernel notebook execution, interactive browser/widget rendering, or external plot renderer was used. Plot construction and real widget object construction were verified in Python; display wrappers were checked with display calls intercepted. These checks satisfy the requested YAML-dependent acceptance criteria but do not constitute broader application QA or financial-design acceptance.

## Evidence

- [Reproducible verification script](../artifacts/work_runs/261027_labels_consumers_1352/verify_labels.py)
- [Focused results and inspectable table/interpretation/report examples](../artifacts/work_runs/261027_labels_consumers_1352/evidence/focused_verification.json)
- [Existing test-discovery output](../artifacts/work_runs/261027_labels_consumers_1352/evidence/existing_unittest.txt)

The task PR targets the authorized session branch. Its merge and remote task-branch cleanup are verified during publication and reported in the final session PR and completion response. The session-to-main PR remains for the user's independent review.
