name: Run prime calculator

on:
  workflow_dispatch:
    inputs:
      mode:
        type: choice
        description: Operation to perform
        options: [check, list, next, factor]
        default: check
      n:
        type: string
        description: "Positive integer (required)"
        required: true

jobs:
  calculate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies (none needed, but keeps it clean)
        run: python -m pip install --upgrade pip

      - name: Create prime_calculator.py
        run: cat > prime_calculator.py <<'EOF'
        import argparse
        import math
        import sys

        def is_prime(n: int) -> bool:
            if n <= 1:
                return False
            if n <= 3:
                return True
            if n % 2 == 0 or n % 3 == 0:
                return False
            i = 5
            while i * i <= n:
                if n % i == 0 or n % (i + 2) == 0:
                    return False
                i += 6
            return True

        def next_prime(n: int) -> int:
            candidate = n + 1 if n % 2 == 0 else n + 2
            while not is_prime(candidate):
                candidate += 2
            return candidate

        def list_primes(limit: int):
            if limit < 2:
                return []
            primes = [2]
            for num in range(3, limit + 1, 2):
                if all(num % p != 0 for p in primes):
                    primes.append(num)
            return primes

        def factorize(n: int):
            if n <= 1:
                return []
            factors = []
            # 2s
            while n % 2 == 0:
                factors.append(2)
                n //= 2
            # odd factors
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
            parser = argparse.ArgumentParser(description="Prime calculator tools")
            group = parser.add_mutually_exclusive_group(required=True)
            group.add_argument("--check", type=int, metavar="N", help="Check if N is prime")
            group.add_argument("--list", type=int, metavar="N", help="List all primes <= N")
            group.add_argument("--next", type=int, metavar="N", help="Find the smallest prime > N")
            group.add_argument("--factor", type=int, metavar="N", help="Prime factorization of N")

            args = parser.parse_args()

            if args.check is not None:
                print("Yes" if is_prime(args.check) else "No")
            elif args.list is not None:
                print(" ".join(map(str, list_primes(args.list))))
            elif args.next is not None:
                print(next_prime(args.next))
            elif args.factor is not None:
                print(" × ".join(map(str, factorize(args.factor))) or "1")

        if __name__ == "__main__":
            main()
        EOF

      - name: Run prime calculator
        run: |
          python prime_calculator.py \
            ${{ inputs.mode == 'check' && '--check' || '' }} \
            ${{ inputs.mode == 'list' && '--list' || '' }} \
            ${{ inputs.mode == 'next' && '--next' || '' }} \
            ${{ inputs.mode == 'factor' && '--factor' || '' }} \
            "${{ inputs.n }}"
