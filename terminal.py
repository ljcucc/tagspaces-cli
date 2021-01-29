def setTextColor(r,g,b):
    print()

def rgb_to_xterm(r, g, b):
    N = []
    for i, n in enumerate([47, 68, 40, 40, 40, 21]):
        N.extend([i]*n)

    mx = max(r, g, b)    
    mn = min(r, g, b)

    if (mx-mn)*(mx+mn) <= 6250:
        c = 24 - (252 - ((r+g+b) // 3)) // 10
        if 0 <= c <= 23:
            return 232 + c

    return 16 + 36*N[r] + 6*N[g] + N[b]