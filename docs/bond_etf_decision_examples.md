# Bondview-v3 — Fixed-Income Analysis Examples

**Status:** PROVISIONAL companion for design review — updated 2026-10-24 from the GitHub `analysis` branch. Analysis 1 and Analysis 2 presentation examples have been revised against [`bond_etf_decision_architecture.md`](bond_etf_decision_architecture.md); remaining analysis examples are pending review. This document does **not** authorize implementation or recommend an investment.

## 1. Purpose and conventions

This companion illustrates what investors could learn from **Analysis 1 (§3.1, Treasury Market Conditions and Scenarios)** and **Analysis 2 (§3.2, Holding-Period Return)** in one investment case. Analysis 1 leads with **presentation sketches**: two candidate primary market results, an optional conditional-scenario result, and an optional PCA supporting note. Detailed method selection and presentation design are deferred. The architecture remains the governing contract, and Analysis 2 does not require a prior Analysis 1 run.

**Constructed-data convention.** All dates, Treasury observations, exposure IDs, issuer-style profiles and numbers below are **illustrative**, not actual historical FRED data, real ETF disclosures, forecasts, or realized returns. Reproducible curve and Analysis 2 arithmetic use existing repository fixtures: [`constructed_market_daily.csv`](https://github.com/lbk209/bondview-v3/blob/analysis/docs/assets/constructed_market_daily.csv) and [`constructed_issuer_snapshots.csv`](https://github.com/lbk209/bondview-v3/blob/analysis/docs/assets/constructed_issuer_snapshots.csv). **Analysis 1 presentation-only mock-ups** for term-premium decomposition, conditional scenarios and PCA are explicitly labeled; their values are not derived from these fixtures, sourced estimates or an underlying synthetic dataset.

**Reading conventions.** Each example leads with what an investor would see, followed by interpretation and inputs/assumptions for reproduction. Yield changes and curve spreads are in **basis points (bp)**; modeled returns are percentages and differences between returns are in **percentage points (pp)**. A rate-change assumption is neither a forecast nor a probability estimate. ETF profiles are distinguished from reference Treasury tenors; no modeled USD gross bond-exposure return is presented as the net KRW outcome of a Korean-listed ETF. All modeled cash-bond exposures are assumed eligible under the architecture's data and factor-compatibility rules.

## 2. One investment case: evaluating Treasury duration

**Investor's question.** “Long-term U.S. Treasury yields have risen. If they rise only modestly from here—or decline—what evidence should I examine, and what conditions would favor short-, intermediate-, or long-duration Treasury exposure?” The market view is the **investor's hypothesis**; no analysis below establishes it as likely.

**Assessment date:** 2026-10-20. **Reference market period:** 2026-04-20 → 2026-10-20. **Conditional investment horizon for Analysis 2:** 183 calendar days (`H = 183/365 = 0.501369863` under ACT/365 Fixed), chosen for illustration, **not** inferred as the likely future path from the prior six months.

### 2.1 Analysis 1 — Treasury Market Conditions and Scenarios (§3.1)

**Purpose.** Help investors interpret maturity-specific Treasury market conditions, distinguish expected-rate and term-premium explanations when supported, and supply coherent yield-curve scenarios to Analysis 2 when useful. The examples below are **display concepts**, not a requirement to publish a separate result for every model.

#### A. Candidate primary user-facing results

##### A1. Treasury curve regime — where has rate pressure concentrated?

> **2Y–10Y steepening, 10Y–30Y flattening.** From April to October, the 2Y yield **fell 53 bp**, while the 10Y **rose 56 bp** and the 30Y **rose 30 bp**. This is a mixed curve twist, not a uniform bull or bear shift.

| Tenor | Yield at start | Yield at end | Change | Immediate interpretation |
|---|---:|---:|---:|---|
| **2Y** | 4.65% | 4.12% | **−53 bp** | Falling short-end yields supported short-tenor *rate-price* returns |
| **10Y** | 4.50% | 5.06% | **+56 bp** | Greatest upward yield movement among these tenors |
| **30Y** | 5.02% | 5.32% | **+30 bp** | Smaller yield rise than 10Y, but greater duration may still magnify the price effect |

**Tenor-selection insight:** The recent rate move was more favorable to the short end than to the 10Y on a rate-price basis. This **describes the past**, rather than favoring a specific ETF for the next holding period. The current compensation and the investor's forward-looking rate view remain relevant.

##### A2. Long-yield decomposition — expected rates or term compensation?

> **Illustrative model interpretation:** Most of an example increase in the 10Y **model-fitted yield** comes from the term-premium component, rather than revised expectations of future short rates.

| Model-implied change over an illustrative interval | Contribution |
|---|---:|
| 10Y fitted zero-coupon yield | **+60 bp** |
| Expected average future short-rate component | +15 bp |
| Term-premium component | **+45 bp** |

**Tenor-selection insight:** Increased term compensation may help explain why long-maturity yields remained under upward pressure even without comparably large changes in expected policy rates. Long-duration ETF exposure could remain sensitive to premium changes independently of the near-term Fed policy path. The model does **not** identify a cause such as fiscal issuance or inflation uncertainty without separate evidence, nor does a larger premium imply an imminent decline.

*Presentation-only mock-up. These +60/+15/+45 bp figures are invented to illustrate the display, **not** an ACM, CR or KW estimate, not measured from the constructed market CSV, and not an attribution of the April–October curve changes above. A real result would use one internally consistent published model.*

#### B. Optional supporting user-facing result — conditional joint movements

##### B1. What follows for 2Y and 30Y if the investor expects a moderate 10Y increase?

**Investor's condition (input, not result):** 10Y yield increases **25–50 bp** over the next six months.

| Example joint curve outcome | Δ2Y | Δ10Y (conditioned) | Δ30Y | Curve interpretation |
|---|---:|---:|---:|---|
| Short end rises fastest | +65 bp | +35 bp | +15 bp | Bear flattening |
| Broad rise | +30 bp | +40 bp | +45 bp | Approximately parallel |
| Long end rises fastest | +5 bp | +40 bp | +75 bp | Bear steepening |

**Finding the model should actually deliver:** How **other tenors move jointly** when the stated 10Y condition holds—including their variation and whether relative curve configurations differ. These examples illustrate why a view about one yield does not determine relative ETF outcomes.

**Use:** Supply the *complete, coherent vectors* to Analysis 2 for matched ETF return comparisons. A standalone scenario table is optional if it adds no investment insight beyond Analysis 2.

*Presentation-only hypothetical vectors, **not** observed historical intervals, estimated conditional quantiles or assigned probabilities. Actual historical conditioning must retain same-interval 2Y/10Y/30Y moves; a model-based method must preserve justified cross-factor relationships.*

##### B2. PCA factor structure — optional explanatory note, not a required result

| Historical factor interpretation | Illustrative explained variance |
|---|---:|
| Broad common movement (level-like) | 75% |
| Relative short/long movement (slope-like) | 20% |
| Intermediate-versus-end movement (curvature-like) | 5% |

**Tenor-selection insight:** A large common factor suggests substantial shared interest-rate exposure across tenors, while slope and curvature differences can still matter for ETF comparisons. The factor analysis is **supporting evidence**, not a preferred-tenor result; if used for Analysis 2 scenarios, PCA requires an additional conditioning/construction method.

*Illustrative PCA percentages, not calculated loadings. Explained variance is **not** the fraction of dates on which all tenors moved in the same direction. Factor labels would require checking actual loadings.*

#### C. Supporting observations and deferred design notes

The A1 curve observations above are drawn from the constructed `DGS2_pct`, `DGS10_pct` and `DGS30_pct` rows for **2026-04-20 → 2026-10-20** in [`constructed_market_daily.csv`](https://github.com/lbk209/bondview-v3/blob/analysis/docs/assets/constructed_market_daily.csv). The intermediate 2026-07-20 observations remain available in that fixture. Spreads should be recalculated from aligned yields, not treated as independent inputs.

| Constructed spread | At start | At end | Change |
|---|---:|---:|---:|
| 10Y − 2Y | −15 bp | +94 bp | **+109 bp** |
| 30Y − 10Y | +52 bp | +26 bp | **−26 bp** |

The April–October changes form one **observed-in-the-constructed-dataset** joint vector `(−53, +56, +30) bp`; they are **not** a projection for the next six months. The decomposed yield in A2 must use matching fitted-model components, not be forced to equal `DGS10`. The scenario vectors in B1 are unrelated hypothetical presentation examples, not selected observations from the fixture. Any carry/roll refinement of a holding-return baseline belongs within **Analysis 2** when justified; it is not a separate Analysis 1 result.

The usefulness of published decomposition estimates, choice of historical conditioning versus regression/PCA, sample/regime sensitivity and whether optional outputs deserve screen space remain for later discussion. No model is mandatory merely because its format appears here.

### 2.2 Analysis 2 — Holding-Period Return (§3.2)

**Purpose.** Compare six-month gross USD return opportunities for short (S), intermediate (I), and long (L) Treasury ETF-like cash-bond exposures under *matched, economically defined joint yield movements*. Separately, examine how each tenor's compensation–duration trade-off changed across assessment dates. These are illustrative modeled exposure results, not realized Korean-listed ETF returns.

#### A. User-facing result — matched-scenario returns

![Modeled six-month return distributions under the same joint Treasury yield scenarios, with seven highlighted scenarios shown in a Plotly-style legend](assets/analysis2_matched_scenario_returns.png)

[**Interactive Plotly chart — toggle scenarios H1–H7 in the legend**](assets/analysis2_matched_scenario_returns.html)

**What the investor learns.** In this constructed example, S produces the highest modeled return for **all 28 selected joint-yield windows**, using either the April or October exposure profile. S's October median is approximately **+2.99%**; I's is **−0.39%**, and L's is **−0.96%**. The advantage is conditional on this selected episode, in which 10Y yields increased **25–50 bp** while 2Y yields generally declined and 30Y yields increased. It is not evidence that the episode will recur or that S is unconditionally preferable.

The paired April/October panels show how **different dated exposure characteristics** change returns under **the same market movements**: S's modeled returns decline modestly between the profiles, I's center remains similar, and L's become less negative. The comparison isolates exposure-profile effects under a common *retrospectively applied* scenario set; it is **not an April-as-of opportunity backtest**, because all 28 selected windows end after April. It also does not depict actual returns earned between April and October.

**Reading the plot:** Each grey box summarizes the **28** selected return outcomes for one exposure at one assessment date (median, quartiles and range). The seven colored scenario lines are individual, same-window yield vectors highlighted from that set; the **same legend color and scenario ID** apply across S, I, L and both dates. The image is a static preview; the linked Plotly version lets the investor show/hide a scenario by clicking its legend entry. The 28 windows substantially overlap, so their count is descriptive rather than a frequency-based forecast.

#### B. Supporting result — compensation and yield-rise resilience across dates

![April-normalized trajectories of six-month compensation and zero-return break-even yield rise for the S, I and L exposures](assets/analysis2_compensation_break_even_indexed.png)

[Interactive version — inspect each date's absolute compensation, break-even rise, YTM and duration](assets/analysis2_compensation_break_even_indexed.html)

**What the investor learns.** All three trajectories begin at `(100, 100)` in April. Moving right means *more six-month yield-based compensation* relative to that tenor's April level; moving up means a *larger rise in its own matched Treasury yield* can be absorbed before its modeled return reaches zero. From April to October, S deteriorates on both measures; I gains compensation with almost unchanged break-even resilience; L improves on both measures. The result identifies **within-tenor changes** rather than treating the structurally much larger absolute 2Y cushion as evidence of an unconditional tenor advantage.

Absolute levels remain available to prevent normalization from hiding economically material exposures:

| Exposure | April compensation | October compensation | April break-even rise | October break-even rise |
|---|---:|---:|---:|---:|
| **S — 2Y** | +2.28% | +2.06% | +126.7 bp | +111.1 bp |
| **I — 10Y** | +2.31% | +2.51% | +32.9 bp | +33.4 bp |
| **L — 30Y** | +2.51% | +2.64% | +15.9 bp | +17.4 bp |

Break-even yield rise is an **individual zero-return threshold**, not the equal-return boundary between two ETFs. It measures each exposure's compensation cushion against a rise in its *own* reference yield. Because different tenor yields need not move by similar amounts, absolute break-even levels are **not comparable probabilities of loss**. The measure adds a useful explanation of the compensation–duration trade-off, not independent evidence beyond its inputs.

#### C. Model, inputs and reproduction

**Common convention.** Both plots use the cash-Treasury gross USD first-order holding-period return approximation in [the architecture, §3.2](https://github.com/lbk209/bondview-v3/blob/analysis/docs/bond_etf_decision_architecture.md#32-holding-period-return-analysis--initial-primary), with `H = 183/365` years. Compensation is estimated from **gross portfolio YTM × H**; the rate-price effect uses the compatible reported duration and the corresponding tenor yield change. Available constructed profiles do not support a separate convexity, roll-down, hedging, spread or fee term; none is invented. The source is an illustrative exposure profile, not actual ETF holdings or Korean-won returns.

**Exposure inputs.** Take the issuer-style dated profiles for S (`DGS2`), I (`DGS10`) and L (`DGS30`) from [`constructed_issuer_snapshots.csv`](https://github.com/lbk209/bondview-v3/blob/analysis/docs/assets/constructed_issuer_snapshots.csv):

| Assessment date | S: YTM / duration | I: YTM / duration | L: YTM / duration |
|---|---:|---:|---:|
| 2026-04-20 | 4.55% / 1.80 | 4.60% / 7.00 | 5.00% / 15.80 |
| 2026-07-20 | 4.35% / 1.90 | 4.85% / 7.30 | 5.18% / 15.50 |
| 2026-10-20 | 4.10% / 1.85 | 5.00% / 7.50 | 5.26% / 15.20 |

**Plot A — scenario construction and returns.** From [`constructed_market_daily.csv`](https://github.com/lbk209/bondview-v3/blob/analysis/docs/assets/constructed_market_daily.csv), form matched `DGS2`, `DGS10` and `DGS30` changes between each eligible endpoint and the nearest available observation approximately six calendar months earlier (accept **183 ± 7 days**). Keep complete joint windows with **+25 to +50 bp change in 10Y**, ending no later than 2026-10-20; **28 windows** qualify. Preserve each window's actual start/end dates and all three observed-together yield changes. Apply every *same* vector to all three exposures using each April or October profile, retaining their different YTMs and durations. The grey boxes use all 28 outcomes per exposure/date. Highlight seven chronologically spaced windows as **H1–H7** (see [`scenario data`](assets/analysis2_conditioned_joint_windows.csv)); a legend toggle controls each complete scenario across the two panels. These fixture-derived vectors are distinct from the *presentation-only hypothetical* rows in Analysis 1, §2.1 B1.

**Plot B — dated compensation and break-even comparison.** For each of the **April, July and October** issuer snapshots, calculate six-month compensation from the stated portfolio YTM and the individual **zero-return break-even yield rise** from that compensation and duration, using the *same first-order return model*. Index **each exposure's April compensation and April break-even level separately to 100**, then connect July and October. Retain absolute values in the supporting table and Plotly hover details; do not compare indexed values as if they were absolute return or yield differences.

**Interpretation boundary.** The scenario set is conditional, heavily overlapping and retrospectively reused for the April profile; neither the scenario frequencies nor the normalized resilience paths are forecasts. Future product-level implementation must use appropriately dated, compatible issuer inputs and a defensible source of market scenarios. The figures illustrate complementary purposes: **conditional cross-tenor returns** and **within-tenor changes in compensation versus rate sensitivity**.

### 2.3 Other analyses (examples pending review)

- **Analysis 3 — Risk and Stress (§3.3):** to be developed after review of the shared investment case and its conditional outcomes.
- **Analysis 4 — Credit Spread (§3.4):** to be developed after review.
- **Analysis 5 — Currency and Hedging (§3.5):** to be developed after review.

The present document is an **example-led design probe**, especially for Analysis 1. Its candidate outputs and open review questions do **not** silently amend the architecture or make any optional term-premium, regression, PCA, or visualization method mandatory. The earlier Aspect presentation and cross-Aspect scorecard are not restored.
