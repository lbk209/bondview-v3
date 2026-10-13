# Bondview-v3 — Critical Design Review

**Review date:** 2026-10-13  
**Repository:** [lbk209/bondview-v3](https://github.com/lbk209/bondview-v3)  
**Branch reviewed:** `main`  
**Status:** Provisional review for discussion; no design decisions accepted by this report alone.  
**Scope:** Architecture and examples review. No implementation or repository changes.

## Review request

Review the current Bondview-v3 `main` branch, focusing on the architecture, examples, and `AGENTS.md`. Critically assess whether the provisional design genuinely follows an ETF-first approach grounded in established fixed-income economics. Identify inconsistencies, missing relationships, premature assumptions, and unnecessary complexity. Recommend a focused revision of the architecture and examples before MVP implementation, without carrying forward v2 decisions by default.

# 1. Overall assessment

I inspected the three files on the current `main` branch:

- [bond_etf_decision_architecture.md](https://github.com/lbk209/bondview-v3/blob/main/docs/bond_etf_decision_architecture.md)
- [bond_etf_decision_examples.md](https://github.com/lbk209/bondview-v3/blob/main/docs/bond_etf_decision_examples.md)
- [AGENTS.md](https://github.com/lbk209/bondview-v3/blob/main/AGENTS.md)

**My conclusion: The architecture represents a substantial and appropriate departure from v2, but it is not yet a fully coherent ETF-first quantitative decision framework.**

The problem is not that the drafts retain the old Component/State/Rule architecture. They largely reject it successfully.

Instead, several new assumptions have become disproportionately influential:

1. A particular investor risk policy has effectively become the main mechanism for generating decisions.
2. The analysis relies heavily on estimated 12-month carry and hypothetical interest-rate shocks, without sufficiently defining the economic relationship between them.
3. The distinction between market observations and actual ETF risk characteristics is sound in principle but insufficiently developed in the calculations.
4. The documents identify useful financial quantities, but have not fully established how those quantities should support buying, holding, or comparing ETFs without forecasts.
5. The proposed MVP encompasses more product structures and analytical branches than necessary to validate the central design.

I would recommend **revising the central economic reasoning before extending the existing documents**, rather than merely incorporating more ETF characteristics into the current structure.

### What should be retained

Several fundamental decisions are economically well-grounded:

- Start with real ETF instruments and their actual exposures.
- Preserve continuous quantities rather than reducing them to categorical states.
- Use conventional duration, convexity, credit-spread, and currency relationships.
- Avoid arbitrary aggregation of independent attractiveness scores.
- Separate observed facts, hypothetical scenarios, and investment judgments.
- Keep market-only analysis available independently of ETF decisions.
- Do not require predictions of future interest rates or ETF returns.

These principles are compatible with the intended v3 direction. They provide a sound foundation for a simpler and more useful system.

# 2. The three most important architectural problems

## 2.1 The investment policy has become too central

**Relevant sections:** Architecture §§5–5.2; Examples A–C.

The current architecture introduces `P-RISK12`, which assumes:

- A 12-month investment horizon
- A +100 bp adverse rate shock
- A maximum acceptable 10% scenario loss
- An estimated 12-month KRW-hedged net carry

These assumptions are explicitly labeled illustrative. Nevertheless, Examples A, B, and C derive their main purchase conclusions from them.

Consequently, the documents risk replacing v2's arbitrary attractiveness scoring with a different arbitrary decision mechanism: a binary risk-budget screen.

The issue is not that risk budgets are inappropriate. They are legitimate investor-policy inputs. The problem is making one particular policy central to the financial architecture.

For example, consider an ETF with effective duration 15 and an estimated annual carry of 5%.

Its instantaneous first-order price sensitivity is:

$$
\Delta P/P\approx-15\Delta y
$$

A +100 bp increase implies approximately a 15% price decline before convexity. That is an economically meaningful measurement regardless of the investor's preferences.

Whether this makes the ETF unsuitable depends on its investment purpose, allocation size, alternatives, and willingness to bear that risk.

**Recommendation:** Make quantitative economic assessment the primary analytical product. Treat investor-specific policy evaluation as an optional subsequent step, rather than the organizing principle of the quantitative engine.

The system should deliver useful information even when no investor loss budget has been specified.

## 2.2 The scenario framework mixes instantaneous price sensitivity and holding-period compensation

**Relevant sections:** Architecture §§4.2–4.3; Examples A–C.

The basic duration formula is established:

$$
\frac{\Delta P}{P}\approx-D\Delta y
$$

However, the examples then calculate:

$$
R_{\text{stress}}\approx
\text{12-month net carry}-D(0.01)
$$

This produces a number labeled as a 12-month stressed result.

That combination can be a reasonable simplified scenario, but it needs an explicit economic convention.

Duration measures the sensitivity of the current price to a change in yield. A 12-month return also depends on the timing of the yield change, evolving duration, reinvestment, curve evolution, and the ETF's portfolio-management behavior.

For example:

- An immediate +100 bp shock followed by unchanged yields is not the same investment path as
- A gradual +100 bp increase over 12 months.

The carry and reinvestment consequences may differ substantially.

The current examples implicitly combine these effects without defining the path.

**Recommendation:** Initially distinguish two calculations.

| Calculation | Meaning |
|---|---|
| Instantaneous rate sensitivity | Approximate current ETF value change for a specified yield shock |
| Holding-period compensation | Income/carry and possible roll effects over a stated period under explicit assumptions |

They can subsequently be combined into a holding-period scenario when the assumptions justify doing so.

This preserves simple conventional calculations without presenting a stylized scenario as a uniquely determined 12-month return.

## 2.3 The relationship between ETF yields, market yields, and KRW compensation is underdeveloped

**Relevant sections:** Architecture §§3.1–3.2, 4.3–4.4.

The documents correctly distinguish ETF portfolio yields from FRED Treasury yields and distribution yields. However, they still rely on assumed KRW-hedged net carry as if it were readily available.

For a Korean investor, the compensation from a USD bond ETF may depend on:

- The actual USD yield associated with the ETF's holdings
- Treasury exposure and relevant credit spreads
- Currency hedge structure
- FX forward points and short-term interest-rate differentials
- Portfolio rebalancing and instrument structure

For hedged ETFs in particular, the U.S. nominal bond yield cannot simply be compared with a Korean cash yield.

Covered interest-rate parity and forward pricing help explain why the currency-hedging adjustment matters.

The architecture acknowledges these issues, but the examples effectively bypass them by supplying hypothetical net carry values of 3.5%, 4%, or 5%.

That is acceptable for testing arithmetic. It is insufficient to establish that the same decision procedure will be practically usable with real ETF data.

**Recommendation:** Separate three distinct quantities:

1. **Published ETF yield measure:** An observed product characteristic with a specified definition.
2. **Estimated economic compensation:** A derived approximation, including necessary currency adjustments where supported.
3. **Scenario return:** A conditional result combining compensation with declared market changes.

Do not require all three to be available before producing a useful ETF assessment.

This is arguably the most important practical data issue to resolve before implementation.

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

## 3.2 The current design does not fully answer what makes one ETF more attractive than another

The architecture lists yield, duration, carry, historical conditions, convexity, and scenarios. But these quantities alone do not define an investment preference.

Consider two hypothetical hedged Treasury ETFs:

| Measure | ETF A | ETF B |
|---|---:|---:|
| Assumed annual KRW carry | 4.0% | 5.0% |
| Effective duration | 7 | 15 |
| First-order effect of +50 bp | -3.5% | -7.5% |
| Carry premium over 3% cash | +1.0 pp | +2.0 pp |

ETF B provides more assumed compensation, but also substantially more rate exposure.

One can calculate useful comparisons, including a break-even rise in yields relative to cash:

$$
\Delta y_{\mathrm{BE}}
\approx
\frac{\text{Carry}_H-\text{Cash}_H}{D}
$$

| Measure | ETF A | ETF B |
|---|---:|---:|
| Break-even rise | **14.3 bp** | **13.3 bp** |
| Calculation | 1.0% carry premium / duration 7 | 2.0% carry premium / duration 15 |

*Illustrative first-order, one-year comparison with matching assumptions, no roll-down or convexity, and the yield shock placed at the comparison horizon.*

Despite its higher carry, ETF B has a slightly smaller break-even rate-rise cushion per unit of duration.

That is economically useful information that neither an ordinal score nor a predefined 10% loss budget is needed to produce.

It still does not establish a universal winner. ETF B may be preferred for deliberate duration exposure; ETF A may be preferred for a shorter risk horizon.

**I recommend making comparisons of this kind central to v3.** The purpose is not to manufacture one optimal metric but to expose economically meaningful trade-offs in a common framework.

## 3.3 The limits of forecast-free decision making should be more explicit

This is a conceptual issue worth settling before implementation.

It is possible to calculate, without forecasting future yields:

- Current compensation relative to a specified alternative
- Rate and spread sensitivity
- Break-even market movements
- Outcomes under hypothetical scenarios
- How these quantities have changed historically

But such calculations do not necessarily demonstrate that purchasing an ETF today has a positive expected excess return.

For instance, a 6% Treasury yield may provide better initial compensation than a 4% yield. That does not establish that long-duration exposure will outperform cash over the next year.

The additional return depends partly on subsequent market developments.

The architecture should therefore distinguish:

**Economic assessment:** What compensation, risks, and conditional outcomes are observable or calculable?

**Investment judgment:** Given an objective and assumptions about acceptable uncertainty, is the exposure appropriate?

This distinction is more fundamental than the particular decision-label vocabulary.

A useful forecast-free system is achievable, provided it does not pretend to derive unconditional buy signals from descriptive quantities.

## 3.4 ETF economics across market environments needs its own explicit analytical procedure

The architecture correctly states that the same ETF should be evaluated under changing market conditions.

But the examples mainly demonstrate this through different values of assumed carry and duration.

A more revealing comparison would distinguish the causes of a changing assessment:

- Did the ETF's portfolio yield increase?
- Did its duration or convexity change?
- Did the relevant yield curve change?
- Did KRW hedging economics improve or deteriorate?
- Did compensation relative to cash change?

The system should be able to compare the ETF at two dates using each date's observed market data and exposure profile, while separately identifying the effects of changing the product exposure itself.

This can be done with ordinary historical snapshots and simple counterfactual comparisons. It does not require reconstructing every historical holding.

Importantly, a higher historical or current yield is an observation about compensation, not evidence that the yield must subsequently decline.

## 3.5 Curve, credit, and FX analyses need consistent exposure matching

The current treatment is directionally correct but should be tightened.

**Curve:** Parallel duration sensitivity is an appropriate baseline. Nonparallel scenarios should use available key-rate sensitivities rather than applying arbitrary maturity labels.

**Credit:** A broad HY or IG OAS series can describe market conditions, but may not match a particular ETF's sector, credit quality, spread duration, or holdings. Market context and product-specific spread sensitivity should be distinguished. Treasury-rate and spread shocks can be modeled separately without assuming they are statistically independent.

**Currency:** Spot USD/KRW changes explain a large part of unhedged historical KRW returns. Hedged compensation additionally requires forward and hedge information. An issuer's hedge policy is an important input, but `(H)` alone is not a numerical hedge specification.

These should be product-dependent calculation choices, not mandatory Constituents or independent attractiveness judgments.

# 4. Review of the existing examples

The current examples are useful as a set of adversarial design tests. However, several have become tests of an unnecessarily specific investment policy rather than tests of the underlying economics.

| Examples | Assessment | Recommended treatment |
|---|---|---|
| A/B — Same long ETF, two conditions | Valuable comparison, but policy-dominated | **Substantially revise** |
| C — Intermediate vs long Treasury | Important cross-ETF test | **Retain, revise decision logic** |
| D — Hedged vs unhedged | Strong economic illustration | Retain, extend hedge assumptions |
| E — Treasury futures | Important product-boundary test | Retain, defer full futures modeling |
| F — High-yield credit | Useful independent rate/spread case | Retain |
| G — Short USD credit-mixed | Correct classification warning | Merge into product validation tests |
| H — Market-only curve | Useful independent market analysis | Retain |
| I — ETF performance and FX | Overlaps substantially with D | Merge into reconciliation tests |
| J — Missing information | Important robustness requirement | Retain as cross-cutting test |

## 4.1 Examples A and B — The most important revision

In Example B, the hypothetical long-duration ETF has:

- Effective duration: 14.5
- Annual KRW-hedged carry: 5%
- KRW cash alternative: 3%
- Assumed +100 bp scenario effect: -14.5%

The document calculates:

$$
5\%-14.5\%=-9.5\%
$$

Since -9.5% is within the illustrative 10% loss budget, it produces `consider_purchase`.

But the same inputs yield:

$$
\Delta y_{\mathrm{BE}}
=\frac{0.05-0.03}{14.5}
\approx 13.8\text{ bp}
$$

In this stylized comparison, a rate increase of only about 13.8 bp would exhaust the ETF's assumed extra annual compensation over cash, before convexity and other omitted effects.

Furthermore, under the +100 bp scenario, the ETF's -9.5% result compares with a +3% cash alternative, a **12.5 percentage-point shortfall**.

Neither calculation invalidates the other. They answer different questions.

But this demonstrates why passing an absolute 10% loss screen and earning a 2% carry premium cannot, by themselves, establish an affirmative purchase rationale.

For long-duration ETFs, convexity also becomes increasingly relevant as yield shocks become large.

**My recommendation:** Retain A and B as a comparison of the same ETF in two economic environments, but have them produce a quantitative assessment first. Add alternative investor policies only as a secondary test.

## 4.2 Example C — Replace the binary winner with a quantified trade-off

Example C currently establishes that the 10Y-oriented ETF passes the assumed loss-budget test while the 30Y-oriented ETF fails.

That proves the policy screen works, but not much about the comparative economic value of the two ETFs.

The example should instead emphasize duration sensitivity, carry compensation, break-even changes, curve exposure where available, and mandate-dependent preference.

A definite choice should appear only if the stated objective and evidence support one.

## 4.3 Examples D, E, F and H — Keep their financial distinctions

These examples are valuable because they test genuinely different economic mechanisms.

D tests currency translation and hedge behavior. E prevents cash-bond formulas from being misapplied to futures. F separates Treasury-rate and credit-spread effects. H demonstrates that the market report does not require an ETF.

I would preserve their economic questions, but avoid requiring all product types to be fully modeled in the first MVP.

## 4.4 Examples as executable specifications

Each revised example should have a predictable structure:

| Element | Required content |
|---|---|
| Economic question | Precisely what is being evaluated |
| Inputs | Explicit hypothetical market and ETF characteristics |
| Assumptions | Holding horizon, scenario conventions, limitations |
| Calculations | Established formulas and expected numerical results |
| Economic interpretation | Conclusions directly supported by those results |
| Optional policy judgment | Only when an investment policy has been supplied |
| Validation | Expected outputs, tolerances, and missing-data behavior |

This permits the MVP to reproduce the examples without embedding arbitrary decisions in the quantitative engine.

It also avoids confusing three different forms of validation: correct arithmetic, correct economic interpretation, and appropriate investment advice.

# 5. Complexity and premature commitments

Beyond the main economic issues, several design details should be simplified or deferred.

| Current commitment | Concern | Recommendation |
|---|---|---|
| 126/21 observations with five-point smoothing (§2, §4.1) | Inherited empirical research choices without demonstrated necessity for v3 | Use raw observations and simple changes first; keep smoothing optional |
| +50/+100/-50 bp stress suite | Useful illustration but not inherently privileged | Support configurable shocks; do not make these a core decision contract |
| 2Y/10Y/30Y curvature second difference | Uneven maturities make a simple second difference economically awkward | Defer curvature-factor analysis; preserve slope and KRD-based measures |
| Seven representative products and ten examples | Too broad for a first economic validation | Narrow MVP products while retaining edge cases as later tests |
| Detailed performance attribution (§4.5) | Can become a substantial standalone modeling problem | Begin with adjusted NAV and broad reconciliation |
| Expense ratio, trading costs, price–NAV execution checks | Outside the specified initial bond-centered scope | Defer detailed analysis; avoid double-counting expenses already reflected in returns |
| Fixed operational decision labels (§5) | Assumes the final user-facing policy design too early | Treat labels as provisional; prioritize quantitative explanations |

I would also revise the architecture diagram in §8. It currently places underlying market explanations downstream of ETF assessment, although the text correctly defines market-only analysis as independently available.

Market interpretation, ETF economic calculations, and realized performance diagnostics should be parallel analytical capabilities that feed an optional decision process.

## `AGENTS.md`

The file is largely consistent with the new project direction. It explicitly treats the two design documents as provisional, rejects inheritance from v2, and discourages unnecessary engineering abstractions.

No material financial-design contradiction was found.

One practical concern is that the session/task-branch and PR workflow is relatively elaborate for a fresh research project. This is an operational choice rather than a financial-model problem, so I would leave it outside the present review.

Two small documentation issues should eventually be corrected: the architecture points to `bond_etf_decision_examples_v1.md`, while the examples point to `bond_etf_decision_architecture_v1.md`. Those links do not match the filenames on `main`. The examples also refer to some provisional decisions as *accepted repairs*, which is stronger than their actual approval status.

# 6. Recommended revision strategy

I recommend a focused second feedback cycle in three stages.

## Stage 1 — Refine the economic architecture

Establish the core quantitative framework independently of a specific investment policy.

Define the relationship among ETF characteristics, market risk factors, current compensation, hypothetical shocks, and alternative investments.

Explicitly specify what can be concluded without forecasting future yields.

## Stage 2 — Rebuild a small set of core examples

Prioritize same-ETF comparisons across market conditions, cross-ETF comparisons, rate/curve sensitivity, and hedged/unhedged KRW economics.

Retain credit and futures as tests of analytical boundaries without insisting on complete coverage immediately.

Use the examples to challenge and refine the architecture once more.

## Stage 3 — Define the MVP validation boundary

Choose a small number of actual Korean-listed U.S. Treasury ETFs for which reliable exposure data can be obtained.

Reproduce the revised hypothetical examples first, then apply the same calculations to historical FRED data and dated ETF characteristics.

Expand the instrument coverage only after validating the core methods.

A possible minimal analytical structure is:

```text
Market observations                 ETF characteristics
          \                              /
           \                            /
            Established financial calculations
              |       |        |       |
     Rate/spread   Compensation  Curve  Currency
       sensitivity                effects effects
                          |
             +------------+------------+
             |                         |
    Economic assessment      Optional policy evaluation
    (continuous measures,    (objective-dependent
     comparisons)             judgments)
```

*Independent market-only reports and realized ETF behavior diagnostics remain available alongside the central calculations. This is a conceptual organization, not a proposal for mandatory software classes or layers.*

# 7. What should be resolved in the next feedback cycle?

I would concentrate the next discussion on four questions, in order of importance.

1. **What is the primary economic assessment?** Is it a set of comparable quantities describing ETF exposure, compensation, and conditional outcomes, rather than an intrinsic buy/sell verdict? I strongly favor this interpretation.

2. **How should compensation be measured?** Decide how far published ETF yield measures, KRW hedge economics, carry, and roll-down can support quantitative comparisons without creating an unnecessarily elaborate forecasting model.

3. **How should market observations map to actual ETF exposures?** Establish practical rules for effective duration, representative yields, key-rate durations, spread exposure, and missing information.

4. **When is an investment decision justified?** Define the boundary between unconditional financial facts, conditional comparisons, and genuinely investor-dependent purchase or holding judgments. Do not decide the final policy labels prematurely.

These decisions should be settled conceptually before finalizing the example outputs.

# 8. Final recommendation

I would not replace the present architecture wholesale. Its general direction is sound, and much of the financial material can be retained.

However, **I would substantially reorganize §§4–5 and Examples A–C before calling the documents an implementable design contract.**

The central change is straightforward:

> Bondview-v3 should first calculate what an actual ETF economically offers and what risks it carries under observable and hypothetical market conditions. It should then support comparisons and, where justified, investor-specific decisions. It should not require a predefined scoring rule, loss budget, or yield forecast to make its analysis useful.

This approach preserves the motivation for moving away from v2 while avoiding the risk of building another specialized decision mechanism before establishing the value of the underlying quantitative analysis.

**No repository files were modified, and no MVP implementation was started.**

---

## Source documents and further reading

- [Bondview-v3 architecture draft](https://github.com/lbk209/bondview-v3/blob/main/docs/bond_etf_decision_architecture.md)
- [Bondview-v3 examples draft](https://github.com/lbk209/bondview-v3/blob/main/docs/bond_etf_decision_examples.md)
- [Bondview-v3 agent instructions](https://github.com/lbk209/bondview-v3/blob/main/AGENTS.md)
- [CFA Institute — Overview of Fixed-Income Portfolio Management](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/overview-fixed-income-portfolio-management)
- [CFA Institute — Yield Curve Strategies](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-curve-strategies)
- [CFA Institute — Yield-Based Bond Convexity and Portfolio Properties](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-based-bond-convexity-and-portfolio-properties)
