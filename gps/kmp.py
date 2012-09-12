def compute_prefix_function(p):
    m = len(p)
    pi = [0] * m
    k = 0
    for q in range(1, m):
        while k > 0 and p[k] != p[q]:
            k = pi[k - 1]
        if p[k] == p[q]:
            k += 1
        pi[q] = k
    return pi

# match strings by kmp algorithm
def kmp_matcher(t, p):
    n = len(t)
    m = len(p)
    pi = compute_prefix_function(p)
    q = 0
    for i in range(n):
        while q > 0 and p[q] != t[i]:
            q = pi[q - 1]
        if p[q] == t[i]:
            q += 1
        if q == m:
            return i - m + 1
    return -1

