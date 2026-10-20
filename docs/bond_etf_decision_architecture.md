# Bondview-v3 — Korean-Listed U.S. Bond ETF Decision Architecture

**Status:** **PROVISIONAL research architecture — aspect-based revision, 2026-10-20.** Defines comparable financial measurements, conventional formulas, data contracts and bounded research requirements. Actual ETF coverage depends on applicability and appropriately dated issuer data. This is neither an implementation roadmap nor authorization to begin Work.

**Previous companion, reference only:** [`bond_etf_decision_examples.md`](bond_etf_decision_examples.md) retains exploratory visualizations and arithmetic fixtures from an earlier design iteration. **It is not an accepted specification, implementation acceptance test, or required chart set.** A new companion examples document should be constructed after this revised aspect contract is reviewed. Earlier Bondview repositories are likewise reference-only, not design authorities.

## 1. Purpose and requirements

### 1.1 Principal objective

Bondview-v3 is a **convenient decision-support tool for choosing Korean-listed ETFs with U.S. fixed-income exposure**. It analyzes the economic opportunities and risks of relevant bond exposures using conventional fixed-income relationships, observed U.S. bond-market data, and issuer-published ETF characteristics. It does not forecast ETF prices or select individual bonds for investment.

Each accepted **financial aspect** comprises one or more conventional, reproducible measures that can be meaningfully compared **across eligible ETFs** and **across dates**, subject to documented input, applicability and comparability conditions. A market-reference analysis can contextualize an aspect without constituting an ETF-level result; missing historical issuer information limits realizable comparisons rather than disqualifying a well-defined measure.

The **same financial definitions** support three ways of examining results, not three independent evaluation engines:

1. **At a selected date:** Examine the economically relevant compensation, rate/credit exposures, scenario risks, and changed conditions for an ETF.
2. **Through time:** For a selected ETF and date range, evaluate how the relevant financial measures evolve. Identify improving, deteriorating, and mixed evidence *by measure*, not by a fabricated aggregate score.
3. **Across ETFs:** Compare all eligible ETFs in a chosen universe across the same applicable financial measures and defensible relative-value relationships, including cross-maturity and suitable credit comparisons. Focused 1:1 comparison is a subset of this view.

The underlying models can also be investigated **at the bond-market reference level**, e.g. Treasury 2Y/10Y/30Y segments and matched corporate-credit spreads, without initially selecting particular ETFs. Such analysis tests the economic meaning of a measure and helps identify market developments worth examining in ETFs. It is **not a compulsory market-assessment stage or a separate investment-recommendation engine**; issuer exposure enters each ETF calculation directly when needed.

A product's reference yield and maturity name do not by themselves identify its duration or carry. ETF translation uses issuer-disclosed characteristics under the provenance and factor-matching rules in §5.

### 1.2 Out of scope

- Portfolio construction, asset allocation, personalized position sizing, holding optimization, trade execution, or an unconditional buy/sell timing engine.
- Recreating ETF holdings, individual-bond cash-flow portfolios, hedge books, futures collateral/roll economics, or historical ETF NAV as a general prerequisite.
- Independently auditing an issuer's portfolio or proving that its disclosed duration, credit mix or benchmark exposure exactly reproduces its actual holdings. The reliance on disclosed characteristics is an explicit scope limitation, not an unsolved research requirement.
- Predicting Treasury yields, credit spreads, currencies, ETF prices, or realized returns simply from their history.
- Using ETF price/return history to generate, weight, calibrate, or override ETF selection conclusions or infer undisclosed duration.
- Custom weighted-average attractiveness scores, ordinal state systems, or rules carried over from earlier Bondview repositories without independent economic justification.
- Detailed expense-ratio, tax, execution-cost or liquidity optimization in the initial bond-centered model; do not double-subtract costs already reflected in a published measure.

## 2. Analytical framework

Market observations and issuer-published ETF characteristics are inputs to **reusable, established financial measures**. Define a measure, its necessary inputs, its unit and the eligible comparisons before choosing tables or charts. Market-level analyses (such as 10Y-minus-2Y Treasury yields) can establish a conventional relationship without needing ETF facts; ETF-level measures (such as disclosed duration or a comparable ETF yield) add the relevant product characteristics without inventing an attractiveness score. Do not require an elaborate market-to-ETF analysis sequence.

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
                      - defined aspect measures and comparisons
                      - optional conditional scenarios / break-even
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

**Market-level reference:** The 10Y–2Y Treasury spread and its history require only observed 2Y and 10Y yields. Duration-based price sensitivity instead requires the duration of a **defined exposure**. A FRED constant-maturity tenor is a market yield series, not an investable bond or an ETF with a known portfolio duration. Market spreads must not be relabeled as ETF yield/carry differences.

**ETF-level calculation:** An ETF's rate-price sensitivity uses its **issuer-published duration** with an economically relevant yield scenario, `-D_ETF * delta_y_relevant`. A benchmark instrument's duration cannot silently stand in for the ETF's published portfolio duration; an issuer's `10Y` product label is not a duration of 10. Input provenance and suitability follow §5.2.

An economic relationship may be illustrated with benchmark segments and later applied to ETF data, but ETF evaluation does not depend on finishing a separate, categorical evaluation of the bond market. Comparisons across dates and products reuse the same definitions, with only justified relative calculations and date handling added.

## 3. Design principles and decision boundaries

1. **Operational aspects, not vague categories.** An accepted ETF evaluation aspect has at least one financially established, reproducible measure; defined units and inputs; and meaningful cross-ETF and historical comparison semantics where the necessary dated data exist. Market observations and eligibility controls are not evaluation aspects merely because they are useful.
2. **Market information and product exposure work together.** Yield levels, curve movements and OAS are market facts; an ETF's duration, credit type and hedge policy govern their instrument-specific implications. Bond-market reference analysis is useful but is not a substitute for exposure-aware calculations.
3. **Conventional, explicit mathematics.** State each measure's conventional formula or well-defined measurement rule, units, required inputs, scope and hand-checkable examples. A family can contain several related measures; no special aspect-attractiveness formula is needed.
4. **Separate observation, assumption and conclusion.** Distinguish market levels, disclosed product characteristics, calculated sensitivities, counterfactual scenarios, compensation proxies, and conditional investment preferences.
5. **Compare measures directly before constructing combinations.** Show economically established aspect outputs across products and time. Optional cross-aspect calculations (for example a conditional carry-versus-rate-move break-even) require a specific financial question and compatible assumptions; they are not primary measures, independent evidence or mandatory charts. No contest among legitimate measures or synthetic attractiveness index is required.
6. **No unsupported attractiveness scalar.** Do not infer a universal investment objective by fitting historical ETF prices, optimizing indicator weights, or making every outcome a single directional score. Mixed conclusions across meaningful measures are valid.
7. **Use issuer disclosures as authoritative operational inputs within scope.** Apply §5.2's provenance, definition and applicability checks; dependence on disclosed measurements is an acknowledged limitation, not a requirement for an independent portfolio audit.
8. **Keep economic interpretation within each measure's scope.** Higher yields or OAS can mean higher stated gross compensation **and** higher underlying risk. Separate yield observations, duration sensitivities and conditional scenarios rather than making any individual aspect a complete investment verdict.
9. **Keep complexity proportional to economic decision value.** Start with Treasury maturity and credit-market relationships rather than detailed ETF replication. Optional convexity, KRD, term-premium, currency/hedge or implementation modeling should have a concrete economic question and usable inputs; a theoretical improvement alone does not mandate a new workstream.
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

**Canonical-source and derivation rule:** Retrieve and store the underlying dated Treasury-tenor observations (initially FRED `DGS2`, `DGS10`, `DGS30`, and other needed `DGS*` series). Derive `y_10 - y_2`, `y_30 - y_10`, `y_30 - y_2`, dated yield changes, and comparable curve measures **from those aligned observations within Bondview**. A precomputed FRED spread such as `T10Y2Y` is not a separate primary input; it may be used only as an optional validation cross-check. Reuse the same source yields across aspects and views. Preserve input units (FRED quotes yields in percent) and convert explicitly for decimal-valued formulas; do not interpolate missing tenor observations simply to complete a spread.

Preserve source, dates, units, publication/cutoff and relevant retrieval/revision metadata; align information available at each historical assessment cutoff. Do not silently interpolate future issuer inputs or forward-fill unavailable market days. A full user-selected historical window is supported; specific smoothing, sampling and lookback periods are research conventions, not established financial laws.

**Historical yield variability** may be calculated from the same dated Treasury inputs under a declared change horizon, reference interval and sampling frequency; daily endpoints with overlapping multi-month changes are permitted. Define `delta_y_n,H(t) = y_n(t) - y_n(t-H)` using a declared business-day alignment convention, and summarize changes in bp where relevant. Rolling windows can be descriptive, but overlapping values are not independent episodes. When translating yield variability to a representative bond or ETF exposure, explicitly provide the compatible duration and factor mapping (§6.2). Neither market variability nor exposure-translated variability is a yield forecast.

### 5.2 Minimum issuer ETF profile

Use dated official issuer or official listing materials directly. **Treat issuer-published characteristics as the source of truth for Bondview's exposure inputs, without asserting that Bondview has audited the issuer's underlying portfolio.** Source checks should establish identity, definition, observation date, units and whether the disclosed measure matches the intended calculation. Do not recreate underlying holdings or infer duration by fitting ETF price returns.

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

Optional inputs: convexity, key-rate duration (KRD), spread duration, hedge coverage and other disclosed characteristics. Missing optional fields **do not** authorize holdings reconstruction. A benchmark proxy is permissible only when economically well matched and visibly labeled `proxy`, without implying the issuer reported it as a portfolio fact. If no suitable measure exists, omit the unsupported precision.

**Disclosure reliance boundary:** ETF characteristics may change between issuer updates, and published measures may use inconsistent definitions or incomplete representations of active exposures. Bondview records those limitations; it does **not** independently validate the issuer's measurements by reconstructing individual holdings, inferring factor loadings from ETF returns or auditing the issuer. Lack of such independent verification does **not** invalidate a clearly labeled calculation based on an official disclosed measure. Flag contradictions or implausible metadata when noticed, but do not turn their resolution into a general research obligation.

### 5.3 Matching market factors to exposures

Choose relevant market factors based on the ETF's **published investment mandate and exposure characteristics**, not merely its name; no independent holdings audit is presumed:

- For initial Treasury evaluations, match a disclosed duration with a defensible reference maturity segment and a **transparent single-factor approximation**. State any material term mismatch; do not equate a constant-maturity label with the ETF's numerical duration.
- For bond-market reference studies, Treasury 2Y/10Y/30Y yields and spreads are useful directly. Any duration-based benchmark scenario needs **explicit representative bond durations**, sourced or illustrative, not synthetic numbers silently derived from CMT labels.
- Published ETF KRDs may improve nonparallel yield-curve scenarios when available and relevant; they are a later refinement, **not** a requirement to reconstruct the ETF's holdings or underlying maturity weights.
- For corporate bonds, separate matched Treasury rate movements from changes in investment-grade or high-yield OAS. Where feasible, match rate duration, spread duration and market-index coverage. Broad OAS series are market proxies, not a precise credit decomposition for every ETF.
- Record FX exposure and hedge policy from issuer materials, but defer sophisticated hedge/FX scenario analysis from the immediate priority set. Never treat `(H)` as a perfect costless hedge.

The matched market factor and compatible exposure measure enter the same calculation. Market-only context is available without a selected ETF, but an ETF conclusion requires its relevant characteristics.

## 6. Baseline financial calculations

Every result distinguishes `market_observation`, `issuer_characteristic`, `derived_sensitivity`, `illustrative_assumption`, `proxy`, and `unavailable/unsupported`. Retain units, dated inputs, comparability conditions and interpretation. The following methods are a reusable analytical toolkit; **their presence does not require every calculation or a chart for every ETF**.

### 6.1 Treasury market yields and term compensation

For Treasury tenor `n` and two valid observations, `delta_y_n(t0,t1) = y_n(t1) - y_n(t0)`. Store yield values in a declared unit, preferably decimal for formulas; `1 bp = 0.0001` decimal yield. Convert FRED percentage quotations explicitly.

From matched underlying FRED tenor series (§5.1), compute:

- `term_spread_2_10(t) = y_10(t) - y_2(t)`;
- `term_spread_10_30(t) = y_30(t) - y_10(t)`;
- `term_spread_2_30(t) = y_30(t) - y_2(t)`.

Observe levels and differences over selected dates. Report changes in both endpoints when interpreting curve movement: a widening 10Y–2Y spread does not uniquely identify the cause or expected return. These are **market-reference** term-compensation measures; they do not directly equal two ETFs' published yields, nor do they measure their relative holding-period carry. At ETF level compare **compatible published ETF yield/carry measures** under §6.3, using tenor spreads as market context, not automatically as ETF attributes.

### 6.2 Interest-rate sensitivity and historical rate variability

**Interest-rate sensitivity (ETF level):** for compatible issuer-published effective/modified duration `D_i` and a matched, declared yield change `delta_y_i` (decimal), the conventional first-order price effect is:

`rate_price_effect_i ≈ -D_i * delta_y_i`.

Duration `D_i` itself is a comparable risk-exposure measurement when definitions are consistent. A declared **common rate shock** allows cross-ETF comparisons of first-order sensitivity; a suitably matched tenor-specific scenario may be used when the ETFs' risk factors differ. The approximate percentage price change for a +1 bp shock is `-D_i * 0.01%`; monetary DV01/BPV additionally requires a declared exposure market value. The shock assumption is not a predicted yield move.

Where valid issuer disclosures support them, conventional refinements include:

- Convexity: `rate_price_effect_i ≈ -D_i * delta_y_i + 0.5 * C_i * (delta_y_i)^2`;
- Nonparallel curve scenarios: `rate_price_effect_i ≈ -sum_k(KRD_i,k * delta_y_k)` using compatible **published key-rate durations**.

Do not double-count parallel duration and KRD contributions to the same shock. For market-only bond illustrations, duration must refer to a **defined representative bond exposure** and be sourced or overtly assumed, never inferred mechanically from a 2Y/10Y/30Y CMT label.

**Interest-rate variability (separate ETF aspect, with market context):** calculate horizon-matched historical yield changes from the dated underlying market series and describe their range, dispersion, quantiles and evolution. For a specific compatible ETF exposure, applying the **same** matched historical factor changes through the duration formula above yields a distribution/time series of approximate **rate-driven price effects**. If the duration belongs to the current ETF disclosure rather than to each past date, label this a **current-exposure historical counterfactual**, not historical ETF prices, total returns or past portfolio exposure. Direct ETF-to-ETF variability comparisons require compatible factor mapping, durations and declared horizons. Market-only yield dispersion is reference context, not a substitute for these ETF-level results.

If examining a long-minus-short pair with matched horizon `H`, the **modeled price-effect difference** is simply:

`price_effect_L_minus_S ≈ -D_L * delta_y_L,H + D_S * delta_y_S,H`.

Its opposite sign describes the additional relative rate-price *loss* (when positive); neither version is a separately standardized attractiveness signal. Nonparallel yield changes are allowed and need not be turned into a break-even comparison. Select daily, weekly or monthly endpoints by descriptive purpose; dense rolling observations are correlated and do not justify a predictive probability claim.

Holding duration and a fixed +50 bp shock constant produces **unchanged sensitivity across time**; it is not an evolving economic condition. Genuine histories require changing observed factor moves and/or legitimately dated changing issuer exposures, with the measurement convention identified.

### 6.3 ETF yield/carry compensation and optional conditional break-even

Distinguish three economically different inputs/outputs:

1. **Market yield and term-spread references:** observed Treasury levels and internally derived spreads (§6.1), not an ETF's portfolio yield or holding-period result.
2. **Comparable published ETF yield measures:** issuer value with its exact portfolio, benchmark, SEC, YTM/YTW or distribution-yield definition and as-of date. Only compare genuinely compatible measures; the difference in two properly comparable ETF yields is itself a valid cross-ETF measurement.
3. **Holding-period carry and roll-down:** conventional income/financing and curve-position effects over a stated horizon, **only where supported by product structure and sufficient inputs**. Report carry and roll separately if they can be estimated soundly; do not require a complete carry/roll model for every ETF.

Distribution yield is not automatically portfolio carry or YTM. A constant-duration ETF does not mechanically realize the roll-down of an individually held bond approaching maturity. Gross USD Treasury yield differences are not automatically comparable net KRW ETF compensation.

For a compatible cash-bond exposure under explicit assumptions, a *partial illustrative return decomposition* may be written:

`illustrative_H_result ≈ defensible_H_carry + justified_H_roll + rate_price_effect + supported_credit_effect`.

A missing material component cannot silently become zero in a purported complete return. Use separately measured inputs when the combined quantity is not defensible.

**Optional break-even calculations:** These are algebraic conditional offsets using conventional compensation and duration inputs, not separate aspects, scores or mandatory historical series:

- A single exposure versus compatible cash: `break_even_rise_bp ≈ 10,000 * (defensible_H_carry - comparable_cash_return_H) / D`, for `D > 0` and matched horizon/currency.
- Long versus short under an explicitly **common parallel yield increase**: `relative_break_even_bp ≈ 10,000 * (c_L,H - c_S,H) / (D_L - D_S)`, for comparable horizon compensation `c_L,H`, `c_S,H` and `D_L > D_S`.

Both use first-order duration approximations and exclude unsupported convexity, roll, financing, hedging and other effects. A positive threshold answers **how large the assumed yield increase may be before the specified compensation advantage is offset**, *if* the defined shock and compensation assumptions hold. It says nothing about the likelihood or representativeness of a parallel move. Tenor-specific/nonparallel changes require their own price-effect calculation; there is no universal single break-even yield increase in that case.

A market-only example may *illustrate* the formula with observed Treasury yields in place of period carry and representative durations, but this is a **strong market-yield proxy**, not actual ETF carry, a validated ETF selection metric or an accepted default calculation. Such a proxy is optional, should be clearly identified and is **not required to produce a historical break-even chart**. With fixed durations, its historical series is a deterministic rescaling of the same yield-spread series, not independent evidence.

### 6.4 Credit and spread exposure

For comparable bond-market references:

`delta_y_corporate ≈ delta_y_matched_Treasury + delta_OAS`.

For compatible rate and spread sensitivities:

`credit_exposure_price_effect ≈ -D_rates * delta_y_matched_Treasury - D_spread * delta_OAS`.

Separating rate and credit components helps answer **whether the corporate market moved adversely because of Treasury rates or credit-specific repricing**. For example, a stable/falling Treasury yield alongside a widening corporate OAS isolates credit-spread deterioration; a negative *Treasury-rate contribution* alone does **not** prove corporate credit distress. Widening OAS may reflect default expectations, liquidity, risk appetite or required risk premiums; **it is a warning/context, not proof of realized fundamental credit deterioration**.

Market OAS levels and changes are credit-market context; ETF-level credit comparisons use comparable published credit exposure/spread data and, when supportable, published spread duration with a matched spread shock. A spread-only sensitivity is a conventional, separately interpretable measure; it does not need an additional spread-cushion or attractiveness formula. Optional gross spread-cushion calculations require a defensible period compensation assumption and do not incorporate defaults, migration, liquidity or optionality automatically. Choose credit benchmarks compatible with the exposure or label them proxies. Never apply a pure-Treasury conclusion to material unassessed corporate credit exposure.

When the interpretation requires it, **optional corroborating public evidence** may include default rates, rating migration, credit-quality trends, financing/liquidity indicators, or lending-standard surveys. These indicators may help distinguish fundamental deterioration from changes in liquidity or the required risk premium, but none automatically proves causation or forecasts losses. Initial Treasury/OAS decomposition **does not depend** on collecting a comprehensive credit-fundamentals dataset; in its absence explicitly limit the conclusion to **credit-specific repricing**, not established default deterioration or attractive risk-adjusted net carry.

### 6.5 Currency and hedge qualification — lower analytical priority

For consistently defined **unhedged** USD bond returns and USD/KRW returns:

`1 + R_KRW = (1 + R_USD) * (1 + R_USDKRW)`.

This is an accounting identity or declared scenario, not an FX prediction. At ETF level, compare **documented currency exposure / hedge coverage** at comparable dates when quantitative disclosures exist; a disclosed hedge policy alone is an eligibility/qualification attribute, not a fabricated numerical currency-risk measure. For applicable unhedged exposure, a common declared USD/KRW scenario permits a comparable sensitivity calculation. Do **not** presume a perfect free hedge or generate net hedged-KRW compensation without adequate inputs. Detailed currency/hedge economics are lower priority, and the quantitative currency aspect remains conditional on available compatible inputs.

### 6.6 Model refinements

These relationships define the **minimum conventional baselines**, not limits on mathematical accuracy. An established refinement (e.g. disclosed convexity, published KRD or improved period matching) may be used when it answers a relevant question, has credible inputs, keeps the baseline reproducible and justifies the added complexity. If it changes a scenario conclusion materially, show both the baseline and refinement and explain why; **do not require a fixed numerical threshold or empirical victory over every simpler calculation**. An analysis of a genuinely different economic question may be retained independently rather than classified as a replacement model.

An enhancement need not preserve every baseline conclusion, but material changes in the economic question, investment objective, source authority or aggregation/ranking logic require an explicit design decision rather than a silent model substitution. Revise established formulas or data contracts for demonstrated economic or numerical defects, justified material improvements with defensible inputs, or a separately accepted change of purpose—not merely because a complementary analysis is added.

## 7. Evaluation aspects and comparison contracts

**Definition.** An ETF evaluation **aspect** is an economically interpretable dimension represented by **one or more established, reproducible measures**, not merely a topic heading. For each measure specify: (i) the fixed-income question, (ii) formula or measurement rule and units, (iii) required market and issuer data, (iv) comparable eligible ETF exposures/conventions, and (v) the meaning of a selected-date and a historical comparison. Dated data gaps or inapplicable products may limit realizable outputs without invalidating the definition. A measure should not require a custom attractiveness score or arbitrary scale.

**Provisional financial aspects (not a fixed five-score model):**

| Aspect and financial question | ETF-level measurements / conventional rules | Reusable market context and comparability conditions |
|---|---|---|
| **1. Yield and compensation:** What income/yield compensation does the exposure offer? | Compatible issuer-published yield levels and differences; defensible holding-period carry and roll only where supported (§6.3). Compare same yield conventions and dates. | Treasury yields and internally derived tenor spreads (§6.1) describe **market** term compensation; they are not automatically ETF yield/carry. |
| **2. Interest-rate sensitivity:** How sensitive is the exposure to changing rates? | Dated published duration; first-order `-D_i * delta_y_i` under a common or appropriately matched declared shock; optional supported DV01, convexity, KRD (§6.2). | The factor and scenario must be compatible across products; Treasury tenor labels do not supply durations. |
| **3. Interest-rate variability:** How large and variable have applicable rate movements been over a specified historical horizon? | Dated matched yield changes applied to supported ETF durations produce rate-driven price-effect histories and distributions (§6.2). Clearly distinguish point-in-time exposures from current-exposure counterfactuals. | Historical yield-change dispersion by tenor is market reference data. Specify change horizon, lookback, sampling frequency and factor matching; overlapping rolling windows are correlated. |
| **4. Credit compensation and risk:** What credit spread and repricing exposure is present? | Comparable published credit characteristics/spreads when valid; rate-versus-credit contributions and `-D_spread * delta_OAS` where suitable spread duration and factors exist (§6.4). | Market OAS level/change and matched Treasury/OAS divergence contextualize credit, but OAS is not an ETF-specific spread or default-adjusted expected return. N/A for pure Treasury exposures. |
| **5. Currency exposure and hedging (lower-priority/conditional):** How does currency/hedge structure affect comparison? | Dated quantitative currency exposure/hedge coverage if published; compatible common FX sensitivity for eligible unhedged exposures (§6.5). | FX series supplies scenarios/reference. Hedge-policy labels alone are product controls, not numeric scores; net hedged-KRW comparison requires separate supported economics. |

**Inputs and controls, not evaluation aspects:** raw market-rate levels/changes as standalone data feeds; ticker, structure, benchmark, eligibility, issuer-source dates, missing values, and confidence/proxy flags. They enable reliable calculation and explain N/A/unavailable/unsupported outcomes. Market-only results remain legitimate **reference analyses** even when an ETF-level aspect result is unavailable.

One aspect can include several established measures, each compared in its own units; shared inputs may be reused without implying independent corroboration. Likewise, one financial question may draw on more than one aspect, but no combined score, conditional-break-even metric, or particular visualization is required to qualify an aspect. Adding or subdividing aspects later requires a distinct economic question and comparable ETF outputs, not numerical symmetry or a target count. Convexity and KRD remain within interest-rate sensitivity, while carry and roll are explicit components of yield/compensation where supportable; model-dependent term premium and real-yield/inflation analysis are optional later candidates, not automatic new aspects.

**Interpretation:** report what improved, deteriorated or differed **on the stated measure**, and what evidence would be needed for a stronger conclusion. Example: a 10Y–2Y Treasury spread can widen while a longer ETF retains greater interest-rate sensitivity. Neither observation needs to be converted into an integrated attractiveness scalar. A conditional break-even (§6.3) can answer a specific what-if question without becoming a mandatory series or aspect.

## 8. Historical and cross-ETF comparability

Apply **the same financial measure** at a selected date, across eligible ETFs at a matched assessment date, and through a user-selected period **when compatible dated inputs exist**. The calculation definition is shared; the underlying ETF exposure history must not be invented to fill gaps. Market-level tenor comparisons can use the same underlying FRED yield inputs but do not replace ETF-specific calculations.

- **Yield/term compensation:** derive historical Treasury yield-spread curves from aligned underlying tenors; for ETFs compare the *same type* of issuer yield or carry only at dates where compatible disclosures exist. Do not infer ETF yield history from today's facts or treat a market spread as the ETF's actual incremental income.
- **Rate sensitivity:** compare disclosed durations and/or price effects under the same compatible shock. Holding one duration and shock fixed creates a constant result, not evidence of changing conditions. If exposures differ in factor mapping, specify the matching instead of applying a spurious universal shock.
- **Rate variability:** quantify actual historical changes in relevant Treasury yields over a stated horizon, and translate them to ETFs using supported exposures. A fixed current duration applied to past factor changes is a **current-exposure counterfactual**, not historical ETF realized P&L. With time-varying issuer data, respect their availability dates and definitions.
- **Credit:** compare appropriate credit-market OAS histories, ETF credit/spread inputs and supported sensitivity effects across dates/exposures. Distinguish spread repricing from proven defaults or changes in fundamentals.
- **Currency:** compare dated hedge coverage or applicable unhedged FX sensitivity when inputs and currency definitions permit. Missing hedge economics means a net KRW comparison is unavailable, not zero.

Daily sampling is possible and computationally modest, but it is not mandated; distinguish **observation frequency**, **yield-change horizon** and **historical reference interval**. Consecutive rolling windows overlap. More years of observations need not represent the current regime better; choose the reference range for the descriptive purpose and report it. Do not mistake the historical sample for a forward probability or calculate scenario frequencies merely because a histogram exists.

Construct **tables and charts only when their numerical measure and comparison question are clear**. Plot full relevant time series rather than cherry-picked endpoints, without requiring one chart per aspect or a particular chart type. A yield spread rescaled by fixed durations is not independent information. Optional conditional-break-even calculations (§6.3) can be shown at a selected date if useful, but a historical break-even plot is **not mandatory**. No comparative measure must prove superiority to another established measure, and no selected-date/history/ETF-universe view is a separate attractiveness engine.

A valid output may identify an improving yield spread, higher duration sensitivity, worsening spread risk, mixed results or insufficient comparable ETF information. It need not establish a universal preferred product. The purpose of aspects is **comparable financial evidence**, not an unexplained verdict.

## 9. ETF universe and comparative results

The selected ETF universe may contain many products; **selected-date, historical and cross-universe views reuse the same aspect definitions and calculation paths**. A 1:1 comparison is a focused presentation of the universe results. Pairwise conditional calculations (including optional break-even) are secondary, require compatible inputs, and are not a separate ranking engine.

For each financially relevant result, distinguish:

| Status | Meaning | Example |
|---|---|---|
| `value` | Supported numerical or descriptive result under recorded conventions | Rate sensitivity of an ETF with published duration |
| `not_applicable` (`N/A`) | Economic mechanism does not apply | Corporate credit OAS for a verified pure Treasury ETF |
| `unavailable` | Applicable but material market/issuer data are missing | No usable portfolio duration disclosed |
| `unsupported` | The baseline model is structurally unsuitable | Cash-bond carry applied to Treasury futures |
| `proxy` / `limited_confidence` | Clearly declared approximation with limitations | Matched benchmark duration in an explicitly provisional scenario |

Comparisons should answer the **defined question of the aspect measure**, such as issuer-duration sensitivity under a declared shock, matched ETF yield differences, or supported credit-spread sensitivity. Each output records its units, data dates and comparability conditions. No minimum aspect count, required chart inventory or composite ranking is implied.

The same measure can be compared over time and across **eligible ETFs with compatible inputs**. Do not claim comparability across mismatched currency-net returns, maturity proxies, issuer-yield definitions, credit-quality segments or unobservable carry. A product may remain in the universe while particular aspect values are N/A/unavailable/unsupported. Historical issuer-data gaps are disclosed, not backfilled with current facts. No overall winner need be established.

## 10. Supplementary views

### 10.1 Bond-market references

Users may inspect current and historical Treasury 2Y/10Y/30Y yields, internally derived spreads and relevant credit OAS **without first selecting an ETF**. These are legitimate market-reference comparisons; optional defined-exposure sensitivity and conditional break-even calculations may be displayed when they answer a specific question, but a benchmark-duration break-even history is not privileged or required.

These optional reference views reuse existing market data and conventional calculations. They do not constitute an independent mandatory market evaluation stage or an unconditional purchase recommendation. A simple tenor-yield chart can remain a diagnostic; more important user-facing analysis should explain **compensation, risk and their evolution**.

### 10.2 ETF prices and realized performance

ETF price/NAV history must **not** enter the ETF selection model, its weights, factor exposures, or calibration. A separate diagnostic may compare realized total-return behavior with published exposure estimates to flag unexplained differences; those observations do **not** silently update selection signals.

A later convenience view may compare appropriately distribution-adjusted historical ETF returns, labeled clearly as **realized performance** rather than bond-market opportunity. Detailed NAV attribution is not required by the core model.

## 11. User interface and implementation boundary

**User interface:** One or more Jupyter `.ipynb` notebooks, organized as easy sequential workflows: select dates/products/market references → load market data and issuer profiles → call imported analytical functions → inspect tables, clear explanations and interactive Plotly charts where useful. The notebooks contain **no substantive function or class definitions**.

**Implementation:** A small collection of cohesive Python `.py` modules implements data acquisition/validation, issuer profiles, applicable bond financial calculations, historical evaluation and optional plotting helpers. One reusable calculation model supports selected-date results, time series and universe-wide comparisons. Add comparison helpers only for legitimate *relative financial calculations*, not separate competing engines.

**Output standard:** Show the economic question, underlying observations, ETF exposure when applicable, quantitative result, dates/units, assumptions/proxies, relevant counterevidence and limitations. A result may be visualized historically, across products, or in both ways whenever it is genuinely informative. Do **not** produce one chart per candidate family by default; do not repeat unchanged fixed-shock sensitivity or near-identical line shifts merely to display more figures.

**Optional views:** Market-reference tables/charts can be used before an ETF is selected; ETF realized performance remains outside the decision model.

**Verification:** Pure calculation and data-contract tests run from Python without interactive notebook execution. Build a **new** companion examples set from the accepted aspect measures, comparing tenors, time and eligible ETF profiles as each measure permits. The previous examples document is reference material, not a specification for the replacement charts or an implementation acceptance contract.

## 12. Minimum numerical and behavioral verification

Use clearly labeled **constructed** financial fixtures and independent numerical checks before interpreting live ETF data. Prioritize correctness of aspect measures and their comparison contracts; **optional conditional formulas** can be tested without becoming required charts.

| Fixture | Expected result / interpretation |
|---|---|
| Underlying Treasury yields 2Y `4.0%`, 10Y `4.5%`, 30Y `4.8%` | Internally derived 10Y–2Y `+50 bp`, 30Y–10Y `+30 bp`, 30Y–2Y `+80 bp`; all from the same aligned raw-tenor inputs |
| Historical 10Y–2Y spread `−10 bp` to `+100 bp` | `+110 bp` market term-compensation change, not an ETF-specific yield/carry change |
| Two eligible ETFs with compatible disclosed durations `D_A=6.5`, `D_B=15`, common `+50 bp` shock | First-order price effects `−3.25%` and `−7.50%`, respectively; the difference is a conditional sensitivity comparison |
| ETF duration `D=8`, rate shock `+50 bp` | `−4.00%` first-order price sensitivity |
| Same with compatible convexity `C=80` | `−3.90%` second-order result (optional refinement) |
| Matched six-month 10Y yield change `+10 bp`, 2Y change `+20 bp` with stated representative durations `D_10=7.5`, `D_2=1.9` | Modeled 10Y-minus-2Y rate-price effect `−7.5(0.001)+1.9(0.002)=−0.0037` = `−0.37 pp`; not total ETF performance |
| Spread duration `6`, OAS shock `+100 bp`, no Treasury-rate move | `−6.00%` spread-only price sensitivity |
| Credit rate duration `5.5`, spread duration `5`, Treasury change `−20 bp`, OAS change `+60 bp` | `+1.10%` Treasury component, `−3.00%` spread component, `−1.90%` combined; no inference of proven defaults |
| Unhedged USD result `−2%`, USD/KRW rise `+8%` | `(0.98 * 1.08) - 1 = +5.84%` conditional KRW result; not an estimate for hedged products |
| **Optional conditional** relative break-even: comparable one-year compensation difference `+1.00 pp`, durations `7.5` and `1.9`, common parallel yield increase | Break-even `17.86 bp`; arithmetic scenario illustration only, not a mandated historical series, ETF carry estimate or attractiveness score |

Calculated values are rounded for display. Define unit-test tolerances against unrounded decimal computations; `1e−10` in decimal-return units can serve for elementary arithmetic checks but is not a bound on economic approximation error.

**Behavioral invariants:**

1. Every accepted aspect has a defined measure, formula or measurement rule, units, eligibility and ETF/time comparability conditions; measures are computed identically in selected-date, historical and universe views.
2. Treasury yields are sourced by tenor and reused. Derived spreads must equal arithmetic differences of aligned `DGS*` inputs; a precomputed FRED spread is not a separate primary dependency. Source units and missing-day alignment are explicit.
3. Market-only tenor relationships can be studied independently, but market spreads cannot silently become ETF portfolio yield/carry measurements. ETF sensitivity requires published compatible duration or an overtly declared proxy, not a maturity name.
4. A fixed duration and fixed shock yield unchanged price sensitivity over time. A historical yield-change series with fixed current duration is a labeled counterfactual rather than historical ETF P&L.
5. Historical rate variability specifies yield-change horizon, reference interval, sampling convention, and factor mapping; rolling observations are not assumed independent. No historical sample becomes an objective future probability.
6. Compensation, roll and yield conventions are not interchanged. Comparable published ETF yields may be compared where valid; unsupported ETF carry, hedge costs or roll-down are not manufactured.
7. Credit OAS market context and ETF spread risk are distinct; rate and spread effects are separated where relevant. Widening OAS is not proof of realized credit deterioration.
8. Currency and product eligibility control N/A/unavailable/unsupported/proxy reporting. No futures cash carry, costless hedge or incompatible cross-currency net-return comparison is fabricated.
9. Dated issuer measurements are used only after their availability dates, with explicit gaps. ETF price/return histories never drive selection measurements.
10. Break-even remains optional conditional arithmetic. Neither a historical duration-normalized break-even plot nor a composite attractiveness score is required; all conditional scenarios declare their assumptions.

Tests establish arithmetic and documented measurement behavior, not trading success. Independent economic review checks whether the comparisons mean what their labels claim.

## 13. Minimum research validation

**Status:** This is a proposed **bounded research question**, not authorization to execute Bernie Work. A separately accepted assignment is required and no development roadmap is implied.

**Research question:** Can established, comparable financial aspect measures describe changing U.S. Treasury/credit conditions and support meaningful comparisons of eligible Korean-listed U.S. bond ETFs **without constructing special attractiveness scores, mandatory composite metrics or detailed replication models**?

Begin with established **bond-market reference measurements** (e.g. 2Y/10Y/30Y yields and internally derived tenor spreads) using actual dated market histories. Demonstrate conventional calculations at the tenor level first, then use a small set of official ETF issuer profiles to establish which aspect measures are comparable between products; this is a research order, not two independent evaluation stages. Do not start by optimizing the appearance of a chart or by requiring unsupported detailed ETF holdings. Appropriate credit-market analysis should be included where source quality permits; currency/hedge modeling and KRD refinements remain lower priority.

**Required inspectable findings for an eventual authorized experiment:**

1. Canonical dated FRED Treasury tenor inputs and relevant OAS histories, with source, units, date alignment, and at least one internally derived tenor-spread history; issuer ETF profiles with dated characteristics, provenance and eligibility checks.
2. **Yield/compensation aspect:** a defined tenor-level comparison through time and, for eligible ETFs with comparable disclosures, a cross-ETF yield/carry comparison. Show market-to-ETF differences honestly rather than manufacturing ETF compensation from benchmark yields.
3. **Rate sensitivity aspect:** at least one conventional duration-based scenario comparison for defined representative market exposures and, where issuer data permit, multiple eligible ETF exposures. Describe how the measure would evolve with dated characteristics, without plotting false time variation from unchanged durations and shocks.
4. **Historical rate variability aspect:** a separate, interpretable measure of historical yield-change magnitude and, where defensible, its translation to an ETF exposure using declared factor/duration conventions. Time series and distribution are optional views, not independent mandatory models or future probabilities.
5. **Credit aspect:** a matched Treasury/OAS divergence measurement and a conventional, supported credit-spread exposure/sensitivity comparison when suitable ETF inputs exist. Differentiate OAS repricing from fundamental credit losses. Document currency-policy qualifications; quantify currency sensitivity only if a valid currency aspect is feasible.
6. Demonstrated **comparison semantics**: for each evaluated aspect, named inputs, formulas, units, one-date interpretation, relevant cross-ETF comparison, and temporal application or explicit historical unavailability. Use `value`, `N/A`, `unavailable`, `unsupported`, and `proxy` meaningfully instead of inventing missing numeric outputs.
7. Reproducible formula fixtures, source/date alignment checks, conventional refinements where justified, and evidence that ETF price histories do not influence financial aspect results. Explain economic interpretation without requiring a performance contest among established measures.

**Research completion:** Economically justified calculations, sourced compatible inputs, reproducible results, and candid limits on unavailable ETF measurements. Completion **does not require** a historical relative break-even series, a composite score, a validated best ETF, a profitable backtest, issuer-holdings auditing, or full net holding-period-return reconstruction. A conditional break-even may be included when its question and assumptions justify it. Create **new examples consistent with the reviewed aspect architecture**; the existing examples are references only. The user/Archie must review the intended interpretation and presentation before any separately authorized development work.

## 14. Open research questions and deferred analyses

The financial methods and scope boundaries in §§1–13 are the current architecture. The following questions concern **data availability, applicability and the strength of possible investment conclusions**, not a requirement to resolve every product-specific uncertainty before useful analysis can proceed.

1. **Comparable ETF holding-period compensation.** Which published yield definitions and available product information support genuinely comparable ETF carry or horizon-return assumptions, especially across hedged/unhedged and active products? **Current approach:** retain observed Treasury-market term comparisons and separately supported ETF yield/carry measures and sensitivities; mark unsupported ETF holding-period carry, roll-down and optional break-even outputs unavailable rather than constructing them from benchmark yields. Revisit only for actual products with sufficient compatible disclosures.

2. **Factor matching for complex or mixed exposures.** For which active, multi-tenor or mixed-credit ETFs does a single Treasury tenor or broad credit-index proxy omit economically important exposure? **Current approach:** use issuer-reported profile information and qualified proxies where defensible, or limit precision when not. Independent holdings reconstruction, disclosure auditing and historical NAV regressions are outside scope. Revisit when a concrete ETF comparison cannot be represented credibly by available published measures.

3. **Interpretation of corporate-credit compensation.** When OAS widens, how far can accompanying public default, rating, lending and liquidity evidence support a stronger claim about underlying credit deterioration or compensation adequacy? **Current approach:** report Treasury/OAS divergence, gross spread compensation and scenario sensitivity without equating widening spreads with proven fundamentals or net expected return. Add corroboration only when stronger claims are needed and the evidence is available.

4. **Value and feasibility of optional model refinements.** When would reported convexity, KRD, credible term-premium estimates, or detailed hedge/implementation economics materially change a practical comparison? **Current approach:** preserve the first-order and observed-market baselines. Treat published convexity/KRD and externally sourced term-premium estimates as optional, and defer detailed FX/hedge and implementation modeling. Revisit a refinement for a specific economic question with compatible inputs; do not require a universal materiality threshold or a competition among independently useful analyses.

These questions are **conditional research directions, not mandatory workstreams or acceptance gates**. Section 13 defines the proposed minimum-research boundary; a separate assignment is needed to start that work. No development roadmap or Work authorization is established here.

## 15. References and research provenance

- [Earlier companion examples — exploratory calculations and visualizations; reference only pending replacement](bond_etf_decision_examples.md).
- [Earlier Bondview-v3 critical design review](bondview_v3_critical_design_review_20261013.md) — reference material, not an accepted roadmap.
- [FRED DGS2](https://fred.stlouisfed.org/series/DGS2), [FRED DGS10](https://fred.stlouisfed.org/series/DGS10), [FRED DGS30](https://fred.stlouisfed.org/series/DGS30), [FRED DEXKOUS](https://fred.stlouisfed.org/series/DEXKOUS). Derive Treasury term spreads from the dated tenor inputs.
- [CFA Institute: fixed-income portfolio management](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/overview-fixed-income-portfolio-management), [yield-curve strategies](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-curve-strategies), [convexity](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-based-bond-convexity-and-portfolio-properties).

This document contains **no current ETF investment recommendation**. Before producing decision-support results, establish the official sources, disclosure dates, definitions, factor compatibility and market cutoffs. This is **source and input validation, not a claim that Bondview independently verified the issuer's underlying holdings or financial reporting**.
