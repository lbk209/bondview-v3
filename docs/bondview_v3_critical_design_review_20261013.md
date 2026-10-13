# Bondview-v3 — Critical Design Review

**Review date:** 2026-10-13  
**Repository:** [lbk209/bondview-v3](https://github.com/lbk209/bondview-v3)  
**Branch reviewed:** `main`  
**Status:** Provisional review for discussion; no design decisions accepted by this report alone.  
**Scope:** Architecture and examples review. No implementation or repository changes.
**Revision:** Revised after the project-owner clarification that *practical ETF selection and trading decision support is the ultimate objective*. Economic analysis is a means to that objective, not the final deliverable. This revision supersedes the earlier review's excessive caution toward practical judgments; it does not imply acceptance of the current draft architecture or examples.

## Review request

Critically examine the current Bondview-v3 `main` drafts against an ETF-first, established-fixed-income approach, and recommend how to revise the architecture and examples before an MVP. The project is intended to **help investors select, buy, hold, and review actual Korean-listed U.S. bond ETFs**, not just describe markets. Reasonable financial conventions, transparent scenarios, and practical investment policies are legitimate ways to reach actionable conditional conclusions; neither predictive certainty nor theoretical optimality is required. The principal mistake to avoid from v2 is building extensive bespoke state/score/rule machinery without first testing simpler, established economic approaches.

# 1. Overall assessment

The review concerns the three `main`-branch files inspected for the original assessment:

- [bond_etf_decision_architecture.md](https://github.com/lbk209/bondview-v3/blob/main/docs/bond_etf_decision_architecture.md)
- [bond_etf_decision_examples.md](https://github.com/lbk209/bondview-v3/blob/main/docs/bond_etf_decision_examples.md)
- [AGENTS.md](https://github.com/lbk209/bondview-v3/blob/main/AGENTS.md)

**Conclusion: The drafts represent a worthwhile break from v2, but their practical decision method and underlying fixed-income approximations need to be made more coherent before becoming an MVP contract.**

The drafts already reject compulsory Components, State Classification, Rule Mapping, and ordinal attractiveness scores. Their main remaining weaknesses are not the *existence* of investment judgments, but the fact that certain illustrative assumptions have become disproportionately decisive without demonstrating that they are useful or robust:

1. The `P-RISK12` policy fixture (12-month horizon, +100 bp stress, 10% loss budget) does substantial decision-making work in Examples A–C. It can be retained as a **legitimate illustrative policy**, but should not silently become the project's universal recommendation rule.
2. Some cash-bond carry and hedged-KRW compensation assumptions are too convenient for hypothetical examples; the architecture must specify practical, credible approximations that can be supported by actual ETF information.
3. Market yield movements, current ETF duration, and potential key-rate/spread sensitivities need a clearer exposure-to-risk-factor relationship.
4. The examples should demonstrate **actionable preferences and review decisions**, rather than merely getting financial formulas right or explaining why certainty is unavailable.
5. A narrower initial ETF scope would test the central economic and decision mechanism faster, without requiring full attribution or every product-specific model.

**Recommended direction:** Keep the ETF-first quantitative core, but organize it around practical questions—*which ETF fits an intended role, whether buying now is reasonable under declared assumptions, how it compares with alternatives, and what would change a holding decision*. Use simple established calculations to reach and explain those judgments. Missing precision should constrain confidence, not automatically prohibit a useful recommendation.

### Principles to retain

- Analyze real ETF instruments and their actual economic exposures directly, without automatically collapsing them into Short/Intermediate/Long buckets.
- Use established duration, convexity, spread, carry/roll, and FX relationships when appropriate to the product.
- Preserve meaningful continuous quantities and comparisons; do not replace conventional finance with an integrated custom attractiveness score.
- Separate measured inputs, simplifying conventions, hypothetical scenarios, and action recommendations—**without treating those as isolated deliverables**.
- Keep independent Duration/Curve/Credit/compensation interpretation available as supporting analysis.
- Allow reasonable assumptions, scenarios and explicit policy judgments without demanding a forecast of future yields or superior realized performance.
- Reject unsupported precision and arbitrary decision rules, not judgment itself.

# 2. The three most important architectural problems

## 2.1 A useful illustrative investment policy is not a universal decision rule

**Relevant sections:** Architecture §§5–5.2; Examples A–C.

`P-RISK12` assumes a 12-month horizon, a hypothetical +100 bp rate shock, a 10% maximum modeled loss, and an estimated 12-month KRW-hedged carry. These are reasonable *illustrative* assumptions for a risk-controlled investor; there is no objection to using them to generate concrete `consider_purchase` or `defer_new_purchase` conclusions.

The issue is whether the current drafts treat one particular screen as the general foundation of ETF recommendations. The fact that one ETF passes a 10% screen while another fails may show **suitability for that mandate**, but it does not establish relative economic attractiveness for other mandates. A defined long-duration hedge can legitimately justify retaining or purchasing exposure even when the same stress screen fails.

For instance, duration 15 implies a first-order price effect of roughly -15% for a +100 bp rate increase, before convexity. That is a useful risk estimate; the decision meaning depends on the ETF's role and alternatives.

**Revision:** Keep `P-RISK12` as one test case, not the central *architecture*. Add a small number of clearly distinguished purposes (e.g., capital preservation, income/compensation, and deliberate duration exposure) where differences matter. Avoid building a generalized policy engine with many arbitrary knobs.

A default reference investment policy is acceptable for an actionable demonstration when user preferences are unknown, provided it is identified as a **reference assumption rather than a personal recommendation**. The system should still be willing to express a conditional ETF preference or `defer` decision, instead of retreating automatically to a market description.

## 2.2 Shock-plus-carry scenarios need explicit conventions, not perfect path modeling

**Relevant sections:** Architecture §§4.2–4.3; Examples A–C.

The standard first-order sensitivity is:

$$
\frac{\Delta P}{P}\approx-D\Delta y
$$

The examples also employ:

$$
R_{\text{scenario}}\approx\text{12-month net carry}-D(0.01)
$$

**This simplified combination is not inherently wrong.** A duration-based price shock plus a stated income/carry assumption is a useful conventional decision aid, especially when the goal is risk screening rather than a path-dependent forecast. But an instantaneous repricing and a 12-month income estimate do not define a unique 12-month realized-return trajectory. An immediate yield shock and a gradual rise can generate different compensation, reinvestment, and evolving-duration effects.

**Revision:** Preserve the simple scenario and identify its convention precisely (for example, *a static-duration, horizon-end repricing approximation with separately assumed period carry*). Display the shock-driven price effect and the period compensation separately before their combined result. Use convexity when material and available; otherwise label the approximation. For ETFs that continually rebalance, do not silently apply a static held-bond roll-down assumption.

The MVP need not simulate monthly yield paths or rebuild security-level holdings to produce a practical stress comparison. Additional modeling is justified only if it would materially change the recommendation.

## 2.3 ETF yield and hedged-KRW compensation need workable estimates

**Relevant sections:** Architecture §§3.1–3.2, 4.3–4.4.

The draft correctly distinguishes portfolio yield, distribution yield, market Treasury yields, and modeled carry. But Examples A–C obtain practical decision labels primarily because hypothetical hedged-KRW net carry is simply supplied. For real Korean-listed U.S. bond ETFs, it may depend on issuer-reported USD portfolio yield, hedge structure, FX forward points and rate differentials, rebalancing, and instrument mechanics.

The implication is **not** that Bondview must solve a perfect net-carry model before recommending ETFs. The implication is that the initial MVP needs a *credible and explainable approximation policy*:

1. Report the issuer's published ETF yield measure with its exact convention and date.
2. Where sufficiently supported, estimate relevant period compensation in the chosen currency (including a practical hedging adjustment for hedged products).
3. Distinguish the compensation estimate from scenario price effects and from a projected realized return.
4. When data are incomplete, use a defensible range, proxy, or qualitative conclusion if the gap is not decisive; return `insufficient_information` only when that information is materially necessary to the particular decision.

A U.S. nominal yield is not automatically a KRW-hedged return or a directly comparable alternative to Korean cash. Conversely, uncertainty about exact carry should not prevent a recommendation based on product fit and well-measured rate-risk differences.

**Priority:** Test the practicality of this approximation with representative real ETF issuer data early, before committing synthetic carry inputs as a general product contract.

# 3. Missing or insufficiently specified economic relationships

## 3.1 ETF duration must be connected to the appropriate market risk factors

**Relevant sections:** Architecture §§4.1–4.2.

The architecture correctly recommends issuer-reported duration and key-rate duration. However, it does not clearly establish which market yield changes can legitimately be applied to each measure.

There are three different cases:

| Available ETF exposure | Appropriate calculation | Limitation |
|---|---|---|
| Effective or modified duration | Parallel rate-shock sensitivity | Assumes a compatible shift in the relevant yield or curve |
| Key-rate durations | Nonparallel yield-curve sensitivity | Requires matching curve nodes and consistent duration definitions |
| Only approximate maturity segment | Provisional representative-tenor sensitivity | Cannot claim precise portfolio-level response |

For example, an ETF with duration 7.5 need not respond precisely to a 35 bp move in DGS10. Its holdings may be distributed across multiple maturities, and its sensitivity may be concentrated differently from that implied by its name.

Key-rate duration is the conventional method for decomposing sensitivity to different segments of the yield curve.

**Proposed revision:** Define the mapping from ETF risk measures to market observations explicitly. Make effective duration the simple baseline, and use key-rate duration when available and economically necessary.

Do not require detailed yield-curve construction to perform a useful parallel sensitivity analysis.

## 3.2 Comparisons should lead toward an ETF preference, not stop at a table of measures

The draft identifies yield, duration, carry, historical conditions, convexity, and scenarios. These are inputs to a **selection decision**, not the final product. Consider two hypothetical hedged Treasury ETFs:

| Measure | ETF A | ETF B |
|---|---:|---:|
| Assumed annual KRW carry | 4.0% | 5.0% |
| Effective duration | 7 | 15 |
| First-order effect of +50 bp | -3.5% | -7.5% |
| Carry premium over 3% cash | +1.0 pp | +2.0 pp |

A useful, simplified one-year *cash-relative rate break-even rise*, ignoring convexity and roll-down, is:

$$
\Delta y_{\mathrm{BE}}\approx
\frac{\text{Carry}_H-\text{Cash}_H}{D}
$$

| Measure | ETF A | ETF B |
|---|---:|---:|
| Break-even rate rise | **14.3 bp** | **13.3 bp** |

The figures reveal that B's greater carry does not compensate for *proportionally* more rate exposure under this particular comparison. They do not by themselves identify the best ETF.

But an actionable decision **can** follow with a modest, stated purpose. For capital preservation over a one-year horizon, A is a defensible preference under these assumptions; for a deliberate long-duration Treasury allocation, B may be preferable despite the risk. Neither judgment requires a probability distribution for future yields or a custom scoring system.

**Revision:** Every core comparison example should end with (i) common-basis financial quantities, (ii) a declared, sufficiently simple selection purpose, (iii) a practical preference, defer, or no-clear-preference conclusion, and (iv) the main condition that could reverse it. Do not require a universal ranking, but do not regard an unresolved trade-off as the default end state either.

## 3.3 Practical investment judgments do not require yield forecasts

A forecast-free framework can measure present compensation, rate/spread sensitivity, break-even movements, relative cash alternatives, and scenarios without claiming to know the next yield move. Those outputs can **support actionable recommendations under reasonable conventional assumptions**.

The appropriate boundary is not *quantitative analysis versus decision support*, but *transparent conditional reasoning versus unsupported certainty*.

For instance, a 6% starting yield provides more initial nominal compensation than a 4% yield for appropriately comparable exposures. That is potentially a strong reason to reassess an ETF, although a subsequent yield rise can still cause a loss. A practical recommendation may weigh that compensation alongside duration, FX, risk tolerance, ETF role, and the available alternatives—without pretending that 6% predicts a reversal.

**Revision:** Make the decision output a first-class objective of the system. The calculation engine supplies financial evidence; the decision step makes a concrete, clearly conditioned judgment. A straightforward `prefer A`, `consider purchase`, `maintain`, `review exposure`, or `defer` is legitimate when the assumptions and economic evidence justify it. Avoid both forced verdicts and excessive abstention.

This does not require a complex personalized advisory platform. A small, explicit reference-policy set is enough to test whether v3 offers better guidance than product labels or duration-only checks.

## 3.4 Changing conditions should change *actionable* assessments when warranted

The same ETF should be reassessed under different market environments, separating changes in:

- Portfolio yields and compensation relative to cash or alternatives;
- Effective duration, convexity, and curve sensitivity;
- Relevant Treasury yield levels, slopes, and observed movements;
- KRW hedge economics or unhedged FX exposure;
- Product structure and reported portfolio exposures.

That decomposition should explain *why* a new purchase, continued holding, or position review looks different today from an earlier date. The purpose is not merely to report the changes. For example, more favorable carry alongside roughly unchanged exposure could reasonably strengthen a conditional purchase case, even though future rates remain uncertain.

Historical snapshot comparisons and simple counterfactuals are sufficient initially; no continuous historical holdings reconstruction is required. A current yield level or observed trend is never automatically a forecast.

New-purchase and hold/review conclusions must remain distinct: deciding not to add exposure is not automatically a reason to sell an existing holding.

## 3.5 Curve, credit, and FX analyses need consistent exposure matching

The current treatment is directionally correct but should be tightened.

**Curve:** Parallel duration sensitivity is an appropriate baseline. Nonparallel scenarios should use available key-rate sensitivities rather than applying arbitrary maturity labels.

**Credit:** A broad HY or IG OAS series can describe market conditions, but may not match a particular ETF's sector, credit quality, spread duration, or holdings. Market context and product-specific spread sensitivity should be distinguished. Treasury-rate and spread shocks can be modeled separately without assuming they are statistically independent.

**Currency:** Spot USD/KRW changes explain a large part of unhedged historical KRW returns. Hedged compensation additionally requires forward and hedge information. An issuer's hedge policy is an important input, but `(H)` alone is not a numerical hedge specification.

These should be product-dependent calculation choices, not mandatory Constituents or independent attractiveness judgments.

# 4. Review of the existing examples

The existing examples are valuable both as economic tests and as **prototype selection/holding decisions**. They should not be stripped of their recommendation outcomes. Their task is to test whether a simple, transparent model can reach reasonable decisions for stated purposes, including cases where the answer changes with conditions or mandate.

| Examples | Assessment | Recommended treatment |
|---|---|---|
| A/B — Same long ETF, two conditions | Useful test that conditions change a practical purchase judgment; overly dependent on one assumed policy | **Retain decision contrast; broaden economic justification** |
| C — Intermediate vs long Treasury | Useful selection test under a risk-controlled mandate | **Keep the conditional preference; show comparative economics** |
| D — Hedged vs unhedged | Strong FX and product-purpose distinction | Retain; improve treatment of hedge economics where feasible |
| E — Treasury futures | Important structural constraint | Retain; defer complete futures model if MVP scope requires |
| F — High-yield credit | Meaningful rates-versus-spread decision | Retain; keep credit mandate distinct |
| G — Short USD credit-mixed | Prevents a misleading 'short Treasury' proxy | Retain as product-fit validation; may consolidate presentation |
| H — Market-only curve | Valuable explanatory capability | Retain as supplementary analysis, not the main MVP deliverable |
| I — ETF return and FX reconciliation | Partially overlaps D | Combine or simplify without losing a distinct diagnostic case |
| J — Missing information | Valuable confidence and fallback behavior | Retain; test when a justified proxy permits an actionable result |

## 4.1 Examples A and B — Keep the decisions, improve their basis

Example A has duration 17, assumed 4% annual KRW-hedged carry, and a +100 bp sensitivity effect of -17%, producing an illustrative -13% stress outcome. It concludes `defer_new_purchase` under `P-RISK12`'s 10% modeled-loss rule. **That is a defensible policy-conditioned conclusion**, not a failure of the design.

Example B has duration 14.5 and assumed 5% carry against 3% KRW cash. Its simplified stressed result is:

$$
5\%-14.5\%=-9.5\%
$$

This passes the same 10% screen and gives a plausible `consider_purchase` *under the declared mandate and carry convention*. However, a passing stress screen is not proof of a generally attractive investment. The additional comparative evidence is:

$$
\Delta y_{\mathrm{BE}}=
\frac{0.05-0.03}{14.5}
\approx 13.8\text{ bp}
$$

In this simplified horizon-end comparison, a rate increase of about 13.8 bp would eliminate the modeled extra compensation over cash; the +100 bp stress result also trails the +3% cash alternative by **12.5 percentage points**. These are **additional perspectives**, not automatic vetoes: a stress-test threshold and a cash-relative break-even answer different questions.

**Revision:** Retain the `defer`/`consider` contrast; calculate carry, rate exposure, and an appropriate comparison consistently; state explicitly why `consider_purchase` is reasonable for the stated objective and what would change that recommendation. Avoid declaring that a contingent purchase judgment is invalid merely because one cannot predict future yields. Report convexity limits, but do not demand an exact convexity estimate before every provisional opinion.

## 4.2 Example C — Preserve an actionable comparison

Example C's 10Y-oriented hedged ETF has lower assumed duration risk and passes `P-RISK12`, while the long-duration alternative fails. **A preference for the 10Y-oriented ETF is reasonable under this reference risk-controlled objective.** The example should retain that conclusion.

Enhance it by showing the carry premium, risk differences, cash-relative compensation, and (where supported) curve exposure. Make explicit that a long-duration hedge mandate could reverse the preference. Do not reduce the output to `no universal winner` merely because different investors could choose differently.

## 4.3 Examples D, E, F and H — Keep the distinct financial mechanisms

D checks unhedged return translation and hedging; E prevents cash-bond carry formulas being applied blindly to futures; F separates rates and credit-spread effects; H supports independent market interpretation. These remain useful.

A sensible MVP need not fully implement every variant. But where inputs and conventional formulas are adequate, the relevant case should still end with a practical conditional selection/suitability judgment—not solely a description of the risk.

## 4.4 Make example outputs executable *and decision-oriented*

Each revised core example should have:

| Element | Required content |
|---|---|
| Practical decision question | Select, consider buying, maintain, review, or defer for an explicitly identified purpose |
| Inputs | Hypothetical market data and ETF exposure characteristics, with units and dates as needed |
| Conventions | Simple assumptions about horizon, carry, shocks, hedge, and comparator |
| Calculations | Established formulas and hand-checkable expected numbers |
| Economic interpretation | Why the quantities matter to the ETF's role |
| Expected decision | A concrete policy-conditioned output **when justified**, or a specific unresolved condition when not |
| Validation | Numeric tolerances, decision behavior under assumption changes, and missing-data/proxy behavior |

Tests should verify **three separate things**: arithmetic, economically consistent explanations, and application of the stated decision policy. The current action labels can serve as test fixtures while their final interface remains provisional.

# 5. Complexity and premature commitments

The best simplification is to reduce modeling that does not improve practical ETF decisions—not to eliminate useful decision policies or conventional scenario assumptions.

| Current element | Concern | Revision |
|---|---|---|
| 126/21 observations, five-point smoothing (§2, §4.1) | Inherited research defaults, not validated v3 decision requirements | Keep as optional descriptive settings; simple raw changes can establish an MVP baseline |
| +50/+100/-50 bp scenarios | Reasonable stress magnitudes, but not a universal economic rule | Keep a small stress suite and make magnitudes configurable; do not automatically interpret them as probabilities |
| 10% loss budget | Legitimate reference mandate, not a theorem | Retain `P-RISK12` as one example; compare at least one different purpose or tolerance |
| 2Y/10Y/30Y second-difference curvature | Uneven spacing weakens an unqualified curvature interpretation | Prioritize simple slope and applicable key-rate analysis; defer complex factor fitting |
| Seven representative ETFs and ten examples | Wider than necessary for the first runnable core | Start with a few well-documented Treasury ETFs; preserve structural edge cases for subsequent testing |
| Detailed historical return attribution (§4.5) | Significant possible modeling effort with limited immediate selection payoff | Begin with adjusted NAV diagnostics and broad residual explanations |
| Expense ratios and detailed trading costs | Outside initial bond-centered scope | Defer detailed treatment; avoid double-counting costs already in reported returns |
| Fixed decision labels | Risk of constraining the user interface prematurely | Keep provisional action labels as useful test outputs, revisable after feedback |

The architecture diagram in §8 places underlying market explanations after ETF assessment, despite their being independently useful. A more coherent design lets shared data and calculations support both **practical ETF judgments** and **independent market-aspect interpretation**, with the former as the primary goal.

## `AGENTS.md`

The file remains broadly aligned with v3: it identifies the draft documents as provisional, rejects implicit inheritance from v2, discourages speculative abstractions, and preserves source/assumption distinctions. No immediate change is required. Future instructions should explicitly reflect the new foundational point that **practical ETF decision support is the objective** and transparent financial approximations are legitimate.

The session/task-branch workflow is elaborate for a research project but is an operational matter outside this review. Two document links should eventually be fixed: the architecture cites `bond_etf_decision_examples_v1.md`, and the examples cite `bond_etf_decision_architecture_v1.md`; neither matches its current `main` filename. The phrase *accepted repair* in the provisional examples should also be softened.

# 6. Recommended revision strategy

I recommend a focused second feedback cycle that **starts with decisions, uses financial analysis to support them, and tests the economics with real ETF inputs**.

## Stage 1 — Define the smallest useful ETF decision process

Specify two or three practical use cases: (a) whether to buy a given Treasury ETF now under a transparent reference objective; (b) choosing between two real ETFs with different exposure or hedge characteristics; and (c) reviewing an existing holding when conditions change. Distinguish a purchase decision from an automatic sell signal.

For each, identify a small set of conventional economic calculations that can change the decision: relevant yield and compensation, duration/curve shock, credit or FX effects where applicable, and comparison with cash or another ETF. No custom score, constituent taxonomy, or elaborate policy optimizer is needed.

**Expected output:** A clear recommendation or a bounded alternative, supported by quantitative evidence and an explicit small set of assumptions. Market-only analysis remains available, but it is not the end product.

## Stage 2 — Revise the architecture and example tests together

Retain A/B as differing conditions for the same ETF and C as an actual cross-ETF preference. Strengthen their risk/compensation interpretation while allowing their conditional action labels. Keep D/F/E as product-specific counterexamples and H as a market-report test. Test both the stability of a decision under reasonable assumption changes and cases in which a changed investment objective should reverse it.

The examples should prove more than the engine's arithmetic: they should prove that **simple, financially recognizable methods yield meaningful conditional ETF choices** without arbitrary integration.

## Stage 3 — Bound the MVP to accessible ETF data

Choose a small set of Korean-listed U.S. Treasury ETFs with usable issuer-reported exposures. Reproduce synthetic numbers and expected conditional decisions; then run the same method using dated real ETF profiles and independent market series. Check whether a practical carry/hedging approximation is available before broadening the scope.

Compare usefulness against simple baselines such as product facts, duration-only stress, or a plain cash alternative. Evaluate explanation quality and actionability, not merely retrospective hit rates; do not require proof of superior realized returns before considering the design useful.

### Minimal conceptual flow (not a mandated module hierarchy)

```text
Practical ETF question + clear investment/reference objective
                         |
              ETF characteristics ---------
                         |                  \
              Market observations ----> Conventional
                                       calculations
                                            |
                     Comparable compensation, sensitivity,
                     risk scenarios and product constraints
                                            |
                   Explicit, simple investment judgment
                                            |
                  Select / consider purchase / defer /
                         maintain / review exposure

Supporting outputs: independent market (Duration/Curve/Credit)
interpretation and optional realized ETF/NAV diagnostics.
```

**No compulsory integrated score, forecasting layer, or specialized v2 architecture is implied.**

# 7. What should be resolved in the next feedback cycle?

Four focused questions should drive the next architecture/examples feedback cycle:

1. **What practical decision must the initial MVP improve?** Define concrete buy/compare/hold-review cases, a small transparent reference mandate, and what counts as a helpful outcome. Avoid making the market report the only product.
2. **What conventional approximation of compensation is credible for actual Korean ETFs?** Decide which published yield measure, hedge adjustments, carry or roll conventions, and cash comparisons are sufficient for a *practical* recommendation without building an elaborate return-forecast engine.
3. **How should independent market observations map to actual ETF risk characteristics?** Use effective duration for compatible parallel shocks; key-rate, spread, and FX methods when the product demands them; credible proxies when exact inputs are unavailable.
4. **How should decisions respond to uncertainty and changing objectives?** Define when to prefer or defer an ETF, when to review an existing holding, and which material missing facts justify withholding a conclusion. Avoid both an always-buy algorithm and automatic abstention.

These are design questions, not an argument that a fully individualized portfolio policy or a statistically optimal market forecast must be solved first.

# 8. Final recommendation

I would **revise, not replace**, the present architecture. Its ETF-first direction and rejection of v2's bespoke Component/State/Rule infrastructure remain valuable. The largest revision should target Architecture §§4–5 and Examples A–C, with practical ETF judgments explicitly preserved as an intended output.

> **Bondview-v3 should use actual ETF exposures and established fixed-income calculations to support useful selection, buying, holding, and review judgments. It may rely on reasonable, transparent conventional assumptions and simplified scenarios. Quantitative description is supporting evidence—not the project's ultimate objective. Avoid both arbitrary recommendation machinery and excessive caution that prevents defensible practical preferences.**

The review's earlier recommendation to make *quantitative assessment the primary analytical product and investor-specific policy merely optional* was too strong. The better formulation is: **the calculations should be independently understandable and reusable, while the system's primary deliverable is a practical, explicitly conditioned ETF decision or comparison.**

The criticism of making **one particular** 10%/+100 bp fixture decisive for every case still stands. This is a call for a better-founded, simpler decision process—not an objection to decision rules, risk budgets, or investment judgments themselves.

**This is a revision of the local critical review only. No repository files were changed, and no MVP work was started.**

---

## Source documents and further reading

- [Bondview-v3 architecture draft](https://github.com/lbk209/bondview-v3/blob/main/docs/bond_etf_decision_architecture.md)
- [Bondview-v3 examples draft](https://github.com/lbk209/bondview-v3/blob/main/docs/bond_etf_decision_examples.md)
- [Bondview-v3 agent instructions](https://github.com/lbk209/bondview-v3/blob/main/AGENTS.md)
- [CFA Institute — Overview of Fixed-Income Portfolio Management](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/overview-fixed-income-portfolio-management)
- [CFA Institute — Yield Curve Strategies](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-curve-strategies)
- [CFA Institute — Yield-Based Bond Convexity and Portfolio Properties](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-based-bond-convexity-and-portfolio-properties)
