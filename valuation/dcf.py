"""Scenario DCF built on 2027E+ cash flows with mean reversion to mid-cycle."""
from .inputs import val

def cost_of_equity(rf, beta, mrp):
    return rf + beta * mrp

def wacc(ke, kd, tax, debt_weight):
    return ke * (1 - debt_weight) + kd * (1 - tax) * debt_weight

def project(fin, sc, years=5):
    """Years 2027E..2031E. OI glides linearly from 2027E to mid-cycle by year 5."""
    tax, da = val(fin, "tax_rate"), val(fin, "da")
    cap0, cap_mid = val(fin, "capex_2027e"), val(fin, "capex_mid")
    rows = []
    for i in range(years):
        w = i / (years - 1)
        oi = sc["oi_2027"] + (sc["oi_mid"] - sc["oi_2027"]) * w
        capex = cap0 + (cap_mid - cap0) * w
        nopat = oi * (1 - tax)
        rows.append({"year": 2027 + i, "oi": oi, "ebitda": oi + da, "nopat": nopat,
                     "da": da, "capex": capex, "fcf": nopat + da - capex})
    return rows

def net_cash_now(fin):
    """Jun-26 net cash rolled forward with H2-2026E free cash flow less dividends."""
    tax, da = val(fin, "tax_rate"), val(fin, "da")
    fcf26 = val(fin, "oi_2026e") * (1 - tax) + da - val(fin, "capex_2026e")
    return val(fin, "net_cash_jun26") + 0.5 * fcf26 - val(fin, "dividends_2026e")

def value(fin, sc, w, g=None, years=5):
    g = val(fin, "terminal_growth") if g is None else g
    rows = project(fin, sc, years)
    pv = sum(r["fcf"] / (1 + w) ** (i + 1) for i, r in enumerate(rows))
    tv = rows[-1]["fcf"] * (1 + g) / (w - g)
    pv_tv = tv / (1 + w) ** years
    ev = pv + pv_tv
    eq = ev + net_cash_now(fin)
    return {"ev": ev, "equity": eq, "per_share": eq * 1e12 / (val(fin, "shares_bn") * 1e9),
            "pv_fcf": pv, "pv_tv": pv_tv, "tv_share": pv_tv / ev, "rows": rows}

def get_wacc(fin):
    ke = cost_of_equity(val(fin, "rf"), val(fin, "beta"), val(fin, "mrp"))
    return wacc(ke, val(fin, "cost_of_debt"), val(fin, "tax_rate"), val(fin, "debt_weight"))

def run_scenarios(fin):
    w = get_wacc(fin)
    out = {n: value(fin, sc, w) for n, sc in fin["scenarios"].items()}
    out["weighted"] = sum(out[n]["per_share"] * fin["scenarios"][n]["prob"] for n in fin["scenarios"])
    out["wacc"] = w
    return out

def sensitivity(fin, waccs, gs, scenario="base"):
    sc = fin["scenarios"][scenario]
    return {(w, g): value(fin, sc, w, g)["per_share"] for w in waccs for g in gs}
