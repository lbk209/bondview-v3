# Bondview-v3 — Analysis 1 and Analysis 2: Discussion and Reconsideration Notes

**Date:** 2026-10-22  
**Status:** Discussion history and critical review material — **not authoritative**, not an approved design contract, not implementation instructions.  
**Reference baseline:** `lbk209/bondview-v3`, **`analysis` branch**, particularly `docs/bond_etf_decision_architecture.md`, `docs/bond_etf_decision_examples.md`, and `docs/assets/constructed_market_daily.csv`. The discussions below also refer to a **locally rewritten examples draft**; it should not be confused with the version committed to GitHub.  
**Purpose:** Preserve the problems raised, objections, corrections to earlier suggestions, results obtained, and unresolved choices so they can be critically reviewed later. This deliberately retains revisions and competing interpretations instead of smoothing them into one settled architecture. No project document is changed by this note.

## The question that repeatedly changed our interpretation

The practical goal was not simply to display U.S. Treasury market conditions, but to help choose among **Korean-listed U.S. bond ETF exposures**. Our discussions tested whether the current separation between **Analysis 1 — Yield-Curve and Carry** and **Analysis 2 — Holding-Period Return** actually produces decision-useful information, or merely separates the inputs and outputs of one calculation into artificial analytical stages.

Three issues became entangled:

- **Market interpretation:** What can we learn from the current curve, its evolution, term premiums, and carry/roll without claiming to know future yields?
- **Joint yield-change scenarios:** Given an investor's partial view—e.g., that the 10Y yield is unlikely to increase substantially—how do we construct coherent movements of the *other* tenors, rather than guess all changes independently?
- **ETF consequences:** How do we apply those movements to dated, ETF-specific yield and duration characteristics, and compare the resulting modeled holding-period returns?

These are distinguishable questions, but they are **not necessarily three separate software stages or three independent analyses**. One later candidate distinction was: independent market interpretation in Analysis 1, scenario generation as a reusable/internal calculation (often within Analysis 2), and exposure/return comparison in Analysis 2. **This was proposed, not accepted as a revised contract.**

The `analysis`-branch architecture already says the analyses organize *economic questions*, not software modules, and that their preferred reading order is **not a mandatory execution dependency**. The debate tested whether the *examples* convincingly satisfied that principle.

---

## Issue: Why did the Analysis 2 example start with a yield-change preference-region chart?

**Initial proposal.** A locally rewritten examples draft showed a two-dimensional diagram: assumed future changes in 10Y and 30Y Treasury yields on its axes, separate panels holding the 2Y change at −50, 0, or +50 bp, and colored regions identifying which illustrative ETF exposure (S, I, L) had the highest modeled first-order six-month gross USD return. The region boundaries came from pairwise break-even return equations. This was meant to avoid arbitrarily choosing **one** joint yield-change forecast while visualizing how ETF preferences depend on yield movements.

**User's objection.** To *use* the chart for an actual ETF decision, must the investor first choose a 2Y panel and then decide where 10Y and 30Y will go? If so, is that not precisely the joint-yield-change assumption the chart was meant to avoid?

**Correction.** The objection was valid. The chart is a correct **Analysis 2 sensitivity calculation**, not merely raw Analysis 1 market data: its colors and boundaries are calculated from ETF return differences. It can answer conditional questions without choosing a unique point, such as *“For what combinations of yield movements does ETF I outperform ETF S?”* Nevertheless, **it does not determine which region is likely or economically plausible**. Selecting a point in the chart is equivalent to supplying a complete joint yield-change vector.

**Revised assessment.** The initial recommendation to make this chart the primary user-facing result of Analysis 2 was withdrawn. A more useful primary result should focus on modeled ETF returns and **paired ETF return differences under a stated, coherent scenario set**, while the region chart can remain optional for sensitivity and break-even examination. This is a change in the recommended **example presentation**, not a finding that conditional return comparison or break-even analysis is invalid.

**A second correction to the correction.** In reacting to the chart's limitations, the assistant briefly suggested that Analysis 1 must supply plausible ranges and that its validity should be reconsidered. The user challenged this as reopening a previously settled discussion. The assistant retreated too far in response and temporarily separated Analysis 1 from scenario formation altogether. The more defensible distinction reached later was: **Analysis 1's market evidence can inform the assumptions used for scenario analysis, but it cannot be required to produce a reliable forecast or uniquely determine a future curve.** The scenario generator should not be mistaken for the entirety of Analysis 1.

**Open point:** When do break-even regions materially aid a real ETF choice beyond a return-difference table? No demonstration yet showed that the preference-region visualization itself should be prominent.

---

## Issue: The investor's 10Y view and a conditional historical joint-scenario method

The user suggested a practical market premise: **“I do not expect the 10Y Treasury yield to rise much further.”** Our simple trial translated that into an illustrative **six-month 10Y change between −25 and +25 bp**.

**Initial assistant criticism:** The ±25 bp restriction was characterized as unsupported or arbitrary.  
**User's response and correction:** A relatively narrow ±25 bp interval is a **reasonable conditional assumption for a range-bound 10Y view**. The numerical threshold can be assessed against actual historical six-month change statistics; it need not be derived from a forecasting model. The assistant conceded that calling it simply “unsupported” was too dismissive.

**Qualification that remains important:** “Unlikely to rise much further” is **asymmetric**, whereas `|Δ10Y| ≤ 25 bp` is a stronger, **symmetric range-bound** assumption that excludes larger yield declines as well as larger increases. Both conditions are legitimate, but not interchangeable. The numerical ±25 bp threshold was *not in fact statistically calibrated* in the demonstration. Checking history could inform the threshold but does not by itself convert a subjective market view into a forecast probability.

### Precisely what the simple historical calculation did

In the constructed `analysis`-branch market fixture, observations spanned **2025-04-21 through 2026-10-20**. The calculation used **392 dated yield records** at 2Y, 5Y, 10Y, and 30Y, although the example condition and ETF comparison focused on 2Y, 10Y, 30Y.

For every eligible start date `u`, the example selected the available observation closest to **183 calendar days later**, allowing a **±3-day tolerance**, and computed **one complete** historical yield-change vector:

\[
\Delta\mathbf y_j = (\Delta y_{2Y,j},\;\Delta y_{10Y,j},\;\Delta y_{30Y,j}), \qquad
\Delta y_{k,j}=y_k(v_j)-y_k(u_j).
\]

The method moved the starting date forward across the dataset, generating **264 overlapping six-month intervals**, and retained complete vectors satisfying

\[
-25\text{ bp}\leq\Delta y_{10Y,j}\leq+25\text{ bp}.
\]

**226** vectors passed; **38** were excluded. Crucially, the 2Y and 30Y yield changes came from **the same start/end dates** as the qualifying 10Y change. The method did **not** fabricate joint scenarios by taking independently selected quantiles from different tenors.

The published conversation example reported the following **marginal** conditional historical percentiles:

| Six-month change | 10th percentile | Median | 90th percentile |
|---|---:|---:|---:|
| 2Y yield | −43.0 bp | +11.1 bp | +38.2 bp |
| 10Y yield | −13.4 bp | +6.0 bp | +18.8 bp |
| 30Y yield | −4.7 bp | +5.1 bp | +13.0 bp |

**Important correction to interpretation:** Each *column* of this table comes from **separate sorting of the same-tenor changes**; the 10th-percentile values for 2Y, 10Y, and 30Y are **not necessarily one historically observed joint vector**. The table describes individual marginal ranges *conditional on the selection event*. It is not a three-point joint scenario specification. Likewise, separately displayed percentiles of different ETFs' returns need not have occurred together.

**What Analysis 2 actually received:** The **226 original paired vectors**, not a single tuple of their separately computed percentile values. Thus **jointness was preserved through the ETF return calculations**, even though the marginal summary table did not display the joint structure.

**Caveat arising from the calculation itself:** The six-month compensation term in the example used a fixed 183/365 years, even for rare historical intervals 180–182 days long. A reproducible implementation should choose and consistently apply an elapsed-horizon convention (or explicitly label a common-horizon approximation).

### Is this an accepted method, and would more history help?

The general practice of applying **historically observed, aligned multi-tenor yield movements** to a current portfolio is established fixed-income scenario and stress analysis. FHFA, for example, describes historical **six-month yield-curve shock** construction for regulatory market-risk scenarios, while warning that naïvely transplanted shocks may be implausible in a different rate environment. See the literature references at the end.

However, **selecting only intervals with `|Δ10Y| ≤ 25 bp` is our particular conditional selection rule**, not a universal professional standard. A longer, real historical dataset would provide more episodes and rate regimes, but would not by itself establish forecasting power. The example's 226 rolling intervals are **highly overlapping**, not 226 independent six-month experiences; inference, calibration, and any uncertainty claims must account for that dependence. Different monetary-policy regimes also make simple pooling debatable.

One more distinction was emphasized: selecting past intervals *because their realized subsequent 10Y change met a condition* describes outcomes **conditional on the event**. It does not estimate the current probability that the event will happen, nor the unconditional future return distribution.

**Tentative result:** Conditional historical simulation is credible as a simple **scenario-selection / sensitivity method worth testing** with longer actual yield data. Its exact conditioning, horizon, lookback, overlap treatment, and regime robustness remain open.

---

## Issue: What did Analysis 2 add, and was it merely mechanical?

**User's challenge:** Once Analysis 1 has produced the joint yield-change set, does Analysis 2 simply apply a known formula? The assistant ultimately agreed: **yes, in the constructed example it did**, conditional on the inputs and model being fixed. This is not a criticism of financial modeling; a well-specified pricing or return model *should* reproducibly transform given inputs into outcomes.

The illustrative dated ETF-style cash-bond exposures were:

| Example exposure | Treasury factor proxy | Gross portfolio YTM | Duration | Approx. six-month baseline `YTM × 183/365` |
|---|---|---:|---:|---:|
| S | 2Y | 4.10% | 1.85 | +2.06% |
| I | 10Y | 5.00% | 7.50 | +2.51% |
| L | 30Y | 5.26% | 15.20 | +2.64% |

For changes in basis points, the first-order **gross USD** approximations were:

\[
\begin{aligned}
\widehat R_S(\%) &\approx 2.0556-0.0185\,\Delta y_{2Y}^{bp},\\
\widehat R_I(\%) &\approx 2.5068-0.0750\,\Delta y_{10Y}^{bp},\\
\widehat R_L(\%) &\approx 2.6372-0.1520\,\Delta y_{30Y}^{bp}.
\end{aligned}
\]

These are recognized *first-order yield-based compensation plus duration price-effect approximations* for **suitable USD cash-bond exposures**, not complete realized Korean ETF returns. No exact cash-bond repricing, portfolio rebalancing, convexity, hedge cost, FX result, or futures ETF carry mechanics was demonstrated. ETF factor-to-tenor mappings must be compatible with available duration/key-rate data rather than inferred from a maturity label alone.

For each of the **same 226 complete joint vectors**, the calculation produced a triple of **paired modeled ETF returns**. Subsequently sorting each ETF's returns separately gave:

| Modeled six-month return | 10th percentile | Median | 90th percentile |
|---|---:|---:|---:|
| S | +1.35% | +1.85% | +2.85% |
| I | +1.10% | +2.06% | +3.51% |
| L | +0.66% | +1.85% | +3.36% |

The assistant initially highlighted I's highest **individual median**. But another valid within-scenario comparison counted which ETF had the highest modeled return **for each complete vector**: **S 69; I 67; L 90** among 226 scenarios. There is no contradiction: the median of a given ETF's marginal return distribution is not equivalent to being best most often in the *joint* sample. The counts do **not** indicate reliable future winning probabilities given constructed, short, overlapping history.

**Further proposed improvement:** Show **paired return differences**, e.g., `R_I − R_S`, `R_L − R_S`, `R_L − R_I`, under each same market movement. Summarize their signs, dispersion, break-even situations, and sensitivity to history or condition choices. Relative rankings are useful, but scenario frequencies should not masquerade as probabilities. Analysis 3 can use the *same underlying revaluation* to examine adverse effects; it does not require duplicating a second pricing engine.

**More ambitious question that remains open:** Are the modeled return differences sufficiently robust and discriminating to be helpful for an actual selection, or do plausible assumptions often change the preferred ETF? If so, uncertainty is itself a valid finding—not something to hide with an ungrounded score.

### “30Y moved less than 2Y” was a weak independent Analysis 1 finding

The historical-condition example concluded that 30Y yield changes were more concentrated than 2Y changes. The user objected that this is not yet investment-relevant without the ETFs' **exposure sensitivities**.

The assistant agreed. In the same conditional sample, approximate 10th–90th percentile **yield-change widths** were about **81 bp at 2Y** and **18 bp at 30Y**. But multiplying by the example durations implies approximately **1.50 percentage points** of S rate-price-effect width versus **2.74 percentage points** for L. Despite less variation in its yield factor, the 30Y-like ETF can have **more modeled price variation** because of its duration.

**Correction:** Presenting narrower *long-yield* changes as though that made the long-duration ETF safer was not justified. The finding can be valid market statistics, but it became clearly decision-useful only after exposure sensitivities were applied—in this particular example, as part of Analysis 2/3.

---

## Issue: Is there enough *independent* value to keep Analysis 1 separate?

This was the most consequential conceptual dispute, and **it has not been fully resolved**.

The user asked whether, if the previous “Analysis 1” is only a preliminary calculation for the later ETF result, the entire exercise should be moved into **Analysis 2's internal process** rather than presented as a standalone analysis. The assistant's evolving response was:

1. Initially, continue treating the conditional historical yield analysis as a user-facing Analysis 1 result and the ETF return transformation as Analysis 2.
2. After objections, acknowledge that the observed narrowness of 30Y changes is a weak *standalone ETF decision finding* and that the historical filtering fits naturally within scenario preparation for Analysis 2.
3. **Do not automatically infer that all of Analysis 1 is useless.** The full architecture's Analysis 1 is broader than conditional historical filtering: current yield curve, forward rates, curve evolution, publishable term-premium decomposition, and supportable carry/roll comparisons may provide independent financial interpretation.
4. Suggest distinguishing **market analysis**, **joint scenario construction**, and **ETF return application**. This functional distinction was not a decision to create three rigid modules or require Analysis 1 to forecast yields.

This was a reason to scrutinize *example outputs*, not to repeatedly “revalidate” Analysis 1 whenever a presentation issue arose. The assistant's tendency to shift conclusions in response to successive objections—sometimes withdrawing too much and then reversing—was explicitly challenged during the discussion.

### Can Analysis 1 compare ETFs, not just dates or Treasury tenors?

Potentially, but with an important boundary:

- **Across dates:** changes in curve level/slope, term-premium vs expected-short-rate components, and perhaps shifts in compensation for longer-duration risk. These can be meaningful market information *before* choosing an ETF.
- **Across tenors:** current maturity-relative yields and model-based compensation, as well as conditionally observed curve behavior. These are not the same thing as ETF risk-adjusted attractiveness.
- **Across selected ETFs:** properly defined issuer portfolio yields and supportable carry/roll estimates might allow ETF-relative comparisons. However, these inputs overlap heavily with Analysis 2's return baseline and may not justify two separate user-facing results unless Analysis 1 answers a genuinely different question. Avoid pretending that a Treasury 10Y term premium is a directly measured ETF-specific premium.

**Unresolved threshold for keeping a standalone Analysis 1:** Can a concrete example provide *meaningful, differentiated market/compensation insight* rather than (i) a routine input table or (ii) an incomplete return calculation that Analysis 2 immediately finishes? This is to be tested **with examples**, not resolved by simply asserting that an analysis must be independent or by demanding future-yield predictions.

### The possibility of independent term-premium insight

The previously proposed **published ACM** example used a *real*, separate historical episode: **2023-07-26 to 2023-10-19**. A Federal Reserve Board note reports for **ACM** an approximately **+116 bp** increase in the 10Y model term premium and **+1 bp** in its expected short-rate component during a roughly **+117 bp** rise in the corresponding 10Y yield measure. This illustrates an actual Analysis 1-type result: understanding *the modeled source of a yield increase* without valuing an ETF under a particular future shock.

**Important limits:** This is **not** a result for the constructed 2026 Bondview dataset, and it is not a proof that a premium will mean-revert or that long-bond ETFs will outperform. The same official research notes material **differences among models and survey-based decompositions** (e.g., the reported CR and KW splits differ from ACM). Model-implied premium and expected short rates are not directly observable; compatible fitted-yield and decomposition series should be compared, not mechanically combined with a FRED constant-maturity par yield.

A conditional scenario method and a market-decomposition method need not compete for the same output. ACM's strongest standalone contribution may be **economic interpretation**, while historical simulation/PCA primarily inform **coherent yield-curve shocks**. Whether the former is sufficient to warrant an Analysis 1 user-facing slot remains a presentation/usefulness question, not a settled implementation requirement.

---

## Issue: Could we improve on conditional historical simulation with PCA or published ACM?

The user asked whether the simple approach was the simplest possible method and compared **principal component analysis (PCA)** with **using the published Adrian–Crump–Moench (ACM) estimates**.

| Question | PCA of historical yield changes | Published ACM estimates |
|---|---|---|
| Main financial question | What factors explain historical **co-movement** of rates across maturities? | What portion of nominal yields reflects **expected short rates** versus **term premiums**, according to a fitted model? |
| Implementation burden | **Low/moderate** for covariance/eigenvector estimation with NumPy; more effort in sensible sample, horizon, interpretation and conditioning | **Low** for downloading and plotting supplied data; reproducing/estimating a full ACM dynamic model is a different, much harder task |
| Independent Analysis 1 contribution | Historical level/slope/curvature-like factors and changing co-movement structure; usefulness must be demonstrated | Economically interpretable premium/expectations levels and changes across dates and available maturities; uncertainty and model disagreement matter |
| Joint yield-change scenarios for Analysis 2 | **Possible**, but PCA *by itself* supplies factors/covariance, **not a unique conditional scenario distribution**. A scenario construction/conditioning step is needed. | **Not directly** from the published premium/expectations time series. Historical ACM component changes may inform a scenario framework, or a separately implemented dynamic model may construct distributions. Downloading estimates alone does neither. |
| Coverage/caveat | Depends on selected historical curve input and horizons; regime instability, factor instability and dependence can matter | NY Fed public ACM data cover Treasury maturities **1Y–10Y**, not a directly supplied 30Y premium series; model-estimated fitted/zero-coupon yields differ from benchmark par yields |

**PCA practical candidate:** Start with a sufficiently long aligned Treasury curve (e.g., 2Y, 5Y, 10Y, 30Y); compute horizon-matched yield changes; estimate covariance and PCA; examine the factor loadings and stability by subsample; and test how to generate full joint tenor vectors conditioned on the investor's 10Y view. Do not assume the first three PCs necessarily provide a future forecast, or that a fitted factor model has to outperform simply retaining observed historical vectors.

**Published ACM practical candidate:** Display dated 10Y fitted yield / expected average short-rate / term-premium decomposition and historical changes, with source and model uncertainty. It is useful to identify why yields may have changed according to a published model. It is **not** a turnkey source of *predicted* 2Y/10Y/30Y six-month changes. Avoid creating an unrelated 30Y ACM value or claiming the decomposition itself proves likely long-duration returns.

**Earlier assistant recommendation, preserved as provisional:** Do **not** force an either/or choice, since their purposes differ. Compare **simple conditional historical simulation vs PCA** for scenario construction; independently test **published ACM** for market interpretation. Add sophistication only where it improves robust, understandable ETF decisions. A regression/yield-beta approach and more ambitious dynamic term-structure models were also discussed as alternatives, without authorization or evidence of superiority.

**Professional-literature nuance:** Saroka and Rebonato's yield-curve deformation work is directly relevant to inferring a coherent full-curve move consistent with a partial subjective view. It is not evidence that every Bondview PCA implementation is automatically well-calibrated or that it can forecast future curve evolution.

---

## Issue: Is “scenario construction → holding-period return” legitimate fixed-income practice?

The user asked whether the overall Analysis 2 workflow is widely recognized by professional fixed-income practitioners:

> Define a holding horizon and market conditions → construct aligned, coherent joint rate changes (historical scenarios, PCA-informed scenarios, or other methods) → value the exposures or approximate their returns → compare alternatives.

**Result of the literature check:** **Yes, the general workflow is established.** CFA Institute's *Yield Curve Strategies* discusses level/slope/curvature positioning, duration/convexity-based price impacts, carry/roll considerations, investor rate views, and scenario analysis. FHFA uses historical rate-movement shock scenarios to assess portfolio market risk.

But that endorsement **does not validate every particular Bondview scenario-selection rule or ETF proxy calculation**. Material distinctions remain:

- A model can calculate **conditional gross USD cash-bond exposure returns** without claiming expected returns or probabilities.
- Yield × horizon plus duration × yield change is a **first-order approximation**; accurate application depends on current ETF exposure, factor mapping, horizon, YTM convention, refinancing/rebalancing assumptions, and omitted components. Futures ETF returns cannot simply inherit a cash-bond formula.
- Historical samples and PCA factors describe *observed structure*, not by themselves a distribution of future yields.
- Reuse the **same complete joint curve movement** across compared ETF exposures. Do not mix independently drawn marginal tenors and mislabel the combination a historical observation.
- The output of Analysis 2 is deterministic **conditional on** scenario vectors, ETF input profiles, and model choices. That is not evidence that Analysis 2 is dispensable: the financially relevant output is the **exposure-level return comparison**, not the mechanical complexity of computing it.
- If risk/stress analysis reuses the same underlying repricing in Analysis 3, avoid claiming the duplicated arithmetic is independent economic evidence.

The clearest professional precedent is **the workflow**, not necessarily a formally titled stand-alone “Analysis 1” plus “Analysis 2” pair.

---

## Corrections and competing design directions to preserve for the next review

These are **review checkpoints and unsettled options**, not final decisions:

**A. Initial chart-centered result → exposure-centered result.** The preference-region chart was mathematically a valid Analysis 2 sensitivity map, but insufficient as the main ETF selection output because the likelihood/plausibility of its regions was not established. Prioritize scenario-conditioned ETF return differences where useful; keep break-even regions only when they add interpretive value.

**B. “Analysis 1 supplies all assumptions” → “Analysis 1 may inform assumptions.”** Earlier responses alternated between making Analysis 1 responsible for forecasting plausible movements and entirely separating it from the scenarios. The defensible middle ground is that its market evidence can influence which conditions are examined, but **no unique curve prediction or mandatory dependency** follows.

**C. “±25 bp is arbitrary” → “reasonable illustration; calibrate and match the investor view.”** A symmetric ±25 bp range is a defensible illustration of a range-bound belief; it is not equivalent to an asymmetric belief that yields cannot rise much more. Historical calibration and robustness checks remain undone.

**D. Marginal percentile table vs joint scenarios.** The percentile rows of 2Y, 10Y and 30Y in the example are **not simultaneous scenarios**. The underlying **226 complete aligned vectors** were passed to Analysis 2. ETF return medians are also marginal; paired differences and within-scenario comparisons give different, often more selection-relevant information.

**E. “30Y yield changes were narrower” → “insufficient without duration.”** The earlier Analysis 1 finding had little standalone ETF selection power and could mislead without exposure sensitivity. The scenario-selection step may belong within Analysis 2 or a shared calculation, not necessarily as a standalone user-facing analysis.

**F. “Analysis 1 has no independent value” was not established.** Conditional historical filtering did not demonstrate its full value. Published term-premium decomposition and carefully defined carry/roll may add economically meaningful market/relative-compensation information; this needs a convincing result-first example, and should not merely restate Analysis 2's compensation baseline.

**G. PCA vs ACM is not a one-winner model contest.** PCA is an implementable co-movement representation; with an added conditioning rule it can underpin joint scenarios. Public ACM is an accessible **market decomposition**, not a ready joint-shock generator. Neither should be introduced solely to make an analysis appear sophisticated.

**H. Common professional workflow ≠ verified Bondview implementation.** Scenario analysis plus return/revaluation is accepted fixed-income practice, but actual ETF exposure support, historical regime effects, overlap, horizon consistency and outputs without probabilistic overclaiming still need verification.

**I. Scope and nomenclature remain provisional.** One option is to retain a separately presented **Analysis 1 (Treasury market conditions and compensation)** and **Analysis 2 (conditional ETF returns)**, while treating scenario construction as Analysis 2's internal/shared preparation. Another is to reduce independent Analysis 1 presentation if term-premium/carry outputs prove unhelpful. No label change or merger was agreed. The current architecture explicitly allows shared inputs and methods, and should not be rewritten based solely on this note.

## Work that would actually resolve the disagreements

The next useful evidence would not be another conceptual defense of the existing headings. More discriminating trials would be:

1. **Real, longer Treasury history:** Compare the conditional empirical method with a PCA-based method under the *same* six-month horizon, same investor 10Y view, and same complete current ETF profiles; assess sample/regime sensitivity and differences in **paired ETF outcome comparisons**, not only covariance fit.
2. **Stand-alone Analysis 1 example:** Produce a dated, sourced ACM expected-rate/term-premium decomposition across time, and/or ETF-compatible carry/roll comparison. Ask what investment insight remains **before** Analysis 2 applies scenario returns. Label estimates/model ambiguity and distinguish it from ETF yield.
3. **Presentation A/B test:** Compare a user-facing output based primarily on market decomposition plus paired ETF conditional returns against the old preference-region chart and separated marginal-percentile tables. Judge actual ETF decision usefulness rather than aesthetic complexity.
4. **Model-consistency audit:** Check scenario horizon, yield definitions, ETF issuer snapshots, cash-bond versus futures applicability, duration/KRD alignment, return-baseline conventions and the boundary between Analysis 2 return comparison and Analysis 3 downside risk.

These are possible next review tasks, **not** instructions to implement, change GitHub, or expand the approved scope.

---

## Sources and artifacts mentioned during the discussion

**Project reference (use `analysis`, not `main`, as the baseline):**

- Architecture: https://github.com/lbk209/bondview-v3/blob/analysis/docs/bond_etf_decision_architecture.md
- GitHub examples version: https://github.com/lbk209/bondview-v3/blob/analysis/docs/bond_etf_decision_examples.md
- Constructed market fixture: https://github.com/lbk209/bondview-v3/blob/analysis/docs/assets/constructed_market_daily.csv
- Locally rewritten examples draft (a separate conversational artifact): `bond_etf_decision_examples.md`, with associated `bond_etf_preference_regions.png`; **do not assume this draft was committed to the branch**.

**External research / professional materials (support broad methods, not our specific scenario calibration):**

- CFA Institute, *Yield Curve Strategies* (2026): https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-curve-strategies — conventional yield views, carry/roll, duration/convexity, scenario analysis and portfolio return drivers.
- FHFA, *Market Risk Scenarios*: https://www.fhfa.gov/data/fhlb-stress-tests/market-risk-scenarios — historical six-month curve changes and rate-environment plausibility limitations.
- FHFA, *Federal Home Loan Bank Stress Tests*: https://www.fhfa.gov/data/fhlb-stress-tests — historical six-month stress-shock design dating back to 1998, sampled at monthly starts.
- NY Fed, *Treasury Term Premia*: https://www.newyorkfed.org/research/data_indicators/term-premia-tabs — published ACM term premiums, fitted yields and expected short-rate components, 1Y–10Y.
- Federal Reserve Board, Diercks and Asnani, *The Treasury Tantrum of 2023* (September 3, 2024): https://www.federalreserve.gov/econres/notes/feds-notes/the-treasury-tantrum-of-2023-20240903.html — especially Tables 1–3; cross-model differences, and the +116/+1 bp ACM decomposition example.
- Saroka and Rebonato, *How to Deform a Yield Curve: The Most Likely Deformation of a Yield Curve Consistent with Subjective Views* (2014): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2443285 — conditional full-curve deformation consistent with partial investor views.

**Final caution:** This document intentionally records arguments made, mistakes acknowledged, illustrative computations, and changes of mind. It is **not evidence that any contested assumption, analysis boundary, implementation method, or ETF investment recommendation has been accepted**.
