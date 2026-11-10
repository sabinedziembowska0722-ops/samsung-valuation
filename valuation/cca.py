"""Comparable-company analysis: implied Samsung value per share (KRW)."""
from statistics import median
from .inputs import val

def implied(fin, peers):
    disc = peers["discount"]["v"]
    sh = val(fin, "shares_bn") * 1e9
    ni, book = val(fin, "net_income_2026e"), val(fin, "book_equity_2026e")
    ebitda = val(fin, "oi_2026e") + val(fin, "da")
    from .dcf import net_cash_now
    nc = net_cash_now(fin)
    out = {}
    for label, key, f in [
        ("P/E (fwd)",    "fwd_pe",        lambda m: ni * m * (1 - disc)),
        ("EV/EBITDA (fwd)", "fwd_ev_ebitda", lambda m: (ebitda * m + nc) * (1 - disc)),
        ("P/B",          "pb",            lambda m: book * m * (1 - disc)),
    ]:
        ms = [p[key] for p in peers["peers"].values()]
        vals = [f(m) * 1e12 / sh for m in (min(ms), median(ms), max(ms))]
        out[label] = {"low": vals[0], "mid": vals[1], "high": vals[2], "multiples": ms}
    out["blended"] = 0.5 * out["P/E (fwd)"]["mid"] + 0.4 * out["EV/EBITDA (fwd)"]["mid"] + 0.1 * out["P/B"]["mid"]
    return out
