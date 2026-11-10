import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
        raw = json.load(f)
    return raw

def val(raw, key):
    """Return the value of an input, whether it is {v,src,conf} or plain."""
    x = raw[key]
    return x["v"] if isinstance(x, dict) and "v" in x else x

def low_confidence(raw):
    return [k for k, x in raw.items() if isinstance(x, dict) and x.get("conf") == "low"]
