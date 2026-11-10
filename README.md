# Samsung Electronics – DCF + CCA + LBO Valuation Model

A reusable, function-based Python valuation framework. It values one company with three methods,
blends them into a fair value, and shows how the buy/hold/sell rating changes with the share price.
Swap `data/*.json` to value another company.

## Run
```
pip install matplotlib
python3 main.py
```
Outputs a console report and `output/football_field.png`.

## Methods
- **DCF** (`valuation/dcf.py`): bear/base/bull scenarios on 2027E–2031E. Operating income mean-reverts from the
  supercycle peak to a mid-cycle level, because a DCF anchored on trailing (2025) cash flow is stale in a memory upcycle.
  WACC via CAPM, Gordon terminal value, WACC × growth sensitivity table.
- **CCA** (`valuation/cca.py`): forward P/E, forward EV/EBITDA and P/B vs. SK hynix, Micron, TSMC, with a 15% discount.
- **LBO** (`valuation/lbo.py`): ability-to-pay analysis (max price for a 15/20/25% sponsor IRR). Illustrative only –
  a ~1,300tn KRW buyout is not realistic.
- **Synthesis** (`valuation/synthesis.py`): 40% DCF / 40% CCA / 20% LBO → fair value, rating (BUY >+15%, SELL <−10%),
  and a rating-vs-price table.

## Data quality – read this
Every input in `data/` carries `src` and `conf` (high/medium/low). Several inputs (2027E earnings, D&A, capex, peer multiples,
share count incl. preferred, beta/MRP) are **analyst-style estimates, not verified filings**. Refresh them from
DART / Bloomberg / FactSet before drawing conclusions. The script prints the list of low-confidence inputs on every run.

## Limitations
Banks need DDM/FCFE instead of DCF/LBO. Cyclical-peak earnings drive the result; the TV share of EV and the scenario
weights matter a lot. CCA high-end is inflated by TSMC (foundry, not memory).

## Disclaimer
Educational project. Not investment advice.
