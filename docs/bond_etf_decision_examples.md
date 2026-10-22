# Bondview-v3 — Fixed-Income Analysis Examples

**Status:** PROVISIONAL companion for design review — 2026-10-22. Rewritten against the `analysis` branch of `lbk209/bondview-v3`: [`bond_etf_decision_architecture.md`](https://github.com/lbk209/bondview-v3/blob/analysis/docs/bond_etf_decision_architecture.md) (Git blob `5f88f0e4ad1e94196a60862c264d890147798371`) and the prior examples (Git blob `8f6d61c2b11e3c761393845a8eabcea9ddbe91fc`). This document does **not** authorize implementation or recommend an investment.

## 1. Purpose and conventions

This companion tests whether Bondview's established financial analyses produce useful investor-facing information, using **one investment question** and distinct outputs from **Analysis 1 (§3.1, Yield-Curve and Carry)** and **Analysis 2 (§3.2, Holding-Period Return)**. Analysis 1 is intentionally **results-first and not yet fully reviewed**: an example can expose missing inputs or insufficient economic interpretation that must be resolved in a later architecture review. The architecture remains the governing contract. It is not necessary to finish Analysis 1 before a valid conditional Analysis 2 calculation can be made.

**Constructed-data convention.** All dates, Treasury observations, exposure IDs, issuer-style profiles and numbers below are **illustrative**, not actual historical FRED data, real ETF disclosures, forecasts, or realized returns. The market and exposure inputs used for reproducible calculations come from the existing repository fixtures: [`constructed_market_daily.csv`](https://github.com/lbk209/bondview-v3/blob/analysis/docs/assets/constructed_market_daily.csv) and [`constructed_issuer_snapshots.csv`](https://github.com/lbk209/bondview-v3/blob/analysis/docs/assets/constructed_issuer_snapshots.csv). Where those fixtures lack an input (notably a published term-premium model series), no number is invented.

**Reading conventions.** Each example leads with what an investor would see, followed by interpretation, inputs/assumptions, and verification. Yield changes and curve spreads are in **basis points (bp)**; modeled returns are percentages and differences between returns are in **percentage points (pp)**. A rate-change assumption is neither a forecast nor a probability estimate. ETF profiles are distinguished from reference Treasury tenors; no modeled USD gross bond-exposure return is presented as the net KRW outcome of a Korean-listed ETF. All modeled cash-bond exposures are assumed eligible under the architecture's data and factor-compatibility rules.

## 2. One investment case: evaluating Treasury duration

**Investor's question.** “Long-term U.S. Treasury yields have risen. If they rise only modestly from here—or decline—what evidence should I examine, and what conditions would favor short-, intermediate-, or long-duration Treasury exposure?” The market view is the **investor's hypothesis**; no analysis below establishes it as likely.

**Assessment date:** 2026-10-20. **Reference market period:** 2026-04-20 → 2026-10-20. **Conditional investment horizon for Analysis 2:** 183 calendar days (`H = 183/365 = 0.501369863` under ACT/365 Fixed), chosen for illustration, **not** inferred as the likely future path from the prior six months.

### 2.1 Analysis 1 — Yield-Curve and Carry (§3.1)

**Financial question.** What changed in the Treasury yield curve, what can those changes establish, and what additional established market information would be needed to evaluate the investor's long-rate view?

#### A. User-facing result — Treasury market assessment

| Constructed observation | 2026-04-20 | 2026-07-20 | 2026-10-20 | April → October |
|---|---:|---:|---:|---:|
| **2Y Treasury yield** | 4.65% | 4.38% | 4.12% | **−53 bp** |
| **10Y Treasury yield** | 4.50% | 4.70% | 5.06% | **+56 bp** |
| **30Y Treasury yield** | 5.02% | 5.11% | 5.32% | **+30 bp** |
| **10Y − 2Y spread** | −15 bp | +32 bp | **+94 bp** | **+109 bp** |
| **30Y − 10Y spread** | +52 bp | +41 bp | **+26 bp** | **−26 bp** |

**What this tells the investor:** The 10Y–2Y spread widened by 109 bp **because both legs moved in opposite directions**: short yields declined while longer yields rose. At the long end, the 30Y yield rose less than the 10Y yield, narrowing the 30Y–10Y spread. The curve did not undergo one common parallel shift.

**What remains unresolved:** Whether the increase in longer yields primarily reflects higher expected future short rates or higher required term-risk compensation; whether either component will persist or reverse; and which joint 2Y/10Y/30Y yield changes will occur over the next 183 days. The existing constructed CSV does **not** contain a published-model decomposition, so **term-premium attribution is unavailable in this example**, not zero.

**Investor-facing follow-on information worth testing in Analysis 1:** An internally consistent published-model decomposition of a given Treasury zero-coupon/fitted yield into the model's expected-average-short-rate and term-premium components, with dated levels **and changes**. Such a result might help interpret the move, but it would not imply a future yield trajectory or itself rank ETFs. A simple par-yield spread cannot substitute for this decomposition.

#### B. Financial interpretation

A larger positive 10Y–2Y spread is an observation about *relative yields*, not evidence by itself that longer bonds are cheap or that the spread must mean-revert. Here the 10Y yield increased 56 bp while the 2Y fell 53 bp; their opposing price effects have very different implications for duration exposures. Similarly, a 30Y yield level of 5.32% is not an ETF's portfolio YTM, nor proof that 30Y yields have reached a historical or economic ceiling.

The current market data can narrow and sharpen the investor's question. They **cannot** justify assuming that the previous April–October movement will recur after October 20. Analysis 2 therefore displays *conditions* under which one exposure has a higher modeled return, rather than accepting a single “most likely” joint curve movement from Analysis 1.

#### C. Construction and inputs

The values are dated rows from [`constructed_market_daily.csv`](https://github.com/lbk209/bondview-v3/blob/analysis/docs/assets/constructed_market_daily.csv), using `DGS2_pct`, `DGS10_pct` and `DGS30_pct`. Recalculate every spread from the underlying yield columns, not from the fixture's precomputed spread columns. All three tenors at each date are aligned. The displayed interval is 183 calendar days; it is not an estimate of future expected yields.

A **published term-premium-model result** requires a separately sourced and dated set of model-fitted/zero-coupon yields, expected-average short-rate components, and premia with matching model definitions. For instance, an ACM or Christensen–Rudebusch series could be examined once obtained. Do **not** force these series to add up to a raw `DGS10` par/constant-maturity yield, and do not mix components from different models. Neither actual nor synthetic values for such a decomposition are included in the available fixtures.

No unsupported roll-down return is calculated: Treasury par yield observations and selected ETF YTM/duration alone are insufficient to establish an ETF portfolio's aging and rebalancing mechanics.

#### D. Arithmetic and design-review checks

- April: `(4.50 − 4.65) × 100 = −15 bp`; October: `(5.06 − 4.12) × 100 = +94 bp`; change: `94 − (−15) = +109 bp`.
- April 30Y−10Y: `(5.02 − 4.50) × 100 = +52 bp`; October: `(5.32 − 5.06) × 100 = +26 bp`; change: `−26 bp`.
- Treasury changes: `Δ2Y = −53 bp`, `Δ10Y = +56 bp`, `Δ30Y = +30 bp`, a **historically observed joint vector** for this particular interval, **not** an assumed future six-month vector.

**Questions for the later Analysis 1 architecture review (not accepted requirements):**

1. Is the derived-curve display, by itself, sufficiently informative, or is a published term-premium decomposition an essential user-facing result for this investment question? The latter needs actual model series and explicit provenance.
2. Should Analysis 1 present observed cross-tenor co-movements over a properly matched reference horizon, and how should regime sensitivity and strongly overlapping samples be disclosed? No PCA/regression model or probabilities are presumed here.
3. What is the minimum additional market evidence needed to evaluate the *plausibility* of a specific long-rate view without turning Analysis 1 into an automatic forecasting or scenario-generation engine?

### 2.2 Analysis 2 — Holding-Period Return (§3.2)

**Financial question.** Under what combinations of Treasury yield changes would the eligible S, I and L exposures have higher modeled returns over the chosen six-month horizon? How much does the answer depend on the other tenors, even if the investor has a view about one long rate?

#### A. User-facing result — conditional ETF preference regions

**Assessment:** 2026-10-20 issuer-style ETF profiles; **horizon:** `H = 183/365` years. **Quantity:** approximate **gross USD cash-Treasury exposure holding-period return**, before fees, transaction costs, taxes, and KRW FX/hedging. No forward path or probability is predicted.

![ETF conditional return-preference regions, with 10Y versus 30Y assumed yield changes and three separate fixed 2Y change assumptions](assets/bond_etf_preference_regions.png)

**How to read the chart:** The horizontal axis is the **assumed 10Y yield change** and the vertical axis the **assumed 30Y yield change**, both in bp over the chosen horizon. Each panel fixes the **2Y yield change** at −50, 0, or +50 bp. A region identifies **which exposure has the largest modeled return**, conditional on the displayed three-tenor movements. Thin boundaries are equal-return conditions. No color represents a forecast probability, an ETF recommendation, or risk-adjusted attractiveness.

**A few points to read from the regions** (illustrations of the formula, **not** selected plausible forecasts):

| Fixed 2Y | Assumed 10Y | Assumed 30Y | S return | I return | L return | Highest modeled return |
|---:|---:|---:|---:|---:|---:|---|
| 0 bp | 0 bp | 0 bp | +2.06% | +2.51% | +2.64% | **L** |
| 0 bp | 0 bp | +30 bp | +2.06% | +2.51% | −1.92% | **I** |
| 0 bp | +30 bp | +30 bp | +2.06% | +0.26% | −1.92% | **S** |
| −50 bp | 0 bp | 0 bp | +2.98% | +2.51% | +2.64% | **S** |

The crucial finding is not which ETF wins at a chosen point: **the market view about one tenor does not by itself determine the relative outcome among different-duration ETFs.** The chart exposes the missing joint-rate assumptions rather than disguising them in a few hand-selected scenarios.

#### B. Financial interpretation

At unchanged factor yields and under this **first-order constant-yield compensation reference**, L's higher YTM produces the highest modeled USD return. But its much greater duration makes its result more sensitive to an increase in the 30Y yield. If 30Y rises materially while 10Y stays flat, I can outperform L; if both long tenors rise enough, S may outperform both. Even if the 30Y does not rise, a sufficiently large **decline** in 2Y yields can make S superior to L. This is not evidence that any of those joint combinations will happen.

**Connection to Analysis 1:** The observed divergence of 2Y and longer yields explains why the investor must consider different curve configurations, not merely “rates rise/fall.” Analysis 1 can investigate market information that bears on the plausibility of configurations, but its yield spreads and term-premium decomposition **cannot uniquely supply the yield-change vector**. Analysis 2's regions are therefore conditional comparisons, not conclusions inferred from Analysis 1.

The chart deliberately considers a broad rectangular shock range (−50 to +50 bp on the 10Y and 30Y axes) to **show where comparative outcomes switch**. This range is an illustrative *display domain*, not an estimated plausible interval, confidence region, or assumption that its points are equally likely. Risk, likelihood, and downside questions need separately justified evidence, potentially in Analysis 3.

#### C. Construction: exposure data and modeling choices

All three exposures use the **2026-10-20 issuer-style ETF profile** from [`constructed_issuer_snapshots.csv`](https://github.com/lbk209/bondview-v3/blob/analysis/docs/assets/constructed_issuer_snapshots.csv); none is a user-substituted benchmark. They are illustrative **USD cash Treasury exposures**.

| Exposure | Matched Treasury factor | Gross portfolio YTM | Effective/modified duration used | First-order compensation `YTM × 183/365` |
|---|---|---:|---:|---:|
| **S — short** | 2Y | 4.10% | 1.85 | +2.055616% |
| **I — intermediate** | 10Y | 5.00% | 7.50 | +2.506849% |
| **L — long** | 30Y | 5.26% | 15.20 | +2.637205% |

The published-style profiles are assumed to have the same compatible **gross portfolio YTM** definition and durations appropriate for the indicated *single-tenor-factor* first-order calculation. Real ETFs may have multiple key-rate exposures. Duration is measured at the **October 20 assessment date**, which is the *initial exposure* being stressed, not the ending duration of a realized April–October investment. All profiles are held fixed for the conditional exercise.

**Calculation choice:** `modeled gross USD return ≈ YTM × H − D × Δy` with `Δy` in decimal units. This is a **recognized first-order professional holding-period-return approximation**, not a Bondview-specific attractiveness score. It does not measure coupon cash received or separate roll-down. No unsupported convexity, spread or hedge terms are invented; convexity was not supplied in the fixture. Yield movements are treated as finite static-exposure shocks, not an explicit sequence of ETF rebalancings or a full cash-flow revaluation. Larger shocks and evolving ETF holdings can reduce approximation accuracy. The display does not infer net Korean-listed ETF performance.

For every chart point, the three factor changes collectively form a **hypothetical joint vector** `(Δ2Y, Δ10Y, Δ30Y)`; unlike Analysis 1's April–October vector, these are **user-inspectable assumptions**, not observed historical intervals. The horizon is chosen independently and shared by the three profiles. No hypothetical shock is derived by replaying the prior six months or automatically generated from 3C.

#### D. Calculations, equal-return boundaries, and verification

Use return units in **percentage points** and yield shocks in **basis points**. With `B_S = 2.055616`, `B_I = 2.506849`, and `B_L = 2.637205` in percentage-point units:

```text
R_S (%) ≈ B_S − 0.0185 × Δ2Y_bp
R_I (%) ≈ B_I − 0.0750 × Δ10Y_bp
R_L (%) ≈ B_L − 0.1520 × Δ30Y_bp
```

These coefficients are the respective durations divided by 100 because a 1 bp yield change is `0.0001` in decimal units and a return percent equals 100 times its decimal fraction.

The **equal-return boundaries** are obtained directly from the same Analysis 2 return approximations, not a distinct decision model:

```text
I = S :  Δ10Y_bp = (B_I − B_S + 0.0185 × Δ2Y_bp) / 0.0750
L = S :  Δ30Y_bp = (B_L − B_S + 0.0185 × Δ2Y_bp) / 0.1520
L = I :  Δ30Y_bp = (B_L − B_I + 0.0750 × Δ10Y_bp) / 0.1520
```

For `Δ2Y = 0`, the I=S threshold is `Δ10Y ≈ +6.02 bp`; L=S is `Δ30Y ≈ +3.83 bp`. If `Δ10Y = 0`, the L=I boundary is `Δ30Y ≈ +0.86 bp`. These are **pairwise** equal-return conditions. Only the boundary portions separating the *highest-return regions* are emphasized in the figure. The three boundaries intersect at approximately `(Δ10Y, Δ30Y) = (+6.02, +3.83) bp` when `Δ2Y = 0`. The boundaries shift when the assumed 2Y change shifts; they do not tell us which region is likely.

**Verification examples:**

- At `(Δ2Y, Δ10Y, Δ30Y) = (0,0,0)` bp, `(S,I,L) = (+2.055616,+2.506849,+2.637205)%`, so L is highest.
- At `(0,0,+30)` bp, L becomes `2.637205 − 0.152 × 30 = −1.922795%`; I remains `+2.506849%`, so I is highest.
- At `(0,+30,+30)` bp, I becomes `2.506849 − 0.075 × 30 = +0.256849%`; S remains `+2.055616%`, so S is highest.
- At `(−50,0,0)` bp, S becomes `2.055616 + 0.0185 × 50 = +2.980616%`, exceeding both I and L.

**Separate historical-stress arithmetic, retained from the prior example:** If the *observed* April 20–October 20 vector `(−53,+56,+30)` bp is applied **as a historical stress**, not the next-six-month expected path, the model gives S `+3.036116%`, I `−1.693151%`, L `−1.922795%`; S−I is `+4.729267 pp`, S−L is `+4.958911 pp`, and I−L is `+0.229644 pp`. These are current-exposure counterfactual returns and **not** the realized ETF returns during those dates. This stress is supplementary; it is not the main scenario or preference map.

**Validation rules:** Reconcile the chart classification against the largest of the three numeric modeled returns at each plotted point; verify return/bp conversions, common horizon, issuer source and as-of date, correct tenor mapping, and pairwise equality. Do not present the preference-region colors as calibrated event frequencies, probabilities, total risks, or buy/sell signals. A valid rate-only price effect without an eligible baseline must be labeled a **partial** result, not a complete return. ETF or benchmark realized total-return series must never be substituted for the compensation baseline.

### 2.3 Other analyses (examples pending review)

- **Analysis 3 — Risk and Stress (§3.3):** to be developed after review of the shared investment case and its conditional outcomes.
- **Analysis 4 — Credit Spread (§3.4):** to be developed after review.
- **Analysis 5 — Currency and Hedging (§3.5):** to be developed after review.

The present document is an **example-led design probe**, especially for Analysis 1. Its candidate outputs and open review questions do **not** silently amend the architecture or make any optional term-premium, regression, PCA, or visualization method mandatory. The earlier Aspect presentation and cross-Aspect scorecard are not restored.
