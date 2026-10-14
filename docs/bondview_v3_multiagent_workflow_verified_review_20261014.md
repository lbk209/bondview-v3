# Bondview-v3: Design-Chat Handoff and Work-Supervised Multi-Agent Workflow

**Status:** Reviewed proposal — for further Bondview-v3 project discussion, **not** an approved execution policy or a confirmed end-to-end implementation.  
**Verification update:** 2026-10-14; official documentation reviewed and public user reports examined. Work execution itself has **not** been run in this user's account.  
**Prepared:** 2026-10-14  
**Scope:** Delegation from a design conversation to a Work session supervising coding and fixed-income-review subagents.  
**Primary purposes:** (1) explain the proposal to the user; (2) let the Work Supervisor understand the manual handoff, delegation boundaries, and task control; (3) provide reusable instructions for setting up and supervising the Coding Agent and Fixed-Income Reviewer; and (4) identify what is verified and how to test what is not.

> **Important distinction:** A single Work session plus a well-designed prompt is the **proposed configuration**, not a verified guarantee. OpenAI documents subagent orchestration for *eligible accounts*, including spawning and routing follow-up instructions. The precise sequential code–economic-review–revision loop, account access, local/cloud repository integration, and unattended completion remain to be demonstrated. See the evidence review and disposable operational smoke test below.

---

## 1. Executive Summary

The proposed workflow has a **manual Design Chat–user–Work Supervisor handoff**, followed by an autonomous **Work Supervisor ⇄ Coding Agent / Work Supervisor ⇄ Fixed-Income Reviewer** process and a **Work Supervisor → user → Design Chat** final handoff.

- **Design Chat — Design Authority:** A normal ChatGPT conversation in which the user and Design Chat define, debate, revise, and approve the Bondview-v3 design and implementation assignment. Design Chat prepares the handoff package and later assesses Work Supervisor's consolidated result with the user.
- **Work Supervisor — Implementation Supervisor:** A ChatGPT Work session with overall responsibility for the implementation assignment. Work Supervisor first explains its understanding to the user for manual review by Design Chat. After authorization, the Work Supervisor supervises the Coding Agent and Fixed-Income Reviewer, manages iterations, makes delegated decisions, and produces the **sole final consolidated deliverable**.
- **Coding Agent — Implementation Subagent:** A coding-oriented subagent delegated by Work Supervisor. It implements, tests, corrects, and documents software changes under Work Supervisor's direction. **The Coding Agent is not assumed to be an existing independent Codex CLI or cloud session.** Parity with dedicated Codex for coding performance, tools, and runtime settings is not established.
- **Fixed-Income Reviewer — Economic Review Subagent:** A separate expert-oriented subagent delegated by Work Supervisor. Fixed-Income Reviewer examines economic validity, conventional fixed-income alternatives, practical ETF selection value, assumptions, and results. Fixed-Income Reviewer challenges Work Supervisor as needed but **reports only to Work Supervisor**, never directly to Design Chat.

The motivation is to eliminate repeated manual relay between the designer and coder **during implementation**, without replacing the established user–Design Chat design process or its final assessment. Work Supervisor and its subagents consume model usage; the workflow attempts to contain that usage without sacrificing essential verification.

### Non-negotiable workflow boundaries

1. **Design Chat ↔ Work Supervisor communication is manual, mediated by the user.** There is no requirement for automatic cross-chat messaging, and no implication that Design Chat can programmatically control Work Supervisor.
2. **Only Work Supervisor/Coding Agent/Fixed-Income Reviewer collaboration is autonomous** once the user authorizes execution. Work Supervisor controls the complete internal workflow, including returns from Fixed-Income Reviewer to Coding Agent via Work Supervisor.
3. **Fixed-Income Reviewer must not report directly to Design Chat.** Fixed-Income Reviewer raises objections with Work Supervisor, Work Supervisor debates them with Fixed-Income Reviewer, and Work Supervisor directs Coding Agent if revisions are warranted. Several such rounds may occur within finite limits.
4. **Work Supervisor is the final decision integrator and final author.** Neither Coding Agent's completion message nor Fixed-Income Reviewer's opinion constitutes the submitted result.
5. **Design Chat remains the design authority.** Work Supervisor may exercise explicitly delegated technical and economic discretion; significant unapproved deviations must be disclosed, not silently treated as approved design decisions.
6. **The final outcome may be complete, partially complete, or blocked by unresolved decisions.** Autonomous operation means no routine user interaction during execution, not a guarantee of successful completion at any cost.

---

## 2. End-to-End Workflow

```text
USER ⇄ DESIGN CHAT (manual)
  Design discussion → approved task → written handoff
                |
                | user transfers instructions and documents manually
                v
          WORK SUPERVISOR — Phase 1
   Read → restate understanding → infer → object → plan
                |
                | user brings Work Supervisor's response to Design Chat;
                | Design Chat reviews; user conveys corrections/approval
                v
          WORK SUPERVISOR — Phase 2
         [autonomous boundary starts]
                |
                v
          Work Supervisor ⇄ Coding Agent (coding)
   implement → test → inspect → revise until provisionally done
                |
                v
          Work Supervisor ⇄ Fixed-Income Reviewer (economic review)
   challenge → reasoned discussion → Work Supervisor's disposition
                |
          if change required
                v
          Work Supervisor ⇄ Coding Agent (revision)
                |
          if economic logic materially changed
                +----------> Work Supervisor ⇄ Fixed-Income Reviewer (targeted re-review)
                |
                v
          Work Supervisor — final integration
   verify, reconcile, disclose deviations, write final report
                |
                | user transfers Work Supervisor's final output manually
                v
USER ⇄ DESIGN CHAT (manual)
   assess outcome; decide further design work if necessary
```

This is a **controlled sequence with bounded rework**, not a requirement to keep Coding Agent and Fixed-Income Reviewer running concurrently. In fact, sequential use normally reduces duplicated context and conflicting revisions. Work Supervisor may request narrow early advice from Fixed-Income Reviewer when Coding Agent encounters a material economic issue, but routine Fixed-Income Reviewer participation begins after provisional implementation completion.

### Phase 1 — Understanding validation (manual Design Chat↔Work Supervisor)

1. Design Chat and the user approve the scope and compile a **Handoff Package** (§3).
2. The user starts a Work session with the Work Supervisor role and supplies the package. Work Supervisor **must not create Coding Agent/Fixed-Income Reviewer, modify code, or begin implementation yet**.
3. Work Supervisor produces an **Understanding Review** (§4), distinguishing what the sources establish from its own inference and proposed challenge.
4. The user relays that review to Design Chat. Design Chat evaluates the quality of Work Supervisor's understanding, answers substantive objections, and prepares corrections or a clarified mandate.
5. The user returns Design Chat's decision to Work Supervisor. The handoff can undergo another manual clarification if a blocking misunderstanding remains; it should not become a default infinite pre-implementation design cycle.
6. On an explicit **execution authorization from the user in the Work Supervisor session**, Work Supervisor proceeds to Phase 2.

### Phase 2 — Autonomous Work Supervisor/Coding Agent/Fixed-Income Reviewer execution

1. Work Supervisor records the approved assignment, design authority, decision boundaries, provisional completion criteria, and limits on iterations/resources.
2. Work Supervisor delegates implementation to Coding Agent. Coding Agent reports completed changes and evidence; Work Supervisor independently checks relevant changes and verification.
3. Work Supervisor requests necessary revisions from Coding Agent until a credible provisional implementation is reached or the work stops according to its limits.
4. Work Supervisor delegates an independent **economic review** to Fixed-Income Reviewer. Fixed-Income Reviewer receives actual implemented economic methods, assumptions, and observed outputs; Fixed-Income Reviewer must consider whether simpler, established fixed-income models would be more suitable.
5. If Fixed-Income Reviewer objects, Work Supervisor asks for evidence, offers counterarguments, explores implications and alternatives, and makes a reasoned disposition. Work Supervisor does **not** automatically accept Fixed-Income Reviewer's position or require Fixed-Income Reviewer's complete agreement.
6. Where a warranted change falls within delegated authority, Work Supervisor sends an updated specification to Coding Agent and checks the resulting implementation. If economic logic changes materially, Work Supervisor requests a focused Fixed-Income Reviewer re-review.
7. Work Supervisor stops based on evidence and finite iteration rules, and authors the **final consolidated deliverable** (§9). It does not redirect Fixed-Income Reviewer to Design Chat or ask the user to mediate Coding Agent/Fixed-Income Reviewer discussion.
8. The user manually transfers Work Supervisor's final report to Design Chat for a separate design-level discussion.

---

## 3. The Design Chat → Work Supervisor Handoff Package

The key risk is not transferring a prompt; it is **losing design context and the standards needed to judge later unforeseen decisions**. Work Supervisor does not need Design Chat's entire conversation history, but it needs enough to understand the reasoning behind the approved design and to distinguish a permitted refinement from unauthorized redesign.

Supply, to the extent relevant to the particular task:

| Material | Required contents | Why Work Supervisor needs it |
| --- | --- | --- |
| **Task brief** | Purpose, users, expected functionality, scope, explicit exclusions, deliverables | Prevents drifting into adjacent research or feature work |
| **Authoritative design references** | Exact files/paths/revisions and precedence order; relevant architecture, vocabulary, evaluation, and implementation specifications | Avoids treating historical ideas as current decisions |
| **Design rationale** | Core economic questions, rationale for major decisions, known tradeoffs, alternatives considered and rejected (with reasons) | Enables sound supervision when implementation choices are not pre-specified |
| **Economic philosophy** | Preference for useful, established fixed-income approaches when adequate; practical ETF selection and trading decisions as the final objective; acceptance of reasonable investment assumptions without pretending returns are guaranteed | Prevents returning to unnecessary custom analytical machinery or overcautious refusal to make useful judgments |
| **Decision boundaries** | What Work Supervisor may change, what requires the next Design Chat review, and what to report unresolved | Limits silent redesign while allowing autonomous progress |
| **Acceptance evidence** | Expected tests, key scenarios, economic checks, relevant comparisons, known counterexamples | Lets Work Supervisor inspect results instead of accepting Coding Agent's self-report |
| **Environment** | Accessible repository/workspace, branch or base revision, allowed tools, data access, outputs and destination | Avoids execution delays and writing to unintended locations |
| **Open questions** | Undecided matters, permissible assumptions, known ambiguities | Keeps uncertainty visible rather than silently resolving it as settled fact |
| **Operational instructions** | Roles, phase boundary, iteration limits, token-economy policy, final report schema | Directs the automatic Work Supervisor/Coding Agent/Fixed-Income Reviewer cycle |

**Document authority rule:** Do not silently assume earlier Bondview-v2 mechanisms (for example, custom State Classification or Rule Mapping) are authoritative in v3. They may be relevant history or comparative material only if the approved v3 assignment calls for them. A list of rejected approaches is not the same as an absolute prohibition on all heuristics.

**Practical principle:** A concise, explicit rationale plus authoritative documents is preferable to copying all past chat turns. Work Supervisor should label conflicts and missing premises rather than manufacturing certainty.

---

## 4. Work Supervisor's Understanding Review Before Execution

This is an **active comprehension check**, not merely a restatement or a request for Work Supervisor to design the system again. Work Supervisor should produce a short but substantive review containing:

1. **Understanding:** Its own statement of the goal, current design, boundaries, relevant source precedence, and expected outputs.
2. **Inferences:** Necessary assumptions and reasonable interpretations *not explicitly established* by the sources; identify them clearly as inferences.
3. **Counterarguments:** Internal inconsistencies, important omitted decisions, simpler alternatives, or substantive economic concerns; distinguish blockers from optional improvements.
4. **Decision examples:** A few concrete choices Work Supervisor would make if the Coding Agent introduced a new economic heuristic, if tests passed but economic output seemed questionable, or if the Fixed-Income Reviewer preferred another model.
5. **Execution plan:** The proposed role division, evaluation gates, iteration/usage limits, and final deliverables.
6. **Questions that genuinely block execution:** Keep these narrowly scoped and avoid re-opening approved choices merely because alternatives exist.

Design Chat then manually reviews Work Supervisor's response and may approve, correct, narrow, or expand the delegation. **Until the user confirms authorization in Work Supervisor, understanding validation is not permission to implement.**

### Suggested Work Supervisor response classification

- **Confirmed by authority:** Directly established by approved instructions or documents.
- **Interpretation:** A plausible inference requiring care, not an approved design requirement.
- **Objection:** A criticism or alternative offered for Design Chat's consideration, not permission to change the design.
- **Delegated decision:** A choice Work Supervisor is expressly allowed to make later without returning to Design Chat.

Design Chat's final corrections supersede Work Supervisor's provisional interpretations. Work Supervisor should record the resolved mandate before calling Coding Agent or Fixed-Income Reviewer.

---

## 5. Agent Responsibilities and Review Perspectives

### Work Supervisor — Work Supervisor and sole integrator

Work Supervisor owns assignment interpretation, scope control, implementation inspection, expert consultation, final dispositions, iteration limits, and final reporting. Work Supervisor must:

- Direct Coding Agent with an actionable implementation specification, not vague aspirations.
- Compare material code changes, outputs, and tests against the design; use Coding Agent's summary as evidence to verify, not as sole proof.
- Keep an issue/decision ledger for material disagreements and changes.
- Ask Fixed-Income Reviewer for a substantive *economic* assessment without prescribing agreement.
- Debate Fixed-Income Reviewer's objections and, where justified, instruct Coding Agent to revise; re-engage Fixed-Income Reviewer for materially changed economic logic.
- Produce the final answer itself, including the rationale for accepted **and rejected** expert objections.
- Record unresolved questions rather than quietly inventing binding design decisions.

### Coding Agent — Coding Subagent

Coding Agent owns coding, testing, debugging, and implementation evidence **under Work Supervisor's direction**. It should:

- Study the task-relevant sources and repository guidance before editing.
- Follow the approved design and clearly disclose implementation assumptions.
- Avoid unnecessary custom economic machinery without a defensible task-specific reason.
- Deliver changed-file references, meaningful diffs, test commands/results, representative outputs, constraints, and any deviations.
- Escalate design ambiguities to Work Supervisor; never settle major economic design questions simply because a particular implementation is convenient.
- Avoid introducing a second manager or independently reporting the final result to the user or Design Chat.

**Technical distinction:** Here Coding Agent is a **Work-delegated coding subagent**. This may satisfy much of the same functional role as Codex, but it is not automatically the user's independent Codex session. Code-quality parity, environment compatibility, and inherited settings are **not guaranteed** and remain items for actual Work setup verification.

### Fixed-Income Reviewer — Fixed-Income Expert Subagent

Fixed-Income Reviewer owns the independent **economic review** of the implemented approach, with emphasis on practical bond ETF selection and decision support. It should:

- Examine the *actual* implemented economic method, assumptions, inputs, outputs, and relevant evidence; it need not run an application if sufficient review material exists.
- Test whether the economic question is sensible and whether conclusions are useful for ETF comparisons or decisions.
- Consider conventional models and metrics (such as duration/convexity, expected rates and curves, carry, rolldown, and valuation where applicable) before endorsing novel heuristics.
- Challenge unnecessary State Classification, Rule Mapping, arbitrary scoring, or other invented constructs if simpler conventional analysis is adequate; do **not** assume all custom rules are categorically invalid.
- Provide concrete objections, their significance, their evidentiary basis, potential alternatives, and implications for the result.
- Discuss findings **only with Work Supervisor**, including Work Supervisor's counterarguments, and be willing to revise or qualify its view when persuaded.
- Avoid treating uncertainty in realized returns as a reason to reject all useful ETF preferences, while not pretending any method guarantees performance.

**Information sharing versus independence:** Strict information isolation between Work Supervisor and Fixed-Income Reviewer is **not required** for the initial design. Fixed-Income Reviewer may read relevant documentation. Independence comes from an explicit different evaluative question: **“Even if correctly implemented, is this economically well justified and useful?”** To reduce anchoring, Work Supervisor should initially foreground the actual method/results and not only its own defense of them.

---

## 6. Delegation, Disagreement, and Decision Authority

The review is **not** a requirement that Fixed-Income Reviewer automatically approve every final result. Fixed-Income Reviewer can disagree and Work Supervisor can reasonably reject an objection. The essential condition is that Work Supervisor makes and records a defensible judgment.

| Situation | Authorized Work Supervisor response |
| --- | --- |
| Programming error or failure to meet approved requirements | Instruct Coding Agent to fix; verify evidence |
| Clear mathematical/economic calculation error within agreed design | Instruct Coding Agent to correct and, if material, request Fixed-Income Reviewer re-review |
| Equivalent, simpler method within the explicitly delegated implementation latitude | Evaluate and instruct Coding Agent if justified; document choice |
| Fixed-Income Reviewer challenges whether the approved economic model itself is sensible | Debate with Fixed-Income Reviewer; decide only within delegated scope; otherwise record a recommendation for Design Chat |
| Competing defensible economic assumptions without a decisive answer | Record tradeoffs and Work Supervisor's rationale; do not force consensus |
| Proposal changes the primary economic question, investment objective, authoritative architecture, or other reserved decision | Do not silently redesign; preserve the approved baseline where feasible and flag for later Design Chat review |
| Work Supervisor and Fixed-Income Reviewer repeat positions without new evidence | Stop discussion; record disagreement and decision |

**Routing rule:** Any Fixed-Income Reviewer → Coding Agent change request must be mediated by **Work Supervisor**. Fixed-Income Reviewer cannot issue binding implementation instructions independently. Design Chat receives only the eventual consolidated Work Supervisor deliverable, via the user.

**When Fixed-Income Reviewer raises a major objection:** Work Supervisor should first ask whether it is (i) a wrong implementation of accepted design, (ii) a flaw in the accepted design, or (iii) a different but reasonable analytical preference. Each calls for a different response. This avoids endless cycles in which each alternative merely exposes another uncertainty.

---

## 7. Finite Loops and Token-Efficiency Rules

### Loop termination

No autonomous process should wait for “no conceivable objection remains.” Completion must be based on **material acceptance criteria, bounded iterations, and clearly reported exceptions**.

Proposed **initial, adjustable** limits for the first deployment (not product hard limits):

| Limit | Initial policy |
| --- | --- |
| Work Supervisor↔Coding Agent pre-review implementation cycles | Up to **3 substantive rounds** |
| Fixed-Income Reviewer economic review passes | **1 initial**, plus at most **1 focused re-review** after a material change |
| Work Supervisor↔Fixed-Income Reviewer exchanges on a single objection | Up to **2 substantive exchanges** unless new evidence materially changes the issue |
| Work Supervisor↔Coding Agent post-Fixed-Income Reviewer correction cycles | Up to **2 substantive rounds** |
| Repeating the same objection without new evidence | **Stop** rather than retry indefinitely |
| Exceeding limits, missing permissions, or unresolved authority | Stop safely and submit a **partial/blocked** final report with evidence |

These numbers are starting defaults for discussion, not empirically optimized thresholds. Design Chat can change them in the Handoff Package. Work Supervisor should maintain a simple round counter and issue ledger. Prompt-level limits guide behavior but **do not constitute a machine-enforced runtime cap**. Any hard cost or execution-time guard requires supported platform controls or external runtime enforcement.

### Recovery checkpoints for long runs

To mitigate task interruption, Work Supervisor should save a compact checkpoint after provisional coding completion and after each substantive economic review/revision. Record: assigned design revision, implemented file references, last tests, open objection, decision, next action, and remaining allowed rounds. A checkpoint is an audit artifact, **not** a guarantee that the platform can resume the same child thread after an interruption.

### Token and work-economy priorities

1. **Quality-preserving economy:** Minimize redundant work, not verification essential to a defensible outcome.
2. **Sequential specialization:** Use Coding Agent for implementation, then Fixed-Income Reviewer for the provisional economic review. Do not keep both active unnecessarily.
3. **Bounded prompts:** Give Coding Agent the needed design references and focused task; give Fixed-Income Reviewer actual economic logic and key outputs rather than dumping every terminal log.
4. **Evidence on demand:** Work Supervisor reads targeted diffs, affected modules, failing tests, or source sections as needed; do not blindly trust a narrative summary or repeatedly ingest the whole repository.
5. **No speculative breadth:** Do not spawn extra agents, analyze unrelated constituents, or expand project scope without specific justification.
6. **Selective re-review:** If Coding Agent changes only presentation, do not automatically request a full economic re-review. If economic logic changes, do request focused Fixed-Income Reviewer input.
7. **Prefer bounded improvements:** Stop when additional rounds bring no material new evidence or improvement.
8. **Visibility:** Report number of substantive rounds and usage information **when the platform actually exposes it**. Do not invent token counts or equate instructions with a guaranteed spend cap.

Work and subagents consume usage for their own model/tool activity. Token efficiency can be a **soft operational constraint**; exact per-task token or monetary consumption cannot be predicted from the prompt alone.

---

## 8. Work Supervisor Launch Instructions (Reusable Prompt)

The following prompt is intended to be supplied to a **new Work session acting as Work Supervisor**, together with the task-specific Handoff Package. It expresses the desired operating structure, not a claim of executable agent-configuration syntax.

> **Replace bracketed placeholders before use.** The user should first run **Phase 1 only**, manually obtain Design Chat's review, then explicitly authorize Phase 2 in the same Work Supervisor session.

```text
You are the Work Supervisor, the Implementation Supervisor for Bondview-v3.

The user and Design Chat have completed the design discussion outside this Work
session. Communication between Design Chat and Work Supervisor is MANUAL and mediated by the user.
Do not attempt to automate messages to Design Chat or report to Design Chat yourself.

Read these supplied materials before acting:
- Approved assignment: [task brief / attached document]
- Authoritative design: [exact file(s), revisions, precedence]
- Design rationale and decision limits: [reference]
- Acceptance criteria, environment, deliverables: [reference]

Your final responsibility is to deliver ONE consolidated implementation result
that is defensible against the approved specification and expert objections.
Do not simply forward Coding Agent's report or Fixed-Income Reviewer's objections as your final answer.

PHASE 1 — UNDERSTANDING VALIDATION (NO IMPLEMENTATION)
1. Read the material and state your understanding in your own words.
2. Separate confirmed requirements from inferred assumptions.
3. Identify substantial counterarguments, contradictions, missing premises,
   and more established approaches worthy of consideration.
4. Explain a few consequential decisions you would make if Coding Agent or Fixed-Income Reviewer raises
   unforeseen implementation or economic issues.
5. Present your intended Coding Agent/Fixed-Income Reviewer delegation plan, completion criteria, finite
   iteration limits, and token-economy policy.
6. Do not spawn Coding Agent or Fixed-Income Reviewer, modify files, or begin implementation.
7. Stop and wait for explicit authorization in THIS Work session. The user
   will relay your understanding review to Design Chat and convey Design Chat's response.

PHASE 2 — AUTONOMOUS IMPLEMENTATION (ONLY AFTER AUTHORIZATION)
1. Record the approved scope and any corrections from the user/Design Chat.
2. Delegate to a CODING AGENT. Coding Agent must implement, test, document key
   assumptions, disclose deviations, and return concrete evidence.
3. Inspect Coding Agent's work for actual design compliance and test sufficiency.
   Iterate with Coding Agent within the authorized scope and finite round limit.
4. On provisional completion, delegate to an independent FIXED-INCOME
   FIXED-INCOME REVIEWER. Fixed-Income Reviewer must review actual economic methods and outputs,
   question unnecessary custom machinery, consider conventional alternatives,
   and assess practical bond ETF selection value.
5. Fixed-Income Reviewer reports ONLY to you. Discuss meaningful objections directly with Fixed-Income Reviewer.
   Do not require Fixed-Income Reviewer's unconditional agreement and do not dismiss objections
   merely because the code follows the approved design.
6. When warranted and permitted, YOU revise the implementation specification
   and direct Coding Agent. If economic logic materially changes, request a focused
   re-review from Fixed-Income Reviewer. Repeat only while justified, within finite limits.
7. Do not change reserved design decisions without authorization. Where
   new fundamental decisions are needed, preserve the feasible baseline,
   document the issue, and deliver a partial result if necessary.
8. Avoid unnecessary subagents, repeated full-context dumps, unproductive
   debate, and irrelevant exploration. Do not sacrifice essential tests or
   economic validity merely to save tokens.
9. Independently verify the final state. You alone produce the final report,
   including implemented behavior, evidence, Coding Agent/Fixed-Income Reviewer disputes, your decisions,
   deviations, unresolved issues, and artifact/revision references.

DEFAULT ROUND LIMITS (override only if approved materials specify otherwise)
- Up to 3 substantive Coding Agent cycles before Fixed-Income Reviewer's initial review.
- 1 initial Fixed-Income Reviewer review plus at most 1 focused Fixed-Income Reviewer re-review.
- Up to 2 substantive Work Supervisor-Fixed-Income Reviewer exchanges for each objection absent new evidence.
- Up to 2 substantive Coding Agent correction cycles after Fixed-Income Reviewer's initial review.
- Stop if an issue only repeats without new information.

If a tool, subagent feature, repository, or necessary permission is not
available, report the specific blocker rather than falsely implying that
implementation, review, or autonomous execution occurred.

Final output must come from Work Supervisor and be addressed to the user, who will then
manually bring it back to Design Chat for further discussion.
```

### Suggested subagent briefs for Work Supervisor to adapt

**Coding Agent (summary):**

```text
Implement the approved Bondview-v3 task exactly within the delegated scope.
Inspect the authoritative documents and affected code. Avoid unapproved
custom economic mechanisms. Run relevant tests and provide changed-file
references, representative outputs, assumptions, deviations, and unresolved
questions. Return findings and evidence to Work Supervisor; accept revision requests
from Work Supervisor. You do not own the final deliverable.
```

**Fixed-Income Reviewer (summary):**

```text
Review the ECONOMIC substance of the implemented Bondview-v3 functionality.
Treat the actual methods and outputs as reviewable, not self-justifying.
Question whether established fixed-income methods and reasonable conventional
assumptions can achieve the ETF decision-support objective more simply and
more defensibly. Identify material issues with evidence, implications, and
alternatives. Debate objections with Work Supervisor and reconsider them when new
reasoning or evidence is provided. Do not direct Coding Agent and do not report to Design Chat or
the user. You do not own the final deliverable.
```

---

## 9. Work Supervisor's Required Final Deliverable

**Work Supervisor, not Coding Agent or Fixed-Income Reviewer, is responsible for the final consolidated report.** The final report should stand alone well enough for the user to bring it back to Design Chat without reproducing all agent transcripts.

Recommended sections:

1. **Executive result:** Complete / partially complete / blocked, with an accurate description of what exists.
2. **Implemented scope:** Features, outputs, source revision or changed files, and how to run or inspect them.
3. **Design compliance:** Trace essential approved requirements to actual implementation or explicit exceptions.
4. **Verification evidence:** Tests, economic scenarios, outputs, known limitations, and what was not checked.
5. **Economic review:** Fixed-Income Reviewer's major objections and alternatives, including critical issues even if not accepted.
6. **Work Supervisor's reasoned decisions:** Accepted, rejected, or deferred objections and why; any Coding Agent revisions made as a result.
7. **Deviations and reserved decisions:** Any unauthorized change avoided, scope compromise, unresolved issue, or next decision for Design Chat.
8. **Execution ledger:** High-level Coding Agent and Fixed-Income Reviewer rounds, significant failures and recoveries, and available (not guessed) usage information.
9. **Final artifact references:** Paths, file names, revisions, and links that actually exist.

Design Chat should be able to distinguish **what the approved design required**, **what Work Supervisor decided within its discretion**, **what Coding Agent actually implemented**, **what Fixed-Income Reviewer disputed**, and **what remains unsettled**.

---

## 10. Evidence-Based Feasibility Review (2026-10-14)

This section distinguishes **product documentation**, **user-reported observations**, and **unverified target-workflow behavior**. Documentation can establish that a feature is offered; it cannot prove that the exact multi-round Bondview workflow will work in a particular account.

### 10.1 Officially documented capabilities

| Requirement | Evidence-based status | Practical implication |
| --- | --- | --- |
| Create task-focused subagents from a parent Work chat | **Documented, subject to eligibility** | The Work Supervisor can request a Coding Agent and Fixed-Income Reviewer. The actual feature must be visible in the selected account. |
| Collect child results, route follow-up requests, wait for agents, and close threads | **Documented orchestration primitives** | Mechanisms for Work Supervisor ↔ child discussion exist. This is not a guarantee of success across every multi-round run. |
| Run code/shell commands, inspect/edit files and repositories | **Documented within available tools/environment** | The Coding Agent can plausibly implement and test Bondview, provided the selected Work environment grants access. |
| Give distinct instructions/perspectives to children | **Documented task delegation** | Role separation is possible by prompting; a custom TOML agent profile is **not required** for the initial Work proposal. TOML custom-agent files are a distinct Codex-local facility. |
| Subagents operate in a hosted Work environment | **Documented for Work Cloud** | A Work Cloud session does **not** automatically use the user's Ubuntu checkout, Codex CLI config, dependencies, or authenticated local tools. |
| Subagents consume additional model usage | **Documented** | Sequential, narrowly scoped children and limited reruns are prudent. Work and Codex may share the same plan allowance/credits. |
| Permissions and actions needing consent | **Documented constraints** | Subagents inherit parent capabilities; a request for unattended operation cannot override authorization rules. |
| Strict cap on number of review rounds or task tokens via prompt | **Not a guaranteed product control** | Treat round and economy policies as soft rules, not reliable programmatic kill switches. |
| Coding Agent has identical performance to standalone Codex | **Not established** | Same broad coding class does not demonstrate coding-tool or quality parity. Do not assert it. |
| Exact Work Supervisor → Coding Agent → Fixed-Income Reviewer → Coding Agent → Reviewer → Supervisor completion | **Not independently verified in this review** | Run the small operational probe in §10.3 before relying on autonomous Bondview implementation. |

**Primary official sources:**

- [OpenAI: Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents): eligibility, tools, follow-up routing, hosted environment, parent permissions, additional token usage, and Work UI visibility.
- [OpenAI: Use ChatGPT](https://learn.chatgpt.com/docs/use-chatgpt): Work code/shell and repository capability; local vs cloud execution.
- [OpenAI Help: ChatGPT Work and Codex](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex): Work/Chat/Codex distinction, platform, environment access, and shared usage model.
- [OpenAI Help: Using Credits for Flexible Usage in ChatGPT](https://help.openai.com/en/articles/12642688-using-credits-for-flexible-usage-in-chatgpt-personal-plans): plan allowance, credits and usage visibility.
- [OpenAI: ChatGPT Work Overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview): environment separation, code/shell and local access; some features are enterprise-specific and **must not** be presumed available on personal plans.

### 10.2 Public usage reports: useful cautions, not proof of the target workflow

Publicly available examples have different credibility and coverage. **A GitHub issue is a user report, not a confirmed current product defect.** Issues may describe old versions and may have been resolved.

1. **Work-native availability issue:** [openai/codex #33559](https://github.com/openai/codex/issues/33559), opened 2026-07-16, reports subagent spawn/wait tools were not exposed in the reporter's ChatGPT Work and Codex Desktop runtime. It was closed as *not planned*. This conflicts with treating documentation as proof that every account already has working tools. It does **not** negate the current official feature description.
2. **Repeated reviews can run away:** [openai/codex #38989](https://github.com/openai/codex/issues/38989), August 2026, describes a Codex multi-agent session with unusually large delegation and repeated review/fix loops. The reported large token tally is a log-derived counter and must not be converted into an invoice estimate. This is a **Codex case**, not evidence of the same defect in Work; it motivates bounded review.
3. **Work task interruption:** [openai/codex #50753](https://github.com/openai/codex/issues/50753), opened 2026-10-04, describes a user-reported long Work job interrupted without a reliable recovery checkpoint. The report itself says the root cause was not established. Long tasks therefore need checkpoints and final artifact verification.
4. **Subagent implementation/review in practice:** [Endian Dev, 2026-08-12](https://endian.dev/blog/2026/84.5/) describes a developer's subagent-oriented implementation/review workflow; its platform and exact setup are **not equivalent evidence for this Work-specific Bondview chain**.
5. **A described Work task with multiple roles:** [OMIKINA, 2026-08-31](https://omikina.com/article/386d2daf4c8ce934b7f9) reports a multidisciplinary agent audit and tests. This is an author's case description, not a reproducible third-party verification of a supervisor holding an extended economic discussion with a revisable coding agent.

**Search outcome:** The official primitives are credible; we did **not** find a sufficiently documented, independently reproducible example of *this exact Work-based sequential two-subagent negotiation-and-revision workflow* on an eligible personal account. Treat that as an **evidence gap**, not proof of impossibility.

### 10.3 Minimal operational feasibility probe (not a Bondview quality benchmark)

The separate companion file `bondview_v3_work_subagent_smoke_test_20261014.md` gives a ready-to-paste Work prompt and observable pass/fail checks. It uses an isolated, dependency-free **zero-coupon bond calculator** with two compounding conventions only to force a reproducible handoff across agent roles. **It does not evaluate bond-model sophistication, investment performance, or quality relative to previous Bondview work.**

Test conditions:

1. In the actual Work environment chosen for later use, open a **new Work session**. Use only an isolated disposable work directory; do not attach the real Bondview repository.
2. Ask the Work Supervisor to **actually spawn** a Coding Agent and Fixed-Income Reviewer, not simulate their dialogue.
3. Verify a real changed file and unit-test output from the Coding Agent, and an actual review from the separate Reviewer thread.
4. Require a reviewer follow-up, a substantive coding revision routed via Supervisor, a focused economic re-review, and Supervisor-authored final synthesis—without extra user prompts.
5. Check Work's agent activity UI and the generated artifacts. Record `PASS`, `PARTIAL`, or `BLOCKED` with specific evidence. If the account offers no subagent tool, report the blocker; **do not pretend this is success**.
6. Inspect Settings → Usage before and after if available; note that the difference is a *small-sample observation*, not a reliable predicted cost for full Bondview work.

A failed smoke test might reflect feature rollout, permissions, runtime, unavailable file tools, agent messaging, or a misinterpreted prompt. Its diagnostic report should separate these rather than conclude that the whole idea is inherently impossible.

### 10.4 Still unverified on the target account

- Whether Work and subagent creation are enabled for the user's current plan/client and selected model.
- Whether the precise Work environment can access and modify the intended Bondview-v3 source code and run its tests; **Work Cloud does not inherit local Ubuntu files automatically**.
- Whether a reviewer child can receive and answer a **follow-up within the same task** after an implementation revision, rather than only returning a one-time summary.
- Whether a supervisor can execute the whole bounded sequence without asking the user for intermediate approval for **authorized** file operations.
- Whether the requested per-agent model/reasoning selections are honored in the Work surface used, and how usage is exposed.
- Whether Work's coding agent yields results as capable as the user's existing Codex workflow. No parity claim or retrospective v2 quality comparison is appropriate.
- Whether a long task can preserve evidence, make verifiable artifacts, and recover sensibly if interrupted.

For an account-specific test, use the **actual desired Work surface** (web/cloud or supported desktop/local). Do not substitute a Codex CLI test and claim it verified Work subagents.

---

## 11. Proposed Decision for the Next Bondview-v3 Review

The provisional choice is to **prefer a single Work session led by the Supervisor with two specialized subagents: Coding Agent and Fixed-Income Reviewer**, rather than build a bespoke orchestrator or use API-priced designer and reviewer agents at the outset.

The first decision is not whether this workflow produces better financial models than the previous Bondview implementation. It is whether an eligible Work session can be given this handoff, report its understanding for **manual Design Chat/Work Supervisor validation**, and subsequently supervise a **bounded, autonomous Work Supervisor/Coding Agent/Fixed-Income Reviewer implementation-review-revision loop** ending in **Work Supervisor's single consolidated result**.

If that works and produces credible audit evidence, the workflow can be refined for real Bondview-v3 tasks. If it does not, the technical limitation should be documented before considering more elaborate alternatives.

**Review status:** Proposed for reconsideration; no final decision or execution claim is made by this document.
