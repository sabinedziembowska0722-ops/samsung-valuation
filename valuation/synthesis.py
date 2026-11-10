from .inputs import val
from . import dcf, cca, lbo

W = {"DCF": 0.40, "CCA": 0.40, "LBO": 0.20}

def rating(upside):
    if upside > 0.15: return "BUY"
    if upside < -0.10: return "SELL"
    return "HOLD"

def blended(fin, peers):
    d = dcf.run_scenarios(fin)
    c = cca.implied(fin, peers)
    l_lo = lbo.ability_to_pay_per_share(fin, 0.25)
    l_mid = lbo.ability_to_pay_per_share(fin, 0.20)
    l_hi = lbo.ability_to_pay_per_share(fin, 0.15)
    fair = W["DCF"] * d["weighted"] + W["CCA"] * c["blended"] + W["LBO"] * l_mid
    return {"dcf": d, "cca": c, "lbo": {"25%": l_lo, "20%": l_mid, "15%": l_hi}, "fair": fair}

def price_table(fair, prices):
    return [(p, fair / p - 1, rating(fair / p - 1)) for p in prices]
