# Bondview-v3 — U.S. Bond ETF Decision Architecture

**Status:** **PROVISIONAL design — 2026-10-22.** Revised locally from `lbk209/bondview-v3`, branch `analysis`, `docs/bond_etf_decision_architecture.md` (verified source Git blob `086f200f7f8d56f2cc788a5c5e1c46341001e2eb`). Subject to design review before implementation authorization.

**Companion:** [`bond_etf_decision_examples.md`](bond_etf_decision_examples.md) is a provisional analysis-based companion with an initial 3A example; it requires consistency review against subsequent architecture revisions. Earlier Bondview repositories are reference-only.

## 1. Purpose, scope, and design position

### 1.1 Investment purpose

Bondview-v3 supports practical consideration of **Korean-listed ETFs exposed to U.S. bonds**—initially cash U.S. Treasury ETFs with different maturity exposures, extending to suitable U.S. corporate-bond ETFs. The tool should answer useful financial questions **across eligible tenors or ETFs, across assessment dates, and under relevant market conditions**, using established fixed-income methods and the ETF exposures disclosed by their issuers.

The output consists of **complementary quantitative fixed-income analyses**, not a weighted attractiveness score or rule-driven buy/sell classifier. Favorable relative outcomes may be reported when they follow from compatible calculations and defined market conditions.

The five **Fixed-Income Analyses** organize financial questions; they may share inputs, formulas and intermediate results. An analysis is not required to be an independent model or software module.

### 1.2 Analytical starting point

Begin with conventional studies of defined 2Y, 10Y, and 30Y Treasury exposure alternatives and relevant market factors, then apply compatible calculations to selected ETF or benchmark exposure profiles. Use the same financial definitions with appropriate product-specific inputs.

The two initial primary decision-oriented analyses are **A. Holding-Period Return** and **B. Risk and Stress**. **C. Yield-Curve and Carry** and **D. Credit Spread** retain separate financial information that may inform A/B but also warrants examination in its own right. **E. Currency and Hedging** is relevant but has a lower initial modeling priority. This is a priority order, not a required number of outputs or prescribed software hierarchy.

### 1.3 Design-review checkpoints

Apply these questions when proposing or revising a financial method; they are **review criteria**, not additional calculation stages or mandatory independent analyses:

1. **Established economic basis:** Is the method recognized in fixed-income theory or professional practice, with its assumptions stated? Compare established alternatives before proposing custom calculations or heuristics.
2. **Exposure applicability:** Is the method compatible with the instrument or ETF structure, factor definitions, disclosed characteristics and available data?
3. **Investment relevance:** Does it answer a defined financial question with interpretable quantities useful for tenor/ETF comparison or examination across dates?
4. **Incremental information or robustness:** Does it add a useful financial perspective, a compatible decomposition, or a defensible alternative approximation of the same quantity? Different methods need not produce independent evidence.
5. **Practical informativeness:** Are the results meaningful for the intended decision support? Do not confuse inability to predict subsequent market movements with lack of investment value: conditional outcomes, market decompositions, relative comparisons and risk measures can inform judgment without forecasting prices. Distinguish an uninformative example from a limitation of the method itself, and do not add complexity without corresponding value.

### 1.4 Boundaries

Bondview evaluates **defined financial exposures and observed market movements** using established fixed-income methods. Its comparisons are conditional on the specified inputs and do not constitute automated trading decisions; estimating the market's subsequent path is outside the initial scope.

- Do **not** construct bespoke states, factor weights, aggregate attractiveness scores, or rules that map market observations into buy/sell stances.
- Use ETF and benchmark price/NAV and total-return histories only as **separate diagnostics**. Do not use those realized returns to determine modeled selection outputs, replace holding-period baseline compensation, or infer undisclosed exposures.
- Do **not** require independent auditing or reconstruction of constituent holdings, cash flows, hedge books or futures-contract economics; apply only the models justified by the selected exposure data.
- Portfolio optimization, investor-specific position sizing, trading execution, taxes and detailed expense-ratio optimization are outside the initial scope. Avoid double counting any costs already reflected in an input.
- A maturity label alone does not establish an ETF's duration, carry or cash flows.

## 2. Data, ETF exposure, and comparability contracts

These are **input and measurement rules**, not a separate financial analysis or a catalog of preassigned mathematical functions. Each analysis in §3 identifies the inputs it actually needs.

### 2.1 Canonical market observations

| Data | Preferred initial source / treatment | Intended analytical role |
|---|---|---|
| U.S. Treasury constant-maturity yields | FRED/H.15 `DGS2`, `DGS5`, `DGS10`, `DGS30`, other `DGS*` series when justified | Dated yield levels, changes, curve comparisons and joint rate scenarios |
| Investment-grade and high-yield credit OAS | Matched, documented ICE BofA/FRED or justified alternative | Credit compensation context, credit-specific repricing and conditional spread scenarios |
| USD/KRW (KRW per USD) | FRED `DEXKOUS` or documented suitable alternative | FX context and conditional unhedged KRW outcomes |
| Cash/short-rate comparator | Clearly specified currency-compatible reference when needed | Cash-relative holding-period comparisons |
| Published Treasury term-premium decompositions | Credible documented models, initially e.g. New York Fed ACM or San Francisco Fed Christensen–Rudebusch | Interpret compatible model-implied yield, expected short-rate and term-premium levels/changes in 3C; estimates, not observed returns or independent cash compensation |
| Real yields and inflation-expectation series | Optional credible sources | Additional interpretation only if a specific analysis benefits |

**Canonical factor rule:** Fetch and retain underlying dated Treasury tenor yields. Derive spreads, curve changes, horizon yield changes and joint scenario vectors **internally from the same aligned underlying observations**. For example, compute `y_10 - y_2` from `DGS10` and `DGS2`; do not separately use `T10Y2Y` as a primary data dependency (it may be a validation cross-check). Reuse the same market observations in all applicable analyses.

Record source, observation date, units, available-as-of cutoff, retrieval metadata and missing values. For published model estimates, also record the model and version/revision where available, its tenor and yield definition, and relevant as-of dates. Use **internally consistent model-fitted yields and components** for decomposition; do not treat a model-implied zero-coupon yield as identical to a FRED constant-maturity par yield. FRED Treasury yields are typically quoted in percentage units; duration-based calculations require decimal yield changes (`50 bp = 0.005`). Define business-day alignment explicitly. Do not fill a missing market point with an unavailable future observation or silently interpolate incomplete yield curves.

### 2.2 Issuer ETF profiles

Use dated official issuer or official listing material as the operational source of ETF characteristics. **ETF-first is the default exposure source.** The user may instead **explicitly select the ETF's designated benchmark as an exposure proxy**, using documented benchmark-published characteristics. Bondview then analyzes the chosen benchmark exposure, **not a reconstructed ETF holding**. It does not estimate tracking differences between the ETF and its benchmark; that divergence is an accepted limitation of the user-selected proxy. The same financial-definition, date, provenance, factor-compatibility and availability standards apply to either source. Bondview checks these matters and obvious inconsistencies; **it does not independently audit portfolio holdings**.

| Profile information | Use and required distinction |
|---|---|
| Ticker, name, issuer, investment mandate, benchmark, bond category | Identity, eligibility and factor matching; benchmark is not identical to portfolio holdings |
| Physical/cash bonds, futures, active or mixed portfolio, leverage/overlay | Determine exposure mechanisms and which financial calculations are supported |
| Disclosed modified/effective duration and definition | Rate sensitivity when compatible with the selected yield factor |
| Relevant tenor/maturity exposure, if published | Factor mapping; never mechanically substitute tenor for duration |
| Disclosed yield measure and precise definition | Portfolio YTM/YTW, SEC yield, benchmark yield and distribution yield are **not interchangeable** |
| Credit quality, benchmark, suitable spread duration, when available | Corporate-credit analysis and spread sensitivity |
| Economic currency exposure and hedge policy/coverage, when available | Currency qualification and conditional FX analysis |
| Optional disclosed convexity, key-rate duration (KRD), other characteristics | Refinements when inputs and interpretation warrant |
| Document URL, observation date, available-to-user date, units | Required provenance for material numbers |

The chosen ETF or benchmark measures may be stale or incomplete, especially for active ETFs and for indexes whose characteristics are not publicly available. Record **which source was selected**, the profile's as-of/available-to-user dates, the yield and duration definitions, and any proxy status. Selecting a benchmark does **not** make unavailable data available, imply its holdings match the ETF, or justify mixing benchmark YTM with ETF duration without explicit measurement compatibility. For a current-exposure historical-shock analysis, a dated current profile is sufficient; historical exposure reconstruction requires applicable historical profiles from **whichever source is selected**. Do not infer undocumented characteristics from ETF or benchmark realized total returns, or reconstruct holdings as a standard prerequisite. If a required input is unavailable, report the corresponding limitation or partial result rather than inventing precision.

### 2.3 Eligibility and measurement compatibility

| Product | Initial eligibility |
|---|---|
| Cash Treasury ETF | Treasury rate, yield and conditional outcome/risk analyses with compatible issuer data |
| Cash investment-grade/high-yield corporate ETF | Relevant Treasury, credit spread and conditional outcome/risk analyses; rate-only assessment is insufficient for material credit exposure |
| Hedged/unhedged bond ETF | Applicable bond measures; currency-specific outputs only when supported; `(H)` does not mean free or complete hedging |
| Active/multi-tenor/mixed ETF | Applicable only to factors sufficiently represented by issuer exposure disclosures and qualified proxies |
| Treasury-futures ETF | Eligible for supported rate-factor sensitivity and yield-curve risk analysis using compatible ETF or selected benchmark characteristics. Cash-bond YTM/carry and 3A return formulas apply only when the **selected exposure is a compatible cash-bond benchmark proxy**, and must be labeled as benchmark-exposure results; estimating the futures ETF’s own full return requires valid futures-specific economics |
| Leveraged, inverse or option-overlay ETF | Catalogable; baseline cash-bond outcome formulas normally unsupported |

Eligibility is assessed **per financial calculation and selected exposure source**, not by an automatic product-wide exclusion. In particular, a benchmark can represent the chosen bond exposure without reproducing a futures ETF's contract returns. Status flags must distinguish **`value`**, **`N/A`** (mechanism inapplicable), **`unavailable`** (required source missing), **`unsupported`** (model inappropriate) and **`proxy`** (qualified substitution); none is equivalent to zero. Compare only quantities with compatible currencies, definitions, horizons, factor sensitivities and dated profiles, identifying ETF versus benchmark source choices. A product can remain eligible for one analysis when another is unsupported.

## 3. Fixed-Income Analyses

Each analysis is specified by **financial question, valid inputs and established methods, quantitative outputs, comparisons across eligible exposures and dates, and limits**. An analysis can reuse calculations from another without a separate formula-layer architecture. No analysis is required to produce an unconditional investment recommendation, a score, or a mandatory chart.

**Complementary, not independent evidence.** Different analyses may share observations, exposure measures, formulas, and even individual numerical results. The same modeled outcome can be reused to explain risk or attribute return components, but must not be counted or described as independent confirmation of an investment preference. Overlap is acceptable when the financial questions or additional outputs are useful; no requirement for mutually exclusive analyses is imposed.

### 3A. Holding-Period Return Analysis — initial primary

**Question.** *For the same historical market-factor movement and holding horizon, what gross holding-period returns can be estimated for the eligible bond exposures? Which exposure produces the higher modeled return, and by how much?*

**Financial quantity.** The principal result is an **estimated gross holding-period total return on the selected USD bond exposure**, expressed as a percentage of initial value and incorporating supported income/accrual and price effects over horizon `H`. The comparable realized quantity for a specified investment is based on ending value plus distributions, relative to initial value, under a declared distribution/reinvestment convention. Report relative differences in **percentage points (pp)**. Distinguish modeled total return from an isolated rate-price effect, a stated yield, and a Korean investor's net KRW ETF return.

**Yield-change input.** Given a historical start date `u` and end date `v`, obtain the *joint* numerical changes `delta_y_k(u,v) = y_k(v) − y_k(u)` for each relevant Treasury tenor `k`, using aligned observations. Set the holding horizon `H` to the elapsed period under a declared year-fraction convention. Apply the same historical yield-change vector to the selected exposure profiles, with the relevant factor mapping and duration/KRD. Across many observed intervals, these vectors form a **historical scenario set**; the word *scenario* denotes a particular observed market-factor movement, not a category or additional model input. User-defined hypothetical shocks may be evaluated separately when useful, including investor-relevant conditional cases; neither historical shocks nor user-defined cases constitute a forecast or a claim about future scenario probabilities.

**Basic return model.** A recognized first-order fixed-income holding-period return approximation combines yield-based compensation over the horizon with duration-based capital gains/losses (`yield * H − duration * yield_change`); this is a professional approximation, not a Bondview-specific scoring heuristic. For a selected **USD cash-bond exposure** `i`, compatible rate-factor yield change `delta_y_i(u,v)` and holding horizon `H`, the model below permits additional **supported** convexity and credit-price refinements:

`R_hat_USD_bond_i,H(u,v) ≈ B_ref_i,H − D_i * delta_y_i(u,v) + 0.5 * C_i * [delta_y_i(u,v)]^2 + supported_credit_price_effect_i(u,v)`.

Here `B_ref_i,H` is the estimated holding-period **baseline compensation** under a declared reference-yield/curve convention; `D_i` is a compatible modified/effective duration and `C_i` is compatible convexity **when available** (otherwise omit that term). With nonparallel changes or multi-factor portfolios, use compatible key-rate durations or other defensible factor sensitivities rather than treating a maturity label as a complete factor map. Credit effects require relevant spread sensitivity and observations. Currency/hedging treatment follows Section 3E and is not inserted as an unqualified additive percentage into this USD-return formula.

**Baseline compensation.** For a compatible, dated issuer-ETF or user-selected benchmark **portfolio YTM**, use `B_ref_i,H ≈ portfolio_YTM_i * H_years` as the default **recognized first-order gross USD yield/carry approximation**, when the selected cash-bond exposure supports it. This approximation is not identical to coupon cash received, realized ETF income, or separately measured roll-down; published ETF portfolio YTM need not exactly characterize a dynamically rebalanced portfolio’s holding-period return. Do not substitute distribution yield or an incompatible yield definition. Do not append an arbitrary roll-down term to this baseline. When adequate information exists, estimate a consistent curve-based carry/roll baseline, or reprice a defined cash-bond basket with specified aging and rebalancing conventions; use the more elaborate method only when it meaningfully improves the comparison. Constituent reconstruction is not a standard prerequisite.

**Model consistency and applicability.** The yield-change price effect and `B_ref` must use consistent reference conventions; separately calculated carry, roll and repricing contributions must not be counted twice. Duration is a local price/yield sensitivity at the **selected assessment-date exposure**, used as a static-exposure approximation under the stated finite shock; convexity may reduce nonlinearity error but does not model changes in ETF holdings over the horizon. The size and shape of the yield movement, factor mapping and exposure evolution matter; historical interval length alone does not determine the accuracy of the static price approximation. The simple YTM baseline is a first-order constant-yield reference, whereas an unchanged-curve or horizon-repricing baseline can include aging/roll effects and requires consistent terminal-curve/shock definitions. Cash-bond compensation is **not** automatically the futures ETF's holding-period return; a user-selected, sufficiently characterized **cash-bond benchmark** may be analyzed as that benchmark exposure, with its proxy identity retained. A futures-based index likewise requires compatible futures return mechanics for a complete holding-period estimate.

**Partial results.** If the selected exposure lacks a defensible baseline or material return components, report only supported components—for example, `rate_price_effect_i(u,v) ≈ −D_i * delta_y_i(u,v)`, with convexity/KRD refinements when justified. Label this **rate-driven price effect**, not total return. Material credit-spread or FX/hedging omissions also limit the scope of any result. Realized ETF or benchmark total-return series remain separate diagnostics: they already include market repricing and must not be inserted as `B_ref` before another rate effect is applied.

**Comparisons and optional break-even.** Apply the **same joint historical market movement** and horizon to eligible comparable exposures. Report each supported outcome and `R_hat_i,H(u,v) − R_hat_j,H(u,v)` in pp, or compare explicitly labeled partial effects when full modeled returns are unavailable. Nonparallel curve moves need not be reduced to a common parallel shift. Under a deliberately chosen common parallel shock, compatible baselines and a nonzero duration difference, an optional first-order equal-outcome boundary is:

`relative_break_even_rise_bp ≈ 10,000 * (B_ref_i,H − B_ref_j,H) / (D_i − D_j)`.

This boundary applies to the stated approximation and does not generally extend to arbitrary nonparallel shifts or material nonlinear effects.

**Output contract.** Record the selected exposure source (**ETF or benchmark proxy**), assessment date, historical start/end dates (or observation-set convention), `H`, factor mapping, baseline method, return scope and units, and relative differences. Applying dated historical yield changes to **current** profile characteristics evaluates that current exposure under those movements; reconstructing an exposure as it stood at a historical assessment date requires characteristics available at that date (Section 4).

### 3B. Risk and Stress Analysis — initial primary

**Question.** *How vulnerable are the candidate exposures to adverse changes in the yield curve or other material market factors? How do their downside magnitudes and risk characteristics compare?*

**Methods.** Established measures include reported effective/modified duration, first-order duration sensitivity `−D_i * delta_y_i`, monetary DV01/BPV with a stated investment amount, convexity when supported, and published KRD for nonparallel shifts. Apply the **same matched historical scenario set or explicitly declared stress conditions** to comparable exposures. Credit-spread and FX factors matter for eligible ETFs; an unassessed material factor prevents labeling a rate-only result as total risk.

For a historical scenario set, report the **distribution of modeled conditional price effects or supported outcomes**, including selected adverse quantiles, the worst observed scenario in the specified sample and ranges where informative. These are **descriptions of an explicitly selected scenario sample**, not independent event counts, probability forecasts or model-implied future quantiles. Avoid automatic value-at-risk labels unless their statistical interpretation is actually justified.

**Outputs and interpretation.** Comparable exposure sensitivities, adverse effects in %, selected downside summaries, and differences across eligible tenors/ETFs. Show which risks drive an adverse result rather than inventing a risk score. Historical evolution may reflect dated issuer exposure changes, dated market conditions or a rolling, explicitly available historical scenario set; distinguish these sources. Do not invent past ETF durations or regard an overlapping rolling-window count as independent experiences.

**Relationship to 3A.** Both may use the same duration/convexity pricing formulas. **3A** examines results and conditional relative preference for a specified market movement; **3B** examines sensitivity and unfavorable outcomes across a defined set of movements. Different financial questions do not require invented separate equations or two independent implementations. A negative outcome already reported for one scenario in **3A** is not a second, independent risk finding in **3B**. When repeating that result for context, identify it as reused and provide additional risk information where supported—such as adverse-outcome distributions, observed stress extremes, exposure sensitivities, or downside comparisons across a common scenario set. If only one specified stress is available, label it as that stress; do not manufacture distribution statistics or an independent conclusion.

### 3C. Yield-Curve and Carry Analysis

**Question.** *How have the level, slope and shape of the Treasury curve changed, and what do currently available yield and supportable carry/roll relationships imply for positioning across maturity segments?*

**Methods.** Derive `y_10−y_2`, `y_30−y_10` and relevant additional differences from the canonical dated Treasury inputs, not precomputed spread sources. Compare the underlying tenor movements, not just the resulting spread. Where a well-defined instrument or ETF disclosure supports it, estimate period carry and roll-down under an expressly declared curve assumption. Conventional forward rates and curve curvature may provide additional context when useful.

**Expected-short-rates and term-premium decomposition.** An established explanation of a consistently defined nominal Treasury zero-coupon yield is `yield_n(t) ≈ expected_average_future_short_rates_n(t) + term_premium_n(t)`. The term premium is **model-estimated**, not directly observed, and definitions can incorporate convexity or residual conventions. Initially examine **published** decompositions, such as New York Fed ACM or San Francisco Fed Christensen–Rudebusch, instead of fitting a new term-structure model. Analyze component levels and changes to assess whether movements in longer-term yields reflect altered expected short-rate paths or required compensation for duration risk. Use the selected model’s **own consistent fitted/zero-coupon yield, expectation and premium series** for a decomposition; do not force equality to a FRED par/constant-maturity yield. Model estimates may differ substantially and do not prove future rates will mean-revert or continue trending. This method provides 3C market context; it does not create an independent ETF return forecast, an additional `3A` carry term, or an automatic buy/sell rule.

A widening 10Y−2Y spread says that the **quoted 10Y yield increased relative to the quoted 2Y yield**; it is not a direct observation of a term risk premium or a forecast of longer-bond outperformance. A *bull steepening* and a *bear steepening* can have the same slope change and opposite rate-price consequences for long-only ETFs. The distinction is addressed through compatible yield-change components and the conditional comparisons in **3A/3B**, not a custom slope-to-stance rule.

**Outputs.** Dated Treasury yields/spreads (bp), changes in curve level/slope, and—as justified by available published-model data—model-implied yield decompositions into expected short-rate and term-premium levels/changes. Compare tenors and their evolution; compare ETF issuer-reported yields only when definitions are compatible. Report separate carry/roll contributions where credible. Market spreads and model-estimated term premiums **are not** ETF portfolio yields or realized returns. This analysis can inform interpretations of market conditions and 3A/3B conditional outcomes without assigning scenario probabilities. Do not manufacture ETF roll-down from an assumed bond that simply ages toward maturity when the ETF maintains a changing portfolio.

### 3D. Credit Spread Analysis

**Question.** *What part of the change in corporate-bond conditions reflects Treasury-rate movements, and what part reflects credit-spread repricing? How has the credit exposure of an eligible corporate-bond ETF changed over time, and how does it respond to comparable spread scenarios?*

**Conventional market decomposition.** For an appropriately matched corporate bond/index reference, a first-order yield-change decomposition is:

`delta_y_corporate ≈ delta_y_matched_Treasury + delta_OAS`.

The relationship requires a coherent benchmark and spread definition. OAS itself is a model-derived spread measure with credit, liquidity, optionality and risk-premium influences; it is **not** a pure realized-default measure. Track Treasury reference yields and OAS separately **through time**, explicitly noting intervals in which falling Treasury yields coexist with widening OAS or vice versa. This remains informative **for a single corporate-bond ETF or credit-market segment**, even if a direct comparison with Treasury ETFs is not sufficiently comparable.

**Exposure sensitivity.** Where relevant issuer rate duration and spread duration are compatible with the selected factors:

`price_effect_credit_i ≈ −D_rates,i * delta_y_matched_Treasury − D_spread,i * delta_OAS_i`.

Report the **rate** and **spread** components separately and their appropriately limited combined first-order effect; use matched IG/HY benchmarks and distinguish benchmark **proxies** from the portfolio's own OAS. An OAS widening may simultaneously increase gross stated yield and worsen mark-to-market outcomes; adequacy of compensation depends on credit losses, liquidity and other evidence not supplied by spread changes alone.

**Outputs.** OAS levels/changes (bp), Treasury-versus-OAS decomposition over time, spread sensitivity (%, where available), and conditional spread-stress outcomes. Compare suitable credit ETFs across dates/products; pure Treasury ETF credit OAS is `N/A`. Optional public default, rating migration, lending or liquidity evidence can support stronger interpretation, but is not mandatory for the basic decomposition. A stronger claim about actual credit deterioration requires more evidence than a widening OAS.

### 3E. Currency and Hedging Analysis — lower initial priority

**Question.** *How do economic currency exposure and hedge arrangements affect the interpretation of USD bond outcomes for a Korean investor?*

For a compatible **unhedged** USD bond holding-period return and matching USD/KRW movement (KRW per USD), use the conventional identity:

`1 + R_KRW = (1 + R_USD) * (1 + R_USDKRW)`.

Translate **supported** USD outcomes only. Analyze quantitative disclosed hedge coverage and applicable FX sensitivity when valid data exist. Hedge-policy labels do not establish hedge cost, coverage through time or an investable net KRW return. Do not assume costless/perfect hedging; do not invent hedge economics or convert a rate-only price effect into a complete KRW outcome. Detailed hedge and FX analysis may be deferred while a product's currency policy remains visibly disclosed.

### 3F. Method refinements and relationships between analyses

Established convexity, key-rate duration, cash-flow repricing, advanced forward/term-structure modeling, and additional credit or hedging economics can enrich particular questions if their economic value and data are defensible. **They are not compulsory formulas to implement** merely because they are known; nor should a valid refinement be excluded just because a simpler duration approximation exists. Multiple methods estimating the *same quantity* are alternative levels of approximation, not independent confirmation of attractiveness. Separate economic questions can legitimately reuse the same formulas.

Do **not** build an extra decision/classification layer that converts every analysis into a favorable/neutral/unfavorable stance. Present the numerical outcomes and meaningful conditional comparisons directly.

## 4. Historical market movements and assessment-date conventions

### 4.1 Construction of historical yield changes

For any observed interval `[u,v]`, construct the coherent Treasury change vector:

`s_(u,v) = (y_2(v) − y_2(u), y_10(v) − y_10(u), y_30(v) − y_30(u))`.

Use the same aligned source dates and factor definitions across alternative exposures. A single selected start/end pair provides one market movement; a collection of dated intervals provides a historical scenario set. The factor values and dates, **not optional descriptive curve-movement labels**, are the inputs to 3A and other compatible analyses. Do not combine independently selected peak movements from different dates into a supposedly observed joint vector.

### 4.2 Horizon, observation dates and reference history

For a selected interval, its start `u` and end `v` determine both the yield changes and the compatible horizon `H = v − u` under a documented year-fraction convention. For a collection of observations distinguish:

- **Holding/scenario horizon `H`:** e.g., 3, 6 or 12 months, used consistently for yield changes and holding-period compensation.
- **Historical reference window `W`:** the period from which observed intervals are selected; choose it according to the financial question and relevant market history.
- **Observation frequency and overlap:** daily rolling, monthly or nonoverlapping observations; overlapping windows are correlated and must not be interpreted as independent events.

For an assessment at `t`, use only market observations and exposure disclosures available **by `t`**, with documented business-day alignment and endpoint rules. When results for successive assessment dates are compared, identify whether the historical scenario sample is fixed or updated, since changing the sample also changes the outcomes.

### 4.3 Exposure profiles across time

- Applying a **current ETF or explicitly selected benchmark profile** to earlier observed yield changes is a **current-exposure calculation**, not a reconstruction of actual historical ETF/benchmark returns.
- Historical assessment-date calculations require the selected source's characteristics as available at each assessment date. If unavailable, report an unsupported historical result or a clearly labeled constant-exposure comparison; do not substitute current exposures without disclosure.
- With both duration and the yield shock fixed, the first-order rate-price effect is constant. Variation across assessment dates must be traceable to changed exposures, market-factor movements or other supported terms.

### 4.4 Historical-record summaries

Across a defined set of historical movements, report comparable return/effect distributions, adverse magnitudes, quantiles or named episodes as supported by the data and the relevant analysis. Preserve the jointly observed tenor changes, their dates and units, and the overlap convention. Curve slope/shape changes can be calculated directly from the yields; descriptive steepening/flattening terminology is not a prerequisite to any return or risk calculation.

## 5. Results, comparison and presentation

At a selected assessment date, show the appropriate numerical results for the requested tenor or ETF universe **by analysis**; for historical views, apply the same definitions to valid dates; for cross-product views, preserve a common relevant factor/scenario convention. A 1:1 comparison is a focused view of the eligible ETF universe, not a separate recommendation engine.

A result should expose the **financial question; relevant assessment date and horizon; eligible exposure identity; market factor/scenario; measured or modeled quantity and units; differences across alternatives; and the material assumptions/proxies or data limitations**. Avoid filling the display with generic repetitions of caveats. Explain concrete economic implications and keep unsupported stronger conclusions out of the output.

Priority examples of useful results:

| Analysis | Directly useful comparison |
|---|---|
| Holding-period return | Supported estimated returns or partial price effects for comparable 2Y/10Y/30Y exposures, ETFs or selected benchmark proxies under the same observed yield movements; report relative differences |
| Risk and stress | Exposure-adjusted adverse outcomes and sensitivity differences across the same eligible alternatives; adverse quantiles for a stated scenario set |
| Yield-curve and carry | Tenor yield/curve evolution, model-based expected-rate versus term-premium decomposition when informative, matched ETF yield comparisons, and supportable carry/roll explanations |
| Credit spread | The time-varying Treasury-rate versus OAS components for a corporate segment or ETF, plus qualified cross-credit ETF exposure comparisons |
| Currency/hedge | Supported unhedged KRW translation or quantitative FX sensitivity, with hedged products separately qualified |

Choose visualizations by the financial question, not by a one-chart-per-analysis requirement. Suitable views include historical lines, tenor/ETF comparison tables, scenario-by-exposure matrices, conditional outcome curves and adverse-outcome distributions. Do not require that all five analyses appear for an ineligible or incompletely disclosed ETF. Market-only Treasury/OAS context remains available without a selected ETF, but is not silently relabeled as ETF performance.

A result may identify the more favorable modeled exposure under a specified historical market movement, or show differing preferences across observed movements. No automatic total ranking, action threshold or trade signal is required.

## 6. Implementation, verification, and bounded initial research

### 6.1 Implementation boundary

A small, cohesive Python implementation should handle dated market data, exposure-source selection and eligibility, conventional quantitative calculations, historical interval/set selection, and plotting helpers where useful. Keep shared financial computations reusable without requiring a separate calculation engine for each analysis.

Use one or more sequential Jupyter notebooks as the practical interface (select data, assessment date, alternatives and analysis → calculate → inspect concise tables and meaningful interactive charts). Keep substantive functions/classes in importable `.py` modules rather than defining them inside notebooks. Preserve provenance, units, scenario conventions and error/status information for reproducibility.

### 6.2 Minimum arithmetic and behavioral checks

Tests should verify accepted financial methods and data contracts, **not invent results that the design must later optimize toward**. Examples, expressed with decimal yield changes unless specified otherwise:

| Calculation | Hand-checkable result |
|---|---|
| Treasury yields 2Y `4.0%`, 10Y `4.5%`, 30Y `4.8%` | Derived 10Y−2Y `+50 bp`, 30Y−10Y `+30 bp` from underlying inputs |
| Duration `D=8`, +50 bp rate change | First-order rate price effect `−4.00%` |
| Compatible convexity `C=80`, +50 bp rate change | `−4.00% + 0.5*80*(0.005)^2 = −3.90%` |
| Durations `D_2=1.9`, `D_10=7.5`, jointly observed +20/+10 bp yield changes (2Y/10Y) | 10Y minus 2Y rate-price effect `−7.5(0.001)+1.9(0.002)=−0.0037 = −0.37 pp` |
| Compatible portfolio YTM `5%`, six-month horizon, modified duration `7`, matched Treasury move +50 bp | First-order USD compensation proxy `B_ref=0.05*0.5=+2.50%`; rate effect `−7*0.005=−3.50%`; modeled gross USD bond-exposure return `−1.00%` before costs/FX/hedging, with no extra roll term |
| Selected historical interval `[u,v]` versus current ETF/benchmark profile at `t` | Use `y_k(v)−y_k(u)` for each aligned tenor, consistent `H=v−u`, and the **selected-source characteristics as of `t`**; do not present the resulting counterfactual as actual historical ETF/benchmark return |
| Rate duration `5.5`, spread duration `5`, Treasury −20 bp, OAS +60 bp | Rate `+1.10%`, spread `−3.00%`, combined `−1.90%` (only those components) |
| Unhedged USD bond return `−2%`, USD/KRW +8% | KRW return `(0.98*1.08)-1 = +5.84%` |
| Optional one-year compatible compensation difference +1.00 pp; durations 7.5 and 1.9; common +yield scenario | Relative break-even `17.86 bp` conditional common rise, **not** a mandated plot or term-premium metric |

Also check: decimal/percentage/bp unit conversions; missing and misaligned observation dates; coherent joint yield movements; assessment-date data availability; start/end and horizon alignment; prevention of carry/roll/repricing double counting; factor mapping; selection-source and dated-profile consistency; yield-definition compatibility; partial-result/status reporting; futures ETF rate-risk eligibility when supported; separation of a cash-bond benchmark proxy from the futures ETF's own return; and exclusion of realized ETF/benchmark total-return histories from modeled selection outcomes.

Reproducibility should distinguish **observed market data**, **published model estimates**, **issuer disclosures**, **assumptions**, **partial price-effect approximations**, and **supported holding-period outcomes**. When using a published yield decomposition, verify that fitted yield and components reconcile under that model’s own conventions; record any residual or model-specific treatment without substituting a par-yield observation. Numeric checks establish calculation behavior, not forecast skill or trading performance.

### 6.3 Bounded initial research deliverables — not a development authorization

An eventual **separately authorized** research assignment should demonstrate:

1. Actual aligned FRED Treasury histories, any relevant matched OAS series, and a small set of dated, official representative ETF profiles with validity/eligibility controls; include a user-selected designated benchmark profile when its documented characteristics are available.
2. A **holding-period return comparison** across 2Y/10Y/30Y reference exposures and eligible Treasury ETF or user-selected benchmark exposures using jointly observed historical tenor changes and a selected start/end interval. Show the supported baseline method, gross USD bond-exposure returns or labeled partial effects, relative outcomes, and selected source. Test valid futures-linked rate sensitivities separately from unsupported futures ETF carry/returns.
3. A **risk/downside comparison** on an appropriately shared scenario set, with inspectable adverse outcomes and consistent factor/exposure definitions.
4. A **yield-curve/carry explanation** using derived underlying tenor spreads and compatible issuer yield measurements. Where available and informative, examine one published, internally consistent term-premium decomposition; record why it was omitted if not usable. Include period carry/roll only when supported, not because a chart needs a value.
5. A **credit-market decomposition over time**, distinguishing Treasury-rate and OAS changes, with a qualified credit ETF example when exposure data support it; this must not depend on a cross-category Treasury-versus-credit winner.
6. Currency/hedge eligibility distinctions, relevant numeric calculation only if valid inputs exist, and the hand-checkable financial, status and as-of-date checks from §6.2.
7. Short, comprehensible conclusions for each analysis about **what the numbers actually establish**, without invented classification maps, performance forecasts or a compulsory integrated score.

This is a **research acceptance scope**, not an order to run Work or a full implementation roadmap. The user and Archie review this provisional architecture and companion examples before granting a development assignment. The analysis-based examples companion remains provisional and should be synchronized with accepted changes as needed.

## 7. Open questions, optional extensions and source context

These are matters for **specific supported exposures**, not mandatory gates to all useful research:

- **Holding-period compensation and roll:** Section 3A retains the recognized first-order yield/carry approximation for compatible, dated ETF or selected-benchmark cash-bond exposures. Which issuer/index yield definitions, exposure detail and curve assumptions justify using a more precise curve-consistent baseline or defined-basket cash-flow repricing? If baseline compensation is unsupported, report the supported partial rate-price effect rather than an unsupported complete outcome. Do not treat a rebalanced ETF as an unchanged single bond; realized benchmark total-return levels are diagnostics, **not** a substitute baseline.
- **Factor mapping and instrument structure:** When do single-tenor yields or simple duration omit material risks for mixed, active or futures-linked ETFs? Use compatible ETF or selected benchmark rate sensitivities, including futures-linked DV01 where available. A cash-bond benchmark can support cash-bond exposure comparisons without establishing the futures ETF’s own carry or contract-return mechanics. Do not mandate holdings reconstruction.
- **Credit compensation adequacy:** When is spread widening mainly market repricing versus changes in default/liquidity conditions? The Treasury/OAS decomposition is useful without proving causation or default outcomes; optional independent public indicators may support stronger claims.
- **Historical-window relevance:** Choose reference history, holding horizon and observation frequency according to the question and market conditions, accounting for changes in regime and correlated overlapping windows; no universal lookback or frequency is prescribed.
- **Published term-premium estimates:** Which available model, maturities and as-of conventions provide useful context for the target Treasury exposures? Model disagreement and possible revisions should inform interpretation; independent model estimation is not a prerequisite.
- **Model refinements and currency economics:** Convexity, published KRD, direct repricing for sufficiently defined cash flows, custom term-structure model estimation, hedge costs and more detailed FX analysis are options for justified questions and usable inputs, not a blanket engineering checklist.

**References and provenance:** [FRED DGS2](https://fred.stlouisfed.org/series/DGS2), [DGS10](https://fred.stlouisfed.org/series/DGS10), [DGS30](https://fred.stlouisfed.org/series/DGS30), [DEXKOUS](https://fred.stlouisfed.org/series/DEXKOUS); [CFA Institute — Fixed-Income Portfolio Management](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/overview-fixed-income-portfolio-management) and [Yield-Curve Strategies](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-curve-strategies); [AQR — Alternative Thinking: Style Premia / Bond Returns](https://www.aqr.com/-/media/AQR/Documents/Insights/Alternative-Thinking/Alternative-Thinking-Style-Premia-Bond-Returns.pdf) for the first-order yield-plus-duration approximation; [New York Fed — ACM Treasury Term Premia](https://www.newyorkfed.org/research/data_indicators/term-premia-tabs), [San Francisco Fed — Treasury Yield Premiums](https://www.frbsf.org/research-and-insights/data-and-indicators/treasury-yield-premiums/) and [Federal Reserve Board — Three-Factor Nominal Term Structure Model](https://www.federalreserve.gov/data/three-factor-nominal-term-structure-model.htm) for model-specific term-premium definitions and published estimates. The provisional [`bond_etf_decision_examples.md`](bond_etf_decision_examples.md) illustrates the analyses but does not override accepted architecture definitions.

**Status boundary:** Financial and exposure-source definitions remain provisional until reviewed and accepted.
