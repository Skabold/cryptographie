import random

def get_large_prime_number(nbits):
    range_min = 2 ** (nbits - 1)
    range_max = 2 ** nbits
    while True:
        n = random.randrange(range_min + 1, range_max, 2)
        if miller_rabin_prime_test(n, trials=30):
            return n

def miller_rabin_prime_test(x, trials=30):
    max_divisions_by_two = 0
    even_component = x - 1
    while even_component % 2 == 0:
        even_component >>= 1
        max_divisions_by_two += 1
    assert (2 ** max_divisions_by_two * even_component == x - 1)
    for _ in range(trials):
        round_tester = random.randrange(2, x)
        if trial_composite(x, round_tester, even_component, max_divisions_by_two):
            return False
    return True

def trial_composite(x, round_tester, even_component, max_divisions_by_two):
    if pow(round_tester, even_component, x) == 1:
        return False
    for i in range(max_divisions_by_two):
        if pow(round_tester, 2 ** i * even_component, x) == x - 1:
            return False
    return True

def eucalg(a, b):
    swapped = False
    if a < b:
        a, b = b, a
        swapped = True

    ca = (1, 0)
    cb = (0, 1)
    while b != 0:
        k = a // b
        a, b, ca, cb = b, a - (b * k), cb, (ca[0] - (k * cb[0]), ca[1] - (k * cb[1]))

    if swapped:
        return (ca[1], ca[0])
    else:
        return ca

def modpow(b, e, n):
    r = 1
    while e:
        if e % 2:
            r = (r * b) % n
        b = (b * b) % n
        e //= 2
    return r
