ALPHA62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def hash(i10):
    """ Convert a base-10 integer into a base-62 integer and return the string """
    if i10 == 0:
        return ALPHA62[0]
    digits = []
    base = len(ALPHA62)
    while i10:
        i10, rem = divmod(i10, base)
        digits.append(ALPHA62[rem])
    digits.reverse()
    return ''.join(digits)
    

def dehash(s62):
    """ Convert a base-62 integer (as type:string) into a base-10 integer and return the integer """
    res = 0
    for i, c in enumerate(s62):
        res += ALPHA62.index(c) * 62**i
    return res
