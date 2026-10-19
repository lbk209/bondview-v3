# Bondview-v3 — Korean-Listed U.S. Bond ETF Decision Architecture

**Status:** **PROVISIONAL research architecture — 2026-10-19.** Describes the intended system, financial models, data conventions, outputs, and research checks. The numerical interpretation of investment attractiveness remains subject to review. This document is neither an implementation roadmap nor authorization to begin Work.

**Companion:** [`bond_etf_decision_examples.md`](bond_etf_decision_examples.md) is an earlier provisional set of examples and requires alignment before its assumptions or outputs can serve as acceptance criteria. Earlier Bondview repositories are reference-only, not design authorities.

## 1. Purpose and requirements

### 1.1 Principal objective

Bondview-v3 is a **convenient tool for choosing Korean-listed ETFs that provide U.S. fixed-income exposure**. It is not a system for selecting individual bonds or forecasting ETF prices. The analysis combines **issuer-disclosed ETF characteristics** with the relevant observed U.S. bond-market data using established fixed-income methods.

The primary user questions are:

1. **An ETF at the selected date:** What compensation, exposures, scenario risks, and important changes in conditions matter for evaluating this ETF now?
2. **An ETF through time:** Over a chosen interval (for example, the preceding year), how have the *market conditions relevant to this ETF's exposure* changed its investment opportunity? Show a time series and distinguish improvement, deterioration, and mixed trade-offs by economic aspect.
3. **Among ETFs:** How do available ETFs in the selected universe compare *by applicable aspect*, including across maturities and, when economically justified, across credit categories? Provide conditional choices when supported, without forcing a universal winner.

Users may also inspect **bond-market data** (for example 2Y and 10Y Treasury yields, historical movements, the 2s10s spread and credit OAS) in optional tables and charts, including before selecting ETFs.

### 1.2 Out of scope

- Portfolio construction, asset allocation, personalized position sizing, holding optimization, trade execution, or a universal buy/sell timing engine.
- Recreating ETF holdings, bond cash-flow portfolios, hedge books, futures collateral/roll economics, or historical ETF NAV from underlying securities as a general prerequisite.
- Predicting future Treasury yields, credit spreads, currencies, ETF prices, or realized returns merely from their history.
- Using ETF price/return history to generate, weight, calibrate, or override ETF **selection** signals or to infer undisclosed duration.
- Custom weighted-average attractiveness scores, ordinal state systems, or rules inherited from Bondview-v2 without separate economic justification.
- Detailed expense-ratio, tax, execution-cost or liquidity optimization in the initial bond-centered model; never double-subtract costs already reflected in a published measure.

## 2. Analytical framework

ETF assessments use two primary inputs: **market observations** and **issuer-published ETF characteristics**. For each financial calculation, market factors are matched to the ETF’s documented exposure. Common data preparation and formulas can be reused across ETFs; the resulting measures support individual assessments, historical analysis and comparisons.

```text
     Market observations                         Issuer-published ETF profile
     Treasury yields/curve                       Identity / type / benchmark
     Credit OAS / relevant FX                     Duration / optional KRD
     Time series and sources                      Yield convention / credit / FX policy
                   \                             /
                    \                           /
                     v                         v
                    ETF FINANCIAL ANALYSIS
                    Choose economically compatible market factors
                    Apply applicable exposure and risk measures
                    Measure compensation, sensitivities and scenarios
                    Preserve source dates, assumptions and coverage
                                      |
                                      v
                   ETF opportunity through time / by aspect
                   Cross-ETF comparison / conditional conclusions

  Optional market-data tables and charts draw on the same
  market observations.
```

**Example:** The 10Y–2Y Treasury yield spread is calculated from market yields. Price sensitivity for a particular ETF is calculated using its disclosed duration and an economically relevant yield shift, `-D_ETF * delta_y_relevant`. Neither DGS10 nor a “10Y ETF” label determines the ETF’s actual duration; a benchmark-bond duration cannot automatically replace a portfolio duration.

Market-data charts and tables may be used independently for context. ETF financial analysis uses the underlying market observations and product characteristics without requiring a preliminary market recommendation.

## 3. Design principles and decision boundaries

1. **Relevant market factors.** Select market observations and risk factors according to the ETF’s issuer-published exposure. Do not use unrelated market measures to determine an ETF result.
2. **Conventional, explicit mathematics.** Specify minimum accepted formulas, units, and interpretable numerical checks. A more complete established formula may be used if its additional inputs are justified and the baseline remains reproducible.
3. **Separate facts, characteristics, scenarios, and judgments.** Market yields are observations; issuer duration is a published product attribute; a `-D*delta_y` result is a sensitivity under a declared shock; a preference additionally involves assumptions and economically compatible comparisons.
4. **No invented attractiveness scalar.** Use a small set of interpretable compensation/risk measures and conditional conclusions. Do not discover weights by fitting historical ETF prices or choose a scalar simply because it produces an attractive time-series plot.
5. **Relevant aspects, not artificial completeness.** Some exposures need credit or hedge analysis; pure Treasuries do not have corporate spread exposure. Distinguish `not applicable` from `unavailable`, `unsupported`, and `proxy/limited confidence`.
6. **Issuer characteristics are operational inputs.** Prefer dated portfolio disclosures and their published approximation over synthetic holdings reconstruction. Preserve definitions and dates; do not treat a proxy as an observed portfolio characteristic.
7. **No implicit market forecast.** Yield trends, shocks, market yield compensation and break-even values are not probabilities that rates will rise or fall, and do not by themselves prove buying now is better than waiting.
8. **Keep complexity proportional to decision value.** Do not expand into futures carry, hedge replication, factor fitting, or historical NAV attribution merely to cover every product with a precise result.
9. **Document comparability.** The same reference period, units, currency assumption, risk convention and market cutoff should be used when claiming comparable results; mismatches are exposed rather than obscured.
10. **Do not presume a portfolio mandate.** Investment holding horizon is distinct from underlying maturity. A 12-month illustrative horizon may compare a 2Y- and 10Y-oriented ETF; it does not limit the universe to 12-month bonds.

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

### 5.1 Market data: observed independently, used in ETF calculations

| Inputs | Initial sources | Proper use |
|---|---|---|
| Treasury constant-maturity yields | FRED H.15 `DGS3MO`, `DGS6MO`, `DGS2`, `DGS5`, `DGS10`, `DGS20`, `DGS30` | Tenor-specific levels, changes, relevant curve reference, common shock definitions; **not** ETF duration or actual ETF YTM |
| U.S. corporate OAS | Permitted, matched ICE BofA/FRED IG/HY series or other documented source | Relevant incremental credit market spread and historical change, with coverage/licensing caveats |
| USD/KRW (KRW per USD) | `DEXKOUS` or documented equivalent | Currency context and consistent FX scenarios, not implied future FX appreciation |
| Dated short/cash reference | Suitable KRW or USD benchmark, as explicitly chosen | Currency-consistent compensation comparator; USD T-bills are not KRW cash |
| Real yields, term-premium/inflation estimates | Recognized, documented source if useful | Optional additional explanatory evidence, not a mandatory signal or standalone purchase rule |

Record source, observation date and publication/cutoff, retrieval time where useful, units, series changes, known historical gaps, and any revisions. Align data by information actually available at each assessment time; do not forward-fill through unavailable periods without disclosure. Historical windows are user-selected; any default lookback or smoothing convention must be declared and justified.

### 5.2 Minimum issuer ETF profile

Use official issuer/official listing materials directly. Do not recreate underlying holdings or infer duration by fitting ETF price returns.

| Profile field | Requirement |
|---|---|
| Ticker, official name, issuer | Required for identity and cataloguing |
| Bond category, investment mandate, benchmark | Required to select relevant market risk factors; benchmark ≠ portfolio holdings |
| Structure (cash, futures, active, leverage/overlay) | Required for model eligibility |
| Economic currency and published hedge policy | Required for currency qualifications |
| Published effective/modified duration **and its definition** | Required for precise first-order rate-sensitivity output |
| Relevant maturity/tenor exposure | Where published; must not be substituted mechanically for duration |
| Issuer-published yield plus **exact yield definition** | Use if available; differentiate portfolio YTM/YTW, benchmark yield, SEC yield and distribution yield |
| Credit quality/category and relevant benchmark | Required for credit-specific conclusions |
| Source document URL, as-of date, units | Required for every material numerical input |

Optional input fields: convexity, key-rate duration (KRD), spread duration, hedge coverage and other disclosed characteristics. Absence does **not** authorize reconstruction of holdings. A benchmark proxy may be used only when economic matching is credible and the result is visibly labeled as `proxy`; otherwise suppress the unsupported magnitude.

### 5.3 Exposure and market-factor matching

Issuer duration is an exposure magnitude, while market yield changes refer to **tenors and curve factors**. Choose a defensible factor representation for each ETF:

- Where published key-rate durations are economically compatible with the selected Treasury curve, use them for **nonparallel** factor changes.
- When only total duration and an approximately matched benchmark segment are available, a **single relevant Treasury tenor or transparent term proxy** is a simplification. State the mismatch; a “10Y” label does not prove sensitivity entirely to DGS10.
- For corporate exposure, distinguish rate duration from spread duration where published and match the OAS quality/maturity universe where feasible. A broad HY OAS is not an exact spread proxy for every HY portfolio.
- For FX and hedge exposure, use the issuer's policy for qualification; don't infer a perfect forward hedge from the name.

The selected factor and the corresponding exposure measure enter the applicable financial calculation together.

## 6. Baseline financial calculations

For every result distinguish `market_observation`, `issuer_characteristic`, `derived_sensitivity`, `illustrative_assumption`, `proxy`, and `unavailable/unsupported`. Preserve units, matched as-of dates and convention.

### 6.1 Treasury curve and rate changes

For tenor `n` and two valid observations:

`delta_y_n(t0,t1) = y_n(t1) - y_n(t0)`.

If yields are stored as decimal numbers, multiply differences by `10_000` to report bp; if stored in percent units, multiply by `100`. Common market context includes `y_10 - y_2`, `y_30 - y_10`, and their changes, with movements in both endpoints shown. These descriptive measures are available in the optional market-only view *and* as inputs to relevant ETF calculations; they do not produce investment verdicts on their own.

### 6.2 Interest-rate sensitivity

For an ETF with economically compatible published duration `D_ETF`, and a **declared hypothetical or historical-sized scenario** yield shift `delta_y_relevant` in decimal units:

`rate_price_effect_ETF ≈ -D_ETF * delta_y_relevant`.

For defensible compatible ETF convexity `C_ETF`:

`rate_price_effect_ETF ≈ -D_ETF * delta_y_relevant + 0.5 * C_ETF * (delta_y_relevant)^2`.

For compatible nonparallel key-rate factors:

`rate_price_effect_ETF ≈ -sum_k(KRD_ETF,k * delta_y_k)`.

**Never double-count** the same shock through both total duration and KRD. A current ETF duration combined with a historical-sized market change is a **current-exposure counterfactual**, not historical ETF P&L or a realized/forecast return. Baseline illustrative shocks: `+50bp`, `+100bp`, `-50bp`, and a nonparallel case where supported. These are not event probabilities.

### 6.3 Yield compensation and carry: avoid false precision

Separate: (i) market Treasury yields/credit spreads, (ii) dated ETF-published portfolio yields under their particular conventions, and (iii) defensible horizon economic carry. **An ETF's distribution yield is not automatically its carry, YTM or YTW.** A target-duration ETF does not inherit the exact roll-down of a fixed held-to-maturity bond.

A compatible, purely illustrative cash-bond scenario may be formed if assumptions are explicitly supportable:

`illustrative_H_result ≈ defensible_H_carry + justified_roll_effect + rate_price_effect_ETF + supported_credit_effect`.

Omit unsupported components *and* avoid calling a partial sum a complete total-return estimate. Expense ratios are deferred from the initial model and embedded reported costs must not be counted twice. No generic hedged KRW carry is inferred from an unhedged USD market yield.

For a compatible comparison with a cash alternative, an optional rate break-even cushion is:

`break_even_rise_bp ≈ 10_000 * (defensible_H_carry - comparable_cash_return_H) / D_ETF`, `D_ETF > 0`.

For ETF A vs B, a common-parallel-shock first-order break-even can be derived from the **difference in comparable period compensation** divided by the **difference in appropriately matched duration sensitivities**. That relationship is valid only under the specified common shock and comparability assumptions; it is not the implied future joint evolution of 2Y and 10Y rates. If compensation comparability fails, provide yield curves, duration risk and explicit caveats rather than manufacturing the break-even value.

### 6.4 Credit and spread exposure

Where rate and spread sensitivities are meaningfully available:

`credit_exposure_price_effect ≈ -D_rates * delta_y_matched_Treasury - D_spread * delta_OAS`.

Corporate yield approximately reflects matched Treasury yields plus a credit-spread component, but OAS does not guarantee compensation net of defaults, downgrades, liquidity or optionality. No pure-Treasury conclusion for a corporate ETF when the credit factor is material and unassessed.

### 6.5 Currency and hedge qualification

For consistently defined unhedged USD bond returns and USD/KRW return:

`1 + R_KRW = (1 + R_USD) * (1 + R_USDKRW)`.

This is an accounting relationship or scenario decomposition, **not a currency forecast**. Hedged ETF return/carry comparisons require a defensible hedge treatment; `(H)` is neither perfect hedging nor zero cost. If reliable hedge information is unavailable, quantify compatible **USD bond-rate** aspects separately and mark comparable **KRW net compensation** unavailable.

### 6.6 Model refinements

The formulas above are **minimum accepted baselines**, not caps on mathematical accuracy. An established improvement (e.g., second-order convexity, compatible KRD or more accurate period conventions) is allowed if: it addresses the same economic question, has credible inputs, retains a separately verifiable baseline, identifies important changes and limits, and offers enough economic benefit to justify complexity. It need not yield exactly the baseline conclusion. A change to the investment objective, data authority or an invented ranking rule is a **design decision**, not a routine formula refinement.

## 7. Investment opportunity measures and interpretation

**Attractiveness is a practical interpretive question, not a preexisting numerical variable.** We cannot validate a universal objective by trial-fitting multiple indicator weights to historical ETF returns. The model should calculate transparent economic quantities first and explain when those support a conditional preference.

Relevant measurable **aspects** may include:

| Aspect | Quantitative evidence | Main qualification |
|---|---|---|
| Market-rate level / change | Relevant current Treasury tenor, changes over selected window | Market yield is not actual ETF return or published ETF YTM |
| Term compensation | Yield-curve slope, relative market tenor yields, optional term-premium estimate | Compensation may rise because risk rises; term premium is model-dependent |
| Rate sensitivity | Issuer duration, convexity/KRD if available, scenario price effects | Scenario, not expected yield move or performance |
| Yield/carry compensation | Compatible issuer yield, supportable carry and break-even when feasible | Distribution yield is not carry; cross-currency comparison needs additional assumptions |
| Credit | Matched credit OAS and rate/spread sensitivity | Credit losses and spread risks cannot be ignored |
| Currency / hedging | Reported policy and defensible FX/hedge qualifications | Do not assume future FX or perfect costless hedging |
| Product compatibility / information quality | Structure, disclosure coverage, proxy flags | May limit or prevent specific calculations |

A conclusion can say a specified *aspect* improved (e.g., 10Y relative yield compensation versus 2Y increased) while another aspect worsened (e.g., additional duration downside remained large). **Such mixed outcomes are not model failure.** Do not convert them into a universal score simply to provide a winner or a monotonic “attractiveness” line.

Permitted conditional judgments: `more_favorable_on_aspect_X`, `less_favorable_on_aspect_X`, `supported_preference_under_assumptions`, `mixed_tradeoffs`, `no_clear_preference`, `insufficient_information`. These are descriptions of *evidence and assumptions*, not accepted numerical threshold classes or unconditional buy/sell instructions.

A yield increase can improve starting compensation without proving the correct purchase date. A historical improvement in compensation can be decision-relevant **without forecasting that yields will fall**. If a user chooses a reference horizon or scenario, it must be stated; the horizon does not restrict the maturities of ETFs eligible for comparison.

## 8. Historical ETF opportunity assessment

For the selected ETF and user-defined interval, produce **time series of its relevant market inputs and well-defined exposure-aware measures**, not an ETF-price-based attractiveness reconstruction. Compare continuously across the interval where data permit, including changes in the shape of the opportunity, not only endpoint labels.

- Use **historical market observations from their actual dates**. Never transplant today's issuer yield back into a time when it was unknown.
- If dated historical ETF characteristics genuinely exist, use each only after its documented public availability date. If unavailable, **hold the currently disclosed structural exposure (e.g., duration) fixed** for a clearly labeled *constant-exposure market counterfactual*; it is not the ETF's actual historical holding, yield or return.
- An ETF's reference market yield can vary historically even under fixed duration; fixed-duration sensitivity to an **unchanged +50 bp scenario is constant**. Do not invent a changing risk metric from a fixed shock and fixed exposure. Risk consequences of **observed yield changes between dates** can vary and should be identified as hypothetical, not realized gains/losses.
- Compare changes in rate compensation, term slope, OAS and other relevant factors while holding the economic comparison conventions stable. State when a changed risk picture is unobservable because historical exposures are unavailable.
- For a universe-wide historical view, evaluate each eligible ETF using the **same explicit methodology and relevant dates**, but do not imply that missing historical issuer characteristics are observed.

The historical analysis may reasonably conclude that one aspect of an opportunity has improved while a second aspect remains adverse. It should explain what changed, why it matters for the ETF's exposure, and what further assumption would be required for an investment preference.

## 9. Universe-wide assessment and aspect applicability

The user should be able to assess **every selected ETF in the supported universe**, not just pairs. The main view should be an **ETF × relevant aspect** comparison, with selectable product subsets, dates, and historical intervals. Direct 1:1 comparison is simply a convenient focused view of the same analysis.

For each aspect/ETF cell, distinguish these statuses explicitly:

| Status | Meaning | Example |
|---|---|---|
| `value` | Valid numerically derived result under recorded assumptions | Duration × standard rate shock |
| `not_applicable` (`N/A`) | Economic exposure/mechanism does not apply | Corporate OAS exposure for a verified pure Treasury ETF |
| `unavailable` | Aspect applies but required issuer/market data are missing | No published duration for a cash-bond ETF |
| `unsupported` | Existing model would be structurally invalid | Cash-bond carry applied to Treasury futures |
| `proxy` / `limited_confidence` | Result is an expressly qualified approximation | Relevant issuer benchmark duration instead of ETF duration |

**Do not equate missing with N/A.** Cross-category rows may carry different relevant columns, and a single “overall winner” is not automatically meaningful when FX or credit risk assumptions differ. Comparisons are justified within the scope of the indicated aspect, compensation convention and scenarios. No weighted-average ranking is required.

This section defines a **result capability**, not a separate comparison calculation engine. The individual ETF calculations are the primary reusable unit.

## 10. Supplementary views

### 10.1 Bond-market data

A user may inspect the current 2Y/10Y levels, the full Treasury curve, historical slope changes, credit spread movements, or other supported market series before selecting a product. This uses **the same underlying data directly** and may help identify unusual developments worthy of an ETF examination.

These views describe market conditions without applying an ETF-specific investment objective or expressing a purchase recommendation.

### 10.2 ETF prices and realized performance

ETF price/NAV history must **not** enter the selection model, its weights, its factor exposures, or its calibration. An optional, separate diagnostic may compare past price/total-return behavior with the modeled exposure to identify unexplained differences. Discrepancies are flagged, **not used to quietly change the model**.

A later convenience screen may show appropriately distribution-adjusted ETF historical returns. Its label must distinguish **realized past performance** from *bond-market opportunity*. Detailed return attribution is not necessary for the core model.

## 11. User interface and implementation boundary

**User interface:** Jupyter `.ipynb` notebook(s), designed as a straightforward sequence: choose product universe and dates → load market data and issuer profiles → call functions → inspect tables/Plotly charts and conclusions. A notebook is for configuration, procedure and presentation, **not definitions of functions/classes or substantial calculation logic**.

**Python implementation:** Imported `.py` functions/classes encapsulate data acquisition/validation, ETF profile handling, conventional financial calculations, aspect applicability, historical evaluation and presentation helpers. Prefer a few cohesive modules to a large specialized framework. Avoid reconstructing ETF holdings.

**User-facing outputs:** (a) an ETF assessment for one product, (b) an ETF-universe table or aspect comparison with visible N/A/limitations, (c) a same-ETF time series with meaningful decomposed financial aspects, and (d) optional Treasury/credit-market charts. Show sources, disclosure dates, units, scenario assumptions, unsupported measures and reasons for conditional judgments. Convenient drilldown and Plotly hover information are appropriate.

**Independent tests:** Pure arithmetic and data-contract checks should run from Python without an interactive notebook session.

## 12. Minimum numerical and behavioral verification

Use clearly labeled synthetic numerical fixtures before drawing conclusions from actual ETFs:

| Fixture | Expected result |
|---|---:|
| ETF duration 8; hypothetical relevant rate shock +50 bp | `-4.00%` first-order price effect |
| Same with compatible convexity 80 | `-3.90%` second-order effect |
| Credit ETF spread duration 6; OAS shock +100 bp, no Treasury-rate shock | `-6.00%` spread-only price effect |
| Unhedged USD bond result -2%; USD/KRW rises +8% | `+5.84%` KRW scenario return |
| 2Y yield 4.0%; 10Y yield 4.5% | `+50 bp` 2s10s spread |
| Hypothetical historical 2s10s moves from -10 bp to +100 bp | `+110 bp` spread change, **before any ETF-specific inference** |

Specify an appropriate declared test tolerance (for simple non-extreme formula calculations, `1e-10` in decimal-return units is an initial computational tolerance, not a real-world economic accuracy guarantee).

Essential behavioral tests:

1. The same market series and ETF profile produce the same ETF results; optional market-only views do not change those results.
2. An ETF's reported duration is used for relevant shock sensitivity; market maturity or FRED 10Y yield is **never** silently treated as ETF duration.
3. A 2Y–10Y Treasury spread movement may be calculated without an ETF, but *risk-adjusted ETF conclusions* require actual issuer exposures and relevant mapping.
4. An ETF universe with a pure Treasury, a credit ETF and an opt-in future distinguishes `N/A`, `unavailable` and `unsupported` correctly.
5. Issuer yield convention/source dates are preserved; future issuer disclosures do not leak backward into historical opportunity series.
6. ETF prices/returns cannot affect assessment outputs, and present exposure applied to historical moves is not historical ETF P&L.
7. Same-ETF opportunity histories show actual changes in relevant market facts but do not report a changing +50 bp duration sensitivity if duration and the shock are held fixed.
8. Futures receive no fabricated cash-bond carry; missing credit/hedging inputs yield limited conclusions, not zero risk.
9. Enhanced formulas retain reproducible baselines and show relevant numerical differences and additional assumptions.
10. Scenario and relative-value conclusions never mislabel themselves forecasts or unconditional buy recommendations.

Unit tests establish formula and contract correctness, not profitable investment timing or universal investment attractiveness. Practical interpretability requires independent economic and user review.

## 13. Minimum research validation

**Status:** Proposed research assignment only; this document does **not** authorize Bernie to execute it. The exact bounded Work prompt and criteria require separate approval.

**Research question:** Can established bond financial measures, **computed directly using issuer-disclosed ETF exposures and relevant market series**, provide useful, verifiable insight into (i) the current differences among ETFs and (ii) how individual ETF opportunities have changed? Identify comparisons that cannot be concluded without additional economic assumptions.

The research must not optimize a composite score against historical ETF returns, select models based on the appearance of plots, or invent directional forecasts.

**Minimum illustrative scope:** Several real, dated Korean-listed U.S. cash-bond ETF profiles with diverse published durations; one relevant credit product if source and spread data permit; a user-selectable historical window such as one year; Treasury and OAS/FX data only when economically needed. Futures excluded by default. Actual ETF ticker choices are not fixed by the architecture.

**Required inspectable findings:**

1. Published ETF profiles and quality/as-of metadata, plus relevant market inputs (both directly visible).
2. Executed conventional formula tests and actual numerical rate/credit scenario examples with assumptions and units.
3. At least one continuous same-ETF market-opportunity history using the appropriate exposure/mapping conventions; explicitly identify counterfactual constant-profile results.
4. An aspect-by-aspect view across the selected ETF universe, showing valid values, nonapplicable cells and missing/unsupported calculations without invented scores.
5. At least one historical example where relative yield compensation changed materially, together with the precise limits of translating that market change into an ETF investment preference.
6. A compact discussion of what can be concluded from theory and documented inputs, what remains conditional, and what would require additional data or an investment objective.
7. An independent summary of which justified extra methods (if any) improved the explanation compared with the baseline, without automatically expanding scope.

**Research completion requires correct, reproducible calculations and a clear assessment of their usefulness and limits.** It does not require a universal attractiveness measure, a profitable backtest, or proof that buying beats waiting. Failure to establish a general ETF ranking can be a **valid economic finding**.

## 14. Unresolved research choices and revision path

- Is a separate, well-defined numerical aspect (e.g. additional yield compensation per extra duration or conditional break-even) sufficient for practical selection, without a universal score?
- What issuer-published yields are economically comparable to historical market yields, and when can carry estimates be stated without false precision?
- Which market factors best approximate ETFs with multi-tenor or complex active holdings when KRDs are not published?
- Which cross-maturity, cross-credit and hedged/unhedged comparisons remain conditional on risk preferences, scenario views or missing hedge/default information?
- How should recent/current issuer characteristics be shown across historical market windows without misleading point-in-time reconstructions?
- Which additional, conventional refinements actually improve **ETF-related** conclusions enough to justify their data and implementation costs?

**After** inspecting the minimal research, revise the architecture and the companion examples consistently. **The development roadmap will be discussed later**; no stage partition or implicit multi-stage authorization is created here.

## 15. References and research provenance

- [Companion examples — provisional and not yet aligned](bond_etf_decision_examples.md).
- [Earlier Bondview-v3 critical design review](bondview_v3_critical_design_review_20261013.md) — reference material, not an accepted roadmap.
- [FRED DGS10](https://fred.stlouisfed.org/series/DGS10), [FRED DEXKOUS](https://fred.stlouisfed.org/series/DEXKOUS), [FRED Treasury data](https://fred.stlouisfed.org/).
- [CFA Institute: fixed-income portfolio management](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/overview-fixed-income-portfolio-management), [yield-curve strategies](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-curve-strategies), [convexity](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-based-bond-convexity-and-portfolio-properties).

This document contains **no current ETF investment recommendation**. Live products, issuer characteristics, market inputs and disclosures must be verified at the observation date before producing any decision-support result.
