"""Illustrative LBO: what could a sponsor pay and still earn a target IRR?
Samsung is far too large for a real buyout (~1,300tn KRW); this is a framework / ability-to-pay floor."""
from .inputs import val
from . import dcf

def run(fin, entry_equity, leverage_pct_ev=0.20, rate=0.055, exit_multiple=5.0,
        fee_pct=0.02, years=5, scenario="base"):
    nc = dcf.net_cash_now(fin)
    tax = val(fin, "tax_rate")
    ev0 = entry_equity - nc
    debt = leverage_pct_ev * ev0
    sponsor = ev0 + fee_pct * ev0 - debt
    rows = dcf.project(fin, fin["scenarios"][scenario], years)
    cash = 0.0
    for r in rows:
        interest = rate * debt
        fcf = r["fcf"] - interest * (1 - tax)
        pay = min(debt, max(fcf, 0)); debt -= pay; cash += fcf - pay
    exit_ev = exit_multiple * rows[-1]["ebitda"]
    exit_eq = exit_ev - debt + cash
    moic = max(exit_eq, 0.0) / sponsor
    return {"irr": moic ** (1 / years) - 1, "moic": moic, "sponsor_equity": sponsor,
            "exit_equity": exit_eq, "exit_ev": exit_ev, "entry_ev": ev0}

def max_entry_equity(fin, target_irr, **kw):
    lo, hi = dcf.net_cash_now(fin) + 1.0, 20000.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if run(fin, mid, **kw)["irr"] > target_irr: lo = mid
        else: hi = mid
    return lo

def ability_to_pay_per_share(fin, target_irr, **kw):
    return max_entry_equity(fin, target_irr, **kw) * 1e12 / (val(fin, "shares_bn") * 1e9)
