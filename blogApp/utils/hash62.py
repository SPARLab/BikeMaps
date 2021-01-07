ALPHA62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def hash(i10):
    """ Convert a base-10 integer into a base-62 integer and return the string """
    digits = []
    while i10 > 0:
        digits.append(i10%62)
        i10 /= 62
    return "".join([ALPHA62[x] for x in digits])

def dehash(s62):
    """ Convert a base-62 integer (as type:string) into a base-10 integer and return the integer """
    res = 0
    for i, c in enumerate(s62):
        res += ALPHA62.index(c) * 62**i
    return res
