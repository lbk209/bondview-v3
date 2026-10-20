# Bondview-v3 — Korean-Listed U.S. Bond ETF Decision Examples and Validation

**Status:** **PROVISIONAL companion examples — 2026-10-20.** Prepared against the revised `bond_etf_decision_architecture.md` dated 2026-10-20; not a live market study, backtest, accepted investment policy, development roadmap, or authorization for implementation.

**Companion architecture:** [`bond_etf_decision_architecture.md`](bond_etf_decision_architecture.md). If a proposed example is inconsistent with an accepted architecture contract, resolve the conflict before using that example as an implementation acceptance test. Earlier Bondview repositories are not design authorities.

> **All yields, exposure values, credit spreads, FX paths, break-even figures, investor policies and results in this document are constructed examples.** ETF tickers mentioned in the legacy validation section identify historically researched product categories only; they are **not** verified current issuer exposures or recommendations. No actual market data, current ETF sheets, or price histories were used to produce the figures.

## 1. Purpose and interpretation

The examples serve three purposes:

1. **Economic usefulness:** Demonstrate whether conventional fixed-income calculations reveal meaningful changes in investment opportunities between Treasury maturity segments and credit markets.
2. **ETF application:** Show how the same models use published ETF exposure characteristics and produce supported numerical outcomes, qualifications, or clearly unresolved preferences.
3. **Verification:** Preserve reference arithmetic, model-applicability rules, missing-data behavior, and separate product/FX/return diagnostics from the predecessor examples document.

The same **financial definitions and functions** should support an individual ETF, a full historical interval, and a chosen ETF universe. Those are different views and valid relative calculations, not three attractiveness engines. A market-reference illustration may be economically useful before any ETF is selected, but ETF-specific numerical sensitivities require compatible issuer disclosures.

### 1.1 Terminology and unit conventions

- Treasury constant-maturity yields (`2Y`, `5Y`, `10Y`, `30Y`) are **market references**, not coupon-bond or ETF yields to maturity. ETF benchmark tenor **does not determine duration**.
- All yield changes in price-sensitivity formulas are **decimal** (50 bp = `0.005`). `1 bp = 0.01 percentage point = 0.0001 decimal`.
- A *market-reference break-even* substitutes documented or explicitly assumed benchmark durations and market yield differences for a compatible compensation calculation. It **does not** equal actual ETF gross carry or net KRW expected return.
- **Current-exposure counterfactual**: the specified duration and/or spread duration is applied to historical-sized market changes. It is neither realized ETF historical P&L nor a future return prediction.
- **Scenario**: a declared hypothetical yield/spread change, not a probability or price forecast. A conditional preference can be valid without establishing that buying now beats waiting.
- **Unavailable**, **not applicable (N/A)**, **unsupported** and **proxy** have different meanings and must never silently be converted to zeros.
- An issuer's distribution yield is **not** automatically economic carry. No historical issuer yield is manufactured from today's ETF facts.
- Figures are economic visual examples, **not a requirement to implement a particular chart type**. Plot only an analytically meaningful time series; do not multiply graphs that repeat the same source information.

### 1.2 What the example set does and does not establish

The primary investment questions are: (i) how has the compensation for extending Treasury maturity changed relative to associated rate risk? (ii) how large is that compensation relative to historically observed yield-change uncertainty? (iii) does corporate-bond repricing reflect Treasury movements or a credit-specific spread change, and what does that imply under a declared credit scenario? The answers can be complementary, adverse, or mixed. They are not votes for an integrated numerical attractiveness score.

Correct arithmetic does **not** validate a general purchase ranking. The source data and compatibility requirements matter as much as the formula. The purpose of the first research implementation is to challenge these assumptions on actual available market and issuer data—not to tune outcomes until a chart appears persuasive.

---

## 2. Treasury maturity opportunity: duration-adjusted compensation assessed over six months

**Economic question:** Has gross compensation for taking 10Y instead of 2Y Treasury exposure improved relative to the additional duration? The 30Y comparisons remain visible to show that the answer can differ by maturity pair.

### 2.1 Dated yield observations and reference assumptions

The **synthetic** daily Treasury series spans April 2023–October 2026. Section 2 examines assessment dates from **April 20 to October 20, 2026**; these dates locate the calculations and do **not** specify a holding period. The underlying daily series preserves the following seven reference observations:

| Assessment date (2026) | Treasury 2Y | Treasury 10Y | Treasury 30Y |
|---|---:|---:|---:|
| Apr 20 | 4.60% | 4.50% | 5.00% |
| May 20 | 4.55% | 4.70% | 5.15% |
| Jun 22 | 4.45% | 4.50% | 4.95% |
| Jul 20 | 4.35% | 4.80% | 5.20% |
| Aug 20 | 4.30% | 4.60% | 5.00% |
| Sep 21 | 4.20% | 4.95% | 5.35% |
| Oct 20 | 4.10% | 5.10% | 5.40% |

Use fixed representative durations **`D_2=1.9`, `D_10=7.5`, `D_30=16.0`**. For each date, approximate **one subsequent year of gross compensation** using that date's observed *annualized* Treasury reference yield. This deliberately simplified compensation proxy does not establish an ETF's actual one-year carry or expected return.

For longer and shorter exposures `L` and `S`, suppose their relevant yields **subsequently increase by the same amount**, `delta_y_common` in decimal units. The first-order conditional difference is:

`relative_result_proxy ≈ (c_L - c_S) - (D_L - D_S) * delta_y_common`.

The **additional common yield increase** at which this proxy difference becomes zero is:

`break_even_common_rise_bp = 10,000 * (c_L - c_S) / (D_L - D_S)`, for `D_L > D_S`.

### 2.2 Visualization: daily evolution of duration-adjusted compensation

![Daily evaluations of a one-year gross-compensation-proxy break-even from April to October 2026 for 10Y/2Y, 30Y/2Y and 30Y/10Y; highlighted October 10Y/2Y break-even 17.86 bp](assets/maturity_break_even_history.png)

The daily curve is calculated **from yields at each date**, not from trailing yield changes or a rolling average. Every point applies the **same one-year compensation convention**. The period across the horizontal axis is the period during which the market opportunity is *observed*, not a return earned over that period.

| Pair | Apr 20 break-even | Oct 20 break-even | Interpretation under the same proxy |
|---|---:|---:|---|
| **10Y vs 2Y** | **−1.79 bp** | **+17.86 bp** | Additional compensation improves substantially relative to extra duration |
| 30Y vs 2Y | +2.84 bp | +9.22 bp | Improves under this measure |
| 30Y vs 10Y | +5.88 bp | +3.53 bp | Extra compensation beyond 10Y deteriorates |

**Economic conclusion:** The 10Y reference exposure became **more favorable than 2Y on this particular gross compensation measure** across the assessment dates. The 30Y/10Y comparison illustrates why that conclusion need not extend to every maturity pair.

In October, `5.10%−4.10%=1.00 pp` of *annualized yield difference* is used as a **one-year gross-compensation proxy**; with additional duration `5.6`, its break-even common increase is `17.86 bp`. Neither the one-year compensation assumption nor this threshold predicts yield movements. A simple six-month **proration** would imply `0.50 pp` additional gross compensation and **`8.93 bp`** common-increase break-even, but that is not a full six-month ETF return model.

**Interpretation limits:** This duration-normalized proxy is a transformation of the observed Treasury spread and the assumed durations, not independent evidence. It excludes genuine ETF carry/roll, reinvestment, nonparallel curve movements, convexity, funding, hedging and portfolio changes. ETF-level holding-period break-even requires compatible issuer-reported characteristics and defensible period compensation rather than market-yield substitution.

**Reproducible source:** [`assets/synthetic_daily_treasury_and_compensation.csv`](assets/synthetic_daily_treasury_and_compensation.csv).

---

## 3. Context for the break-even cushion: historically observed rate-risk variation

**Economic question:** The 10Y/2Y compensation proxy improved, but how large have the **relative rate-price consequences** of paired 2Y and 10Y yield changes been? This question uses actual changes *between dates* in a production dataset, rather than only the yields available at each date.

### 3.1 Daily-ending six-month yield changes

Use a **six-month change horizon**, a **three-year historical reference period** ending October 20, 2026, and **daily observation endpoints**. This example uses constructed yields, so its dates and statistics illustrate a method, not actual Treasury history. For each available end date `t`, select the latest available observation on or before the calendar date six months earlier, and calculate:

`delta_y_10,6m(t) = y_10(t) - y_10(t−6 months)`  
`delta_y_2,6m(t) = y_2(t) - y_2(t−6 months)`

Using the fixed reference durations from Section 2:

`X_6m(t) = 7.5 * delta_y_10,6m(t) - 1.9 * delta_y_2,6m(t)`.

The yield changes above are decimals; multiply `X_6m` by `100` for **percentage points (pp)**. Positive `X_6m` indicates that the 10Y exposure had a *less favorable rate-price effect* than 2Y across that window; negative means the opposite. This is a difference between modeled **price effects**, not a complete relative return.

The **six-month horizon** is the duration of each rate change; the **three-year reference period** determines how many market environments are included; **daily sampling** determines how frequently one such six-month change is recomputed. These choices are independent and adjustable. Daily sampling is computationally cheap and permits inspection of change over time, but consecutive six-month windows overlap heavily; they are not independent episodes.

For comparison with a six-month rate-risk horizon, prorate October's Section 2 **annualized** 10Y/2Y yield premium `1.00 pp` to a **`0.50 pp` indicative six-month gross-compensation proxy**. That corresponds to an **`8.93 bp` common-increase break-even** if both yields move equally. Section 2's familiar **17.86 bp** result instead assumes *one year* of compensation and **must not** be directly compared with six-month `X` values.

The simplified conditional comparison is therefore:

`relative_result_6m_proxy ≈ 0.50 pp - X_6m`.

It is favorable to 10Y on this proxy **when `X_6m < 0.50 pp`** and unfavorable when the additional 10Y rate-related loss exceeds the assumed compensation. This comparison applies **October's reference compensation** to past-sized relative rate movements; it is not the historical return or carry actually available at the starting dates of those windows.

### 3.2 Visualization: evolution and distribution from the same daily observations

**Evolution through time:** Each point is the rate-related relative loss over the **preceding six months**, ending on the displayed date. The dashed line marks October's fixed **+0.50 pp** six-month compensation reference, not a historical compensation value at every past date.

![Daily-ending six-month additional 10Y relative rate-price losses with October six-month compensation reference at 0.50 percentage points](assets/relative_rate_risk_evolution.png)

**Distribution:** The same sequence of daily `X_6m(t)` values is grouped into ranges by magnitude. Thus a point on the time series becomes **one observation** in the histogram: the time series answers *when* a given relative effect occurred, while the histogram answers *how large such effects have been across the reference period*.

![Histogram of the daily-ending six-month relative rate-price effects, showing the October six-month compensation reference at 0.50 percentage points](assets/relative_rate_risk_context.png)

**Reading the distribution:** The relevant question is **how much** the additional 10Y rate-price effect improves or erodes the indicative six-month `0.50 pp` compensation, not how many densely overlapping windows fall on either side of that threshold. The distribution is summarized below in the same units as its horizontal axis. The relative-result column applies `0.50 pp − X_6m` to each reported value; it is not an observed ETF return.

| Descriptive measure of six-month `X_6m` | Additional 10Y rate loss (`X_6m`) | Indicative 10Y-minus-2Y relative result (`0.50 − X_6m`) | Interpretation |
|---|---:|---:|---|
| Median | +0.277 pp | **+0.223 pp** | The middle observation retains a modest compensation advantage for 10Y under the model |
| Mean | +0.823 pp | **−0.323 pp** | Larger adverse effects pull the sample-average modeled result below zero; this is not an expected return |
| 90th percentile | +3.835 pp | **−3.335 pp** | An upper-tail relative rate loss substantially overwhelms the compensation proxy |

The **median and mean tell different stories**: the typical middle observation remains slightly favorable to 10Y, but larger adverse relative rate effects dominate the sample mean. The mean is a description of the constructed, overlapping-window history—not a probability-weighted estimate of what happens next. The full observed synthetic range of `X_6m` is approximately **−3.31 to +5.96 pp**, emphasizing that **magnitude and asymmetry matter more than a threshold count**.

**Reading the evolution chart:** It shows *when* the modeled disadvantage developed and whether it persisted. In the constructed path, `X_6m` remains elevated over extended intervals around **November 2024–March 2025** and **May–October 2026**, with materially lower or negative intervals between them. On **October 20, 2026**, `X_6m = +5.45 pp`, which corresponds to a **−4.95 pp** relative-result proxy after the fixed `0.50 pp` compensation. These time patterns describe the invented yield history, not historical Treasury episodes. Nearby daily points share most of the same six-month window, so prolonged runs are not independent events.

**Interpretation alongside Section 2:** A more favorable current *gross compensation* relationship can coexist with sizable adverse **nonparallel** changes in 2Y and 10Y yields. Section 2 quantifies a conditional offset assuming equal yield changes; Section 3 describes the relative rate-price consequences of paired yield changes, which need not be equal. Neither measure disproves the other or yields a complete investment recommendation.

**Scope and history choices:** The three-year lookback and six-month horizon are **illustrative selections**, not fixed Bondview rules. Shorter reference histories can emphasize recent rate regimes but omit stresses; much longer histories may mix structurally different conditions. The lookback/horizon and overlap convention should be clearly disclosed and user-adjustable. With real market inputs the rate changes are genuinely observed, but applying fixed reference durations remains a **modeled counterfactual**, not realized ETF performance.

**Reproducible source:** [`assets/synthetic_daily_rolling_6m_relative_rate_risk.csv`](assets/synthetic_daily_rolling_6m_relative_rate_risk.csv), derived from the same daily Treasury history used in Section 2.

---

## 4. Corporate-bond market: Treasury-rate changes versus credit repricing

**Economic question:** Are changes in corporate-bond conditions mainly attributable to changing Treasury rates or to **additional credit spread**? If Treasury yields stabilize or fall while credit spreads widen, what can we conclude about corporate bonds?

### 4.1 Constructed market and reference exposure

Reuse Section 2's imaginary April–October interval and add a hypothetical 5Y Treasury series and investment-grade (IG) index OAS series:

| Synthetic month | Treasury 5Y | IG OAS |
|---|---:|---:|
| Apr | 4.55% | 85 bp |
| May | 4.60% | 100 bp |
| Jun | 4.50% | 105 bp |
| Jul | 4.65% | 95 bp |
| Aug | 4.60% | 130 bp |
| Sep | 4.75% | 125 bp |
| Oct | 4.70% | 120 bp |

For a **defined hypothetical** cash corporate exposure, let `D_rates=5.5` and `D_spread=5.0` (not an actual ETF disclosure).

`credit_price_effect ≈ -D_rates * delta_y_5Y - D_spread * delta_OAS`.

This describes rate and credit sensitivity, not corporate ETF historical return. It excludes coupons, default losses, migration, liquidity, convexity and active portfolio changes.

### 4.2 Visualization: distinct sources of the market shock

![Cumulative synthetic current-exposure effects from changing Treasury 5Y yields and IG OAS, separately and combined](assets/treasury_vs_credit_contributions.png)

| Contribution, April–October | Calculation | Price sensitivity |
|---|---|---:|
| Treasury rates | `−5.5 × 0.0015` | −0.825% |
| Credit spread | `−5.0 × 0.0035` | −1.750% |
| Combined | Sum, first order | **−2.575%** |

**Useful conclusion:** The constructed deterioration is more strongly linked to **credit-spread repricing** than to Treasury-rate repricing. If Treasury yields had been stable or falling while OAS widened, the same method would isolate credit-specific adverse repricing even more clearly.

**Important boundary:** OAS widening may reflect changing expected defaults, liquidity, risk appetite, or required risk premium; it does **not** by itself prove fundamental corporate distress. Conversely, a *negative Treasury-rate contribution* merely reflects a Treasury yield rise, not a unique credit-market problem. The stronger credit warning comes from adverse **spread changes relative to Treasuries**.

### 4.3 Additional gross credit compensation: separate question

With OAS rising from 85 to 120 bp and **assuming** one-year incremental gross compensation equal to OAS, the illustrative spread-widening break-even is:

`gross_spread_cushion_bp = OAS_bp / D_spread`.

It changes from `85 / 5 = 17 bp` to `120 / 5 = 24 bp`. This means increased **gross spread compensation under this assumption**, not proof of sufficient **net** compensation. No expected default loss was subtracted; the example does not recommend purchasing the corporate ETF. The spread cushion is another interpretation of the **same OAS series**, not independent evidence that the credit market is safer.

**ETF application:** Verify the product's investment-grade/high-yield segment, maturity mix, spread duration if available, and the market OAS proxy's coverage. A broad HY OAS must not be silently used as an exact effective spread for a different credit profile.

---

## 5. Applying common analysis to an illustrative ETF universe

**Economic question:** When these bond-market relationships are relevant to actual products, what can a comparable ETF table establish—and where must it stop?

The table below consists of **invented products and hypothetical exposure values**, not live products. It provides a structural illustration only; published ETF data would have to replace every portfolio characteristic. Assume all four cash-bond exposures are being discussed on an **underlying USD-bond basis**, not comparable after-hedge KRW returns.

| Product | Economic reference | Rate duration | Spread duration | Assumed issuer-style YTM | Relevant corporate OAS |
|---|---|---:|---:|---:|---:|
| ETF A | 2Y Treasury | 1.9 | N/A | 4.20% | N/A |
| ETF B | 10Y Treasury | 7.5 | N/A | 5.00% | N/A |
| ETF C | 30Y Treasury | 16.0 | N/A | 5.30% | N/A |
| ETF D | 5Y-matched IG credit | 5.5 | 5.0 | 5.80% | 120 bp (market reference) |

At a **common hypothetical +50 bp Treasury rate shock** and a separate **+100 bp credit-spread shock**, applying Section 6's formulas yields:

| ETF | Rate-only +50 bp shock | Additional +100 bp credit OAS shock | Combined price-only shock |
|---|---:|---:|---:|
| A | −0.95% | N/A | −0.95% |
| B | −3.75% | N/A | −3.75% |
| C | −8.00% | N/A | −8.00% |
| D | −2.75% | −5.00% | −7.75% |

The additional spread shock is assumed **only for the corporate product**, not silently for Treasury ETFs. Combined shocks are **price sensitivities**, not the complete one-year total returns of the respective funds.

**What is established:** A has the smallest modeled rate sensitivity, C the largest, and D introduces a distinct credit risk. All comparisons use the same scenario convention where applicable. **What is not established:** A universal attractiveness ranking, comparable net KRW compensation, or an assertion that A will outperform C. The hypothetical issuer-style YTMs are **not** automatically one-year carry and must not simply be added to the price shocks.

**Important market-versus-ETF distinction:** Section 2's `+17.86 bp` uses **market** 10Y/2Y yield proxies and benchmark-style durations, while the product table lists *different* hypothetical issuer-style YTM values. A true product-level break-even requires **compatible holding-period compensation**, including currency and structural assumptions where relevant. Do not transplant the market-reference break-even into an ETF decision as if the two yield definitions were identical.

**Applicability logic:** A verified pure Treasury ETF has credit OAS `not_applicable`; a corporate ETF without disclosed applicable spread duration may have credit-spread sensitivity `unavailable` or an expressly labeled proxy; a futures ETF with cash-bond carry formula is `unsupported`. All eligible ETFs may appear in the universe, but some analyses must remain partial or conditional.

---

## 6. Existing policy-conditioned purchase cases — retained as synthetic controls

The earlier examples A, B and C verify an **illustrative investor-policy response**, not the existence of an accepted universal purchase rule. This section preserves their arithmetic and interpretation without making the 12-month risk budget the center of Bondview's design.

### 6.1 Legacy Example A — long-duration ETF, modest compensation

**Historically referenced product category:** an issuer-identified hedged long Treasury ETF (formerly illustrated by ticker `453850`; current details must be rechecked). **All following values hypothetical.** Assume current 30Y market yield `4.80%`, 6M/1M yield changes `+70/+20 bp`, portfolio-duration proxy `17.0`, comparable **assumed** 12-month KRW-hedged net carry `4.00%`, assumed 12-month KRW cash return `3.80%`, adverse shock `+100 bp`, investor stress-loss budget `10.00%`.

`rate_price_effect = -17.0%`; `illustrative_net_carry_plus_rate_stress = 4.00% - 17.00% = -13.00%`. If the policy rejects modeled stress losses exceeding 10%, the result is **defer under this specific policy**, not an unconditional sale recommendation or a prediction that rates will continue rising. Convexity is omitted and should be flagged. The assumed 4% net carry is **not inferred from the issuer distribution yield**.

### 6.2 Legacy Example B — same category, changed compensation

Separate hypothetical snapshot: 30Y Treasury yield `6.00%`, 6M/1M changes `+80/0 bp`, reported/illustrative duration `14.5`, comparable **assumed** KRW-hedged 12-month net carry `5.00%`, assumed KRW cash `3.00%`, same +100 bp stress and 10% loss budget.

`rate_price_effect = -14.50%`; `illustrative_net_carry_plus_rate_stress = 5.00% - 14.50% = -9.50%`. The stress screen **passes** for the hypothetical policy, while the cash-relative assumed compensation is `+2.00 pp`. A valid output is *more suitable under the illustrated risk condition, subject to other assumptions*. **Passing the stress budget alone does not justify “buy.”** Different duration values in two dates/snapshots must never be presented as historical issuer values without actual dated disclosures. Without supportable net carry, the decisive numeric policy conclusion should be downgraded.

### 6.3 Legacy Example C — intermediate versus long Treasury exposure

Two contemporaneous hypothetical hedged exposures (historically illustrated by tickers `0085N0` and `453850`):

| | Intermediate | Long |
|---|---:|---:|
| 6M relevant yield change | +50 bp | +65 bp |
| 1M relevant yield change | −15 bp | +10 bp |
| Effective duration | 7.5 | 16.0 |
| **Assumed** 12M net KRW carry | 3.50% | 4.20% |
| +100 bp price sensitivity | −7.50% | −16.00% |
| Illustrative carry-plus-stress result | **−4.00%** | **−11.80%** |

Under the same *illustrative* 10% stress-loss budget, intermediate passes and long fails. This can support an intermediate-duration conditional preference for a stated risk-controlled new allocation; it cannot prove that intermediate exposure offers the best unconditional return or that a different investment objective is invalid.

---

## 7. Model boundaries, product routing, and separate diagnostics

These reproduce valuable safeguards from the earlier examples. They are **not** all core buy/sell or attractiveness calculations.

### 7.1 Legacy Example D — FX identity and separate hedging assumption

An **unhedged**, compatible USD bond return of `−2.00%` combined with a USD/KRW rise of `+8.00%` gives `(0.98 × 1.08 − 1) × 100 = +5.84%` in KRW. If a corresponding hedged product's hypothetical realized return were `−2.70%`, its `−0.70 pp` difference from the underlying `−2.00%` **would not uniquely prove hedging cost**; it could include forward points, slippage, fees, benchmark and implementation effects.

For Bondview's initial bond-market research, **defer detailed FX/hedging analysis**. Keep issuer hedge policy, numeraire and comparability explicit; do not prefer an unhedged ETF simply because its historical KRW return was greater. Actual historical ETF price/NAV data may later be used only in an **independent performance/diagnostic view**, never as selection signals or replacements for published duration.

### 7.2 Legacy Example E — Treasury futures are not ordinary cash Treasury bonds

A historical reference instrument (formerly `308620`) is a Treasury-futures ETF, not a static coupon-bond portfolio. Suppose 10Y Treasury yields rose 40 bp. Without disclosed compatible futures DV01/duration, collateral treatment, roll economics or index details, the system may report **market context** but cannot manufacture cash-bond yield/carry or precise fund return. Default exclude from ordinary cash-bond assessment; user opt-in permits only supported aspects and appropriate warnings.

### 7.3 Legacy Example F — high-yield credit shock

With a hypothetical HY corporate exposure of `D_rates=4`, `D_spread=4`, a matched Treasury yield fall of `−40 bp` and HY OAS increase of `+150 bp`:

`rate contribution = -4 * (-0.0040) = +1.60%`; `spread contribution = -4 * 0.0150 = -6.00%`; combined **price-only** result `= -4.40%`.

The adverse effect is dominated by spread deterioration **despite favorable rates**. Do not turn this into a proof of realized defaults or infer a buy/sell decision from the fund's distribution yield. A policy explicitly excluding speculative-grade credit can reject it for product compatibility; a policy accepting HY needs additional credit-risk/compensation review.

### 7.4 Legacy Example G — short USD credit is not automatically pure Treasury

A historically illustrated short USD active-bond product (formerly ticker `440650`) can contain credit instruments even if its name or benchmark appears Treasury-like. Verify the documented bond-quality category and structure; when substantial credit exposure exists, using only short-end Treasury rates is incomplete. Small duration does not imply low **KRW** drawdown if unhedged currency or credit risk is material.

### 7.5 Legacy Example H — market-only bull steepening calculation

| Treasury tenor | Earlier | Later | Change |
|---|---:|---:|---:|
| 2Y | 5.20% | 4.40% | −80 bp |
| 10Y | 5.55% | 5.20% | −35 bp |
| 30Y | 5.80% | 5.70% | −10 bp |

`10Y−2Y` slope: `+35 bp → +80 bp` (**+45 bp**). `30Y−10Y` slope: `+25 bp → +50 bp` (**+25 bp**). All three yields fell while both curve segments steepened: **bull steepening of those defined segments**.

With clearly **hypothetical fixed current exposure durations** `1.9/7.5/15.0`, applying each historical-sized yield change gives counterfactual first-order price sensitivities of `+1.52%`, `+2.625%`, and `+1.50%`. These are **not historical ETF total returns** and cannot by themselves justify a forward-looking preference for 10Y.

### 7.6 Legacy Example I — ETF-price performance is an excluded selection input

If market 10Y yields are nearly unchanged while a Korean-listed unhedged 10Y ETF has a large negative **distribution-adjusted** KRW total return and USD/KRW declined sharply, FX is a plausible reconciliation factor. This is a **diagnostic/performance question**; it must never override market observations or update ETF-selection inputs by inferring hidden rate-duration from price returns. Distinguish ex-distribution raw prices from genuine total returns. Any unexplained residual should be flagged, not force-fit.

### 7.7 Legacy Example J — poor or missing issuer data

An active long Treasury ETF has a published headline yield but no trustworthy portfolio duration, defensible comparable hedged carry, or required supporting data. It may still appear in the universe and display relevant bond-market context; precise duration stress, carry break-even or unequivocal relative preference is **unavailable**. A clearly labeled benchmark-duration proxy may support limited illustration if compatible; a prohibited leveraged structure can be rejected on an explicitly stated policy without inventing missing numerical values.

---

## 8. Validation contract and arithmetic fixtures

### 8.1 Hand-checkable reference calculations

| ID | Fixture | Expected result | Status/meaning |
|---|---|---:|---|
| V1 | Duration 8; +50 bp Treasury shock | −4.00% | First-order price sensitivity |
| V2 | Same, compatible convexity 80 | −3.90% | Second-order price sensitivity |
| V3 | Spread duration 6; +100 bp OAS, no Treasury move | −6.00% | Spread-only price sensitivity |
| V4 | Unhedged USD result −2%; USD/KRW +8% | +5.84% | FX accounting identity, not a forecast |
| V5 | 2Y 4.0%, 10Y 4.5% | +50 bp | Treasury 2s10s slope |
| V6 | 2s10s −10 bp → +100 bp | +110 bp | Historical slope change |
| V7 | Apr 10Y vs 2Y market-reference break-even | −1.785714 bp | Gross duration-normalized proxy |
| V8 | Oct 10Y vs 2Y one-year market-reference break-even | +17.857143 bp | Gross duration-normalized proxy |
| V8a | Same October data, six-month linearly prorated compensation | +0.500000 pp; +8.928571 bp break-even | Aligned with Section 3 six-month risk windows; not true ETF carry |
| V9 | Oct 30Y vs 10Y market-reference break-even | +3.529412 bp | Gross duration-normalized proxy |
| V10 | IG rates +15 bp, `D_rates=5.5` | −0.825% | Treasury-rate contribution |
| V11 | IG OAS +35 bp, `D_spread=5` | −1.750% | Credit-spread contribution |
| V12 | IG total first-order sensitivity | −2.575% | V10 + V11, **not** realized return |
| V13 | Example A illustrative carry-plus-stress | −13.00% | Policy fixture only |
| V14 | Example B illustrative carry-plus-stress | −9.50% | Policy fixture only |
| V15 | Example C intermediate/long stresses | −4.00% / −11.80% | Policy fixture only |
| V16 | Example F HY rates/spread effect | −4.40% | Price-only credit fixture |
| V17 | Example H slope changes | +45 bp / +25 bp | Defined curve endpoints |
| V18 | Example H three current-exposure effects | +1.52% / +2.625% / +1.50% | Counterfactual price-only effects |

For simple floating-point computations, define and report a numeric tolerance, e.g. `1e−10` in **decimal return units** for elementary synthetic formula fixtures. This is a **test tolerance**, not a credible tolerance for real ETF approximations, source dates or economic estimation errors.

### 8.2 Behavioral checks

1. The **same** market inputs, issuer characteristics, formula assumptions and cutoff yield the same calculation in individual, historical and universe views; visualization does not determine the numeric output.
2. All market yield and spread units convert correctly to decimal inputs and bp outputs; all reference periods and information cutoffs are consistent.
3. Duration comes from published ETF exposure for a product analysis, or from an **explicitly defined benchmark exposure** for market-reference studies; `10Y` is never treated as duration `10`.
4. Yield-curve slope and duration-normalized break-even have interpretable relationships but **do not count as two independent confirmations** of attractiveness.
5. **Full-period** compensation histories use yields at each dated assessment, not rolling yield differences. A fixed duration and a fixed +50 bp scenario produce **no changing sensitivity line**.
6. Yield-change variability uses **joint, horizon-matched and dated** observations; historical six-month relative losses are compared only to six-month compensation assumptions. Daily rolling windows overlap substantially, and their observed frequency is not a future probability.
7. Pure Treasury OAS is `not_applicable`; missing applicable issuer yield is `unavailable`; structurally invalid futures cash carry is `unsupported`; a benchmark approximation is marked `proxy`.
8. A widening corporate OAS is distinguished from movements in Treasury yields and is described as **credit-specific repricing, not proved fundamental distress**.
9. Spread compensation without modeled default/migration loss is **gross**, not an expected net credit return or an unconditional buy signal.
10. Historical ETF total returns and NAV prices can appear in separate diagnostics **but must not determine ETF attractiveness**, weight coefficients, or substitute unpublished duration.
11. A common scenario may apply to several ETFs, but comparisons of issuer yields, KRW compensation, futures carry and credit risk are suppressed or qualified when definitions differ.
12. Synthetic `P-RISK12`-style risk-policy results are **conditional fixtures only**; no automatic adoption of the arbitrary 10% threshold or an unconditional buy/sell label.
13. A model improvement (convexity or KRD) can affect a justified calculation if its inputs are compatible, with baseline results still reproducible and the additional value explained.
14. Completing these tests does **not** establish that the system can outperform markets or that an optimal investment timing rule exists.

### 8.3 Reproducible visualization data and expected interpretations

| Figure or dataset | Required economic interpretation | Forbidden implication |
|---|---|---|
| `maturity_break_even_history.png` | Extra long-duration yield compensation **relative to extra duration** changed throughout the period | A universal 30Y buy/sell recommendation |
| `relative_rate_risk_evolution.png` and `relative_rate_risk_context.png` | The same daily six-month relative-rate observations display their evolution and distribution | A forecast of probabilities or realized ETF relative performance |
| `treasury_vs_credit_contributions.png` | Rates and credit spreads contributed differently to the price-only scenario | An explanation of actual ETF returns or proof of corporate default deterioration |
| The daily Treasury and rolling-risk CSV files, plus the monthly credit-reference CSV in `assets/` | Reproducible constructed market inputs, rate-risk comparisons and credit illustration | Verified live market data or issuer facts |

A plot that only reproduces an existing yield table, a fixed +50 bp sensitivity line under constant duration, or multiple parallel scenario lines differing only in intercept should not be counted as independent economic evidence. The companion figures demonstrate **distinct questions** rather than specify mandatory chart layouts for production.

---

## 9. Remaining research questions and handoff boundaries

- Can dated published yield conventions and published ETF durations support **actual ETF-level** compensation-versus-risk comparisons, or must the first result remain a **market-reference** comparison with qualified ETF translation?
- How reliable is historical yield-change variability for providing context about relative break-even cushions when sample windows overlap and the curve changes nonparallelly?
- For IG/HY categories, does an available OAS series match the issuer's credit exposures sufficiently to support interpretation, and which fundamental credit-risk evidence would be required to conclude that widening spreads are adequately compensated?
- Which additional conventional analyses—carry/roll, term premium, convexity, key-rate durations—add independent or decisively more useful information than simpler baselines?
- Which user policy and investment horizon, if any, are needed to go beyond an aspect-level observation to an ETF-level purchase preference? The hypothetical `10%` loss threshold is **not** an accepted universal rule.
- How should cross-currency issuer yields be compared, if at all, before proper hedge-cost inputs exist? FX remains a lower-priority research topic.

**Next action is design review, not automatic execution.** A separate approved Bernie assignment may later test real accessible issuer and market data, reproduce the numerical cases, and report which comparisons are supported or unsupported. After independent quantitative review and user assessment, update the architecture and any later development roadmap. Nothing in this document authorizes such execution on its own.

## 10. Source context and prior example preservation

The older examples were constructed examples, not a validated backtest. Original cases **A–J** are preserved by purpose as follows: A/B/C → Section 6, D/E/F/G/H/I/J → Section 7. New time-series maturity and credit cases are Sections 2–5, with chart-level regression rules in Section 8. Earlier historical ETF tickers are illustrative identification references, not required current-universe members. Product identity and disclosures must be verified before any genuine assessment.

Suggested fixed-income references: [CFA Institute — Fixed-Income Portfolio Management](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/overview-fixed-income-portfolio-management); [Yield Curve Strategies](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-curve-strategies); [Convexity and Portfolio Properties](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-based-bond-convexity-and-portfolio-properties). Market-series identifiers used in real research can be sourced from [FRED](https://fred.stlouisfed.org/); this document did not retrieve or verify actual observations.
