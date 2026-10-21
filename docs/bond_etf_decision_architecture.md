# Bondview-v3 — U.S. Bond ETF Decision Architecture

**Status:** **PROVISIONAL design revision — 2026-10-21.** Based on `lbk209/bondview-v3` `main`, `docs/bond_etf_decision_architecture.md` (Git blob `ed0cf0c058fba8406a06d744a30317faf66f04c4`). This review draft updates Section 3A and its essential supporting contracts, plus the design-review checkpoints; the remaining analyses and companion examples are deferred. It is **not an approved implementation specification, investment recommendation, or authorization for a Work assignment**.

**Companion documents:** The existing [`bond_etf_decision_examples.md`](bond_etf_decision_examples.md) illustrates a different, aspect-centered organization and is **reference-only** until a new companion is written against this architecture. Prior Bondview repositories (`bondview-v2`, `bondview`) are also reference-only. Do not inherit their classifications or decision rules by implication.

## 1. Purpose, scope, and design position

### 1.1 Investment purpose

Bondview-v3 supports practical consideration of **Korean-listed ETFs exposed to U.S. bonds**—initially cash U.S. Treasury ETFs with different maturity exposures, extending to suitable U.S. corporate-bond ETFs. The tool should answer useful financial questions **across eligible tenors or ETFs, across assessment dates, and under relevant market conditions**, using established fixed-income methods and the ETF exposures disclosed by their issuers.

The output is **multiple distinct financial analyses**, not a weighted attractiveness score, an invented indicator framework, or a rule-driven buy/sell classifier. A conditional preference is legitimate when it follows directly from an explicitly defined financial question and comparable calculated outcomes. It does not have to become a universal judgment about the product.

The terms **Fixed-Income Analyses** and **analyses** are used for the user-facing categories. They are descriptive organizing labels, not claims that each item is an independent academic theory, software engine, or standardized industry taxonomy. Inputs and intermediate calculations may be shared freely; they need not appear as user-facing analysis categories. The word *aspect* is not used as a mandatory architectural unit.

### 1.2 Analytical starting point

Begin with conventional studies of defined 2Y, 10Y, and 30Y Treasury exposure alternatives and relevant market factors. Then apply compatible calculations to issuer-published ETF profiles. The same economic definitions are used, with product inputs and limitations added as needed. **This does not create separate market and ETF decision engines**, nor require a market verdict before analyzing an ETF.

The two initial primary decision-oriented analyses are **A. Conditional Holding-Period Outcome** and **B. Risk and Stress**. **C. Yield-Curve and Carry** and **D. Credit Spread** retain separate financial information that may inform A/B but also warrants examination in its own right. **E. Currency and Hedging** is relevant but has a lower initial modeling priority. This is a priority order, not a required number of outputs or prescribed software hierarchy.

### 1.3 Design-review checkpoints

Apply these questions when proposing or revising a financial method; they are **review criteria**, not additional calculation stages or mandatory independent analyses:

1. **Established economic basis:** Is the method recognized in fixed-income theory or professional practice, with its assumptions stated?
2. **Exposure applicability:** Is the method compatible with the instrument or ETF structure, factor definitions, disclosed characteristics and available data?
3. **Investment relevance:** Does it answer a defined financial question with interpretable quantities useful for tenor/ETF comparison or examination across dates?
4. **Incremental information or robustness:** Does it add a useful financial perspective, a compatible decomposition, or a defensible alternative approximation of the same quantity? Different methods need not produce independent evidence.
5. **Practical informativeness:** Are the results meaningful for the intended decision support? Distinguish an uninformative example from a limitation of the method itself, and do not add complexity without corresponding value.

### 1.4 Boundaries

- Do **not** infer future yield, spread, FX or ETF price movements from recent trends, fit a forecasting model, or assume that an observed historical movement will recur. Forecasting is not required.
- Do **not** construct bespoke component classifications, states, factor weights, aggregate attractiveness scores, or unexplained rules that map observations into investment stances.
- Do **not** use historical ETF prices, NAVs, realized ETF returns or benchmark total-return index levels to determine modeled selection outputs, substitute for baseline compensation, estimate undisclosed factor exposure, tune weights, or override selected exposure characteristics. Realized ETF/benchmark performance may be shown separately as **diagnostics**; it is not fed into the conditional Section 3A calculation.
- Do **not** require independent reconstruction or auditing of ETF holdings, bond-level cash flows, hedging books, financing economics or futures mechanics. Recognize the limits of issuer disclosures rather than filling unsupported gaps with assumed precision.
- Portfolio optimization, investor-specific position sizing, trading execution, taxes and detailed expense-ratio optimization are outside the initial scope. Expense ratios are not a separate analysis at this stage; avoid double-counting costs if an input already reflects them.
- ETF maturity labels do **not** establish duration, carry or the security cash flows required for exact bond repricing.

## 2. Data, ETF exposure, and comparability contracts

These are **input and measurement rules**, not a separate financial analysis or a catalog of preassigned mathematical functions. Each analysis in §3 identifies the inputs it actually needs.

### 2.1 Canonical market observations

| Data | Preferred initial source / treatment | Intended analytical role |
|---|---|---|
| U.S. Treasury constant-maturity yields | FRED/H.15 `DGS2`, `DGS5`, `DGS10`, `DGS30`, other `DGS*` series when justified | Dated yield levels, changes, curve comparisons and joint rate scenarios |
| Investment-grade and high-yield credit OAS | Matched, documented ICE BofA/FRED or justified alternative | Credit compensation context, credit-specific repricing and conditional spread scenarios |
| USD/KRW (KRW per USD) | FRED `DEXKOUS` or documented suitable alternative | FX context and conditional unhedged KRW outcomes |
| Cash/short-rate comparator | Clearly specified currency-compatible reference when needed | Cash-relative holding-period comparisons |
| Real yields, term premium, inflation-expectation series | Optional credible sources | Additional interpretation only if a specific analysis benefits; model-estimated term premium is not an observed return |

**Canonical factor rule:** Fetch and retain underlying dated Treasury tenor yields. Derive spreads, curve changes, horizon yield changes and joint scenario vectors **internally from the same aligned underlying observations**. For example, compute `y_10 - y_2` from `DGS10` and `DGS2`; do not separately use `T10Y2Y` as a primary data dependency (it may be a validation cross-check). Reuse the same market observations in all applicable analyses.

Record source, observation date, units, available-as-of cutoff, retrieval metadata and missing values. FRED Treasury yields are typically quoted in percentage units; duration-based calculations require decimal yield changes (`50 bp = 0.005`). Define business-day alignment explicitly. Do not fill a missing market point with an unavailable future observation or silently interpolate incomplete yield curves.

### 2.2 Issuer ETF profiles

Use dated official issuer or official listing material as the operational source of ETF characteristics. **ETF-first is the default exposure source.** The user may instead **explicitly select the ETF's designated benchmark as an exposure proxy**, using documented benchmark-published characteristics. Bondview then analyzes the chosen benchmark exposure, **not a reconstructed ETF holding**. It does not estimate tracking differences between the ETF and its benchmark; that divergence is an accepted limitation of the user-selected proxy. The same financial-definition, date, provenance, factor-compatibility and availability standards apply to either source. Bondview checks these matters and obvious inconsistencies; **it does not independently audit portfolio holdings**.

| Profile information | Use and required distinction |
|---|---|
| Ticker, name, issuer, investment mandate, benchmark, bond category | Identity, eligibility and factor matching; benchmark is not identical to portfolio holdings |
| Physical/cash bonds, futures, active or mixed portfolio, leverage/overlay | Determine applicable analysis and exclusions |
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
| Treasury-futures ETF | **Outside ordinary cash-bond models by default**; explicit opt-in and a separate valid treatment required |
| Leveraged, inverse or option-overlay ETF | Catalogable; baseline cash-bond outcome formulas normally unsupported |

Status flags must distinguish **`value`**, **`N/A`** (mechanism genuinely inapplicable), **`unavailable`** (required source missing), **`unsupported`** (model inappropriate) and **`proxy`** (qualified substitution). Do not translate any such flag into zero or a neutral result. ETF-to-ETF comparisons require compatible currency, reporting conventions, market factors, time horizons and dated exposures; identify ETF-versus-benchmark source choices explicitly in comparisons. A product can remain in the universe when one analysis cannot produce a result.

## 3. Fixed-Income Analyses

Each analysis is specified by **financial question, valid inputs and established methods, quantitative outputs, comparisons across eligible exposures and dates, and limits**. An analysis can reuse calculations from another without a separate formula-layer architecture. No analysis is required to produce an unconditional investment recommendation, a score, or a mandatory chart.

**Complementary, not independent evidence.** Different analyses may share observations, exposure measures, formulas, and even individual numerical results. The same modeled outcome can be reused to explain risk or attribute return components, but must not be counted or described as independent confirmation of an investment preference. Overlap is acceptable when the financial questions or additional outputs are useful; no requirement for mutually exclusive analyses is imposed.

### 3A. Conditional Holding-Period Outcome Analysis — initial primary

**Question.** *Over a specified holding horizon and under a specified market-factor movement, what gross bond-exposure holding-period outcomes can be supported for each eligible Treasury maturity exposure or ETF (or user-selected benchmark proxy)? Which outcome is more favorable under the same conditions, and when does the ordering change?*

**Financial output and units.** The primary quantity is an **estimated holding-period total return on the defined bond exposure**, in percent of initial investment, combining the modeled economic income/accrual and price effects over `H`. For a defined investment, the corresponding realized quantity would reflect ending value and distributions (with a specified reinvestment convention) relative to beginning value. The Section 3A output is instead a **conditional model estimate**, not the ETF's or benchmark's observed realized return. Distinguish it from (a) an isolated price effect, (b) a yield level or distribution yield, and (c) a Korean investor's net KRW ETF return. Report comparable relative-return differences in **percentage points (pp)**.

**Basic conditional-return model.** For an eligible underlying **USD cash-bond exposure** `i`, holding horizon `H` and historical market-movement scenario `s`, use a conventional first-order approximation, with supported optional refinements:

`R_hat_USD_bond_i,H(s) ≈ B_ref_i,H − D_i * delta_y_i,H(s) + 0.5 * C_i * [delta_y_i,H(s)]^2 + supported_credit_price_effect_i,H(s)`.

Here `B_ref_i,H` is the **holding-period baseline compensation under a declared reference-yield/curve convention**; `D_i` is a compatible modified/effective duration, and `C_i` is compatible convexity **only if supported** (omit the convexity term otherwise). For eligible multi-factor exposures use factor-appropriate duration/KRD or explicit matched-rate and spread durations rather than silently mapping all risks to one Treasury tenor. The familiar decomposition `B_ref ≈ carry + roll` is valid only when both contributions are well defined and nonoverlapping. Additional material return components require support; Section 3E handles currency translation/hedging consistently rather than treating a generic FX percentage as an automatically additive term in this USD bond-return equation.

**Baseline compensation, default and refinements.** When the selected ETF or benchmark profile supplies a compatible, dated **portfolio YTM** and the instrument/exposure permits the approximation, use `B_ref_i,H ≈ portfolio_YTM_i * H_years` as the **initial first-order gross USD compensation proxy**, with YTM in decimal units. This approximates yield accrual under a constant-yield/no-additional-rate-shock reference, **not** actual cash coupon receipts, an independently estimated roll-down, a guaranteed return, or a net ETF return. Do not substitute distribution yield, incompatible YTW/SEC yield, or an undisclosed benchmark yield merely to fill the term. Do **not** add an extra roll-down figure on top of this approximation without an explicit, consistent decomposition. Where defensible information is available, refine `B_ref` with curve-consistent carry/roll estimation or cash-flow repricing for a defined bond basket, specifying the portfolio aging/rebalancing convention. A conventional cash-bond model does not automatically represent a futures ETF or a rebalanced ETF as one bond held unchanged to maturity. **Detailed constituent reconstruction is not mandatory.** A more complex baseline is worthwhile only when its exposure inputs and incremental accuracy can be justified.

**Historical market-movement input.** The **primary input** for `delta_y_i,H(s)` is the numerical yield change derived from **jointly observed historical Treasury tenor yields**, not a manually invented change or a bull/bear label. For a user-selected historical start `u` and end `v`, calculate each tenor change `delta_y_k(u,v) = y_k(v) − y_k(u)` using the same aligned dates for 2Y/10Y/30Y; the interval length supplies the corresponding horizon `H` in a single-period analysis. Map that coherent yield-change vector to each selected exposure using its valid rate-factor sensitivities. A scenario set can similarly use many jointly observed intervals of a fixed horizon from a separately chosen reference history (Section 4). Classification as bull/bear steepening/flattening is **optional descriptive grouping**, never a required input to the financial calculation. Explicit what-if shocks can still be used as **secondary** sensitivity cases.

**Baseline/shock consistency.** Under the simple YTM-based default, the historical matched-tenor yield change is applied as a market-factor shock relative to the **constant-yield/no-additional-shock approximation**. If `B_ref` instead incorporates horizon repricing and aging along an **unchanged initial curve**, define the scenario yield shift **relative to that baseline curve at the horizon**; preserve the observed tenor movement as the market-factor input but do not count roll or other price changes twice. State the tenor-mapping and approximation limits when a published portfolio duration does not fully describe nonparallel moves. A change in the selected historical dates changes the scenario; it does not silently replace the issuer/benchmark assessment-date profile.

**Unsupported components and scope of return.** If a compatible baseline cannot be estimated, calculate only the supported partial result, for example `rate_price_effect_i,H(s) ≈ −D_i * delta_y_i,H(s)` (plus valid convexity/KRD refinements), and label it **rate-driven price effect**, not complete holding-period return. For credit ETFs, material omitted spread repricing likewise makes the result partial. For hedged or unhedged Korean-listed ETFs, a modeled **gross USD underlying bond-exposure return** must not be called realized or net hedged KRW ETF performance; require a separately supported currency/hedge treatment to make that stronger claim. ETF price/NAV histories and **benchmark total-return index histories** may support separate diagnostics. Their realized returns already include market repricing and **must not be inserted as `B_ref` and then have the duration shock added again**.

**Conditional relative comparison.** When modeled quantities and reporting conventions are compatible, compare each eligible exposure under the **same jointly observed historical movement** and report `R_hat_i,H(s) − R_hat_j,H(s)` in pp. Nonparallel 2Y/10Y/30Y movements are valid and should not be reduced to a common parallel change. When only partial price effects are supportable, compare them as **relative partial effects**, not relative complete returns. A higher conditional return establishes a **scenario-specific** preference on that financial measure, not an overall investment ranking.

**Secondary what-if/break-even calculation.** With compatible baseline compensation and an **expressly chosen common parallel yield shock**, a first-order equal-outcome boundary is:

`relative_break_even_rise_bp ≈ 10,000 * (B_ref_i,H − B_ref_j,H) / (D_i − D_j)` (nonzero duration difference; compensation in decimal returns).

This is conventional *conditional offset arithmetic*, not a separately validated attractiveness indicator or mandatory chart. A single universal break-even yield change generally does not exist for unrestricted nonparallel movements; convexity and other return terms can also alter this simple boundary.

**Outputs.** State the exposure source (ETF or selected benchmark proxy), assessment date, historical start/end dates or scenario-set convention, compatible holding horizon, baseline method/assumptions, modeled return or expressly **partial** effect, units, and relative differences. Recalculate for successive assessment dates only with profile inputs available at those dates, specifying whether scenarios are held fixed or refreshed. Historical shocks applied to current characteristics are **current-exposure counterfactuals**, not reconstructions of historical ETF returns (Section 4).

### 3B. Risk and Stress Analysis — initial primary

**Question.** *How vulnerable are the candidate exposures to adverse changes in the yield curve or other material market factors? How do their downside magnitudes and risk characteristics compare?*

**Methods.** Established measures include reported effective/modified duration, first-order duration sensitivity `−D_i * delta_y_i`, monetary DV01/BPV with a stated investment amount, convexity when supported, and published KRD for nonparallel shifts. Apply the **same matched historical scenario set or explicitly declared stress conditions** to comparable exposures. Credit-spread and FX factors matter for eligible ETFs; an unassessed material factor prevents labeling a rate-only result as total risk.

For a historical scenario set, report the **distribution of modeled conditional price effects or supported outcomes**, including selected adverse quantiles, the worst observed scenario in the specified sample and ranges where informative. These are **descriptions of an explicitly selected scenario sample**, not independent event counts, probability forecasts or model-implied future quantiles. Avoid automatic value-at-risk labels unless their statistical interpretation is actually justified.

**Outputs and interpretation.** Comparable exposure sensitivities, adverse effects in %, selected downside summaries, and differences across eligible tenors/ETFs. Show which risks drive an adverse result rather than inventing a risk score. Historical evolution may reflect dated issuer exposure changes, dated market conditions or a rolling, explicitly available historical scenario set; distinguish these sources. Do not invent past ETF durations or regard an overlapping rolling-window count as independent experiences.

**Relationship to 3A.** Both may use the same duration/convexity pricing formulas. **3A** examines results and conditional relative preference for a specified market movement; **3B** examines sensitivity and unfavorable outcomes across a defined set of movements. Different financial questions do not require invented separate equations or two independent implementations. A negative outcome already reported for one scenario in **3A** is not a second, independent risk finding in **3B**. When repeating that result for context, identify it as reused and provide additional risk information where supported—such as adverse-outcome distributions, observed stress extremes, exposure sensitivities, or downside comparisons across a common scenario set. If only one specified stress is available, label it as that stress; do not manufacture distribution statistics or an independent conclusion.

### 3C. Yield-Curve and Carry Analysis

**Question.** *How have the level, slope and shape of the Treasury curve changed, and what do currently available yield and supportable carry/roll relationships imply for positioning across maturity segments?*

**Methods.** Derive `y_10−y_2`, `y_30−y_10` and relevant additional differences from the canonical dated Treasury inputs, not precomputed spread sources. Compare the underlying tenor movements, not just the resulting spread. Where a well-defined instrument or ETF disclosure supports it, estimate period carry and roll-down under an expressly declared curve assumption. Conventional forward rates, curve curvature or term-premium estimates may be used for a specific, justifiable question; they are not automatic initial dependencies.

A widening 10Y−2Y spread says that the **quoted 10Y yield increased relative to the quoted 2Y yield**; it is not a direct observation of a term risk premium or a forecast of longer-bond outperformance. A *bull steepening* and a *bear steepening* can have the same slope change and opposite rate-price consequences for long-only ETFs. The distinction is addressed through compatible yield-change components and the conditional comparisons in **3A/3B**, not a custom slope-to-stance rule.

**Outputs.** Dated Treasury yields/spreads (bp), changes in curve level/slope and the separate carry/roll contributions where credible. Compare tenors and their evolution; compare ETF issuer-reported yields only when definitions are compatible. Market spreads **are not** ETF portfolio yields. This analysis can have useful standalone market/curve information while informing more direct ETF conditional outcomes. Do not manufacture ETF roll-down from an assumed bond that simply ages toward maturity when the ETF maintains a changing portfolio.

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

Established convexity, key-rate duration, cash-flow repricing, forward/term-premium analysis, and additional credit or hedging economics can enrich particular questions if their economic value and data are defensible. **They are not compulsory formulas to implement** merely because they are known; nor should a valid refinement be excluded just because a simpler duration approximation exists. Multiple methods estimating the *same quantity* are alternative levels of approximation, not independent confirmation of attractiveness. Separate economic questions can legitimately reuse the same formulas.

Do **not** build an extra decision/classification layer that converts every analysis into a favorable/neutral/unfavorable stance. Present the numerical outcomes and meaningful conditional comparisons directly.

## 4. Historical scenario analysis and assessment-date conventions

### 4.1 Why “historical scenario analysis,” not “historical replay”

**Historical scenario analysis** (historical-shock application) means taking a **jointly observed historical change in relevant market factors** and applying that change to a specified reference exposure or current ETF profile as a **conditional scenario**. *Replay* might wrongly suggest reconstructing the actual historical ETF portfolio and realized return, or assuming history repeats. Neither is intended here. The term **historical simulation** is also used in risk management, but no probabilistic VaR machinery is required.

Example: For an observed six-month interval `[u,v]`, construct the joint Treasury change vector `s_(u,v) = (y_2(v)−y_2(u), y_10(v)−y_10(u), y_30(v)−y_30(u))`. Use this **same internally coherent vector** for comparing eligible 2Y/10Y/30Y reference exposures or corresponding ETFs at a chosen assessment date `t`, matching the **user-selected ETF or benchmark source** and its duration or more detailed supported exposures. The user may choose specific historical start/end dates directly; their elapsed interval sets `H` for that single-period comparison, and the corresponding Section 3A compensation uses the **same horizon**. Do not assemble unrelated peak 2Y, 10Y and 30Y movements from different dates and call them one observed curve scenario.

**Scenarios are conditional, not forecasts.** Bondview does not assume `s_(u,v)` will occur after `t`, and does not extrapolate trends. For a future choice, the likelihood of particular movements remains uncertain. The analysis says *what follows economically if the specified movement happens*, and how outcome/risk comparisons vary across the historically observed scenario set. Selection of recent rather than very old observations is an explicit reference-period judgment, **not** proof that recent outcomes will repeat.

### 4.2 Horizon, observation dates and reference history

For a **single selected historical interval**, the start `u` and end `v` determine the yield-change vector **and** the holding/scenario horizon `H = v − u` (with a declared year-fraction convention). For analysis of **many historical scenarios**, distinguish the following three settings:

- **Holding/scenario horizon `H`:** e.g., 3, 6 or 12 months; rate-factor changes and any holding-period compensation compared against them must have compatible horizons.
- **Scenario reference history `W`:** e.g., a recent few years or an explicitly selected longer reference; more years need not better represent current conditions. A selected shorter regime may miss extremes.
- **Scenario observation frequency:** e.g., daily ending dates for rolling six-month yield changes, or monthly/nonoverlapping endpoints for a different descriptive purpose. Daily calculation is inexpensive; heavily overlapping windows are correlated.

For a historical assessment at `t`, a scenario must use observations available **by `t`**; do not leak future changes into earlier decisions. Define alignment for the nearest valid source date at the intended horizon boundary. State whether the user is viewing an **unchanged scenario set** over successive assessment dates or an **as-of-date updated set**. The latter changes the comparison's inputs in two ways (market/profile conditions and sample composition); do not attribute their effects to ETF attractiveness without separation.

### 4.3 Optional grouping of historical yield-curve scenarios

Observed historical rate-change vectors may be grouped descriptively into conventional **bull steepening**, **bull flattening**, **bear steepening**, and **bear flattening** categories. State the chosen definitions—for example, falling/rising 10Y yield for *bull/bear* and increasing/decreasing `y_10−y_2` for *steepening/flattening*—along with the rate-change horizon, reference tenors and any explicit neutral/noise thresholds. The categories are established market terminology, but a particular mechanical classification rule is **not** universally standardized. Retain **neutral, mixed/twist, curvature-dominated, and unclassified** movements where appropriate rather than forcing every observation into four labels.

**Preserve the actual jointly observed 2Y/10Y/30Y changes, their dates and magnitudes** in all financial calculations; a category is not a substitute for the numerical scenario, and the 30Y response must not be inferred from the 2Y–10Y label. Where informative, compare supported conditional outcomes (**3A**) and downside summaries (**3B**) by historical episode or within the declared groups. Group frequencies and counts describe only the selected historical sample (including any overlapping windows), **not** probabilities of future market movements. Do not map the categorical labels directly to investment preferences through custom rules.

### 4.4 Current exposure versus actual past exposure

- Applying a **current ETF or explicitly selected benchmark profile** to previously observed yield-change scenarios is a **current-exposure counterfactual**. It is neither a reconstruction of ETF/benchmark historical returns nor a claim that the chosen exposure source had the same characteristics when the scenario originally occurred.
- A historical time series of exposure-dependent outputs must use **dated characteristics from the selected ETF or benchmark source** when they were available. If a past profile is unavailable, leave the result unavailable or use a clearly declared constant-exposure counterfactual, never silently rewrite history. The same date/availability rule applies to ETF and benchmark sources.
- With a fixed duration and fixed shock, the rate-price effect is constant: a chart implying it evolves is misleading. Its variation can instead come from changed exposures, different observed/scenario movements, or supportably changed carry/roll inputs.
- A time-series crossing or a smaller/larger gap between scenario results may indicate **changed conditional outcomes**, but is not by itself a favorable purchase-timing signal. Such a claim would require additional assumptions about future conditions and investor objectives.

### 4.5 Scope of the historical record

A scenario distribution may summarize adverse magnitudes, relative-result differences, quantiles and dates of notable episodes. Do not equate dense overlapping scenario counts with independent events or forward probabilities. Retain the **market factors jointly** and the dates/units needed to reproduce each result. Market history is shared across all relevant analyses, not recollected separately for each chart.

## 5. Results, comparison and presentation

At a selected assessment date, show the appropriate numerical results for the requested tenor or ETF universe **by analysis**; for historical views, apply the same definitions to valid dates; for cross-product views, preserve a common relevant factor/scenario convention. A 1:1 comparison is a focused view of the eligible ETF universe, not a separate recommendation engine.

A result should expose the **financial question; relevant assessment date and horizon; eligible exposure identity; market factor/scenario; measured or modeled quantity and units; differences across alternatives; and the material assumptions/proxies or data limitations**. Avoid filling the display with generic repetitions of caveats. Explain concrete economic implications and keep unsupported stronger conclusions out of the output.

Priority examples of useful results:

| Analysis | Directly useful comparison |
|---|---|
| Conditional holding-period outcome | Price effects and supported holding-period outcomes for 2Y/10Y/30Y or eligible ETFs across **the same historical scenarios**, including differences and conditional winner when justified |
| Risk and stress | Exposure-adjusted adverse outcomes and sensitivity differences across the same eligible alternatives; adverse quantiles for a stated scenario set |
| Yield-curve and carry | Tenor yield/curve evolution, matched ETF yield comparisons, supportable carry and roll explanations of differences |
| Credit spread | The time-varying Treasury-rate versus OAS components for a corporate segment or ETF, plus qualified cross-credit ETF exposure comparisons |
| Currency/hedge | Supported unhedged KRW translation or quantitative FX sensitivity, with hedged products separately qualified |

Choose visualizations by the financial question, not by a one-chart-per-analysis requirement. Suitable views include historical lines, tenor/ETF comparison tables, scenario-by-exposure matrices, conditional outcome curves and adverse-outcome distributions. Do not require that all five analyses appear for an ineligible or incompletely disclosed ETF. Market-only Treasury/OAS context remains available without a selected ETF, but is not silently relabeled as ETF performance.

A result may show a conditional relative preference for **one particular scenario** or mixed outcomes over a scenario set. No automatic total ranking, action threshold, daily trade signal or bespoke favorable-state classification is required. Do not infer that a higher current yield must produce higher future returns.

## 6. Implementation, verification, and bounded initial research

### 6.1 Implementation boundary

A small, cohesive Python implementation should handle dated market data, ETF profiles/eligibility, conventional quantitative calculations, historical scenario selection and optional plotting helpers. Reuse inputs and shared computational functions as engineering requires. The architecture **does not mandate** a separate `Baseline Financial Calculations` layer, a class hierarchy, one function per analysis, an engine per market/ETF view, or a fixed module count.

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

Also check: decimal/percentage/bp unit conversions; missing and nonmatching dates; preservation of simultaneously observed yield-curve vectors; absence of future data in historical assessments; single-interval start/end dates and `H` alignment; reference-curve/shock conventions that prevent roll double counting; incorrect factor mapping; eligible/ineligible products; ETF-versus-benchmark selection and dated-source consistency; yield-definition mismatch; unavailable-versus-N/A reporting; absence of disclosures not yet available at past assessment dates; no fabricated carry/roll/hedge values; no futures cash-bond treatment by default; and no influence from ETF **or benchmark total-return history** on modeled selection outcomes.

Reproducibility should distinguish **observed market data**, **issuer disclosures**, **assumptions**, **partial price-effect approximations**, and **supported holding-period outcomes**. Numeric checks establish calculation behavior, not forecast skill or trading performance.

### 6.3 Bounded initial research deliverables — not a development authorization

An eventual **separately authorized** research assignment should demonstrate:

1. Actual aligned FRED Treasury histories, any relevant matched OAS series, and a small set of dated, official representative ETF profiles with validity/eligibility controls; include a user-selected designated benchmark profile when its documented characteristics are available.
2. A **conditional scenario comparison** across 2Y/10Y/30Y reference exposures and several eligible Treasury ETFs using **jointly observed historical tenor changes**, including a selected historical start/end interval. Show baseline method and supported gross USD bond-exposure outcomes versus partial rate-price effects, relative outcomes, source choices and assumptions.
3. A **risk/downside comparison** on an appropriately shared scenario set, with inspectable adverse outcomes and consistent factor/exposure definitions.
4. A **yield-curve/carry explanation** using derived underlying tenor spreads and compatible issuer yield measurements; include period carry/roll only when supported, not because a chart needs a value.
5. A **credit-market decomposition over time**, distinguishing Treasury-rate and OAS changes, with a qualified credit ETF example when exposure data support it; this must not depend on a cross-category Treasury-versus-credit winner.
6. Currency/hedge eligibility distinctions, relevant numeric calculation only if valid inputs exist, and the hand-checkable financial, status and as-of-date checks from §6.2.
7. Short, comprehensible conclusions for each analysis about **what the numbers actually establish**, without invented classification maps, performance forecasts or a compulsory integrated score.

This is a **research acceptance scope**, not an order to run Work or a full implementation roadmap. The user and Archie review this provisional architecture and any successor examples before granting a development assignment. The existing examples document is reference material; a new companion should be built for the accepted analysis definitions, not patched merely to preserve earlier visualizations.

## 7. Open questions, optional extensions and source context

These are matters for **specific supported exposures**, not mandatory gates to all useful research:

- **Holding-period compensation and roll:** **Initial Section 3A policy:** with compatible, dated portfolio YTM from the selected ETF or benchmark source, use `YTM * H_years` as a qualified **first-order gross USD compensation proxy**, without separately inventing roll-down. Which issuer/index yield definitions, exposure detail and curve assumptions justify replacing this proxy with curve-consistent carry/roll or defined-basket cash-flow repricing? When even the proxy is unsupported, report the supported partial rate-price effect instead of an unsupported complete outcome. Do not treat active/rebalanced ETFs as an unchanged single bond. Realized benchmark total-return levels are diagnostics, **not** the baseline.
- **Complex factor mapping:** When does a single Treasury tenor or broad credit index omit material risks for a mixed/active ETF? Use issuer-provided KRD, spread duration or qualified proxies when sound; do not mandate holdings reconstruction.
- **Credit compensation adequacy:** When is spread widening mainly market repricing versus changes in default/liquidity conditions? The Treasury/OAS decomposition is useful without proving causation or default outcomes; optional independent public indicators may support stronger claims.
- **Scenario-history relevance:** How long a reference history, what holding horizon and which sampling convention best illuminate the selected economic question? Longer is not automatically more relevant; historical conditions may span different regimes. No fixed lookback or rolling frequency is yet accepted.
- **Model refinements and currency economics:** Convexity, published KRD, direct repricing for sufficiently defined cash flows, model-based term premium, hedge costs and more detailed FX analysis are options for justified questions and usable inputs, not a blanket engineering checklist.

**References and provenance:** [FRED DGS2](https://fred.stlouisfed.org/series/DGS2), [DGS10](https://fred.stlouisfed.org/series/DGS10), [DGS30](https://fred.stlouisfed.org/series/DGS30), [DEXKOUS](https://fred.stlouisfed.org/series/DEXKOUS); [CFA Institute — Fixed-Income Portfolio Management](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/overview-fixed-income-portfolio-management) and [Yield-Curve Strategies](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-curve-strategies). The prior [`bond_etf_decision_examples.md`](bond_etf_decision_examples.md) and previous design reviews are **references**, not specifications for the replacement.

**Document boundary:** This draft contains no current bond ETF recommendation, no proof that official issuer characteristics reproduce holdings, and no authorization to change GitHub or begin financial-model implementation.
