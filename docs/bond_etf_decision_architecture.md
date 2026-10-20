# Bondview-v3 — Korean-Listed U.S. Bond ETF Decision Architecture

**Status:** **PROVISIONAL research architecture — 2026-10-20.** Describes the intended system, financial models, data conventions, outputs, and research checks. The numerical interpretation of investment attractiveness remains subject to review. This document is neither an implementation roadmap nor authorization to begin Work.

**Companion:** [`bond_etf_decision_examples.md`](bond_etf_decision_examples.md) is an earlier provisional set of examples and requires alignment before its assumptions or outputs can serve as acceptance criteria. Earlier Bondview repositories are reference-only, not design authorities.

## 1. Purpose and requirements

### 1.1 Principal objective

Bondview-v3 is a **convenient decision-support tool for choosing Korean-listed ETFs with U.S. fixed-income exposure**. It analyzes the economic opportunities and risks of relevant bond exposures using conventional fixed-income relationships, observed U.S. bond-market data, and issuer-published ETF characteristics. It does not forecast ETF prices or select individual bonds for investment.

The **common financial calculations** support three ways of examining results, not three independent evaluation engines:

1. **At a selected date:** Examine the economically relevant compensation, rate/credit exposures, scenario risks, and changed conditions for an ETF.
2. **Through time:** For a selected ETF and date range, evaluate how the relevant financial measures evolve. Identify improving, deteriorating, and mixed evidence *by measure*, not by a fabricated aggregate score.
3. **Across ETFs:** Compare all eligible ETFs in a chosen universe across the same applicable financial measures and defensible relative-value relationships, including cross-maturity and suitable credit comparisons. Focused 1:1 comparison is a subset of this view.

The underlying models can also be investigated **at the bond-market reference level**, e.g. Treasury 2Y/10Y/30Y segments and matched corporate-credit spreads, without initially selecting particular ETFs. Such analysis tests the economic meaning of a measure and helps identify market developments worth examining in ETFs. It is **not a compulsory market-assessment stage or a separate investment-recommendation engine**; issuer exposure enters each ETF calculation directly when needed.

A product's reference yield and maturity name do not by themselves identify its actual duration or carry. Translate bond-market results to an ETF only with compatible disclosed characteristics and transparent assumptions.

### 1.2 Out of scope

- Portfolio construction, asset allocation, personalized position sizing, holding optimization, trade execution, or an unconditional buy/sell timing engine.
- Recreating ETF holdings, individual-bond cash-flow portfolios, hedge books, futures collateral/roll economics, or historical ETF NAV as a general prerequisite.
- Predicting Treasury yields, credit spreads, currencies, ETF prices, or realized returns simply from their history.
- Using ETF price/return history to generate, weight, calibrate, or override ETF selection conclusions or infer undisclosed duration.
- Custom weighted-average attractiveness scores, ordinal state systems, or rules carried over from earlier Bondview repositories without independent economic justification.
- Detailed expense-ratio, tax, execution-cost or liquidity optimization in the initial bond-centered model; do not double-subtract costs already reflected in a published measure.

## 2. Analytical framework

Market observations and issuer-published ETF characteristics are the principal inputs to **reusable conventional financial calculations**. Analysis begins with an economic question—such as whether extra long-duration exposure is better compensated, or whether worsening credit conditions explain an adverse corporate-bond move—and uses only the necessary data and exposure measures. Market-level illustrations can validate and explain an economic relationship before it is applied to actual ETFs.

```text
     Bond-market observations                 Issuer-published ETF characteristics
     Treasury yields / curve                  Identity / bond type / benchmark
     Credit OAS / dated histories             Duration / published yield convention
     Relevant factor variability              Credit exposure / FX hedge policy
                    |                                      |
                    +------------------+-------------------+
                                       v
                      CONVENTIONAL FINANCIAL CALCULATIONS
                      - relevant market relationships
                      - compatible exposure sensitivities
                      - compensation and risk comparisons
                      - scenario and break-even conditions
                      - provenance, applicability, assumptions
                                       |
                                       v
                          REUSABLE FINANCIAL RESULTS
                                       |
                 +---------------------+---------------------+
                 v                     v                     v
           Single-date view       Historical view       ETF-universe view

     Optional market-reference tables and charts reuse the same inputs
     and appropriate financial calculations; no preliminary market
     investment judgment is required.
```

**Market-level reference:** The 10Y–2Y Treasury spread and its history require only Treasury yield observations. A duration-normalized *market reference* additionally requires documented durations of defined benchmark exposures or explicit hypothetical duration assumptions; the FRED constant-maturity tenor is not itself a bond with known duration.

**ETF-level calculation:** An ETF's rate-price sensitivity uses its **published duration** with an economically relevant yield scenario, `-D_ETF * delta_y_relevant`. A benchmark instrument's duration cannot silently stand in for the actual ETF duration; an issuer's `10Y` product label is not a duration of 10.

An economic relationship may be illustrated with benchmark segments and later applied to ETF data, but ETF evaluation does not depend on finishing a separate, categorical evaluation of the bond market. Comparisons across dates and products reuse the same definitions, with only justified relative calculations and date handling added.

## 3. Design principles and decision boundaries

1. **Investment questions precede classifications.** Choose established analyses according to the decision they illuminate, not to populate a predetermined number of constituents, aspects, or charts. Different measures can answer the same question without becoming interchangeable.
2. **Market information and product exposure work together.** Yield levels, curve movements and OAS are market facts; an ETF's duration, credit type and hedge policy govern their instrument-specific implications. Bond-market reference analysis is useful but is not a substitute for exposure-aware calculations.
3. **Conventional, explicit mathematics.** Specify minimum accepted formulas, units, assumptions and hand-checkable examples. Justified established enhancements are allowed when the baseline remains independently reproducible.
4. **Separate observation, assumption and conclusion.** Distinguish market levels, disclosed product characteristics, calculated sensitivities, counterfactual scenarios, compensation proxies, and conditional investment preferences.
5. **Preserve distinct evidence without double counting it.** A yield spread and a break-even cushion derived from that same spread can provide different *interpretations*, not two independent votes. Historical market variability, credit spreads and term-premium estimates may add information but require their own limitations and source checks.
6. **No unsupported attractiveness scalar.** Do not infer a universal investment objective by fitting historical ETF prices, optimizing indicator weights, or making every outcome a single directional score. Mixed conclusions across meaningful measures are valid.
7. **Use issuer characteristics as operational inputs.** Prefer dated official disclosures, accept transparently labeled approximations, and avoid reconstructing ETF holdings merely to improve mechanical precision.
8. **Do not confuse compensation with adequate compensation.** Higher yields or OAS can mean higher stated gross compensation **and** higher underlying risk. A break-even condition is not a forecast that market changes will remain below it.
9. **Keep complexity proportional to economic decision value.** Evaluate Treasury maturity and credit-market relationships before attempting detailed ETF replication. Key-rate duration, convexity refinements, derivatives mechanics and extensive hedge modeling are optional when justified, not mandatory analytical workstreams.
10. **Maintain applicability and comparability.** Distinguish `not applicable`, `unavailable`, `unsupported`, and `proxy`; show differences in reference currency, maturity, yield conventions and disclosure dates. An investment horizon does not restrict the maturities of the products compared.

## 4. Universe, applicability and product boundaries

**Long-run catalog scope:** all Korean-listed ETFs offering U.S. fixed-income exposure, including Treasury and corporate-bond funds. Catalog inclusion does not guarantee every financial aspect is numerically assessable.

**Initial model research:** Use a few representative, well-documented ETFs across relevant duration exposures, adding a credit example if valid credit inputs exist. The implementation agent may choose actual tickers based on current disclosure quality; no ETF list or issuer is mandated by this architecture.

| Product type | Default treatment | Limitation |
|---|---|---|
| Physical/cash Treasury ETF | Eligible for relevant rate and yield analysis | Issuer yield definition and duration conventions still matter |
| Corporate investment-grade/high-yield ETF | Eligible for rates plus relevant credit aspects | Treasury-only risk assessment is incomplete; OAS does not price all credit risk |
| Hedged/unhedged U.S. bond ETF | Eligible; show documented currency structure | Do not treat an `(H)` label as free/perfect hedging or USD yields as KRW net returns |
| Active / mixed exposure | Eligible according to published portfolio-level characteristics | Benchmark is not proof of actual current exposure |
| Treasury-futures ETF | Excluded from standard cash-bond evaluation by default; explicit user opt-in | Futures basis/collateral/roll differ; opt-in never validates cash-bond carry formulas |
| Leveraged, inverse or option-overlay product | May be catalogued, normally `unsupported` for the baseline model | Must not be assigned ordinary cash-bond calculations by default |

**Every numerical aspect has its own eligibility check.** An ETF may be included in a table while having `N/A` for corporate OAS, `unavailable` for a missing issuer yield, or `unsupported` for futures cash-bond carry. None of these should silently become zero or a neutral attractiveness score.

## 5. Input contracts and factor matching

### 5.1 Market data: observations and economic reference analyses

| Inputs | Initial sources | Proper use |
|---|---|---|
| Treasury constant-maturity yields | FRED H.15 `DGS3MO`, `DGS6MO`, `DGS2`, `DGS5`, `DGS10`, `DGS20`, `DGS30` | Tenor levels/changes; 2Y/10Y/30Y relationships; common scenarios; historical yield variability; **not** ETF duration, actual ETF YTM or investable benchmark bond prices |
| U.S. investment-grade/high-yield OAS | Permitted, appropriately matched ICE BofA/FRED or documented alternative | Spread compensation, Treasury-versus-credit divergence and scenario stress; not evidence of realized or forecast default losses by itself |
| USD/KRW (KRW per USD) | `DEXKOUS` or documented equivalent | Currency-policy context initially; quantitative FX treatment deferred unless necessary and justified |
| Dated short-rate/cash reference | Suitable KRW or USD benchmark, as explicitly chosen | Optional comparable-currency compensation analysis; USD T-bill yields are not KRW cash returns |
| Real yields, estimated term premium, inflation expectations | Recognized, defined sources if economically useful | Candidate **additional** explanations of long-end yields; term premium is model-derived, not an observed pure return signal |

Preserve source, dates, units, publication/cutoff and relevant retrieval/revision metadata; align information available at each historical assessment cutoff. Do not silently interpolate future issuer inputs or forward-fill unavailable market days. A full user-selected historical window is supported; specific smoothing and lookback periods are research conventions, not established financial laws.

**Historical yield variability** may be derived from the Treasury yield series under a declared sampling convention. For an `h`-observation change, define `delta_y_n,h(t) = y_n(t) - y_n(t-h)` on compatible accepted observations. Describe its historical dispersion or empirical distribution in **bp**, specifying the reference window and horizon. This is realized historical uncertainty **context**; it is not a yield forecast or an objective probability of a future shock. Align the yield-change horizon with any break-even or scenario comparison before interpreting relative magnitudes.

### 5.2 Minimum issuer ETF profile

Use official issuer/official listing materials directly. Do not recreate underlying holdings or infer duration by fitting ETF price returns.

| Profile field | Requirement |
|---|---|
| Ticker, official name, issuer | Required for identity and cataloguing |
| Bond category, investment mandate, benchmark | Required to select relevant market risk factors; benchmark ≠ portfolio holdings |
| Structure (cash, futures, active, leverage/overlay) | Required for model eligibility |
| Economic currency and published hedge policy | Required for currency qualifications |
| Published effective/modified duration **and its definition** | Required for precise first-order ETF rate-sensitivity output |
| Relevant maturity/tenor exposure | Where published; must not be substituted mechanically for duration |
| Issuer-published yield plus **exact yield definition** | Use if available; differentiate portfolio YTM/YTW, benchmark yield, SEC yield and distribution yield |
| Credit quality/category and relevant benchmark | Required for credit-specific conclusions |
| Source document URL, as-of date, units | Required for every material numerical input |

Optional inputs: convexity, key-rate duration (KRD), spread duration, hedge coverage and other disclosed characteristics. Missing optional fields **do not** authorize holdings reconstruction. A benchmark proxy is permissible only when economically well matched and visibly labeled `proxy`, without implying actual portfolio exposure. If no suitable measure exists, omit the unsupported precision.

### 5.3 Matching market factors to exposures

Choose relevant market factors based on what an ETF actually holds, not merely its name:

- For initial Treasury evaluations, match a disclosed duration with a defensible reference maturity segment and a **transparent single-factor approximation**. State any material term mismatch; do not equate a constant-maturity label with the ETF's numerical duration.
- For bond-market reference studies, Treasury 2Y/10Y/30Y yields and spreads are useful directly. Any duration-based benchmark scenario needs **explicit representative bond durations**, sourced or illustrative, not synthetic numbers silently derived from CMT labels.
- Published ETF KRDs may improve nonparallel yield-curve scenarios when available and relevant; they are a later refinement, **not** a requirement to reconstruct the ETF's holdings or underlying maturity weights.
- For corporate bonds, separate matched Treasury rate movements from changes in investment-grade or high-yield OAS. Where feasible, match rate duration, spread duration and market-index coverage. Broad OAS series are market proxies, not a precise credit decomposition for every ETF.
- Record FX exposure and hedge policy from issuer materials, but defer sophisticated hedge/FX scenario analysis from the immediate priority set. Never treat `(H)` as a perfect costless hedge.

The matched market factor and compatible exposure measure enter the same calculation. Market-only context is available without a selected ETF, but an ETF conclusion requires its relevant characteristics.

## 6. Baseline financial calculations

Every result distinguishes `market_observation`, `issuer_characteristic`, `derived_sensitivity`, `illustrative_assumption`, `proxy`, and `unavailable/unsupported`. Retain units, dated inputs, comparability conditions and interpretation. The following methods are a reusable analytical toolkit; **their presence does not require every calculation or a chart for every ETF**.

### 6.1 Treasury curve, relative maturity compensation and yield variability

For Treasury tenor `n` and two valid observations:

`delta_y_n(t0,t1) = y_n(t1) - y_n(t0)`.

If stored internally as decimal yields, convert a difference to basis points with `10,000 * delta_y`; if stored as percentage-valued observations, use `100 * delta_y`. Prefer decimal units for financial computation and explicitly convert source-unit inputs.

Market-reference comparisons include `y_10 - y_2`, `y_30 - y_10`, `y_30 - y_2`, and the history of these differences. Report movements in both endpoints; a change in a slope does not uniquely identify a change in long-bond risk or expected return.

Historical yield-change **dispersion** (e.g. realized standard deviation or historical quantiles in bp at a stated lookback/horizon) can provide context about how large market moves have been relative to measured compensation. When compared with a break-even cushion, state the common time horizon and any nonparallel-factor mismatch. Past variability is **not** a forecast or a probability that a break-even threshold will be crossed.

### 6.2 Interest-rate sensitivity

For compatible ETF effective/modified duration `D_ETF` and an explicitly hypothetical yield change `delta_y_relevant` in decimal units:

`rate_price_effect_ETF ≈ -D_ETF * delta_y_relevant`.

When compatible convexity `C_ETF` is available:

`rate_price_effect_ETF ≈ -D_ETF * delta_y_relevant + 0.5 * C_ETF * (delta_y_relevant)^2`.

For appropriate nonparallel Treasury factors and **published compatible** key-rate durations:

`rate_price_effect_ETF ≈ -sum_k(KRD_ETF,k * delta_y_k)`.

Do not add parallel and key-rate effects for the same shock. Use `+50bp`, `+100bp`, `-50bp` and selected nonparallel scenarios only where economically helpful. Constant `D_ETF` and a fixed hypothetical shock imply **constant fixed-shock sensitivity over history**, so that sensitivity alone cannot generate a changing attractiveness history.

For a **bond-market benchmark** illustration, use a *defined representative bond's* duration or openly assumed illustrative duration, not the numerical Treasury tenor or ETF characteristics by implication. Present such outputs as benchmark scenarios. Present `-D_current * delta_y_historical` as a **current-exposure counterfactual**, never as actual ETF historical price performance.

Key-rate and convexity refinements should be used only when they add meaningful information and have defensible inputs. Detailed ETF structure analysis is not a prerequisite for interpreting underlying 2Y/10Y/30Y market changes.

### 6.3 Compensation, carry and conditional break-even

Keep distinct:

1. **Observed market compensation:** relevant Treasury yields, term spreads and credit OAS.
2. **Published ETF yield:** issuer value with exact portfolio, benchmark or distribution yield convention and as-of date.
3. **Defensible holding-period compensation:** carry, financing/hedge terms and roll effects appropriate to the exposure and horizon, **only where supportable**.

A distribution yield is not automatically portfolio carry/YTM. A constant-duration ETF does not realize the roll-down of one fixed held-to-maturity bond. No gross USD market yield is automatically a net hedged KRW return.

For a compatible cash-bond exposure under explicit assumptions:

`illustrative_H_result ≈ defensible_H_carry + justified_roll_effect + rate_price_effect + supported_credit_effect`.

A missing term cannot silently become zero in a purported **complete return** result. Where only partial effects exist, report them individually and label the result partial/counterfactual, not a total-return forecast.

**Single-exposure break-even against a compatible cash comparator:**

`break_even_rise_bp ≈ 10,000 * (defensible_H_carry - comparable_cash_return_H) / D`, where `D > 0` and returns are expressed as decimals over a matching horizon/currency.

**Relative-exposure break-even under a common parallel rate shock:** for long and short exposures with comparable period compensation `c_L,H`, `c_S,H` (decimal returns) and compatible durations `D_L > D_S`, the incremental-rate-shock threshold is

`relative_break_even_bp ≈ 10,000 * (c_L,H - c_S,H) / (D_L - D_S)`.

This threshold is a **conditional offset of additional duration risk**, not a claim about the likelihood of a parallel shock or the performance of bonds with different rate paths. It may be negative if the longer exposure has a compensation disadvantage.

**Market-reference exploration:** substituting the *relevant observed Treasury yields* for `c_L,H` and `c_S,H`, and stated **representative benchmark durations** for the ETF durations, produces an *indicative market-yield-based* break-even **proxy**, not actual ETF carry or a one-year return estimate. It can be followed across the full observation period to investigate whether relative maturity compensation has changed. Clearly state the strong approximation and avoid treating the result as an ETF-level net-return decision. For actual ETF comparisons, use compatible issuer yield/carry data and only escalate to a true horizon-return break-even when justified.

Historical term/yield spreads and their duration-normalized proxies often depend on the **same Treasury observations**. They have different interpretation units but are not independent signals. Pairing them with **historical yield variability** can add an economically different description of observed rate uncertainty, without proving future probabilities or a final buy decision.

### 6.4 Credit and spread exposure

For comparable bond-market references:

`delta_y_corporate ≈ delta_y_matched_Treasury + delta_OAS`.

For compatible rate and spread sensitivities:

`credit_exposure_price_effect ≈ -D_rates * delta_y_matched_Treasury - D_spread * delta_OAS`.

Separating rate and credit components helps answer **whether the corporate market moved adversely because of Treasury rates or credit-specific repricing**. For example, a stable/falling Treasury yield alongside a widening corporate OAS isolates credit-spread deterioration; a negative *Treasury-rate contribution* alone does **not** prove corporate credit distress. Widening OAS may reflect default expectations, liquidity, risk appetite or required risk premiums; **it is a warning/context, not proof of realized fundamental credit deterioration**.

Credit OAS can be compared with an explicitly defined spread-duration shock to obtain an **indicative gross spread cushion** under comparable period assumptions. Such a cushion ignores defaults, migration, liquidity and optionality unless separately modeled; it is not net expected credit return. Choose credit benchmarks compatible with the exposure or label them proxies. Never apply a pure-Treasury conclusion to material unassessed corporate credit exposure.

### 6.5 Currency and hedge qualification — lower analytical priority

For consistently defined **unhedged** USD bond returns and USD/KRW returns:

`1 + R_KRW = (1 + R_USD) * (1 + R_USDKRW)`.

This describes an accounting identity or declared scenario, not an FX prediction. For the initial research, record the issuer's currency/hedge policy and qualify cross-currency comparisons. Do **not** presume a perfect free hedge or generate net KRW compensation without adequate inputs. Detailed currency and hedge modeling is deferred without removing currency eligibility checks from the ETF profile.

### 6.6 Model refinements

These relationships define the **minimum conventional baselines**, not limits on mathematical accuracy. A defensible established improvement (e.g. compatible convexity, KRD, improved period matching) is acceptable when it: answers the same economic question; has credible additional inputs; retains a verifiable baseline; makes a material difference explainable; and does not introduce disproportionate complexity or ETF-holdings replication.

An enhancement need not preserve every baseline conclusion, but material changes in the economic question, investment objective, source authority or aggregation/ranking logic require an explicit design decision rather than a silent model substitution.

## 7. Investment opportunity analyses and interpretation

**Attractiveness remains an interpretive investment question, not a validated universal scalar.** A small number of independently meaningful financial analyses can support useful conditional decisions without weighted-score aggregation or a forced overall winner. Do not choose an analysis because it makes an attractive plot; choose it because it answers a meaningful fixed-income question.

The following **seven candidate information families** are **not seven mandatory scoring dimensions, independent model engines, or required charts**. Their individual numerical results and interpretations may remain valuable even when several help answer the same question.

| Candidate family | Examples of evidence | Role and limitation |
|---|---|---|
| Market-rate level and change | Treasury tenor yields and dated movements | Foundational observations; not a standalone investment verdict |
| Term compensation | 2s10s, 10s30s, matched tenor yield differences, model-estimated term premium if justified | Relative-maturity compensation; may rise because risk rises |
| Rate sensitivity / risk | Duration shocks, convexity where available, historical yield-change variability with explicit horizon | Scenario/exposure risk; past variability is not a forward risk probability |
| Yield/carry compensation | Compatible published yield measures, defensible period carry and conditional break-even | Economically important but sensitive to yield convention, funding, roll, hedging and missing inputs |
| Credit | Matched Treasury versus OAS change, spread sensitivity, gross credit compensation cushion | Explains credit repricing; OAS is not default-adjusted expected profit |
| Currency and hedging | Disclosed policy, optional legitimate FX/hedge scenarios | Relevant qualification; detailed analysis deferred initially |
| Product compatibility and data quality | Instrument structure, source dates, missing/proxy disclosures | **Eligibility and confidence controls**, not a numerical investment signal |

A single investment question can draw on multiple families. For example, *whether the compensation for extending from 10Y to 30Y has improved* may be examined through market yield differences, duration-normalized break-even conditions, and observed historical yield variability. These may offer **different economic interpretations**, even when some are transformations of the same source yields. Preserve them separately where informative, but **do not double-vote overlapping evidence**.

For corporate credit, a change in total yield and the rate-versus-OAS decomposition answer different questions: one shows the changed financing/market rate, while the other identifies whether credit-specific repricing dominated. The additional OAS might be better gross compensation or a response to greater risk; the model should present both interpretations and their limits.

**Provisional research priorities, not a fixed architecture of new constituents:**

- Relative maturity compensation and **its duration-adjusted break-even history** for 2Y/10Y/30Y reference exposures.
- Historical yield-change variability as **additional context** for interpreting a break-even margin, with consistent horizons and no forward probability claim.
- Treasury-versus-corporate-OAS divergence over time and conditional credit-spread compensation/stress.
- Basic ETF exposure translation and product suitability; advanced KRD and detailed FX/hedge models only when warranted.

Other sound analyses—including term premium, carry/roll, and convexity—remain available for subsequent investigation; not being in the first experiment does not reject them. Equally, the provisional count of seven is not a design contract.

A valid conclusion may report `improved_on_measure_X`, `deteriorated_on_measure_Y`, `mixed_tradeoffs`, `conditional_preference_under_specified_assumptions`, `no_clear_preference`, or `insufficient_information`. These are explanatory results without invented thresholds. **Improvement in gross compensation is not proof that buying now is preferable to buying earlier or waiting.**

## 8. Historical investment opportunity assessment

Use the same applicable financial calculations across a **full user-selected date interval**, not only endpoint snapshots. Prioritize time series that explain **economically changing conditions**; a chart is not useful merely because Section 6 contains a formula.

- For Treasury maturity comparisons, show the **evolution** of relative yield compensation, and, where assumptions are documented, the **duration-adjusted break-even margin** between representative maturities or actual comparable ETF exposures. Label a market-yield-proxy margin separately from defensible ETF carry-based break-even.
- A 2Y/10Y/30Y break-even plot needs a defined pair of benchmark durations or actual compatible ETF durations. It cannot be deduced from the Treasury CMT maturity labels alone. Treat its changing value as a comparison of **compensation relative to additional duration**, not as a forecast or composite attractiveness score.
- When relevant, relate break-even magnitudes to **historical distributions of horizon-consistent yield moves**. This adds context about observed risk without claiming that historical frequencies are future scenario probabilities.
- For credit, track Treasury-rate and OAS changes separately, and illustrate episodes when spread deterioration offsets improving Treasury rate conditions. Distinguish credit-specific repricing from proven fundamental credit deterioration.
- Use historical Treasury/OAS observations from their actual publication dates. Never insert today's issuer yield into an earlier date. Use point-in-time ETF disclosures only after their public availability dates.
- If historical issuer duration/exposure values are unavailable, an explicitly labeled **constant-current-exposure counterfactual** may be applied to the historical market record. The counterfactual is not historical ETF P&L, historical total return or a reconstruction of its actual portfolio.
- With fixed duration and a fixed hypothetical +50 bp shock, the calculated sensitivity **does not change**. Do not fill historical plots with this unchanged output; changing historical-sized shocks and new valid exposure measurements are different quantities and must be labeled accordingly.
- Distinguish genuinely independent economic evidence from alternate transformations of the same spread. Multiple useful interpretations may be displayed, but do not present them as independent corroboration.

The analytical result should identify which relevant condition improved, which deteriorated, and what additional assumption would be needed to infer a stronger investment conclusion. Plotly and specific chart designs belong primarily in the companion examples/user-interface work; the architecture specifies the **economic information** worth visualizing, not a mandated chart inventory.

## 9. ETF universe and comparative results

The selected ETF universe may contain many products; **individual, historical and cross-universe views reuse the same financial definitions and calculation paths**. A 1:1 comparison is a focused presentation of the universe results, with any additional pairwise break-even relationship explicitly computed from compatible inputs rather than a separate ranking engine.

For each financially relevant result, distinguish:

| Status | Meaning | Example |
|---|---|---|
| `value` | Supported numerical or descriptive result under recorded conventions | Rate sensitivity of an ETF with published duration |
| `not_applicable` (`N/A`) | Economic mechanism does not apply | Corporate credit OAS for a verified pure Treasury ETF |
| `unavailable` | Applicable but material market/issuer data are missing | No usable portfolio duration disclosed |
| `unsupported` | The baseline model is structurally unsuitable | Cash-bond carry applied to Treasury futures |
| `proxy` / `limited_confidence` | Clearly declared approximation with limitations | Matched benchmark duration in an explicitly provisional scenario |

Comparisons should answer an **identified economic question**: rate-risk sensitivity across tenors, additional compensation relative to that risk, or credit spread compensation versus Treasury exposure. A row or column exists because it communicates relevant evidence, **not** because seven provisional families mandate seven charts or rankings.

The same measure can be compared through time and across all eligible ETFs. Avoid directly comparing incompatible currency-net returns, maturity proxies, ETF published yield conventions, credit-quality segments, or unobservable carry. A product may appear in the universe while some results remain N/A/unavailable/unsupported. It is legitimate to conclude that no overall winner is established.

## 10. Supplementary views

### 10.1 Bond-market references

Users may inspect current and historical Treasury 2Y/10Y/30Y yields, curves, yield spreads and relevant credit OAS **before selecting an ETF**. Where assumptions are explicit, economically meaningful reference calculations (including benchmark-duration break-even history) may also be displayed to help identify a market development that warrants further ETF review.

These optional reference views reuse existing market data and conventional calculations. They do not constitute an independent mandatory market evaluation stage or an unconditional purchase recommendation. A simple tenor-yield chart can remain a diagnostic; more important user-facing analysis should explain **compensation, risk and their evolution**.

### 10.2 ETF prices and realized performance

ETF price/NAV history must **not** enter the ETF selection model, its weights, factor exposures, or calibration. A separate diagnostic may compare realized total-return behavior with published exposure estimates to flag unexplained differences; those observations do **not** silently update selection signals.

A later convenience view may compare appropriately distribution-adjusted historical ETF returns, labeled clearly as **realized performance** rather than bond-market opportunity. Detailed NAV attribution is not required by the core model.

## 11. User interface and implementation boundary

**User interface:** One or more Jupyter `.ipynb` notebooks, organized as easy sequential workflows: select dates/products/market references → load market data and issuer profiles → call imported analytical functions → inspect tables, clear explanations and interactive Plotly charts where useful. The notebooks contain **no substantive function or class definitions**.

**Implementation:** A small collection of cohesive Python `.py` modules implements data acquisition/validation, issuer profiles, applicable bond financial calculations, historical evaluation and optional plotting helpers. One reusable calculation model supports selected-date results, time series and universe-wide comparisons. Add comparison helpers only for legitimate *relative financial calculations*, not separate competing engines.

**Output standard:** Show the economic question, underlying observations, ETF exposure when applicable, quantitative result, dates/units, assumptions/proxies, relevant counterevidence and limitations. A result may be visualized historically, across products, or in both ways whenever it is genuinely informative. Do **not** produce one chart per candidate family by default; do not repeat unchanged fixed-shock sensitivity or near-identical line shifts merely to display more figures.

**Optional views:** Market-reference tables/charts can be used before an ETF is selected; ETF realized performance remains outside the decision model.

**Verification:** Pure calculation/data-contract tests run from Python without interactive notebook execution. Visual demonstrations in the companion examples should exercise economic usefulness, not become implementation specifications for specific chart types.

## 12. Minimum numerical and behavioral verification

Use clearly labeled **synthetic** financial fixtures and independent numeric checks before interpreting live ETF data. Examples:

| Fixture | Expected result / interpretation |
|---|---|
| ETF duration `D=8`, rate shock `+50 bp` | `-4.00%` first-order price sensitivity |
| Same with compatible convexity `C=80` | `-3.90%` second-order result |
| Spread duration `6`, OAS shock `+100 bp`, no Treasury-rate move | `-6.00%` spread-only price sensitivity |
| Unhedged USD bond result `-2%`, USD/KRW appreciation `+8%` | `+5.84%` conditional KRW result (FX deferred as priority) |
| 2Y `4.0%`, 10Y `4.5%` | `+50 bp` 2s10s market yield spread |
| Historical 2s10s from `-10 bp` to `+100 bp` | `+110 bp` relative yield compensation change, **not an ETF verdict** |
| Illustrative constant durations `D_2=1.9`, `D_10=7.5` and gross reference yields six months ago `y_2=4.60%`, `y_10=4.50%` | 10Y-vs-2Y indicative relative break-even **`-1.79 bp`**, under explicit one-year yield-as-compensation proxy and common parallel shock |
| Same durations, current reference yields `y_2=4.10%`, `y_10=5.10%` | **`+17.86 bp`**; change in indicative break-even margin `+19.64 bp`, **not a forecast** |
| Add `D_30=16.0`, market yields 30Y six months ago `5.00%`, now `5.40%`, with 10Y yields as above | 30Y-vs-10Y indicative margin changes from `+5.88 bp` to `+3.53 bp`: **relative compensation deteriorates under the proxy** |
| Credit rate duration `5.5`, spread duration `5`, Treasury change `-20 bp`, OAS change `+60 bp` | `+1.10%` Treasury price component, `-3.00%` credit spread component, `-1.90%` combined; credit repricing offsets favorable rate movement |

The historical break-even fixtures use **hypothetical matched representative duration values and observed-like market yields as gross compensation proxies**, not ETF portfolio YTMs, hedge-adjusted carry, realized return or point-in-time historical ETF disclosures. Computed values are rounded for display; unit-test tolerance must be defined against unrounded decimal values (for elementary non-extreme calculations, `1e-10` decimal-return units is an example numerical tolerance, not a bound on economic approximation error).

Behavioral invariants:

1. Single-date, historical and universe presentations use **the same** financial definitions and consistent conventions; market-only views do not alter ETF results.
2. Relevant bond-market reference yield/term analysis can operate without an ETF; ETF-specific rate sensitivity uses issuer duration or a transparently declared proxy, **not the Treasury tenor as duration**.
3. A full historical series of indicative relative break-even margins changes only with its documented yield, duration or other accepted compensation inputs. Under fixed durations it is a transformed time series of yield differences, **not independent evidence**.
4. Holding ETF duration and shock fixed leaves `-D * shock` unchanged through time. Do not present that static sensitivity as an evolving opportunity signal.
5. Empirical yield variability reports its historical sampling convention/horizon and does not claim future probabilities. A benchmark yield proxy cannot silently become comparable ETF period carry.
6. Credit-rate and spread effects are separated where relevant; widening OAS is not automatically interpreted as proof of deteriorated issuer fundamentals.
7. A pure Treasury, credit ETF and opt-in Treasury future distinguish `N/A`, `unavailable`, `unsupported`, and `proxy` appropriately. Never fabricate futures cash carry or unhedged-to-hedged net KRW compensation.
8. Point-in-time issuer yields and durations do not leak into prior dates. Constant-current-exposure studies are clearly labeled counterfactual, not historical ETF P&L.
9. ETF price/return histories have **no effect** on selection outputs. Model refinements preserve reproducible baselines and disclose additional data/assumptions.
10. No single metric, historical trend, empirical distribution or break-even threshold is silently interpreted as a universal buy signal; mixed economic evidence is preserved.

Tests establish financial arithmetic and documented behavior, not trading success. Independent review must separately examine economic validity and practical usefulness of actual sourced results.

## 13. Minimum research validation

**Status:** This is a proposed **bounded research question**, not authorization to execute Bernie Work. A separate accepted assignment is required. It does not define the future development roadmap.

**Research question:** Can established fixed-income analyses produce **several distinct, decision-relevant interpretations** of Treasury maturity and corporate-credit opportunities, and can those results be translated to practical Korean-listed bond ETF comparisons **without detailed ETF implementation modeling or an arbitrary attractiveness index**?

Begin with **economically meaningful bond-reference examples** (especially Treasury 2Y/10Y/30Y) using actual dated market histories and clearly documented representative duration assumptions. Then apply supported measures to **a few actual ETF issuer profiles** to examine where fund-specific exposure or yield conventions materially affect the conclusions. This is a research order, **not a requirement to construct separate market and ETF evaluation engines**. Include a credit-spread example where matching public data and products are available; detailed FX and ETF KRD are lower priorities. The user/agent need not fix ticker selections in this architecture.

**Required inspectable findings for an eventual authorized experiment:**

1. Dated market input histories and issuer product profiles with units, sources, comparable conventions and limitations.
2. A full-period **duration-normalized relative-compensation/break-even time series** for at least one Treasury maturity pair, with documented benchmark versus actual ETF inputs. Explain what changed economically and what the measure cannot prove about buying now.
3. A comparison of that compensation margin with **historical yield-change variability**, on a declared compatible horizon, examining whether this adds risk context beyond a rescaling of the same spread.
4. A matched Treasury-versus-credit-OAS **divergence example**, plus an appropriate spread-risk or gross compensation interpretation; distinguish credit repricing from inferred fundamentals.
5. Direct application of supported calculations to several published ETF exposures, showing meaningful cross-maturity/credit differences and explicit N/A, missing, unsupported and proxy cases. No sophisticated holdings reconstruction or futures carry is required.
6. Reproducible numerical fixtures, time-alignment checks, baseline-versus-justified-enhancement comparisons where applicable, and evidence that ETF price histories never drive the selection result.
7. A concise assessment of which outputs add **new economic information**, which offer a useful *interpretation of overlapping data*, which are redundant or misleading, and what remains conditional on investors' objectives, future rate/spread paths or unavailable data.

**Research completion:** Correct, reproducible methods, the stated outputs, and honest conclusions/limitations. It **does not require** a universal attractiveness score, fully comparable ETF net returns, a profitable backtest, or a definitive preferred ETF. The user and Archie evaluate quantitative validity and qualitative decision usefulness before a later architecture/examples revision or roadmap discussion.

## 14. Unresolved research choices and revision path

- When does an economic reference comparison among Treasury 2Y/10Y/30Y segments add usable decision information, and what minimum issuer characteristics are needed to apply it reliably to an ETF?
- Is a **duration-normalized compensation time series** sufficiently useful, and does combining it with empirically measured yield variability provide genuinely different risk information without implying future probabilities?
- When are observed market Treasury yields an acceptable **gross reference proxy**, and when are compatible issuer yield/carry inputs required before asserting an ETF-level break-even or horizon result?
- How should term-premium and yield-curve models be used, if at all, without creating unnecessary complexity or assuming a model-estimated premium predicts performance?
- In corporate credit, what additional public evidence would help interpret OAS widening as compensation versus deterioration in default/liquidity fundamentals, and which claims must remain explicitly conditional?
- When do convexity, ETF-level KRD, currency/hedge modeling or product-implementation details materially alter a practical selection conclusion enough to justify their costs?
- Which separately useful measures should coexist in an explanation even when they are based on overlapping market observations, and what information is duplicated rather than added?

After reviewing the minimal experiment, revise this architecture and the companion examples consistently. The companion `bond_etf_decision_examples.md` is intentionally **not revised here**; future examples can show helpful financial visualizations, their assumptions and independent economic insights. **The development roadmap is deferred.** No implicit authorization for subsequent Work is granted.

## 15. References and research provenance

- [Companion examples — provisional and not yet aligned](bond_etf_decision_examples.md).
- [Earlier Bondview-v3 critical design review](bondview_v3_critical_design_review_20261013.md) — reference material, not an accepted roadmap.
- [FRED DGS10](https://fred.stlouisfed.org/series/DGS10), [FRED DEXKOUS](https://fred.stlouisfed.org/series/DEXKOUS), [FRED Treasury data](https://fred.stlouisfed.org/).
- [CFA Institute: fixed-income portfolio management](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/overview-fixed-income-portfolio-management), [yield-curve strategies](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-curve-strategies), [convexity](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-based-bond-convexity-and-portfolio-properties).

This document contains **no current ETF investment recommendation**. Live products, issuer characteristics, market inputs and disclosures must be verified at the observation date before producing any decision-support result.
