# Korean-Listed U.S. Bond ETF Decision Support — Design Examples and Review

**Status:** Companion research examples, v1, internally reviewed against [`bond_etf_decision_architecture_v1.md`](bond_etf_decision_architecture_v1.md), 2026-10-13.

**IMPORTANT: EVERY MARKET VALUE, DURATION, CARRY, RETURN, POLICY, AND OUTPUT BELOW IS A HYPOTHETICAL TEST FIXTURE — NOT A LIVE ETF ASSESSMENT.** Product names/tickers and broad structural roles were checked using sources, but all numerical market/exposure values below are fabricated for reasoning and eventual synthetic tests. No market backtest or live assessment has been performed. The eventual MVP must agree when fed **these exact synthetic inputs**, not necessarily when fed real data.

## 1. What these examples are meant to prove

The examples are **executable-in-principle behavioral requirements**, not marketing narratives. Each has a concrete question, constructed inputs, conventional calculations (or an explicit unavailable-measure branch), and expected output type. They deliberately include cases that overturn simplistic rules such as `rising yields → always avoid long bonds` or `unhedged ETF recently won → always buy unhedged`.

The intended output is an economically defensible *decision conditioned on a stated objective*. It need not score the same four aspects separately, combine scores, or predict ETF returns. Aspect-level market explanation is independently available.

### 1.1 Fixed research configuration

- Base currency: KRW; unless stated otherwise, example mandate is `P-RISK12`: new purchase, 12-month assessment, accepts currency-hedged Treasury exposures, excludes leverage, and uses a **10%** maximum modeled loss under **hypothetical +100 bp parallel Treasury shock** after an *explicitly supplied hypothetical net 12-month carry proxy*. This is a risk-policy stress fixture, **not a 100 bp yield forecast** or an optimization result.
- `net_carry_12m` is an assumed period-consistent modeled component, **not** ETF dividend yield, SEC yield, future return, or actual distribution. For a real ETF, it must be derived from supportable published yield/hedging/fee assumptions; otherwise remove carry from quantitative stress and downgrade the conclusion.
- Use conventional first-order `R_stress = net_carry_12m - D * 0.01` **only where a cash-bond exposure and net carry proxy are supportable**. Convexity is deliberately omitted from these minimal arithmetic fixtures and must be flagged for long-duration instruments; a production analysis should include convexity where usable.
- Treasury trend display: five-observation endpoint average, 126-observation and 21-observation lags; bp changes are observed/hypothetical *past movements*. No Trend/Recent Move state, ±25 bp/±10 bp classification, hysteresis, or arbitrary weighted sum.
- Results: `consider_purchase`, `conditional`, `defer_new_purchase`, `not_suitable_under_policy`, or `insufficient_information`. Screen failure can justify defer; screen passing is **not a sufficient buy signal**. A favorable/nonfavorable relative comparison uses the same policy and comparable economic exposures.
- If alternative ETF selection is requested, and the only reason for choosing is an assumed FX direction, **do not** declare a winner without the investor's FX objective. A descriptive realized FX attribution cannot be smuggled into an FX forecast.

### 1.2 Representative real products (identification only)

| Ticker | ETF | Structural reason for inclusion | Reference |
|---|---|---|---|
| `0085N0` | ACE 미국10년국채액티브(H) | 7–10Y-oriented, currency-hedged active Treasury profile | [ACE official product series](https://www.aceetf.co.kr/info/report/1160) |
| `0085P0` | ACE 미국10년국채액티브 | Comparable unhedged Treasury profile | [ACE official distribution notice](https://www.aceetf.co.kr/cs/notice/7002) |
| `453850` | ACE 미국30년국채액티브(H) | Long Treasury sensitivity; currency-hedged | [ACE official notice](https://www.aceetf.co.kr/cs/notice/7002) |
| `476760` | ACE 미국30년국채액티브 | Long Treasury sensitivity; unhedged | [ACE official notice](https://www.aceetf.co.kr/cs/notice/7002) |
| `308620` | KODEX 미국10년국채선물 | **Futures**, not physical 10Y Treasury ETF | [KODEX official naming notice](https://www.samsungfund.com/etf/lounge/notice-view.do?no=58734) |
| `455660` | ACE 미국하이일드액티브(H) | HY credit, requires spread/default framework | [KRX issuer listing](https://kind.krx.co.kr/disclosure/etfisudetail.do?method=searchEtfIsuSummary&strIsurCd=45566) |
| `440650` | ACE 미국달러단기채권액티브 | Short-duration USD bonds with **credit-mixed holdings**, not pure Treasury | [Fund overview and holdings sample](https://www.funetf.co.kr/product/etf/view/KR7440650000) |

**Avoid a misleading pairing:** `440650` is not assumed to be the pure Treasury equivalent of `0085N0` merely because its name includes “short bonds.” The observed holdings and the index label can differ materially in credit exposure. `308620` cannot use cash-bond carry formulas simply because “10Y” appears in its name.

---

## 2. Example A — Same long-duration ETF: adverse conditions and modest compensation

**Decision question.** With current economic conditions and the defined `P-RISK12` investor loss budget, is a new purchase of `453850` reasonable? No shorter-maturity comparison is required.

**Hypothetical input snapshot A:**

| Variable | Constructed value |
|---|---:|
| Market 30Y Treasury yield | 4.80% |
| 6M / 1M 30Y yield movement | +70 bp / +20 bp |
| ETF effective duration proxy | 17.0 |
| Modeled 12M **KRW-hedged net carry** | 4.00% |
| KRW cash comparison for 12M | 3.80% |
| Standard adverse rate scenario | +100 bp |
| Allowed scenario loss | 10.00% |

**Calculations (first order):** `rate_effect = -17 × 0.01 = -17.00%`; `illustrative_12m_stress = 4.00% - 17.00% = -13.00%`; cash-relative net compensation under the assumed unchanged market conditions = `+0.20 percentage points`. Historical `+70/+20bp` is descriptive, not inserted again into the forward scenario.

**Expected output:** `defer_new_purchase` for **this specific risk policy**: modeled adverse loss exceeds the investor's 10% budget; small cash-relative compensation offers limited cushion. The upward rate movement reinforces awareness of the current exposure, but **must not be represented as a forecast of further rises** and is not the sole decision cause. A high-duration mandate with a larger loss budget may reach a different conclusion. Convexity omission is a confidence qualification.

**Underlying-market explanation:** 30Y yields rose over both the 6M and 1M observation periods; the exposure has substantial sensitivity to an adverse yield shock.

**Regression invariant:** Do not convert this result into `sell existing holdings`; the holding decision needs separate portfolio context.

## 3. Example B — Same long-duration ETF: different compensation changes the decision

**Same real ticker:** `453850`. A wholly separate, hypothetical market snapshot, not a dated real observation or proof that yields will fall.

| Variable | Constructed value |
|---|---:|
| Market 30Y Treasury yield | 6.00% |
| 6M / 1M 30Y yield movement | +80 bp / 0 bp |
| Current effective duration proxy | 14.5 |
| Modeled 12M **KRW-hedged net carry** | 5.00% |
| KRW cash comparison for 12M | 3.00% |
| Standard adverse rate scenario | +100 bp |
| Allowed scenario loss | 10.00% |

**Calculations:** `rate_effect = -14.5%`; `illustrative_12m_stress = 5.00% - 14.50% = -9.50%`; net compensation above the assumed cash alternative = `+2.00 percentage points`. Duration proxy changes between A and B because yield level and/or portfolio composition may differ; an actual ETF snapshot must supply this rather than assuming it.

**Expected output:** `consider_purchase` **subject to checking actual carry/hedge terms, convexity, and exposure suitability**. The loss-budget test now passes and the cash-relative compensation is stronger. The six-month yield history remains upward; **the architecture must not automatically veto the purchase because of that trend**, nor declare this an unconditional buy or predict a reversal.

**Design challenge passed if:** The same ETF produces a more favorable new-purchase assessment in B than A *without introducing a mean-reversion forecast or a hidden Trend-first Rule Table*. If actual net carry is unverifiable, the result should change to `conditional/insufficient_information` instead of manufacturing the displayed 5%.

## 4. Example C — Intermediate-duration Treasury against long duration

**Products:** `0085N0` (hedged 10Y-oriented) vs `453850` (hedged 20Y+-oriented). Assume their profiles and carry are contemporaneously sourced. This is a *separate* hypothetical snapshot and is not numerically intended to coexist with Examples A and B.

| Property | 10Y-oriented `0085N0` | Long `453850` |
|---|---:|---:|
| Relevant observed 6M yield change | +50 bp | +65 bp |
| Recent 1M yield change | -15 bp | +10 bp |
| Illustrative current effective duration | 7.5 | 16.0 |
| Assumed 12M KRW net carry | 3.50% | 4.20% |
| Rate effect for +100bp | -7.50% | -16.00% |
| 12M illustrative stressed result | -4.00% | -11.80% |
| `P-RISK12` loss-budget test | Pass | Fail |

**Expected output:** For the *defined* 12M risk-controlled new allocation, `0085N0` is **more suitable**; `453850` is `defer_new_purchase` under the same stress budget. The 10Y ETF is still only `conditional` or `consider_purchase`: a passing risk test alone does not create a reason to invest rather than holding cash. Mention that 10Y recent yield relief and long-end persistence differ, **without assigning probabilities to future moves**.

**Decision must remain conditional on mandate:** For a portfolio requiring high-duration crisis sensitivity or longer liability hedging, the relative preference can reverse; that is a different, declared objective rather than a contradiction.

## 5. Example D — Same Treasury market exposure, different currency structures

**Products:** `0085N0` (hedged) vs `0085P0` (unhedged). Input is an explicitly **hypothetical realized return window**, used to verify actual-return decomposition; this is not a future return scenario.

| Input | Hypothetical historical value |
|---|---:|
| Comparable underlying USD Treasury-bond total return | -2.00% |
| USD/KRW spot change (KRW per USD) | +8.00% |
| Unhedged ETF's idealized KRW return | `(0.98 × 1.08 - 1) × 100 = +5.84%` |
| Hedged ETF realized total return for fixture | -2.70% |
| Assumed hedged residual relative to local return | -0.70 percentage points |

The -0.70 pp is **not proved to be hedge cost**: it may combine forward points, hedge slippage, fees and ETF implementation differences. No exact hedge effect is inferred from spot alone.

**Expected output:** explain how an unhedged ETF can rise in KRW despite a negative local USD bond return; explain why the hedged ETF differs. For a user whose mandate explicitly avoids USD/KRW risk, prefer `0085N0` *despite* its weaker historical window. For a user intentionally seeking USD exposure, `0085P0` can be appropriate. Without a currency objective, report `no universal preference` rather than extrapolating the +8% FX move.

**Architecture fails if:** It calls the unhedged version the superior bond exposure solely because its recent KRW ETF price outperformed, or treats `(H)` as perfect hedging at zero cost.

## 6. Example E — Futures ETF must be routed differently

**Product:** `308620`, KODEX 미국10년국채선물, officially renamed in 2024.

**Hypothetical situation:** DGS10 rose 40bp over six months. A market-only report correctly describes unfavorable historical direction for a long Treasury-futures exposure. But the ETF uses a Treasury futures index, not a static basket of 10Y coupon-paying bonds. For this fixture, the exact futures DV01, collateral yield, roll mechanics and index currency treatment have **not** been supplied.

**Expected output:** Market trend is available; product type is verified; numeric cash-bond `yield-to-maturity/carry/roll` projection is `not assessed`, and precise bond-equivalent stress is `insufficient_information` until an appropriate futures exposure measure exists. A *qualitative* rate-risk assessment remains available. The system may give a conditional suitability result if the mandate accepts futures, but cannot manufacture a total-return forecast or mark missing cash carry as zero.

**Architecture fails if:** It simply reads “10Y” in the fund name, sets duration to 10 and applies the same cash-bond yield-plus-roll equation as `0085N0`.

## 7. Example F — Treasury yields falling but high-yield spreads widening

**Product:** `455660`, ACE 미국하이일드액티브(H). A speculative-grade credit profile, not a Treasury-only instrument.

**Hypothetical contemporaneous observed changes:** representative Treasury rate -40bp; HY OAS +150bp; assumed `D_rates=4.0`, `D_spread=4.0` for illustrating economic sensitivities only.

**First-order contributions:** rates: `-4.0 × (-0.0040) = +1.60%`; spread repricing: `-4.0 × (+0.0150) = -6.00%`; combined **price-only** effect `≈ -4.40%`. No realized HY ETF return, default estimate, convexity or income is claimed.

**Expected output:** `Treasury rates helped, credit spread deterioration dominated the price-only shock`. Do not label the ETF favorably based solely on declining Treasury yields or its high indicated distribution yield. Under `P-RISK12`'s non-speculative mandate, output `not_suitable_under_policy`. Under a declared high-yield income mandate, compute separate credit-stress/compensation scenarios before any purchase judgment; it can be `conditional` rather than uniformly avoided.

**Architecture fails if:** Treasury and spread movements are both counted as one rates factor, or if coupon/distribution yield is equated with credit risk-adjusted attractiveness.

## 8. Example G — A short USD bond ETF is not automatically a short Treasury ETF

**Product:** `440650`, ACE 미국달러단기채권액티브.

Its product description and observed holdings sample include short USD-denominated credit bonds, including non-Treasury issuers; the benchmark label alone is insufficient to identify pure Treasury risk.

**Expected output:** classify its **documented economic exposure** as short-duration USD **credit-mixed** unless verified new issuer documents show otherwise. Report Treasury short-end conditions as relevant background, add a credit-spread/credit-quality warning or analysis if matching data are available, and retain its unhedged USD/KRW exposure. If effective duration/credit sensitivity is unavailable, provide partial interpretation and mark precision limitations.

**Architecture fails if:** It uses FRED DGS6MO as a complete explanatory model, equates short maturity with a KRW money-market fund, or guarantees low KRW drawdown merely because rate duration is small.

## 9. Example H — Market-only yield-curve analysis, with optional exposure implications

No ETF is required to produce this report.

**Two hypothetical market snapshots (Treasury yields):**

| Tenor | Six months ago | Current | Change |
|---|---:|---:|---:|
| 2Y | 5.20% | 4.40% | -80 bp |
| 10Y | 5.55% | 5.20% | -35 bp |
| 30Y | 5.80% | 5.70% | -10 bp |

- 2Y–10Y slope: old `35bp`, current `80bp`, change **+45bp**.
- 10Y–30Y slope: old `25bp`, current `50bp`, change **+25bp**.
- All three yields fell while the two slope measures steepened: **bull steepening in both specified curve segments**.

Optional *current-exposure sensitivities to these historical-sized moves* using hypothetical durations 1.9, 7.5 and 15.0: rate price effects `+1.52%`, `+2.625%` and `+1.50%`, respectively. These are **not actual historical ETF returns and not forecasts**. Because tenor-specific moves differ, they give useful relative exposure implications without requiring a Curve Rule Table.

**Expected output:** explain market condition and how the move relates to maturity-specific rate sensitivity; do not automatically claim that 10Y exposure is more attractive going forward because its illustrative historical price sensitivity is largest. A purchase decision must also consider current compensation, investor risk tolerance, and actual product type.

## 10. Example I — Instrument performance contradicts an oversimplified market explanation

**Hypothetical observation:** 10Y yields are stable and a 10Y-oriented unhedged Korean ETF exhibits a large negative KRW adjusted total return. USD/KRW fell sharply (USD weakened against KRW), and the fund's NAV follows its underlying USD bond performance adjusted for currency reasonably closely.

**Expected output:** identify currency as the dominant candidate explanation, quantify it if FX/NAV inputs permit, and **do not** conclude that its bond holdings suddenly experienced large adverse Treasury-rate movement. If FX does not reconcile the residual, flag other factors (benchmark, distribution adjustment, premiums, fees, futures/active deviation) rather than forcing a false explanation.

**Architecture fails if:** It uses falling ETF price as sufficient evidence of rising Treasury yields or allows the price move to override FRED market observations.

## 11. Example J — Missing/poor data must alter the conclusion

**Hypothetical:** long active Treasury ETF current headline yield is known but no defensible effective duration, convexity, hedged KRW carry or adjusted NAV history exists. Current FRED 30Y yield trends are available.

**Expected output:** produce the **market-only** directional report; state the ETF is designed for the long Treasury market; use a *declared provisional proxy range* for qualitative rate sensitivity if economically justifiable, but **do not** output a precise +100bp scenario return, break-even shock or definite buy recommendation. `insufficient_information` is permitted for the policy decision. A user-supplied mandate can still reject a product with known prohibited leverage/credit characteristics without missing sensitivity estimates.

This is not a general excuse to abandon evaluation: it is an explicit boundary for *unsupported numerical precision*.

---

## 12. Architecture-to-examples feedback review

The first draft assumptions were challenged by the examples and the architecture was revised accordingly. This is the first feedback loop **completed in this deliverable**, not a claim of real market validation.

| Example challenged | Defect found in initial architecture concept | Accepted repair in companion architecture | Rechecked expected behavior |
|---|---|---|---|
| A and B | Rising yields could become an unconditional long-duration veto | Risk-budget, cash-relative compensation and investment objective precede a trend-based veto | Same ETF can be deferred under A, considered under B |
| C | Passing a rate-risk screen might be mislabeled an unconditional buy | Explicit distinction between eligibility and affirmative purchase rationale | Intermediate more *suitable* under policy, but purchase conditional |
| D and I | ETF prices might be treated as an independent Treasury-yield trend signal | FRED determines rate conditions; total-return/FX is an explanatory reconciliation | FX attribution without duplicate signal or FX forecast |
| E | One universal bond-return formula would mis-handle futures | Route derivative exposures to appropriate model; show not assessed if no DV01/collateral | 308620 does not get fabricated cash-bond carry |
| F and G | All USD bond ETFs would be routed through pure Treasury evaluation | Credit spread and issuer-quality branch, classification by verified exposure | HY and short USD mixed-credit funds are not treated as Treasuries |
| H | A market-only report would need a fictitious ETF as a consumer | Market interpretation is directly exposed | Bull steepening defined and quantified without an ETF |
| J | Missing input would silently become generic duration or zero effect | Explicit proxy confidence, unavailable values and incomplete-output behavior | No spurious precise buy conclusion |

### Checks to run during MVP implementation

- Synthetic arithmetic: `A=-13.00%`, `B=-9.50%`, `C_10Y=-4.00%`, `C_long=-11.80%`, `D_unhedged=+5.84%`, `F_price_only=-4.40%`, `H_slopes_change=+45bp/+25bp`, `H_rate_sens=+1.52%/+2.625%/+1.50%`.
- For A/B, verify changes in investment *policy* alter suitability without changing observed yields, and hypothetical changes in yields/compensation do not require a future-yield forecast.
- For C, ensure the same stress and numeraire are used; do not implicitly introduce a weighting across separate scores.
- For D/I, ensure adjusted ETF prices and correct USD/KRW quotation direction; no false attribution from ex-distribution prices.
- For E/G, ensure unavailable or structurally incompatible calculations are excluded rather than defaulted to zero.
- For F, calculate rates and OAS effects separately and retain a default/credit-risk caveat.
- For H, verify slopes from yields **before** attaching steepening labels; no forward-looking claim from historical-sized shock sensitivities.
- For all cases, expose what data were assumed, which formulas are established, where approximations enter, and what policy preference drives the decision. No exhaustive lineage or classification database is necessary.

## 13. Remaining open issues for the next review

1. Can issuer-published effective duration, yield conventions, monthly distributions and currency hedge exposures be reliably acquired for representative Korean ETFs without excessive manual work? Verify on real source documents in the MVP.
2. Are approximate 12-month **hedged KRW net carry** inputs credible enough to support a cash-relative stress decision for `453850` and `0085N0`? If not, restrict the first decision to rate sensitivity/fit and show compensation separately; do not keep the same confident labels by assumption.
3. For active portfolios and Treasury futures, when should empirical ETF NAV sensitivity supplement issuer-reported duration? Ensure explanatory regressions are not mistaken for structural holdings-level duration.
4. Which user objective/policy fixture is the appropriate default, and is the output useful under plausible alternatives (income-oriented, duration-seeking, capital preservation)? Test sensitivity to the loss budget before calling the policy broadly useful.
5. Are FX spot, forward-rate/carry proxies and local market closing calendars adequate to explain hedged/unhedged ETF differences? Residuals are acceptable if acknowledged.
6. Corporate spread source access may be limited. Credit model should degrade honestly rather than extend a Treasury-only model to speculative-grade products.
7. Empirical economic usefulness remains unproven by these examples. After the design passes synthetic tests, review historical events and compare decisions with simple duration-only/hold/cash baselines without overstating realized-return conclusions.

## 14. Relationship to MVP

Implement the arithmetic and **behavioral expectations** from §§2–11 first. Execute these exact synthetic fixtures in tests. Then run the same engine on actual FRED series and actual ETF product and return data, honoring data availability and information timing. The real market results **need not have the hypothetical numeric values or purchase labels**; the methods, product routing, policy conditions and ways of qualifying unavailable information must be consistent.

Do **not** modify accepted Bondview-v2 Constituents or copy their ordinal score table to make the challenger look similar. Use Bondview only as an optional benchmark for the narrow questions it already computes.

**Source of example methods:** [CFA fixed-income portfolio overview](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/overview-fixed-income-portfolio-management); [CFA yield-curve strategies](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-curve-strategies). The financial identities are established; the particular investor budget, stress magnitude, carried-value fixture and behavioral outputs are explicitly hypothetical choices.
