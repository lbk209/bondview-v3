# Bondview-v3 — U.S. Bond ETF Decision Architecture

**Status:** Provisional design. This document defines the current Bondview-v3 financial-analysis architecture and shared data, scenario, exposure and interpretation contracts.

**Companion:** [`bond_etf_decision_examples.md`](bond_etf_decision_examples.md) illustrates applications of the architecture. Examples are explanatory and do not supersede the design contracts. Earlier Bondview repositories are reference-only.

## 1. Purpose, scope, and design position

### 1.1 Investment purpose

Bondview-v3 supports practical selection and comparison of **Korean-listed ETFs exposed to U.S. bonds**, beginning with U.S. Treasury maturity exposures and extending to suitable U.S. corporate-bond ETFs. It uses established fixed-income methods and appropriately dated market and exposure data to evaluate alternatives **across Treasury tenors or ETFs, assessment dates, and explicitly defined market conditions**.

Bondview may evaluate **2Y, 10Y and 30Y Treasury reference exposures** without attributing those results to a specific ETF. An eligible ETF is evaluated using its disclosed exposure characteristics; a user-selected benchmark may serve as a qualified proxy (§2). Lack of sufficient product-level inputs limits claims about that product, but does not invalidate supported Treasury-tenor analysis.

The outputs are interpretable financial quantities and conditional comparisons that help investors judge return opportunities and risks. A useful result may establish a consistent outcome within a scenario set, a conditional relative advantage, a break-even condition, or an important unresolved trade-off. Bondview does not require an unconditional winner, a composite attractiveness score or a rule-based buy/sell instruction.

The five **Fixed-Income Analyses** organize financial questions and user-facing interpretations. They may share data, calculations and outputs; they are not required to correspond to separate numerical engines or software stages.

### 1.2 Analytical relationship and investor inputs

The preferred investment-investigation order is **Analysis 1 — Treasury Market Conditions and Scenarios** (Treasury market interpretation and relevant scenario evidence), **Analysis 2 — Holding-Period Return** (conditional tenor/ETF outcomes and comparisons), and **Analysis 3 — Risk and Stress** (sensitivities and adverse consequences). **Analysis 4 — Credit Spread** and **Analysis 5 — Currency and Hedging** address additional material risk and return effects for eligible products. These analyses may qualify or revise an otherwise rate-only or gross USD comparison.

Investors may express a **partial, economically meaningful market view**—for example, whether 10Y yields are expected to rise, remain approximately stable or decline over a stated horizon—without separately predicting the changes of every Treasury tenor. Such a view may be translated into a **coherent joint yield-change scenario set** using justified historical evidence or established modeling methods. Record the condition, range, horizon, data and method. The resulting set is not automatically a forecast distribution.

Analysis 1 can both provide useful standalone Treasury market insight and contribute market evidence or conditional scenarios for Analysis 2. Analysis 2 may also operate directly on coherent scenarios supplied by the user or another defensible source. Analysis 3 and the other analyses may reuse those same factors and results without counting their reuse as independent evidence.

This order is a guide to financial interpretation, not a mandatory dependency graph. Analyses remain available independently when their relevant inputs and questions are supported.

### 1.3 Design-review checkpoints

Apply these **general criteria** when reviewing financial analyses, models, data choices, implementations and examples. They guide financial judgment across the architecture; specific calculations and operating rules belong in the relevant analysis or shared contract. They are not additional processing stages.

When proposing to replace or reject an existing design decision, identify the assumption, evidence or requirement that justifies the change. Distinguish a limitation of a particular example or implementation from a limitation of the underlying method or architecture. The scope of the proposed revision should be proportionate to the evidence, favoring the narrowest change that adequately addresses the identified problem.

1. **Economic and methodological validity.** Use economically sound financial definitions and methods that address the stated question. Prefer established approaches where suitable, compare credible alternatives when justified, and avoid introducing bespoke constructs without a clear economic advantage.
2. **Applicability and evidentiary support.** Match each method and claim to the relevant exposure or instrument, measurement definitions and quality of available evidence. State material limitations, distinguish direct measurements from proxies or estimates, and retain useful partial results without overstating what they establish.
3. **Assumptions and inference integrity.** Specify assumptions appropriate to the question, preserve material relationships among variables, and keep data, modeling choices and conclusions internally consistent. Distinguish observations, estimates, investor judgments and hypothetical conditions; do not infer stronger causal, predictive or probabilistic claims than the evidence supports. Do not require users to supply detail that the analysis can reasonably address with a justified method.
4. **Investment decision relevance.** Favor results that illuminate economically material opportunities, comparisons, changes or trade-offs for the contemplated decision. Assess informativeness and interpretability without requiring an unconditional preference or treating qualified or inconclusive results as failures by default.
5. **Incremental analytical contribution and consistency.** Justify an analytical component by the financial question and information it adds, not by a need for distinct formulas or sequential stages. Reuse evidence and computations consistently, reconcile overlapping results and avoid double counting or representing reused evidence as independent confirmation.
6. **Proportionate validation and complexity.** Match verification to the claim being assessed, distinguishing mathematical correctness, implementation behavior, exposure applicability, empirical reliability and practical usefulness. Apply appropriately scoped checks and sensitivity analysis; do not extrapolate their findings beyond what they test. Prefer the simplest sufficiently sound approach and add complexity only for material improvements in fidelity or decision value.

### 1.4 Common evidence and interpretation boundaries

**Observation, estimation and assumption.** Actual market observations, published-model estimates, issuer/benchmark disclosures and investor assumptions are different evidence types and retain their provenance. Statistical scenario sets describe the selected observations or model under stated conditions; they do not, without an additional validated forecasting interpretation, establish future event probabilities. Current ETF/benchmark exposure applied to historical yield movements is a **current-exposure counterfactual**, not an actual historical ETF return.

**Conditional, not predictive, conclusions.** Bondview evaluates outcomes under identified market conditions. It does not need to forecast the unique future Treasury curve or future ETF price to produce a useful conditional comparison. A result that holds across all scenarios in a specified set can establish a useful conditional finding about return resilience or relative advantage, but does not establish outcomes outside that set. A reported quantile or frequency from overlapping historical scenarios is descriptive unless a defensible probabilistic model is provided.

**Data and examples.** Operational analysis uses documented actual market observations and qualified issuer or benchmark exposures. Constructed or synthetic data are permitted in examples and arithmetic tests when clearly labeled; they do not substitute for verification with actual inputs.

**Scope exclusions.** Do not require independent reconstruction or auditing of ETF holdings, cash flows, hedges or futures books as a default. Realized ETF/benchmark price, NAV and total-return histories are separate diagnostics and must not silently substitute for compatible modeled-return baselines or missing exposure characteristics. Portfolio optimization, investor-specific position sizing, execution, taxes and detailed expense-ratio optimization are outside the initial scope. Do not double-count costs already reflected in input measures.

## 2. Data, ETF exposure, and comparability contracts

These are shared input, provenance, eligibility and comparability requirements. Each analysis uses only the information justified by its financial question and selected exposure.

### 2.1 Canonical market observations

| Data | Preferred initial source / treatment | Intended role |
|---|---|---|
| U.S. Treasury constant-maturity yields | FRED/H.15 `DGS2`, `DGS5`, `DGS10`, `DGS30`, other `DGS*` tenors as justified | Yield levels, dated curve comparisons and joint rate movements |
| Investment-grade and high-yield credit OAS | Matched documented ICE BofA/FRED series or suitable alternative | Credit compensation, repricing and credit-spread scenario conditions |
| USD/KRW (KRW per USD) | FRED `DEXKOUS` or suitable documented alternative | FX context and supported unhedged KRW outcomes |
| Cash/short-rate comparator | Defined currency- and horizon-compatible reference | Cash-relative comparisons when useful |
| Published Treasury term-premium decompositions | Documented credible sources; available models may include NY Fed ACM or SF Fed Christensen–Rudebusch | Interpret model-consistent expected-rate and premium components of Treasury yields |
| Real yields and inflation-expectation series | Optional credible sources | Specific supported market interpretation when material |

**Canonical factor rule:** Retain dated underlying Treasury yield observations. Derive spreads and observed **joint tenor changes** from properly aligned source dates; for example, obtain `y_10 - y_2` from `DGS10` and `DGS2`, using a published spread series only as a cross-check when useful. Reuse consistent factor observations for compared exposures. Partial investor conditions, statistically constructed scenario sets and explicit hypothetical vectors are distinct from directly observed joint historical vectors; their provenance and method must not be conflated.

Retain source, observation and availability dates, units, missing-data status, retrieval metadata and applicable data/model versions or revisions. Ensure compatible measurement definitions, business-day and endpoint alignment, and information availability at each assessment date. Missing observations may be estimated or imputed only through a justified, documented method; distinguish such values from direct observations.

### 2.2 ETF, benchmark and Treasury reference exposures

Use dated official issuer or exchange/listing disclosures for ETF characteristics. **ETF-first** is the default product-level source. The user may explicitly choose the ETF's designated benchmark as a qualified **benchmark exposure proxy**, using documented benchmark characteristics. Benchmark results describe that selected benchmark exposure and do not assert that ETF holdings, tracking or realized returns match it; portfolio reconstruction or tracking-difference estimation is not a prerequisite.

When neither eligible ETF nor benchmark data support a requested product calculation, **Treasury-tenor reference analysis remains available** where the market-factor definitions and exposure assumptions are explicit. Such tenor-level results are not relabeled as returns on a named ETF.

| Profile information | Use and required distinction |
|---|---|
| Ticker, name, issuer, mandate, benchmark, bond category | Exposure identity, eligibility and source |
| Cash bonds, futures, active/mixed exposure, leverage or overlay | Applicable rate and return mechanics |
| Dated modified/effective duration, with definition | Compatible yield sensitivity; tenor is not a substitute for duration |
| Relevant tenor and maturity exposure | Map portfolio sensitivities to market factors |
| Disclosed yield measure and definition | Distinguish portfolio YTM/YTW, SEC yield, benchmark yield and distribution yield |
| Credit quality and documented spread duration | Relevant corporate-credit treatment |
| Economic currency exposure, hedge policy and available hedge coverage | FX/hedge qualification and supported return effects |
| Published convexity, key-rate duration or other material measures | More precise exposure treatment when warranted |
| Source link, observed/as-of and available-to-user date, units | Provenance and reproducibility |

Selected ETF or benchmark data can be stale, incomplete or unsuitable for certain calculations. Record which source was selected and retain compatible yield, duration, currency, horizon and factor definitions. Do not silently combine benchmark YTM with ETF duration, infer missing exposures from realized return history, or substitute today's profile for a past profile when describing actual historical exposures. A valid current profile can be applied to earlier observed shocks **as a current-exposure scenario analysis**. Missing inputs require qualified partial results or an explicit unsupported/unavailable status, not fabricated accuracy.

### 2.3 Eligibility and measurement compatibility

| Selected product or exposure | Initially supported financial scope |
|---|---|
| Cash U.S. Treasury ETF | Compatible Treasury yield, rate sensitivity, conditional return and stress analysis |
| Cash corporate-bond ETF | Compatible Treasury-rate and credit-spread effects; omit unsupported total-return claims when credit inputs are material |
| Hedged/unhedged bond ETF | Supported bond measures; separate FX or hedge outputs when data permit; `(H)` does not imply costless/perfect hedging |
| Active, multi-tenor or mixed ETF | Calculations justified by disclosed factor sensitivities or a distinctly selected benchmark proxy |
| Treasury-futures ETF | Supported rate-factor sensitivity using compatible ETF or benchmark measures; cash-bond YTM/carry and return formulas apply only to an explicitly selected **cash-bond benchmark proxy**, not automatically to the futures ETF's own return |
| Leveraged, inverse or option-overlay ETF | Catalogable; first-order cash-bond return formulas are normally inapplicable |
| Generic 2Y/10Y/30Y Treasury reference | Market-tenor and defined hypothetical exposure outcomes with clearly stated instrument assumptions; no unsupported ETF attribution |

Eligibility is assessed **by calculation and selected exposure source**, not by automatic exclusion of an entire product. Distinguish **`value`**, **`N/A`** (inapplicable), **`unavailable`** (required data missing), **`unsupported`** (method inappropriate) and **`proxy`** (qualified substitution); none is interchangeable with zero. Compare only outputs with compatible currency, horizon, date, factor sensitivity and yield definitions. A product can support one financial analysis and lack inputs for another.

## 3. Fixed-Income Analyses

Sections **3.1–3.5** define the five Analyses: (1) Treasury Market Conditions and Scenarios, (2) Holding-Period Return, (3) Risk and Stress, (4) Credit Spread, and (5) Currency and Hedging. Section 3.6 defines shared method refinements, not a sixth analysis. Each Analysis states its economic question, supported methods and outputs, and role in tenor/ETF comparison. The shared evidence, scenario, date and interpretation contracts in §§1–2 and 4 apply throughout.

### 3.1 Treasury Market Conditions and Scenarios Analysis

**Question.** *What does U.S. Treasury market evidence reveal about interest-rate conditions and relationships across maturities relevant to tenor selection?*

**Yield-curve conditions and movements.**

*How have Treasury yield levels and curve shapes changed across maturities, and what do those changes reveal about maturity-specific interest-rate conditions?*

Derive maturity-specific yields and 10Y−2Y, 30Y−10Y and other relevant spreads from aligned Treasury observations. Examine both the shape of the curve and the **underlying tenor changes** that produced it: the same change in slope can accompany materially different rate-price consequences. Compare levels, changes and economically meaningful curve features across tenors and assessment dates. Where supported, examine compatible forward-rate information to interpret the market-implied rate structure, distinguishing it from a forecast of future spot rates.

**Expected short rates and term premiums.**

*To what extent do model-estimated expected short rates and term premiums explain changes in Treasury yields?*

For a consistently defined nominal Treasury zero-coupon yield, an established decomposition is:

`model_yield_n(t) ≈ model_expected_average_future_short_rates_n(t) + model_term_premium_n(t)`.

When useful, apply suitable published decompositions using mutually consistent model-fitted yields, expected short-rate components and term premiums. These model quantities are not directly interchangeable with observed constant-maturity or par yields. Examine expected-rate and term-premium **levels and changes** to identify their model-estimated contributions to Treasury yield movements and interpret interest-rate conditions relevant to tenor selection. These contributions can also guide investigation of potential macroeconomic influences, such as monetary-policy expectations, Treasury supply, inflation uncertainty and investor demand. Term premiums are model-estimated and may differ across models; no particular published model, maturity coverage or decomposition is required when unsupported. Attributing yield movements to specific underlying macroeconomic causes requires additional evidence.

**Conditional joint yield movements.**

*Given an investor's partial rate view and investment horizon, what corresponding movements across other Treasury maturities are supported by historical relationships or justified models?*

An investor may provide a limited, interpretable view—such as a rise, decline or approximate stability in 10Y yields over a chosen horizon—without specifying independent future changes for 2Y and 30Y. Under a **documented numerical condition** representing that view, examine complete multi-tenor yield movements using coherent historical observations or an appropriately justified conventional statistical/model-based method.

Historical conditioning, regression, PCA and other term-structure approaches are possible methods; select according to the financial question, available data and intended output. PCA may also describe historical common yield-curve movement factors (often level, slope and curvature), but its factors alone do **not** produce conditional joint scenarios without a justified conditioning and scenario-construction step. A simple historical method may be sufficient; added sophistication requires a useful analytical benefit.

The scenario output is the **set of coherent joint yield-change vectors**, with its conditioning rule, market factors, horizon, reference period and construction method. When a view conditions one tenor, retain the **same-interval movements of the other tenors** in historical scenarios, or the relevant cross-factor relationships implied by the justified modeled method; independently predicting every tenor is not a default requirement of the investor. Marginal ranges and co-movement descriptions may explain the set but must not be combined into purported historical joint vectors. Direction-only views require a clearly defined rate-change range or a justified conditioning convention; no universal rising/stable/falling thresholds are imposed. The selected historical or model-conditioned set is not automatically an estimated future probability distribution.

**Results and analytical relationships.**

Provide relevant dated yield-curve measures, supported interpretations of their movements and model-consistent decomposition estimates where useful. Yield-curve evolution, compatible forward-rate information and supported expected-rate/term-premium decomposition can provide **standalone market insight**.

When needed, provide coherent conditional joint scenarios or descriptive summaries for Analysis 2 without requiring a separate user-facing result. These functions need not use the same model: a yield decomposition is not automatically a scenario generator, and scenario construction need not independently establish ETF attractiveness.

Compare maturities and dates without equating Treasury-market/model measures with actual ETF portfolio returns. Analysis 1 need not predict a unique future curve or precede an independently specified Analysis 2 scenario.

### 3.2 Holding-Period Return Analysis — initial primary

**Questions.** *For the selected holding period and coherent market conditions, what supported gross returns are implied for eligible Treasury-tenor, ETF or benchmark exposures? Which outcomes and relative advantages persist or change across an entire relevant scenario set, and how do the opportunities compare across assessment dates?*

#### Return model

**Financial result.** The primary quantity is the **modeled gross USD holding-period total return of a compatible cash-bond exposure**, as a percentage of initial value, including supported compensation/accrual and rate-price effects. Relative modeled returns are expressed in **percentage points (pp)**. Do not equate this estimate with a quoted yield, a rate-only price change, an actually realized ETF return or a net KRW investor return. An observed realized total return instead uses the actual ending value and distributions under a stated convention.

**Scenario inputs.** Select the assessment date `t`, the eligible ETF, explicitly selected benchmark or reference Treasury exposure, and holding horizon `H`. Analyze either (i) a **complete, dated historical joint yield-change vector or a set of such vectors**, (ii) coherent modeled/conditioned vectors informed by Analysis 1 or another defensible source, or (iii) fully specified hypothetical vectors with their assumptions and any held-fixed factors. Preserve the **same complete scenario** when comparing exposures, and map its factors to each exposure using compatible sensitivity definitions. A separately supplied scenario remains valid without first running Analysis 1. General scenario and date conventions are in §4.

**Recognized return approximation.** The first-order cash-bond approach combines holding-period yield-based compensation with duration-based repricing. For a compatible exposure `i` in scenario `s`:

`R_hat_USD_bond_i,H(s) ≈ B_ref_i,H − D_i * delta_y_i(s) + 0.5 * C_i * [delta_y_i(s)]^2 + supported_credit_price_effect_i(s)`.

`B_ref_i,H` is a baseline compensation estimate under a stated yield/curve convention; `D_i` is a compatible effective or modified duration; `C_i` is compatible convexity **only when available**. `delta_y_i(s)` is a **decimal** yield change mapped consistently from the scenario to the selected exposure. Where nonparallel movements or multi-tenor holdings make one yield factor inadequate, use supported key-rate durations or other compatible factor sensitivities. For such cases, replace the scalar sensitivity with the corresponding multi-factor repricing approximation rather than summing an inappropriate single-tenor duration effect. Material corporate-credit repricing requires qualified spread factors and sensitivities (§3.4).

**Baseline compensation.** For a compatible dated issuer ETF or selected benchmark **portfolio YTM**, the initial gross USD approximation is:

`B_ref_i,H ≈ portfolio_YTM_i * H_years`.

The selected yield definition must be suitable; distribution yield is not a substitute. This baseline is a first-order yield-based compensation proxy, not realized coupon income or an independently measured roll-down return, and may not precisely describe a rebalanced ETF. Baseline approximation errors can affect absolute returns and relative comparisons across ETFs or assessment dates. A curve-consistent carry/roll refinement of the baseline may be considered when supported by exposure data and material decision benefit, with appropriate aging/rebalancing conventions and no double counting. A detailed reconstruction of every issuer holding is not a prerequisite.

**Instrument and model scope.** A selected cash-bond ETF or compatible selected cash-bond benchmark can support the stated baseline and repricing approach. Futures-linked ETF returns require their own supported futures/roll/collateral economics; a chosen cash-bond benchmark produces results **for the benchmark exposure**, not the futures ETF itself. Static assessment-date duration approximates local exposure over the stated shock; convexity improves local nonlinearity but does not capture future portfolio changes. For unsupported baseline, spread, hedge or other material terms, report a qualified **partial return or rate-price effect** rather than a complete total return. Realized ETF/index total-return histories are independent diagnostics, not a hidden baseline to which rate effects are added.

#### Return comparisons

**Comparison across a scenario set.** For each joint vector `s`, calculate supported outcomes for **all compatible candidates** and the **paired differences** `R_hat_i,H(s) − R_hat_j,H(s)`. Characterize the collection of paired outcomes and economically meaningful conclusions, including:

- **Scenario-wide results:** e.g., a positive modeled outcome for one exposure, or a relative advantage that holds **throughout the specified set**.
- **Conditional comparative results:** the magnitude and direction of relative returns, circumstances that reverse a preference, and return compensation relative to the extra duration assumed.
- **Descriptive distributions:** supported ranges, quantiles, adverse and favorable outcomes, or within-scenario counts under the explicitly selected historical/model set, without relabeling empirical counts as predictive probabilities.
- **Changes across assessment dates:** changes in conditional opportunities and relative differences using compatible, preferably common or explicitly reconciled scenario definitions and appropriately dated exposure profiles (§4.3).

Meaningful trade-offs and insufficient discrimination are reportable financial results. Quantiles of different tenors' yield changes or different ETFs' modeled returns calculated **separately** are marginal summaries; they are not a simultaneously observed joint scenario. Preserve pairing when drawing cross-exposure conclusions.

**Break-even and sensitivity comparisons.** Relative-return comparisons can also identify conditions under which two exposures produce equal modeled returns. For two compatible single-factor cash-bond exposures under the first-order approximation, ignoring unsupported refinements:

`R_hat_i,H(s) − R_hat_j,H(s) ≈ (B_ref_i,H − B_ref_j,H) − D_i * delta_y_i(s) + D_j * delta_y_j(s)`.

Setting this difference to zero gives a conditional **equal-return relation** among the relevant joint yield changes; it does not require assuming a parallel shift. Present a tabulated boundary or a fixed-factor slice/region plot only when it improves understanding of the actual comparison. For the special case of a **common parallel yield change** and nonzero duration difference:

`relative_break_even_rise_bp ≈ 10,000 * (B_ref_i,H − B_ref_j,H) / (D_i − D_j)`.

The scalar expression does not apply as a universal cross-tenor threshold under nonparallel movements. When supported convexity, spread effects or key-rate sensitivities materially change relative returns, calculate break-even conditions using the full compatible model rather than retaining an inapplicable linear approximation. Such comparisons establish **conditional return relations**, not the expected future yield path.

#### Output contract

Report the selected ETF/benchmark/reference source; assessment date and exposure-profile date; horizon and year fraction; scenario source, type and conditioning (including historical endpoints where applicable); factor mapping; baseline and supported repricing components; modeled return **scope and units**; and matched relative comparisons. Provide a concise conclusion across the specified set whenever supported, clearly distinguishing conditional conclusions from claims about outcomes outside the set. Credit, currency and hedging extensions in Analyses 4–5 can subsequently modify a rate-only/gross USD comparison when defensibly modeled.

### 3.3 Risk and Stress Analysis — initial primary

**Question.** *How vulnerable are candidate exposures and the conditional comparisons from Analysis 2 to material adverse market changes? Which risk sensitivities and adverse outcomes explain the differences among tenors/ETFs?*

**Methods.** Use recognized rate-risk quantities: disclosed effective/modified duration, DV01/BPV for a stated position size, compatible convexity and key-rate durations where supported. Apply the same **complete joint yield scenarios** used for comparable holding-period returns when appropriate; also permit separately specified historical stress episodes or transparently constructed hypothetical stresses. Incorporate compatible spread, FX or hedge sensitivities when those risks are material and supported by the instrument and data. A rate-only measure must remain labeled as such.

**Additional risk information.** Quantify directional rate sensitivity, exposure-scaled downside magnitude, selected adverse outcomes, worst observed or specified stress episodes, and conditional distributions of **supported** return/price effects. Distinguish current-exposure historical stress from actual past ETF performance. For a historical set, describe the reference sample, overlap and empirical quantiles; unsupported probability or value-at-risk interpretations must not be inferred from scenario counts. When useful, compare changes in exposures and supported downside measures across assessment dates with dates and assumptions aligned.

**Relationship to Analysis 2.** Both Analyses may use the **same pricing equations and scenarios**. Analysis 2 asks which returns and relative preferences arise under the conditions; Analysis 3 emphasizes **adverse sensitivity, magnitudes and risk drivers**, including vulnerabilities that may qualify an attractive conditional return. Do not repackage an already displayed negative Analysis 2 return as independent risk evidence. If only one specified stress is available, present it as a single stress rather than inventing a risk distribution or score.

### 3.4 Credit Spread Analysis

**Question.** *How do Treasury rates and credit-spread changes jointly affect the market conditions, compensation and return/risk of eligible corporate-bond exposures? Which effects materially qualify or change comparisons based only on Treasury rates?*

**Market interpretation.** For a suitably matched corporate bond/index yield and spread definition, use the recognized first-order relation:

`delta_y_corporate ≈ delta_y_matched_Treasury + delta_OAS`.

Report the rate and OAS changes separately and examine their evolution across dates and suitable IG/HY sectors. OAS is a **model-derived spread** affected by credit, liquidity, optionality and risk premiums; it is not a direct measure of realized defaults. The decomposition can be useful for a single credit segment even when a direct comparison with a Treasury ETF is not supported.

**Exposure and return effects.** For an eligible credit exposure with compatible rate and spread sensitivities:

`price_effect_credit_i ≈ −D_rates,i * delta_y_matched_Treasury − D_spread,i * delta_OAS_i`.

Apply matched rate/spread scenarios and issuer/selected-benchmark sensitivities. Show rate and spread contributions and their supported combined first-order effect. Where yield-based compensation, rate and spread components are mutually compatible, **feed credit-related pricing into Analysis 2's return comparison** rather than treating it solely as a later risk note; do not add a second spread effect if the chosen comprehensive repricing model already contains it. An OAS rise can increase quoted compensation while producing an immediate negative price effect. More evidence is required to infer expected defaults or the adequacy of compensation for actual credit losses.

**Results.** Matched dated Treasury and OAS levels/changes, yield decomposition, qualified spread sensitivities and historical/conditioned credit-stress outcomes; compare valid corporate products, segments and assessment dates. For pure Treasury exposures, credit OAS is `N/A`. Additional default, rating, liquidity or other public indicators may refine interpretation when useful; they are not mandatory for the basic rate/spread analysis.

### 3.5 Currency and Hedging Analysis — lower initial priority

**Question.** *How do the economic currency exposures and hedge arrangements of eligible products change the interpretation and comparison of USD bond outcomes for a Korean investor?*

For a **compatible unhedged** USD holding-period bond return and matched USD/KRW return (KRW per USD), use the conventional multiplicative relation:

`1 + R_KRW = (1 + R_USD) * (1 + R_USDKRW)`.

Evaluate the same holding horizon and coherent currency/rate conditions where a joint comparison is intended. Disclosed hedge policy and measurable coverage may inform a qualified hedged-product sensitivity; labels alone do not determine actual hedge ratio, forward points, hedge costs, tracking differences or complete KRW returns. A hedged portfolio must not be analyzed as if its hedging were perfect and costless.

**Results and relationship to Analysis 2.** Report supported KRW translation, FX sensitivity, disclosed hedge characteristics and conditional cross-product differences, with costs or residual exposures included only where data and instrument conventions justify them. Supported FX/hedging economics **may change the relative return conclusion** from gross USD Analysis 2; when they cannot be quantified, keep the USD analysis valid within its stated scope and identify the missing KRW component. Detailed hedging modeling remains optional in the initial phase without implying zero hedge cost or currency risk.

### 3.6 Method refinements and relationships between analyses

Convexity, key-rate duration, curve-consistent carry/roll, defined-basket cash-flow repricing, historical conditional modeling, PCA, regression, published term-structure estimates and advanced hedging/credit economics may improve a particular result **when their inputs and added economic value are justified**. Methods estimating the same quantity are alternatives or robustness checks, not independent confirmations of investment attractiveness.

Scenario construction and shared repricing calculations may serve several analyses. Keep **modeling responsibility** distinct from user-facing **financial questions**: an independently informative market decomposition need not generate yield scenarios, and a single scenario set may support both return comparison and risk evaluation. Credit/FX components can extend or qualify the rate-only calculation.

## 4. Historical market movements and assessment-date conventions

### 4.1 Joint yield-change scenarios

A single observed historical interval `[u,v]` yields a coherent factor movement:

`s_(u,v) = (y_2(v) − y_2(u), y_10(v) − y_10(u), y_30(v) − y_30(u))`.

All entries use the **same aligned start and end dates**. A collection of such intervals is a historical scenario set. In a conditionally selected set (for example, historical intervals whose 10Y changes met a defined rise/stability/decline condition), retain **each complete joint vector** and its dates; selecting 2Y, 10Y and 30Y percentile values independently does **not** define a jointly observed scenario.

A complete hypothetical vector, a statistically constructed/model-conditioned joint vector, and a directly observed historical vector are distinct scenario types. Model-conditioned sets may be informed by an investor's partial tenor view, provided the condition, conditioning methodology, factor coverage and sources are recorded. No fixed classification, covariance model, PCA method, unique future vector or model-generated probability estimate is required by this architecture. When the data support only partial movements or sensitivities, report their limited scope instead of silently completing a curve.

### 4.2 Holding horizon, reference history and assessment dates

Use the following distinct time concepts consistently:

- **Holding/scenario horizon `H`:** the investment holding period used for compensation and the stipulated rate/spread movements; for a historical interval this follows its endpoints and the year-fraction convention.
- **Historical reference window `W`:** the market-history period from which intervals, scenarios or model inputs are selected. It may differ from the investment horizon.
- **Observation frequency and overlap:** daily rolling, monthly or nonoverlapping intervals. Overlapping horizon changes are dependent observations; their counts are not independent event probabilities.
- **Assessment date `t`:** the date whose exposure characteristics and available market information are used for the contemplated decision.

For hypothetical or model-conditioned scenarios, specify the forward holding horizon and conditioning assumptions rather than inventing historical endpoints. For historical intervals use actual aligned endpoints; if a common-horizon approximation is substituted for slightly different elapsed periods, disclose the convention and avoid interpreting the results as exact elapsed-horizon returns.

Only data and disclosures available at assessment date `t` may influence results presented as available at `t`. Record reference-history choice, endpoint treatment, missing observation rules and revisions when relevant. If the same analysis is reported for successive assessment dates, distinguish changes driven by market observations, scenario samples, estimation methods and exposure characteristics.

### 4.3 Exposure profiles across dates

Applying an **assessment-date ETF or selected benchmark profile** to an earlier market movement produces a conditional current-exposure outcome, not a historically realized product return. Historical assessment-date comparisons require characteristics available at each assessment date, or a clearly declared constant-exposure/benchmark assumption. Never fabricate historical duration or portfolio YTM.

When comparing opportunity changes across assessment dates, apply a **common or explicitly reconciled scenario basis** wherever possible. Otherwise identify whether different findings arise from changes in the exposure, yield/compensation, selected market conditions or historical/model estimation window. With exposure and yield shock fixed, the first-order price effect remains fixed.

### 4.4 Scenario-set summaries and interpretation

Analyze modeled outcomes using the **complete joint scenario observations** and supported exposure measures. Marginal tenor-change percentiles may summarize market conditions, but do not imply that same-ranked tenor percentiles occurred together. For cross-exposure comparisons, retain within-scenario pairing before calculating relative return differences or scenario-wide conclusions.

Historical-condition counts, empirical quantiles and frequency of an ETF being best describe the selected set; they are **not** unconditional future probabilities. Scenario-wide statements—such as a positive modeled return for every selected movement—apply only to the specified scenario set and return model. Report relevant conditional assumptions and material limitations once at the appropriate result level.

## 5. Results, comparison and presentation

Report quantities that answer the investor's financial question **across candidate tenors/ETFs, across valid assessment dates and under specified market conditions**, using compatible model and exposure definitions. The preferred explanatory order is market interpretation, conditional return comparison, then risk and material credit/FX qualifications. Results from an individual analysis may also stand alone.

For **Analysis 1**, distinguish independently informative market results (e.g., curve evolution, forward-rate structure or supported yield decompositions) from **conditional joint-scenario evidence** that can inform Analysis 2. For **Analysis 2**, place supported **tenor/ETF holding-period returns, paired differences and meaningful conclusions across the supplied scenario set** ahead of raw scenario-axis charts. Relative outcomes may include consistent findings across the specified set, meaningful conditional advantages, break-even conditions, or clearly identified sensitivity to unresolved conditions. For **Analysis 3**, emphasize additional adverse-outcome or sensitivity information rather than reproducing Analysis 2 returns as if they were independent findings. Credit and FX/hedge effects may modify a comparison as well as describe associated risks.

| User question | Suitable user-facing evidence |
|---|---|
| How have Treasury yield-curve conditions and model-estimated components changed? | Dated curve/tenor comparisons, compatible forward rates or model-consistent expected-rate/term-premium components |
| What joint market movements are relevant to an investor's partial view? | A specified complete conditional historical or modeled scenario set; descriptive tenor ranges plus provenance, horizon and conditioning rule |
| Which exposures benefit under those conditions? | Compatible modeled returns, within-scenario paired return differences, conditional dominance or break-even relationships across eligible tenors/ETFs |
| Have relative opportunities changed since an earlier assessment? | Comparable dated yield/exposure assumptions, aligned scenario basis and changes in supported relative outcomes |
| What risks or omitted return drivers change the interpretation? | Exposure-adjusted adverse effects, material credit/FX and hedging qualifications, supported alternative return components |

Each user-facing result should make its **assessment date, instrument/benchmark identity, horizon, scenario/source definition, numerical measure and units** clear. State material approximations and unsupported components concisely. Distinguish ETF, benchmark and generic Treasury-tenor outputs.

Use tables, charts and concise narrative where they add interpretive value. Use sensitivity and break-even visualizations when they clarify financially meaningful comparisons. Prioritize supported investment conclusions over exploratory displays, and explain when the conditions are insufficient to distinguish alternatives.

## 6. Implementation, verification, and bounded initial research

### 6.1 Implementation boundary

Use a small, cohesive Python implementation for dated market observations, selected ETF/benchmark/Treasury reference exposures, coherent observed and constructed scenario sets, recognized fixed-income calculations and result presentation. Share financial computations among analyses rather than implementing duplicate pricing engines. Scenario-generation methods are implementation choices subject to the review criteria in §1.3, not mandatory extra software stages.

Provide one or more sequential Jupyter notebooks to select the assessment date, exposures, investor condition and horizon; inspect calculations and display decision-relevant tables and visualizations. Keep substantive methods in importable `.py` modules. Retain dates, units, provenance, source identity, scenario rules and meaningful error/availability statuses.

### 6.2 Calculation and behavioral verification

Tests verify arithmetic, implementation behavior, method applicability and evidence contracts. Interpret results within the scope of the assumptions and inputs tested.

| Calculation / property | Hand-checkable expectation |
|---|---|
| Treasury yields 2Y `4.0%`, 10Y `4.5%`, 30Y `4.8%` | Derive 10Y−2Y `+50 bp`, 30Y−10Y `+30 bp` from dated underlying yields |
| Duration `D=8`, +50 bp yield change | First-order rate price effect `−4.00%` |
| Compatible convexity `C=80`, +50 bp yield change | First-order `−4.00%` plus `0.5 × 80 × (0.005)^2` = `−3.90%` |
| Two exposure durations `1.9`, `7.5`, matched +20/+10 bp movements (2Y/10Y) | 10Y minus 2Y rate-price effect `−7.5 × 0.001 + 1.9 × 0.002 = −0.37 pp` |
| Portfolio YTM `5%`, horizon 0.5 years, duration `7`, matched +50 bp | Compensation proxy `+2.50%`, rate price effect `−3.50%`, modeled compatible gross USD cash-bond exposure return `−1.00%` |
| Historical scenario `[u,v]` | Construct aligned, same-interval changes for every required tenor, with `H` derived from the interval |
| Investor condition on 10Y yield changes | Retain entire matching historical joint vectors; separately sorted 2Y/10Y/30Y quantiles are not combined into a fabricated observed vector |
| Joint scenarios applied to two alternative exposures | Evaluate both exposures on each **same complete scenario**, then calculate paired return differences; scenario-wide claims match the specified set |
| Current exposure shocked with earlier yield movements | Label counterfactual current-exposure calculation, not historical realized ETF return |
| Matched rate duration `5.5`, spread duration `5`, Treasury −20 bp, OAS +60 bp | Rate `+1.10%`, spread `−3.00%`, combined `−1.90%` for those supported components only |
| Unhedged USD bond result `−2%`, USD/KRW +8% | KRW return `(0.98 × 1.08) − 1 = +5.84%` |
| Compatible one-year yield compensation difference `+1 pp`, durations `7.5`, `1.9`, common yield rise | Conditional first-order break-even rise `17.86 bp`, not a universal cross-tenor threshold |
| Cross-tenor first-order return comparison | Use joint movements and the compatible expression `R_i−R_j ≈ (B_i−B_j)−D_iΔy_i+D_jΔy_j`; no single common-shock threshold without that explicit assumption |

Also verify source/as-of availability, missing data and endpoint alignment, decimal/percentage/bp conversions, scenario conditioning and factor mapping, horizon consistency, issuer vs selected benchmark identity, yield definition compatibility, carry/roll/price-effect double-count prevention, valid futures applicability, qualified partial outcomes, paired relative-return statistics and clearly labeled scenario-count/quantile interpretations. Historical prices/NAV/total returns remain separate diagnostics rather than a hidden replacement for model inputs.

Verification should fit the adopted method and exposure, with additional checks for more complex PCA, credit, key-rate duration, repricing or hedge models when relevant.

### 6.3 Initial research demonstrations

An initial, separately authorized research effort should demonstrate the financial outputs:

1. Actual aligned Treasury market history and a small representative set of dated, issuer-reported ETF exposures; qualified benchmark or reference-tenor alternatives when necessary.
2. A user-facing **Analysis 1 market result** that independently explains dated Treasury curve conditions or supported yield decompositions, and a clearly sourced illustration of how a partial investor condition may yield coherent joint scenarios using a defensible simple method. Do not require the same model to provide both capabilities.
3. A **holding-period return comparison** for compatible 2Y/10Y/30Y tenors or eligible selected ETF/benchmark exposures using a defined scenario set, including compensation inputs, rate effects, within-scenario paired differences and a meaningful conclusion across the set where supported.
4. Complementary adverse-outcome/rate-sensitivity analysis and, for eligible products, supported credit and currency/hedging effects that may alter the interpretation of relative returns.
5. Reproducible provenance, source/assessment dates, material approximation labels and calculation/behavioral checks in §6.2.

Research findings inform subsequent method and scope choices under §1.3. No research demonstration alone authorizes repository or implementation changes beyond its separately approved assignment.

## 7. Method selection, extensions and source context

Use the following boundaries when selecting methods as the analysis definitions develop:

- **Joint scenario modeling:** Begin with coherent observed or justified conditional historical yield movements when informative. Evaluate PCA, regression or other term-structure methods only for a specified incremental financial benefit; preserve conditional structure and do not claim a unique future curve or probability forecast without support. The horizon, reference history and interest-rate regime are material documented inputs.
- **Independent market interpretation:** Published model-consistent term-premium/expected-rate decompositions and compatible forward-rate measures may be used where their definitions, maturity coverage and financial question support them. A decomposition does not automatically generate scenarios, and an observed co-movement statistic alone is not necessarily an independently useful ETF conclusion.
- **Holding-period compensation and return fidelity:** Use the documented first-order yield/carry and duration approach for compatible cash-bond exposures. Refine with convexity, published key-rate duration, consistent cash-flow repricing or justified roll only when supported and materially useful; do not double count carry and roll or treat rebalanced ETFs as unchanged individual bonds.
- **Product-specific mechanics:** A futures, mixed, leveraged or otherwise specialized ETF requires compatible economics for full-return claims. A separately selected cash-bond benchmark supports comparison of **that benchmark exposure**, not an assertion about the ETF's own futures/overlay return.
- **Credit and currency:** Corporate spread and unhedged FX effects can affect modeled outcomes, while disclosed hedging may require additional economics. Report partial components clearly where full comparison is not supported.

**References and data context:** [FRED DGS2](https://fred.stlouisfed.org/series/DGS2), [DGS10](https://fred.stlouisfed.org/series/DGS10), [DGS30](https://fred.stlouisfed.org/series/DGS30), [DEXKOUS](https://fred.stlouisfed.org/series/DEXKOUS); [CFA Institute — Fixed-Income Portfolio Management](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/overview-fixed-income-portfolio-management) and [Yield-Curve Strategies](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-curve-strategies); [AQR — Alternative Thinking: Style Premia / Bond Returns](https://www.aqr.com/-/media/AQR/Documents/Insights/Alternative-Thinking/Alternative-Thinking-Style-Premia-Bond-Returns.pdf) for the recognized first-order yield-plus-duration approximation; [New York Fed — ACM Treasury Term Premia](https://www.newyorkfed.org/research/data_indicators/term-premia-tabs), [San Francisco Fed — Treasury Yield Premiums](https://www.frbsf.org/research-and-insights/data-and-indicators/treasury-yield-premiums/) and [Federal Reserve Board — Three-Factor Nominal Term Structure Model](https://www.federalreserve.gov/data/three-factor-nominal-term-structure-model.htm) for published-model definitions and estimates.
