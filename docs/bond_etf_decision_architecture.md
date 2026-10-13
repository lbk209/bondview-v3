# Korean-Listed U.S. Bond ETF Decision Support — System Architecture

**Status:** Research architecture, v1; refined through an architecture → examples → review → architecture feedback loop on 2026-10-13. **Not a Bondview-v2 design amendment.**

**Companion:** [`bond_etf_decision_examples_v1.md`](bond_etf_decision_examples_v1.md). The examples are a design contract, not observations or a backtest.

## 1. Purpose and decision contract

Build a usable **investment decision-support system for Korean-listed U.S. bond ETFs**. At an observation date, it should answer: (a) is a *new purchase of this ETF* reasonable for a specified investment objective and risk capacity under present conditions? (b) how does its economic exposure compare with relevant alternatives? (c) if already owned, what changed enough to justify reviewing or resizing the holding? (d) what are the important underlying bond-market conditions?

The system's contribution is **more informed, risk-aware selection than an unstructured ETF choice**. It need not forecast the direction or level of future yields, ETF prices, or realized returns, maximize an arbitrary attractiveness function, produce universal rankings, or guarantee superior realized results. Describing a yield trend, a rate sensitivity, and scenario implications is not a yield forecast. Likewise, a conditional preference under explicit risk/compensation assumptions is not a return forecast.

**The default assessment is relative to the same ETF in its own present and historical market environments, not necessarily relative to another ETF.** Cross-ETF comparisons are an additional capability, not a prerequisite for assessing purchase suitability. Do not conflate new-purchase suitability, holding suitability, sale timing, or realized performance.

This architecture is intentionally detailed enough to guide implementation. It may later be split into architecture, model specification, data contracts, and investment-policy documents.

### 1.1 Non-goals

- An exchange execution engine, intraday order optimizer, fully personalized financial planner, or guaranteed timing model.
- A compulsory four-Constituent model, categorical State Classification, Rule Table, generic weighted sum, or integrated numerical attractiveness score.
- Rebuilding individual Treasury security histories from every coupon and issuance date merely to evaluate a maturity segment.
- Treating ETF prices as a substitute for underlying U.S. bond-market observations.
- Inferring that historically high yields **must** decline or that a rate trend will persist.

## 2. Model-first design commitments

1. **Start with the ETF decision question**, then use an established quantitative relationship that materially helps answer it. No mandatory Component/State/Evaluation architecture. If a calculated measure does not change the decision or its economically useful explanation, it need not be included.
2. **Separate measured quantities, standardized scenario results, and investment policy.** Use exact formulas where defensible; use approximate exposures and declared scenario conventions when exact data are unavailable. Label them; do not turn policy assumptions into claimed financial laws.
3. **Prefer continuous quantities.** Preserve yields, bp changes, effective durations, spread durations, carry estimates, scenario P&L, FX contribution, and total-return series. Classify only if a label actually improves use. No thresholds solely to produce a neat score.
4. **No automatic double vote for one mechanism.** A falling ETF price and rising Treasury yields may be manifestations of the same rate shock. ETF price history helps reconcile and monitor the instrument; it does not automatically contribute a second negative judgment on rate direction.
5. **An exposure-relative decision is conditional on its job.** A high-duration hedge and a 12-month capital-preservation allocation can reach different recommendations from the same data. This is appropriate, not an inconsistency.
6. **A missing input must not be silently filled by an unrelated proxy.** Proxy use is allowed with a visible confidence downgrade; unsupported modules should say `not assessed` rather than invent zero impact or a neutral score.
7. **A negative conclusion need not mean sell.** Purchase, ongoing holding, and execution involve different objectives, taxes, costs, and position constraints.
8. **Reuse empirical conventions for research comparability, not as axioms.** In the first MVP, inspect 126 accepted observations (~6 months) and 21 (~1 month), with a 5-observation end-point mean, matching the earlier Bondview Duration study. Those are chosen research defaults, not established optimal horizons. A robustness view without smoothing and with other windows is optional.

## 3. Inputs and boundaries

### 3.1 Market observations (independent of any ETF)

| Inputs | Initial sources | Why needed |
|---|---|---|
| U.S. Treasury constant-maturity yields | FRED H.15: `DGS3MO`, `DGS6MO`, `DGS2`, `DGS5`, `DGS10`, `DGS20`, `DGS30` | Nominal rates; level and tenor-specific movements; slope/curvature; standardized yield-shock analysis |
| USD/KRW (KRW per USD) | FRED `DEXKOUS`, or documented higher-frequency local FX reference | Currency-related explanations and retrospective decomposition |
| U.S. IG/HY corporate OAS when relevant | Available FRED ICE BofA OAS series, subject to license/history availability | Credit spread level, change and stress; never approximate credit purely from Treasury yields |
| Short-rate / cash reference | User-provided or sourced **KRW** cash yield, or explicitly a USD cash benchmark if that is the chosen objective | Comparison of compensation in the appropriate numeraire; do not equate U.S. T-bill yield with KRW cash return |
| Optional term-structure / inflation data | FRED zero-coupon curve / TIPS and forward-rate sources if necessary | Enrich valuation interpretation only when used for a meaningful decision |

Treasury yields are **market observations**, not a position's total-return series or a specific issued bond's yield-to-maturity. The 10Y constant-maturity series identifies an approximately 10Y market segment, not a bond with numerical modified duration of exactly 10.

Historical data processing: retrieve/capture source, units, time zone, source date, and retrieval time; preserve missing rows; align observations using only information known at the assessment cutoff; do not forward-fill through market holidays as if observed; explicitly respect known discontinuities (e.g., the DGS30 period); do not mix a later ETF closing price with information not yet released at its timestamp.

For spread data, record licensing and accessible lookback. ICE BofA OAS observations on FRED have historical-access limitations; a three-year restricted series must not be used to claim decades-long percentile conclusions.

### 3.2 ETF-specific characteristics

Only ETF-specific information comes from its **issuer materials, listing disclosures, and actual price/NAV/distribution history**, rather than inventing a parallel holdings database as a prerequisite. Where possible capture: ticker and current official name, benchmark, type (cash bonds, futures, active, high yield, options, leverage), effective/key-rate duration, spread duration, convexity, yield convention, maturity range, currency exposure and hedging, distributions, expense ratio, NAV/iNAV/market price, listing date, and availability as-of date.

- Product names are *not* adequate numerical exposure estimates. `10Y` may indicate benchmark maturity segment or Treasury futures; it is not automatically modified duration 10.
- An active fund may use multiple underlying ETFs, bonds and/or derivatives. Its official benchmark is a **reference**, not proof that the holdings deliver identical exposure. Prefer official portfolio-level sensitivity if available.
- A futures ETF must not receive ordinary cash-bond yield/carry treatment: futures basis, collateral income, rolls and KRW index conventions differ.
- Currency `(H)` denotes a hedge-oriented structure, not a perfect hedge. Obtain the issuer's actual policy where possible.
- For performance, use distribution-reinvested adjusted NAV/total-return histories, not raw ex-distribution closing prices. Prices plus cash distributions may be reconstructed carefully if adjusted NAV is unavailable; document corporate actions and missing distribution dates.
- Market price vs NAV and spread/liquidity information, if available, contribute to an execution caution, not to a forecast of bond yields.

If effective duration is missing, use an issuer benchmark/index estimate **only when economic matching is credible**. If still unavailable, use illustrative sensitivity ranges and explicitly mark magnitude-based decisions provisional. A generic par bond duration proxy is *not* silently identified with actual ETF sensitivity.

### 3.3 User-policy inputs (not market model parameters)

Minimal initial profile: assessment type (`new_purchase`, `hold_review`, or `comparison`), holding/decision horizon (e.g. 12 months), base currency KRW, whether USD exposure is intentional, acceptable standardized scenario loss, permissible credit quality and derivatives exposure, and comparison cash alternative. Provide an example default profile for demonstrations, but **never treat it as the user's actual investment objectives**.

Missing user constraints can yield a well-founded *conditional* judgment. Do not force a buy/sell recommendation by silently inserting risk preferences. Prefer a minimal few meaningful assumptions to dozens of adjustable numerical knobs.

## 4. Quantitative engine: conventional relationships, not mandatory Constituents

All reported numeric results have `value`, `unit`, `source`, `as_of`, `method`, `assumptions`, and `coverage/quality` where pertinent. Calculations operate on the actual exposure's available representation; there is no universal requirement to calculate every row for every ETF.

### 4.1 Observed U.S. Treasury conditions and curve

- Endpoint average: `M5_n(t) = mean of last 5 accepted yields` for tenor `n`.
- Six-month yield movement: `delta_y_6m,n = M5_n(t) - M5_n(t-126)`.
- One-month movement: `delta_y_1m,n = M5_n(t) - M5_n(t-21)`.
- Slopes, in bp: `s_2_10 = y_10 - y_2`; `s_10_30 = y_30 - y_10`; curvature can be shown via a transparent 2Y/10Y/30Y second difference, with equal-spacing caveat, or preferably an established term-structure factor fit later.
- Curve movement labels (`bull steepening`, `bear flattening`, etc.) **must name endpoints and direction of both relevant yields**; do not infer an absolute ETF buying judgment from the label.

This market-only view is a first-class output even if no ETF is selected. It may show divergent short- and long-end conditions.

### 4.2 First- and second-order interest-rate sensitivity

For a cash-bond/benchmark exposure with compatible effective/modified duration `D` and convexity `C`, and a **declared hypothetical change in the relevant yield** `delta_y` expressed in decimal units:

`rate_price_effect ≈ -D * delta_y + 0.5 * C * (delta_y)^2`

Report duration-only if convexity unavailable, with convexity omission conspicuous for large/long-end shocks. When key-rate durations exist, use `-sum(KRD_k * delta_y_k)` for nonparallel curve scenarios; **do not** sum this and the parallel `-D*delta_y` for the same shock. Total duration is often close to the sum of key-rate durations under consistent definitions.

The use of `-D_current * delta_y_historical` is a **current-exposure sensitivity applied to a historical-sized move**; it is not a reconstruction of historical ETF performance, which requires time-varying duration, coupons, distributions, FX and strategy behavior.

For illustrative scenarios, begin with `{+50bp, +100bp, -50bp}` parallel shocks and one nonparallel curve shock. These are **stress magnitudes, not probability estimates or forecasts**. Stress size and tolerable loss belong to the declared investment policy and stress suite.

### 4.3 Compensation and horizon scenarios

For a defined holding period `H`, cash-bond *scenario* total return is approximately:

`local_total_return_scenario ≈ H_carry + roll_down_if_defensible + rate_price_effect + credit_price_effect - direct_costs_if_not_already_net`

Use a consistent yield/carry convention (e.g. portfolio YTW/income proxies), funding basis, and period. **An ETF's distribution yield is not automatically its economic carry or yield-to-maturity.** A cash-bond ETF that keeps its target duration by reinvesting/rebalancing does not earn the roll-down of a fixed held-to-maturity bond without adjustment. If robust carry/roll information is unavailable, report sensitivity-only and separately show current published yields; do not fabricate a total-return projection.

A *rate break-even shock* (under compatible assumptions, first order, against a cash comparator) is a helpful derived output:

`break_even_rise_bp ≈ 10,000 * (net_carry_plus_roll_H - cash_return_H) / D`

It expresses a **scenario compensation cushion** from Rates Valuation plus Duration, not a fifth assessment dimension or a probability of a yield move. Do not apply this formula to futures products or credit funds without modeling their additional economics.

Compensation may be evaluated against cash, its own history, another tenor, or a risk budget. Clearly name the comparator; a high U.S. nominal yield alone does not establish a high hedged KRW return.

### 4.4 Credit and currency

Credit bonds: first-order nonparallel rate and credit-spread shocks should be distinguished:

`credit_bond_price_effect ≈ -D_rates * delta_y_treasury - D_spread * delta_OAS`

Defaults/recoveries and spread convexity are separate unmodeled risks; a spread is not guaranteed compensation for realized losses. Distinguish issuer/quality exposure from Treasury duration, and do not use generic Treasury-only rankings for high-yield products.

Currency: for an **unhedged, approximately USD-denominated** local return `R_USD`, with spot USD/KRW return `R_FX`, an approximate KRW decomposition is:

`1 + R_KRW ≈ (1 + R_USD)*(1 + R_FX)`

For a hedged fund, use a documented hedge-coverage approximation and forward-point/carry/cost estimate when available, else show a bounded/qualitative residual. **Do not subtract spot FX from a hedged ETF as though the hedge were exact.** Spot history can help explain a realized hedged/unhedged return gap but does not recover its forward hedge mechanics uniquely.

### 4.5 Realized ETF behavior: diagnostic and instrument verification

Track adjusted NAV total-return series, market-price total returns if available, distribution reinvestment and inception coverage. Compare to benchmark/market factors as an *approximate reconciliation*:

`observed_KRW_total_return = explained_rates + explained_credit + explained_FX_and_hedge + carry_and_income + fees_and_tracking + residual`

This is an **attribution bookkeeping representation**, not a claim of exact daily additive decomposition without consistent log or interaction accounting. Keep cross terms/residual explicit and do not double-subtract expenses already reflected in NAV returns.

Possible findings: a hedged fund still experiences residual FX or hedging costs; a futures index return differs materially from an on-the-run cash Treasury approximation; distributions create raw-price drops; a fund's realized sensitivity diverges from its stated benchmark. Explain such differences rather than silently changing the market model to fit ETF performance.

## 5. Decision engine: an explicit, small policy—not a universal score

Decision outputs must be *operational*: `consider_purchase`, `conditional`, `defer_new_purchase`, `not_suitable_under_policy`, `insufficient_information`; for a holding use `maintain_or_review`, `review_size`, `review_mandate` rather than interpreting `defer purchase` as an automatic `sell`. Each result cites the dominant quantitative evidence and the decisive **user-policy assumption**. No global rank is required when exposures serve different mandates or there is no clear dominance.

### 5.1 Order of reasoning

1. **Match the mandate and product mechanics.** Is this ETF a plausible way to obtain the intended exposure (Treasury/corporate, maturity, hedge, leverage, futures/active constraints)? An incompatible product cannot be rescued by yield alone.
2. **Establish the market and economic exposure.** Treasury tenor yields, curve movement, rate sensitivity; spreads and FX where applicable. Preserve quantitative magnitudes and distinguish market observations from ETF-specific realized behavior.
3. **Calculate comparable risk/compensation scenarios.** Use the same declared stress for competing exposures when meaningful, relevant duration/spread sensitivities, feasible carry estimates, KRW numeraire and cash alternatives. Scenarios are not likelihood-weighted forecasts.
4. **Apply policy priorities, not arbitrary weighted scores.** For a risk-controlled purchase, test mandate and loss tolerance before preferring extra yield; for deliberate long-duration diversification, the legitimate objective may be maintaining duration exposure despite stress. A current unfavorable rate trend is **context**, not an unconditional rejection rule.
5. **Check actual ETF behavior and implementation.** Distribution-adjusted total returns and mismatch with modeled exposure, fee and hedge/roll differences, known price-NAV gaps. Never treat historical ETF and Treasury movements as independent votes on the same factor.
6. **Return a reasoned decision or unresolved trade-off.** Use `conditional` when policy-relevant information is genuinely absent, not to avoid reasonable judgment. Include the rejected alternative (when comparison requested) and the assumption that would change the decision.

**No intrinsic necessity for a mathematical integrated attractiveness scalar.** The unified inputs and scenario relationships can yield an overall ETF decision without assigning scores to Duration, Curve, Credit, or Valuation. Underlying aspect analysis remains accessible as a first-class market report.

### 5.2 Example policy fixture (for documents/tests only)

`P-RISK12`: KRW investor; 12-month assessment horizon; comparison with **assumed, not observed** KRW cash return; hedged Treasury exposure permitted; no leverage/complex options; baseline willingness to withstand at most a **10% modeled 12-month scenario loss** from a declared adverse parallel +100bp shock *inclusive of a defensible net carry proxy when available*. Credit requires an explicit additional spread stress and permission to take speculative-grade credit risk. This is an illustrative investment policy—not an empirical optimum, price forecast, or default suitable for every user.

The **10%** here is an investor loss budget, not a market classification threshold. A model can be run with another budget without retuning market Components. If net carry is unavailable, a duration-only stress can serve as a conservative risk flag, but may not be falsely reported as a complete total-return scenario.

The risk budget is a **necessary screening condition, not a sufficient condition for purchase**. A new purchase also needs a recognizable investment rationale (income, rate exposure, diversification, cash-relative compensation) and product/hedge fit. In particular, past rising rates plus a passing risk test does not establish a positive expected return.

## 6. Result contract and user-facing examples

Produce the following, as supported by inputs:

1. **Market snapshot** — observed levels, 1M/6M movements, slope/curve changes, credit OAS and FX where relevant, measurement dates, and economically plain descriptions.
2. **ETF exposure and qualification** — verified product type, tenor or risk segment, duration/source/quality, credit exposure, currency policy, active/futures/cash-bond flags.
3. **Quantitative assessment** — duration and/or spread stresses (parallel and curve), carry/cash comparisons where valid, FX bridge for currency pair, and observed ETF total returns with residual attribution warnings.
4. **Practical output** — policy-conditioned purchase suitability; optional comparative preference; holding-review opinion if separately requested; primary evidence and assumption that would overturn the conclusion. `No clear preference` and `no purchase` are valid outputs.
5. **Supplementary aspect view** — Duration, Curve, Credit and compensation conditions when relevant; neither four fixed scores nor full Bondview-style lineage/classification is necessary.

Numerical data must be identified as observed, derived, assumed, or missing; comparisons must use the same relevant cutoff and numerator/denominator definitions. Any example output without real inputs must prominently say **hypothetical fixture**.

## 7. Representative product coverage and routing

The companion examples exercise these verified Korean-listed products; current terms/durations must be rechecked against issuer documents at implementation time:

| Symbol | Product (as of research) | Role and model routing |
|---|---|---|
| `0085N0` | ACE 미국10년국채액티브(H) | Hedged 7–10Y-oriented active Treasury bond exposure; bond rate/carry branch, FX-hedge estimate |
| `0085P0` | ACE 미국10년국채액티브 | Unhedged counterpart; same underlying rate branch, FX decomposition |
| `453850` | ACE 미국30년국채액티브(H) | Hedged 20Y+-oriented long Treasury; high duration and convexity scrutiny |
| `476760` | ACE 미국30년국채액티브 | Unhedged long Treasury; FX overlay and long-end rate sensitivity |
| `308620` | KODEX 미국10년국채선물 | Treasury-futures branch: futures index, collateral and roll, not cash-bond YTM |
| `455660` | ACE 미국하이일드액티브(H) | Speculative-grade credit branch: rates + OAS + credit-loss limitations |
| `440650` | ACE 미국달러단기채권액티브 | **USD short-duration credit-mixed** fund; NOT a pure short Treasury proxy despite its index description |

Coverage exclusion for initial MVP: leveraged/inverse and covered-call/option overlays unless explicitly routed by a dedicated derivative model. Other products can be added by type, not by forcing them into the same formulas.

## 8. Research architecture, implementable without overengineering

```text
FRED/Treasury/FX/spread observations           ETF issuer profile + total-return history
                |                                       |
                v                                       v
       Market data preparation                  Product/exposure preparation
                |                                       |
                +---------> Conventional calculations <-+
                                  |
                      Market snapshot + exposure
                                  |
              Scenarios + compensation + reconciliation
                                  |
                     Explicit investment policy
                                  |
             ETF assessment / optional comparison
                                  |
                   Underlying market explanations
```

An MVP can be a notebook with small, testable pure functions and cached input files; no new heavyweight plugin architecture is needed. External data acquisition, ETF profiles and actual market prices can be separate adapters without becoming separate analytical authorities. Export a compact dated JSON/CSV snapshot and a readable report. Local copies of research files must not overwrite Bondview-v2 documents.

### 8.1 What an MVP must prove

- Reproduce **all numerical example fixtures** when given their stated hypothetical inputs, or explicitly reject unsupported calculations (e.g., cash carry on a futures ETF).
- Generate actual U.S. rate market reports from FRED and actual ETF profiles/returns from permitted sources; show time alignment and data gaps.
- Provide both a within-ETF changing-conditions assessment and relevant cross-ETF comparisons without implicit forecasts or arbitrary integrated scores.
- Distinguish FX and credit from pure Treasury duration and explain major model-vs-ETF return mismatches rather than overriding calculations to make results look good.
- Compare practical decision usefulness and complexity with basic baselines: product facts alone, duration-only scenario, and cash/hold. Do not infer superior performance from elegant explanations alone.

## 9. Feedback loop — changes made after checking examples

This version already incorporates one internal review iteration with the companion file:

| Initial simplification tested | Example-driven failure | Revision now in architecture |
|---|---|---|
| Treat all ETFs with Treasury tenor name as similar cash bonds | `308620` is futures; `440650` is credit-mixed | Product-type routing and unsupported-formula safeguards (§3.2, §7) |
| Infer buying preference directly from observed direction and rate duration | 30Y high-compensation case can become less unsuitable without requiring a falling-yield forecast | Mandate + scenario budget + compensation, trend as context (§5) |
| Treat currency `(H)` as removing all FX exposure | Hedged and unhedged 10Y pair have hedge carry and imperfect coverage | Separate FX identities, estimate residual (§4.4) |
| Require one general scalar across bonds | HY credit spread widening can dominate falling Treasury yields | Credit-specific route and conditional eligibility (§4.4–5) |
| Use hypothetical `-DΔy` as historical ETF performance | Current duration and historical term yields do not reconstruct ETF realized returns | Clear counterfactual/actual-return split (§4.2, §4.5) |
| Use annual distribution yield as carry | Monthly payments do not identify portfolio economics | Yield-convention and missing-data checks (§4.3) |

**Remaining concerns, not disguised as solved:** Reliable ETF duration/carry/hedge data may be unavailable; simple duration+carry scenarios can understate convexity, derivatives, default events and active rebalancing; the selected risk budget and horizon can alter purchase decisions; without an economic goal no universal ranking is defensible; unhedged vs hedged preference cannot be decided from historical FX alone; proof of improved realized investment outcomes awaits prospective or out-of-sample testing. These do not block a useful MVP but must constrain the claims made.

## 10. Sources and verification notes

Economic methods: [CFA Institute — Fixed-Income Portfolio Management](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/overview-fixed-income-portfolio-management), [Yield Curve Strategies](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-curve-strategies), [Convexity](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-based-bond-convexity-and-portfolio-properties).

Market series: [FRED DGS10](https://fred.stlouisfed.org/series/DGS10), [FRED DEXKOUS](https://fred.stlouisfed.org/series/DEXKOUS), [ICE BofA HY OAS via FRED](https://fred.stlouisfed.org/series/BAMLH0A0HYM2) (check usage/history restrictions).

ETF identity and structure: [ACE ETF September 2026 distribution notice](https://www.aceetf.co.kr/cs/notice/7002); [ACE 10Y launch material](https://www.aceetf.co.kr/info/report/1160); [KODEX 308620 official name change](https://www.samsungfund.com/etf/lounge/notice-view.do?no=58734); [KRX 455660 listing](https://kind.krx.co.kr/disclosure/etfisudetail.do?method=searchEtfIsuSummary&strIsurCd=45566); [ACE 440650 fund details](https://www.funetf.co.kr/product/etf/view/KR7440650000). The representative fund set is for architecture stress tests, **not a contemporaneous buy list**. Read current issuer fund sheets before MVP calculations.
