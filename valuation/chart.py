import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def football_field(res, price, path):
    d, c, l = res["dcf"], res["cca"], res["lbo"]
    bars = [("DCF (bear-bull)", d["bear"]["per_share"], d["bull"]["per_share"], d["base"]["per_share"]),
            ("CCA P/E fwd", c["P/E (fwd)"]["low"], c["P/E (fwd)"]["high"], c["P/E (fwd)"]["mid"]),
            ("CCA EV/EBITDA fwd", c["EV/EBITDA (fwd)"]["low"], c["EV/EBITDA (fwd)"]["high"], c["EV/EBITDA (fwd)"]["mid"]),
            ("CCA P/B", c["P/B"]["low"], c["P/B"]["high"], c["P/B"]["mid"]),
            ("LBO ability-to-pay\n(25%-15% IRR)", l["25%"], l["15%"], l["20%"])]
    fig, ax = plt.subplots(figsize=(10, 4.8))
    for i, (n, lo, hi, mid) in enumerate(bars):
        ax.barh(i, (hi - lo) / 1000, left=lo / 1000, color="#2f6f9f", height=0.5)
        ax.plot([mid / 1000] * 2, [i - 0.25, i + 0.25], color="white", lw=2)
        ax.text(lo / 1000 - 3, i, f"{lo/1000:,.0f}", ha="right", va="center", fontsize=8)
        ax.text(hi / 1000 + 3, i, f"{hi/1000:,.0f}", ha="left", va="center", fontsize=8)
    ax.axvline(price / 1000, color="#c0392b", ls="--"); ax.axvline(res["fair"] / 1000, color="#27774a", ls="-")
    ax.text(price / 1000, -0.6, f" Price {price/1000:,.0f}k", color="#c0392b", fontsize=9)
    ax.text(res["fair"] / 1000, len(bars) - 0.4, f" Blended fair value {res['fair']/1000:,.0f}k", color="#27774a", fontsize=9)
    ax.set_xlim(100, 780); ax.set_yticks(range(len(bars))); ax.set_yticklabels([b[0] for b in bars]); ax.invert_yaxis()
    ax.set_xlabel("Value per share (KRW thousand)"); ax.set_title("Samsung Electronics - valuation football field")
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    plt.tight_layout(); fig.savefig(path, dpi=160); plt.close(fig)
