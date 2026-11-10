from valuation.inputs import load, val, low_confidence
from valuation import dcf, synthesis
from valuation.chart import football_field

fin, peers = load("samsung.json"), load("peers.json")
price = val(fin, "price_krw")
res = synthesis.blended(fin, peers)
d, c, l = res["dcf"], res["cca"], res["lbo"]
k = lambda x: f"{x/1000:,.0f}k"

print(f"=== {fin['company']} valuation (data as of {fin['as_of']}) ===")
print(f"Price {price:,} KRW | WACC {d['wacc']:.2%} | net cash now ~{dcf.net_cash_now(fin):.0f}tn\n")
print("[DCF] value per share (KRW)")
for n in ("bear", "base", "bull"):
    s = d[n]; print(f"  {n:5s} EV {s['ev']:7.0f}tn  per share {k(s['per_share']):>6}  (TV = {s['tv_share']:.0%} of EV)")
print(f"  probability-weighted: {k(d['weighted'])}\n")
print("[CCA] low / mid / high per share")
for key in ("P/E (fwd)", "EV/EBITDA (fwd)", "P/B"):
    v = c[key]; print(f"  {key:16s} {k(v['low']):>6} / {k(v['mid']):>6} / {k(v['high']):>6}")
print(f"  blended (50% P/E, 40% EV/EBITDA, 10% P/B): {k(c['blended'])}\n")
print("[LBO] max price per share a sponsor could pay for target IRR (illustrative)")
for t, v in l.items(): print(f"  IRR {t}: {k(v)}")
print()
up = res["fair"] / price - 1
print(f"BLENDED FAIR VALUE: {res['fair']:,.0f} KRW  | upside {up:+.1%}  -> {synthesis.rating(up)}")
print("\nRating vs. share price (prices are volatile - rating is a function of price):")
for p, u, r in synthesis.price_table(res["fair"], range(150000, 330000, 30000)):
    print(f"  {p:>8,} KRW  upside {u:+6.1%}  {r}")
print("\nDCF sensitivity, base case (KRW k per share): rows WACC, cols terminal growth")
gs = [0.015, 0.025, 0.035]; ws = [0.09, 0.10, 0.105, 0.11, 0.12]
t = dcf.sensitivity(fin, ws, gs)
print("        " + "".join(f"{g:>8.1%}" for g in gs))
for w in ws: print(f"  {w:5.1%} " + "".join(f"{t[(w,g)]/1000:8,.0f}" for g in gs))
football_field(res, price, "output/football_field.png")
print("\nChart saved: output/football_field.png")
print("Low-confidence inputs (verify!):", ", ".join(low_confidence(fin)))
