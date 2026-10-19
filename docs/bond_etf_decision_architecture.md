# Korean-Listed U.S. Bond ETF Selection — System Architecture

**Status:** PROVISIONAL research architecture, revised 2026-10-19. It is an intended-system specification and bounded research proposal, **not** a finalized quantitative attractiveness model, a development roadmap, or authorization to run Bernie.

**Repository:** `lbk209/bondview-v3`  
**Base document:** `docs/bond_etf_decision_architecture.md` on `main` (2026-10-13 research architecture).  
**Companion:** [`bond_etf_decision_examples.md`](bond_etf_decision_examples.md), **not yet revised to conform to this architecture**. Existing examples remain provisional research fixtures, not automatically accepted tests. Bondview-v2 is reference-only.

## 1. Purpose and decision scope

Bondview-v3 is a **convenient decision-support system for selecting Korean-listed ETFs with U.S. fixed-income exposure**. It uses observations of the underlying bond market and **issuer-published ETF exposure characteristics**, not ETF historical prices, to help answer two primary questions:

1. **Current cross-ETF comparison:** Which eligible ETF exposures are relatively more attractive under current bond-market conditions, across different maturity segments and, where defensible, credit categories? Why?
2. **Same-ETF change through time:** Over a selected date range, how have the market conditions relevant to an ETF's disclosed exposure become more or less favorable? Which observations support that assessment?

**Independent market assessment** is also a useful first-class output: the U.S. Treasury curve, yield changes, credit conditions and related risk/compensation observations can be analyzed with no ETF selected.

This system is for ETF selection, **not** an individual-bond investment platform, portfolio-construction optimizer, holding-size planner, trade execution engine, or ETF price forecasting engine. A change in attractiveness is an opportunity assessment, **not** evidence that the next market move or optimal buy date is known.

**Working design commitments:** underlying market assessment is separable from ETF translation; disclosed ETF characteristics are accepted as operational inputs; ETF prices/returns cannot influence attractiveness; established quantitative methods are preferred; results must support comparisons across durations; Python modules support a Jupyter notebook interface. **Unresolved:** an exact numerical attractiveness measure, investment-policy thresholds, universal rankings, and the minimum economically credible compensation measures.

## 2. Independent market assessment and ETF translation

The distinction is analytical rather than a compulsory code/module hierarchy.

```text
Public U.S. bond-market observations
  Treasury yields, curve, historical changes, credit spreads, etc.
                          |
                          v
         ETF-INDEPENDENT MARKET ASSESSMENT
       (available without selecting any fund)
                          |
                          +----------------------------+
                                                       |
                              Issuer-published ETF characteristics
                              structure, duration, yield convention,
                              credit type, currency/hedge policy
                                                       |
                                                       v
                                    EXPOSURE-AWARE ETF ASSESSMENT
                                     sensitivities / compensation /
                                           comparable scenarios
                                                       |
                                                       v
                                    CONDITIONAL ETF COMPARISONS
                                  today versus alternatives; same
                                        ETF through selected history
```

The market layer can state that 10Y Treasury yields increased, the 2s10s slope steepened, or credit OAS widened. **Those observations alone do not establish a buy decision.** The ETF layer determines which observations are relevant to a particular product's published exposure and whether a comparison is economically meaningful.

This differs conceptually from the earlier v2 approach in which an ETF profile affected Core constituent evaluation itself. That comparison explains the intended separation; **no v2 architecture, scoring, states or rules are inherited**.

## 3. The two ETF questions and common conventions

### 3.1 Cross-maturity and cross-category comparison

An assessment or holding **horizon** (e.g., one year for an illustrative scenario) is not the maturity of an underlying bond or a restriction to similarly maturing ETFs. A common horizon can compare short, intermediate and long Treasury exposures.

For an ETF comparison, explicitly identify:
- the market and product exposures actually being compared;
- observed compensation/yield information and its definition;
- interest-rate risk and relevant credit/currency differences;
- common scenario assumptions, units, and dates;
- the conditions under which a preference reverses or cannot be determined.

Treasury and corporate exposures may both have improving *absolute* starting yields while their *relative* attractiveness changes in the opposite direction as credit spreads move. Separate these questions. A credit OAS does not eliminate expected-default, liquidity or downgrade risks.

A universal complete ranking is **not required**. Meaningful outcomes may be conditional, mixed, incomparable or insufficiently supported.

### 3.2 One ETF over a user-selected date range

Show **continuous histories of relevant quantitative market opportunity measures**, not just endpoint labels, and explain material changes. Do not plot historical ETF price changes as an attractiveness measure.

**Historical exposure discipline:** If dated issuer profiles are available, use them only for dates at which they were public. Otherwise, a **fixed disclosed exposure** (for example today's issuer duration) may be applied to historical market observations as a clearly marked *constant-exposure counterfactual*. It must not be described as the ETF's actual historical holdings or returns.

In particular, **today's issuer-published yield must never be copied backward into earlier dates**. Historical Treasury yields or OAS may serve as explicitly labeled *market reference series*; they are not necessarily the ETF's actual historical YTM or carry.

The reference investment assumptions must remain consistent across dates. A worsening credit environment can offset an apparently improved starting yield. A steadily improving indicator may justify considering purchase, not imply imminent gains.

## 4. Universe and permissible product types

**Final intended catalog:** all Korean-listed ETFs with U.S. fixed-income exposure, including eligible Treasury and corporate-bond exposures. Catalogued, quantitatively assessable, and directly comparable are **different statuses**; inclusion in the catalog does not guarantee every model can be applied.

**Initial experimentation:** choose only a few representative products with verified issuer information and economically distinct exposures. Product/ticker choice is an implementation matter, not a fixed architecture list.

- **Ordinary cash-bond ETFs:** evaluate using supported market observations and disclosed exposures.
- **Treasury futures ETFs:** excluded from the standard universe by default; permit user opt-in with a prominent *futures are not cash bonds* warning. Rate risk may be shown if compatible issuer exposure is disclosed. Do **not** invent ordinary cash-bond yield, carry or roll calculations.
- **Hedged / unhedged ETFs:** include with policy and comparability qualifications. `(H)` does not prove a perfect, costless hedge.
- **Active / mixed-credit ETFs:** use documented exposure rather than inferred holdings; require appropriate credit/rate risk separation when claiming a quantified credit conclusion.
- **Leveraged, inverse, covered-call, option-overlay or otherwise complex products:** catalog if appropriate, but do not force into standard cash-bond models; an unsupported assessment is valid.

## 5. Market-data contract

| Observation | Candidate source | Application and warning |
|---|---|---|
| U.S. Treasury constant-maturity yields | FRED/H.15: `DGS3MO`, `DGS6MO`, `DGS2`, `DGS5`, `DGS10`, `DGS20`, `DGS30` | Tenor yields, changes, slope/curve; **not** ETF yield-to-maturity or its duration |
| U.S. IG/HY credit OAS | Available ICE BofA/FRED or another permitted documented source | Credit-market conditions; respect licensing, series coverage and vintage limits |
| USD/KRW (KRW per USD) | FRED `DEXKOUS` or documented equivalent | Currency scenarios and context, **not** expected FX direction |
| A relevant cash / short-rate reference | Dated currency-consistent source when needed | Optional comparison; USD Treasury bills are **not** KRW cash |
| Real yields, inflation expectations, term premium | Documented sources when economically useful | Optional explanatory context; model-derived term premium is not a standalone timing rule |

Record observation date, source, units, data cutoff, retrieval/revision information where relevant, missing observations, and comparison alignment. Avoid forward-looking input leakage. A six-month or one-year lookback is user-selectable; previously inherited 21/126-day windows and five-day averaging are **research conventions, not accepted mandatory formulas**.

## 6. Minimal issuer-based ETF profile

Take characteristics from official issuer documents and listing disclosures **without reconstructing constituent securities**. Record their meaning, dates and source. The minimum is intentionally small:

| Field | Requirement |
|---|---|
| Ticker, official ETF name, issuer | Required for identification |
| Underlying investment/benchmark category | Required for economic routing; benchmark ≠ proof of current holdings |
| Product structure | Cash bonds, futures, active, derivatives, leverage/overlay as applicable |
| Currency exposure and hedge policy | Required for comparability qualification |
| Published effective/modified duration and its definition | Required **to produce numerical rate-sensitivity results** |
| Published portfolio yield and exact convention | Use when available; distinguish YTM, YTW, index yield, SEC yield and distribution yield |
| Credit category / rating or benchmark | Required **for credit-specific conclusions** |
| Maturity segment and relevant reference tenor | Where disclosed |
| Document/source, disclosure/as-of date, units | Required for material numerical inputs |

Optional: convexity, key-rate duration, spread duration, hedge coverage, distribution information, etc. **Missing characteristics do not justify a substantial ETF-modeling project.** A compatible issuer-index proxy may be used only with prominent disclosure and downgraded quality; an incompatible or unsupported calculation should be `not assessed`, not zero or a fabricated precision. Source recency is reported, but a universal staleness threshold is not yet adopted.

## 7. Accepted baseline mathematics and optional refinements

For every calculation, identify **observed** input, **issuer-published** characteristic, **derived hypothetical sensitivity**, **assumption/proxy**, and **missing** quantity. Record units, method and compatible scope.

### 7.1 Treasury levels, changes and curve

For tenor `n`, `delta_y_n(t0,t1) = y_n(t1) - y_n(t0)` using observations actually available at the selected times. If `y` is in decimal yield units, convert to basis points by multiplying by `10,000`; if `y` is in percent units, multiply the difference by `100`.

Simple slopes include `y_10 - y_2` and `y_30 - y_10`. Explain how both endpoints moved, not merely whether the resulting slope steepened or flattened. No rate-change statistic is itself a prediction.

### 7.2 Duration and convexity

For an economically compatible bond exposure with published effective/modified duration `D`, and a **hypothetical** parallel or appropriately matched yield change `delta_y` expressed as a decimal:

`rate_price_effect ≈ -D * delta_y`.

If a compatible convexity `C` is available, a legitimate refinement is:

`rate_price_effect ≈ -D * delta_y + 0.5 * C * (delta_y)^2`.

If credible key-rate durations exist, nonparallel curve shocks may instead use `-sum(KRD_k * delta_y_k)`. Never add a key-rate result and a parallel-duration result for the same shock. A current `D` applied to a historical-sized shock is **current-exposure scenario sensitivity**, not realized ETF performance.

An initial illustrative shock suite is `{+50bp, +100bp, -50bp}`, with a nonparallel example where defensible. None represents a probability-weighted forecast.

### 7.3 Compensation and carry

**Observed Treasury yield or corporate spread** describes market compensation. **Issuer-published ETF yield** is product-specific but depends on its reporting convention. **ETF economic carry** requires stronger assumptions about cash flows, portfolio turnover, funding, hedging and period.

An ETF distribution yield is **not automatically YTM, YTW, or carry**. For an ETF maintaining target duration through rebalancing, fixed-bond held-to-maturity roll-down cannot be directly assumed.

Where comparable and defensible, an illustrative cash-bond horizon scenario may be evaluated:

`illustrative_H_return ≈ defensible_H_carry + justified_roll_effect - D*delta_y + supported_credit_effect`.

Omit unsupported terms and **do not present the incomplete sum as complete total return**. Do not transform unhedged USD yield into hedged KRW compensation by assuming away forward/hedging costs.

An illustrative *rate-shock break-even versus cash*, where all measures share a comparable horizon and currency basis, is:

`break_even_rise_bp ≈ 10,000 * (defensible_H_carry - compatible_cash_return_H) / D` for `D > 0`.

A pairwise break-even may similarly be calculated only if **incremental comparable compensation** and the **difference in appropriate duration exposures** are well-defined under the stated shock assumption. If input comparability fails, withhold the numeric break-even instead of substituting a distribution yield.

### 7.4 Credit exposure

For a credit product with compatible rate and spread durations:

`credit_price_effect ≈ -D_rates * delta_y_matched_Treasury - D_spread * delta_OAS`.

Corporate yield changes may reflect both Treasury yield changes and spread moves. OAS is not guaranteed realized compensation after defaults, downgrades or liquidity effects. Avoid precise credit predictions without a valid spread input/measure.

### 7.5 Currency exposure

For consistent unhedged USD bond and FX returns over the same period:

`1 + R_KRW = (1 + R_USD) * (1 + R_USDKRW)`.

This is an FX accounting/scenario identity, **not** a forecast of USD/KRW. Hedged funds require issuer hedge policy and a defensible treatment of residual FX and forward/cost effects; otherwise, return/carry comparison must be explicitly incomplete.

### 7.6 General rule permitting a better model

Specified formulas are **minimum reproducible baselines**, not restrictions to first-order approximations. A conventional enhancement is allowed when it: (1) answers the same economic question; (2) uses defensible compatible inputs; (3) preserves a separately checkable baseline and explains changes; (4) makes no ETF-price-history selection signal; and (5) provides a proportionate economic benefit. A higher-order term can legitimately change a conclusion; it need not artificially match the baseline answer.

Material changes to the economic question, source policy, risk interpretation, decision objective, or construction of an opaque score require an explicit design decision. Do not expand into holdings reconstruction, hedge/futures replication or forecasting merely because more elaborate techniques exist.

## 8. Attractiveness — an unresolved quantitative research question

**No particular numeric attractiveness scalar, ordinal label threshold, or universal ETF ranking is accepted yet.** The purpose of the first quantitative experiment is to find a transparent and useful definition, or to establish that multiple measures with conditional explanations are better.

Candidate evidence, where comparable and available:

| Measure | Role in assessment |
|---|---|
| Relevant market yield: level and changes | Starting compensation of the relevant bond-market segment, not ETF total return |
| Issuer-reported ETF yield at its as-of date | More direct but convention-dependent ETF compensation evidence |
| Disclosed duration and standardized price sensitivities | Interest-rate risk of the stated exposure |
| Yield-curve shape / relative tenor yields | Compensation differences between shorter and longer market segments |
| Corporate OAS plus spread exposure | Credit risk compensation and sensitivity, distinct from Treasury yields |
| Defensible carry / cash-relative or pairwise break-even | Quantitative compensation-for-risk perspective when the input basis permits it |
| FX / hedge qualifications | Currency risks and why seemingly similar products can be incomparable |

Three candidate interpretations are worth testing; **none is yet mandatory**:

1. **Multi-measure baseline:** present yield conditions, issuer profile, sensitivities and historical changes without forcing a single score; explain the risk/compensation tradeoff conditionally.
2. **Compensation relative to risk:** use defensible yield differences, carry cushions or break-even rate shocks to distinguish alternatives.
3. **Common reference scenario:** under a clearly illustrative horizon, market shock and risk tolerance, assess which exposures better meet the *stated* objective. Such assumptions are **research fixtures**, not a personalized investment policy.

The initial experiment should show whether (2) or (3) actually improves on (1). Merely producing a ranking is not evidence that a model is useful. `no_clear_preference`, `mixed_tradeoffs`, and `insufficient_information` are defensible results. A rising historical opportunity series can make an ETF worth considering without proving a buy signal.

## 9. Strict separation of ETF price history

The selection engine must **not** use ETF historical prices, total returns, NAV time series, or regressions fitted to ETF returns as attractiveness inputs, calibration targets, or substitutes for issuer-published exposures.

A separate optional validation capability may check whether historical behavior is broadly consistent with documented exposures and market conditions; discrepancies are reported, **not automatically fed back into the selection model**. Later user-facing convenience features may display properly distribution-adjusted historical ETF returns, independently labeled as **realized performance**, not market-based attractiveness.

The original architecture's detailed ETF return-attribution program is **deferred**. It is not required to establish an ETF selection model.

## 10. Required user-facing results

**A. Market view without an ETF.** Show relevant Treasury levels, curve slopes, selected historical changes, and credit spread context if available. Distinguish observations from market narratives and uncertainty.

**B. Current ETF comparison.** For selected ETFs, show compatible market reference data, dated issuer characteristics, rate/credit/FX exposure, common scenario results, available yield compensation, and clear conditional preference or incomparable/insufficient outcomes. Explain what would reverse the preference.

**C. Same-ETF historical assessment.** Given ETF and date range, show continuous time histories of the relevant *market-based opportunity measures* and matched sensitivity/scenario information; interpret improvement or deterioration across the period. If no defensible single attractiveness quantity exists, **do not invent one simply to make a line chart**. Provide component plots and dated conditional explanations instead.

In each view expose key units, effective source dates, data coverage, hypothetical assumptions and unsupported comparisons. No need for a fixed weighted score or a single chart containing all possible metrics.

## 11. Quantitative and behavioral verification

Required **hand-checkable synthetic examples**, with declared compatible inputs:

| Scenario | Expected value |
|---|---:|
| Duration 8; rate shock +50 bp | First-order price effect **-4.00%** |
| Same, convexity 80 | Second-order price effect **-3.90%** |
| Spread duration 6; OAS shock +100 bp; no rate change | Spread-price effect **-6.00%** |
| USD bond return -2%, USD/KRW return +8% | Unhedged KRW return **+5.84%** |
| 2Y Treasury 4.0%, 10Y Treasury 4.5% | 2s10s slope **+50 bp** |

For floating-point *arithmetic* tests of these non-extreme fixtures, document a tolerance; `1e-10` in decimal return units is a reasonable initial computational tolerance, **not** an empirical model-accuracy guarantee.

Behavioral invariants:

- Equivalent market/profile/assumption inputs produce the same quantitative result.
- No price/NAV return history can affect attractiveness or selection results.
- A historical change and a scenario shock cannot be labeled forecast or realized ETF P&L.
- Present issuer yield must not be treated as an actual historical yield.
- Incomplete carry, hedge or credit inputs cannot become assumed zero effects or fictitious exact outputs.
- Treasury futures cannot receive ordinary cash-bond carry regardless of user opt-in.
- Credit exposures cannot silently be evaluated as pure Treasuries.
- Hedged and unhedged KRW opportunities cannot be declared identical by ignoring hedge mechanics.
- Any improved model retains and reports its baseline where material.

Reproducible arithmetic tests do **not** establish that the model improves investment selection. Real-data demonstrations and an independent assessment of economic usefulness remain necessary.

## 12. Proposed minimum attractiveness research exercise

**Status: PROPOSED, not authorized for execution by this document alone.** The user and Archie will separately approve a bounded Bernie assignment after reviewing the architecture.

**Question:** Can a transparent multi-measure assessment already distinguish useful ETF investment opportunities across maturity and credit, or does an additional compensation/risk measure substantially improve the answer?

**Minimal inputs:** Dated real U.S. Treasury curve observations and relevant credit OAS if accessible; a small number of representative Korean-listed U.S. bond ETFs with verifiable issuer-published exposures. Prefer a short/intermediate/long Treasury contrast and at least one credit case when adequate input exists. Exclude futures from ordinary comparison. Select an illustrative one-year historical market window, while allowing inspection of its full time path. Do **not** select based on ETF historical performance.

**Minimum outputs for independent assessment:**

1. A reproducible **ETF-independent market overview** with current and historical yield/curve evidence.
2. A dated **current cross-ETF table** with published ETF characteristics, transparent baseline duration/stress results and valid compensation measurements.
3. At least one **same-ETF opportunity history** across the selected window, explicitly distinguishing historical market proxy values from issuer-disclosed ETF data.
4. A **comparison of alternative attractiveness interpretations**: the multi-measure baseline versus at least one supportable compensation/risk or reference-scenario alternative; report explicitly when additional inputs are unavailable.
5. Testable synthetic numerical references, actual observations/source cutoffs, and a list of **economic disagreements or ambiguous preferences**.
6. A short user-oriented interpretation: which comparisons look practically informative, which fail to differentiate ETFs, and which tempting conclusions would rely on unjustified assumptions.
7. A compact recommendation on **what should be retained, rejected or revised** in the architecture before defining the later roadmap.

An experiment may earn **research PASS** if it supplies correct, inspectable calculations, honest unsupported cases, and the intended comparison evidence. PASS does **not** mean a universally valid attractiveness score has been discovered or that any investment timing strategy has been validated. An observed inability to rank ETFs with present inputs may be an important legitimate result.

## 13. Jupyter notebook and Python-module interface

**Primary experience:** one or more Jupyter `.ipynb` notebooks emphasizing procedure and ease of use: select date/products/analysis → load data → invoke functions → inspect results. Plotly may provide interactive curves, time-series hover values, scenario comparisons and understandable tooltips.

**Definitions belong in `.py` modules**, not the notebook: data acquisition/preparation, issuer profiles, financial formulas, assessment functions, display helpers and any classes. Keep the structure simple; there is no requirement for a heavy domain-framework or bespoke plugin architecture.

**Verification belongs in independent Python tests**, which should run without interactively executing the notebook. Preserve the same valuation conventions in notebook and test outputs.

## 14. Outstanding design questions and boundaries

The minimal research should inform, not assume answers to:

1. Can *attractiveness* be represented usefully as one explainable numeric series, or is a vector of compensation and risk measures preferable?
2. What reliable comparable compensation measure is available for a physical Treasury ETF? For a corporate ETF? For KRW-hedged and unhedged versions?
3. Does a common horizon, cash reference or downside tolerance clarify choice, or introduce arbitrary preference assumptions? These reference parameters are **not bond maturity filters**.
4. Which credit/maturity/currency product pairs permit a reasoned comparison, and which remain non-comparable?
5. How much historical profile coverage is essential, compared with a clearly identified fixed-exposure market counterfactual?
6. Which additional conventional calculations add real decision value relative to the baseline, rather than just complexity?

The eventual broad universe and optional advanced features do **not** imply implementation in the minimum research exercise. **No post-prerequisite development-stage roadmap is specified here.** After the research is reviewed, revise this architecture **and** its companion examples consistently before defining a roadmap.

## 15. References and version boundary

- [Existing companion examples](bond_etf_decision_examples.md) — **not yet aligned; prior hypothetical policy labels and product cases are not silently accepted as requirements under this revision**.
- [Earlier critical design review](bondview_v3_critical_design_review_20261013.md) — research critique, not an implementation authorization.
- [FRED DGS10](https://fred.stlouisfed.org/series/DGS10), [FRED DEXKOUS](https://fred.stlouisfed.org/series/DEXKOUS) and [FRED U.S. Treasury rates](https://fred.stlouisfed.org/).
- [CFA Institute — Fixed-Income Portfolio Management](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/overview-fixed-income-portfolio-management), [Yield-Curve Strategies](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-curve-strategies), [Bond Convexity](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/yield-based-bond-convexity-and-portfolio-properties).

This architecture contains no current ETF buy recommendation and makes no assertion that a particular current yield or issuer profile is verified for investment use. For real outputs, verify source information and disclosure dates contemporaneously.
