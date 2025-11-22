#!/usr/bin/env python3
import math
import argparse

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r = int(math.isqrt(n))
    for k in range(3, r + 1, 2):
        if n % k == 0:
            return False
    return True

def primes_up_to(N: int):
    if N < 2:
        return []
    sieve = [True] * (N + 1)
    sieve[0] = sieve[1] = False
    for p in range(2, int(math.isqrt(N)) + 1):
        if sieve[p]:
            step = p
            start = p * p
            sieve[start:N+1:step] = [False] * (((N - start) // step) + 1)
    return [i for i, ok in enumerate(sieve) if ok]

def next_prime(n: int) -> int:
    if n < 2:
        return 2
    x = n + 1
    if x % 2 == 0:
        x += 1
    while not is_prime(x):
        x += 2
    return x

def factorize(n: int):
    n = abs(n)
    factors = []
    if n < 2:
        return factors
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    f = 3
    while f * f <= n:
        while n % f == 0:
            factors.append(f)
            n //= f
        f += 2
    if n > 1:
        factors.append(n)
    return factors

def main():
    ap = argparse.ArgumentParser(description="Prime calculator (check, list, next, factorize).")
    ap.add_argument("--check", type=int, help="Check if n is prime.")
    ap.add_argument("--list", type=int, help="List primes up to N.")
    ap.add_argument("--next", dest="nextn", type=int, help="Next prime after n.")
    ap.add_argument("--factor", type=int, help="Prime factorization of n.")
    args = ap.parse_args()

    did = False

    if args.check is not None:
        n = args.check
        print(f"{n} is prime" if is_prime(n) else f"{n} is NOT prime")
        did = True

    if args.list is not None:
        N = args.list
        ps = primes_up_to(N)
        print(f"Primes up to {N} ({len(ps)}):")
        print(ps)
        did = True

    if args.nextn is not None:
        n = args.nextn
        print(f"Next prime after {n} is {next_prime(n)}")
        did = True

    if args.factor is not None:
        n = args.factor
        fs = factorize(n)
        print(f"Prime factors of {n}: {fs}")
        did = True

    if not did:
        ap.print_help()

if __name__ == "__main__":
    main()
