import math

def maximize(l, f):
    # -------------------------------------------------------------------------
    # Assumptions
    # -------------------------------------------------------------------------
    assert(len(l) > 0)
    # -------------------------------------------------------------------------

    (maximum, maximum_result) = (l[0], f(l[0]))
    maximum_result = f(maximum)
    for elem in l:
        result = f(elem)
        if result > maximum_result:
            (maximum, maximum_result) = (elem, result)
    return maximum

if __name__ == "__main__":
    l = ['Barbara', 'kingsolver', 'wrote', 'The', 'Poisonwood','Bible']
    f = len
    print maximize(l, f)

    l = [5, 6, 7, 8, 9, 10, 11, 12, 15, 0]
    f = math.sqrt
    print maximize(l, f)

    l = [1, 2, 3, 4]
    f = math.sqrt
    print maximize(l, f)

    l = [4, 3, 2, 1]
    f = math.sqrt
    print maximize(l, f)
