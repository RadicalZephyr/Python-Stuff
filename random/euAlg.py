def euAlg(x, y):
    g = max(x, y)
    l = min(x, y)
    while (g > 1) and (l > 1):
        g, l = max(l, g - l), min(l, g-l)
    return g