# Bondview-v3 — Fixed-Income Analysis Examples

**Status:** Provisional examples companion for review, 2026-10-21. Based on the `analysis` branch of `lbk209/bondview-v3`; this document is not an implementation authorization or investment recommendation.

## 1. Purpose and general conventions

This document illustrates how the financial analyses in [the Bondview-v3 decision architecture](https://github.com/lbk209/bondview-v3/blob/analysis/docs/bond_etf_decision_architecture.md) can appear to an investor, what the displayed results mean, and which specific inputs and calculations produce them. The architecture governs the financial definitions, exposure eligibility, data provenance, and limits; the examples add concrete choices needed to reproduce the shown outputs rather than restating its theory.

**Data convention:** All market histories, ETF identifiers and profiles, disclosure dates, and numerical results in these examples belong to a **constructed illustrative dataset**, not actual FRED observations, issuer disclosures, or realized investment performance. The existing companion CSV fixtures supply the inputs; their numerical values may be used for arithmetic checks.

Common presentation conventions:

- The **user-facing result and its investment interpretation come first**. Supporting data, assumptions, and calculation checks follow.
- ETF and issuer/benchmark exposure sources are distinguished. The modeled quantity is identified by its currency, horizon, gross/net scope, and supported components. **Percentage points (pp)** measure differences between returns; **basis points (bp)** measure yield changes.
- A dated ETF profile applied to an earlier market movement is a **current-exposure counterfactual**, not a historical reconstruction of an ETF's actual return. Results are conditional on the specified joint factor movement, not a forecast or a trading signal.
- Illustrations for the other analyses will be added when reviewed. There is no requirement to preserve the previous Aspect-based chart suite or a combined scorecard.

## 2. Analysis examples

### 2.1 Analysis 3A — Holding-Period Return

**Investment question:** For the same observed historical Treasury market movement and holding horizon, what gross USD holding-period returns are modeled for comparable eligible exposures, and how large are the differences?

#### A. User-facing result

**Selected assessment:** 2026-10-20 (ETF exposure characteristics as of this date)  
**Historical market movement:** 2026-04-20 → 2026-10-20 (183 calendar days)  
**Holding horizon:** `H = 183/365 ≈ 0.50137` years (ACT/365 Fixed)  
**Output:** Approximate **gross USD cash-Treasury exposure total return**, before ETF fees, trading costs, taxes, and KRW currency/hedging effects.

| Eligible exposure | Baseline compensation | Treasury rate-price effect | **Modeled gross USD return** | Difference vs S |
|---|---:|---:|---:|---:|
| **S — short / 2Y factor** | +2.06% | +0.98% | **+3.04%** | — |
| **I — intermediate / 10Y factor** | +2.51% | −4.20% | **−1.69%** | −4.73 pp |
| **L — long / 30Y factor** | +2.64% | −4.56% | **−1.92%** | −4.96 pp |

*The table rounds components to two decimals; relative differences are calculated from unrounded returns. “Baseline compensation” is a yield-based approximation, not measured coupon cash flow or separately calculated roll-down.*

**Conditional comparison:** S has the highest modeled return for this selected joint Treasury movement. It exceeds I by **4.73 pp** and L by **4.96 pp**. I exceeds L by approximately **0.23 pp**. These differences compare the specified exposures under the same dated movement, not a universal ETF ranking.

#### B. Financial interpretation

The Treasury curve moved **nonparallelly**: the matched 2Y yield fell **53 bp**, while the 10Y yield rose **56 bp** and the 30Y yield rose **30 bp**. The decline in 2Y yields increases S's modeled price; rising longer yields reduce the modeled prices of I and L.

All three exposures receive positive baseline compensation in this approximation. For I and L, however, the adverse price effects exceed that compensation over the chosen horizon. L has the highest reported YTM and the smallest *yield increase* among the two longer tenors, yet its greater duration produces a larger adverse rate-price effect. Thus a higher stated yield does not necessarily translate into a higher conditional holding-period return.

The result answers a bounded question about today's selected ETF exposures subjected to the stated past market-factor movement. It does **not** report what investors actually earned between those dates, predict the next six months, or include a Korean investor's realized KRW return. A different joint market movement could change the relative outcome.

#### C. Example construction: data and choices

**C1. Historical Treasury movement.** Use the same aligned start/end observations from [`assets/constructed_market_daily.csv`](https://github.com/lbk209/bondview-v3/blob/analysis/docs/assets/constructed_market_daily.csv). Retain the jointly observed tenor changes rather than choosing a separate shock independently for each ETF.

| Treasury factor | 2026-04-20 | 2026-10-20 | Change |
|---|---:|---:|---:|
| 2Y (`DGS2`) | 4.65% | 4.12% | **−53 bp** (`−0.0053`) |
| 10Y (`DGS10`) | 4.50% | 5.06% | **+56 bp** (`+0.0056`) |
| 30Y (`DGS30`) | 5.02% | 5.32% | **+30 bp** (`+0.0030`) |

**C2. Selected exposure profiles.** Use the 2026-10-20 issuer-style snapshots in [`assets/constructed_issuer_snapshots.csv`](https://github.com/lbk209/bondview-v3/blob/analysis/docs/assets/constructed_issuer_snapshots.csv); assume their available-to-user dates equal their snapshot dates, as specified in the fixture. Each selected source is the **ETF profile**, not an explicitly substituted benchmark proxy.

| ETF | Exposure mechanism | Matched Treasury factor | Gross portfolio YTM | Modified/effective duration used |
|---|---|---|---:|---:|
| S | Cash Treasury | 2Y | 4.10% | 1.85 |
| I | Cash Treasury | 10Y | 5.00% | 7.50 |
| L | Cash Treasury | 30Y | 5.26% | 15.20 |

These cash-Treasury exposure profiles all use a comparable gross portfolio YTM definition and USD economic exposure without hedging. The published-style durations are treated as compatible first-order sensitivity measures for the indicated single-tenor factors; no maturity label is used as duration. This single-factor representation is an example-specific simplification, not a general claim about all ETFs tracking those maturity segments.

**C3. Return-construction choices.** Consistent with [Architecture §3A](https://github.com/lbk209/bondview-v3/blob/analysis/docs/bond_etf_decision_architecture.md#3a-holding-period-return-analysis--initial-primary) and its historical conventions (§4):

- **Baseline:** `gross portfolio YTM at the selected assessment date × ACT/365 holding-period year fraction`. This is the permitted first-order gross USD compensation proxy; no independent coupon accrual, roll-down, or curve carry is added.
- **Price effect:** `−compatible duration × observed matched yield change`, with yield changes in decimal units. No convexity or key-rate-duration refinement is assumed because the fixture supplies no such compatible measures.
- **Scope:** cash-Treasury rate and baseline components only. There is no credit spread term for these exposures. USD/KRW conversion and hedge economics are outside this 3A result, not silently set to a zero contribution to a KRW outcome.
- **Exposure timing:** apply the October 20 YTM and duration profiles to the April–October market-factor vector. These are held fixed for this calculation; April historical ETF-profile data are **not** blended with October data to manufacture a realized return.

#### D. Calculations and verification

The applicable first-order 3A approximation, with no supported convexity or credit adjustment for this example, is:

$$
\widehat R_{i,H}^{USD}\ \approx\ B_{i,H}^{ref}-D_i\Delta y_i,\qquad
B_{i,H}^{ref}=\mathrm{YTM}_{i}\frac{183}{365},\qquad
\Delta y_i=\frac{y_i(v)-y_i(u)}{100}.
$$

YTM and market yields are divided by 100 when entering the formula as decimals. In the calculations below, displayed outputs are percentages (for example, `0.03036116 = 3.036116%`).

| Reconciliation | S | I | L |
|---|---:|---:|---:|
| `YTM_pct × 183/365` | +2.055616% | +2.506849% | +2.637205% |
| `−D × Δy × 100` (in %) | +0.980500% | −4.200000% | −4.560000% |
| **Sum = gross modeled return** | **+3.036116%** | **−1.693151%** | **−1.922795%** |

Hand-checkable calculations:

1. **Elapsed time:** `2026-10-20 − 2026-04-20 = 183 days`; `H = 0.501369863`.
2. **S price effect:** `−1.85 × (−0.0053) × 100 = +0.9805%`; `4.10 × 183/365 + 0.9805 = +3.036116%`.
3. **I price effect:** `−7.50 × 0.0056 × 100 = −4.20%`; `5.00 × 183/365 − 4.20 = −1.693151%`.
4. **L price effect:** `−15.20 × 0.0030 × 100 = −4.56%`; `5.26 × 183/365 − 4.56 = −1.922795%`.
5. **Cross-ETF gaps from unrounded totals:** `S − I = +4.729267 pp`, `S − L = +4.958911 pp`, `I − L = +0.229644 pp`.

**Verification conditions:** Check aligned dates and factor assignments; the conversion between percent/bp/decimal yield changes; the exact 183-day convention; the single selected assessment-date profile per ETF; the common yield definition; and arithmetic reconciliation before rounding. If a necessary baseline or rate sensitivity is absent or unsuitable in an actual input, report the supported partial component with its status instead of presenting a fabricated total return. An observed ETF total-return series, if supplied separately, cannot be inserted as the baseline for this model.

### 2.2 Analyses awaiting examples

- **3B — Risk and Stress:** to be developed after review of 3A.
- **3C — Yield-Curve and Carry:** to be developed after review.
- **3D — Credit Spread:** to be developed after review.
- **3E — Currency and Hedging:** to be developed after review.

The earlier Aspect examples, cross-aspect measurement matrix, and charts are not included in this active companion. Their data and individually valid calculations remain recoverable from repository history and may be reused in later analysis-specific examples.
