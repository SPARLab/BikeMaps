ALPHA62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def hash(i10):
    digits = []
    while i10 > 0:
        digits.append(i10%62)
        i10 /= 62
    return "".join(map(lambda x: ALPHA62[x], digits))

def dehash(s62):
    res = 0
    for i, c in enumerate(s62):
        res += ALPHA62.index(c) * 62**i
    return res
