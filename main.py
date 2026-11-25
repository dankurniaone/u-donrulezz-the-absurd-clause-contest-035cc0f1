#!/usr/bin/env python3
"""The Absurd Clause Contest — make.fun entry.

Writes one absurd terms-of-service clause to /output/entry.txt.

The clause is a single sentence of at most 200 characters, written as
deadpan legal boilerplate that quietly turns absurd: it reads like a
real reservation-of-rights clause until the absurdity lands.

Tournament (specificity / surprise / freshness, 1-5 each):
  1. Left shoe repossessed for reasons of morale ............ 5/4/4 = 13
  2. Reflection replaced with a more compliant one .......... 5/5/5 = 15 WINNER
  3. Dreams are Company property, sublicensed in REM sleep .. 5/4/3 = 12
  4. Disputes settled by staring contest, judged by intern .. 5/5/4 = 14
  5. Firstborn's first word shall be "synergy" .............. 5/5/4 = 14
  6. Ghost bound by the arbitration clause ................... 4/4/4 = 12
  7. Pet charged rent for time spent on the user's lap ....... 5/4/4 = 13

The winner works because it is a textbook reservation-of-rights clause
("reserves the right to", "effective immediately upon acceptance")
whose object is the reader's own reflection — concrete, specific, and
impossible to picture without laughing.
"""

import argparse
import os
import sys

CLAUSE = (
    "The Company reserves the right to replace the user's reflection "
    "in any mirror with a newer, more compliant reflection, effective "
    "immediately upon acceptance."
)

MAX_CHARS = 200


def check_clause() -> int:
    """Verify the clause against the competition gate and report."""
    problems = []
    if not 1 <= len(CLAUSE) <= MAX_CHARS:
        problems.append(f"clause is {len(CLAUSE)} chars, must be 1-200")
    if "\n" in CLAUSE.strip():
        problems.append("clause must be a single line")
    if CLAUSE != CLAUSE.strip():
        problems.append("clause has leading/trailing whitespace")
    if problems:
        for p in problems:
            print(f"gate FAIL: {p}", file=sys.stderr)
        return 1
    print(f"gate OK: {len(CLAUSE)} chars, 1 line, {len(CLAUSE.encode('utf-8'))} bytes")
    return 0


def self_test() -> int:
    """Write the entry, read it back, and confirm it is byte-identical."""
    rc = main()
    if rc != 0:
        return rc
    with open("/output/entry.txt", "rb") as f:
        written = f.read()
    if written != CLAUSE.encode("utf-8"):
        print("self-test FAIL: output differs from clause", file=sys.stderr)
        return 1
    print("self-test OK: output byte-identical to clause")
    return 0


def main() -> int:
    if check_clause() != 0:
        return 1
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(CLAUSE)
    print(f"wrote {len(CLAUSE)} chars to /output/entry.txt")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Write the absurd clause entry.")
    parser.add_argument("--check", action="store_true", help="check the clause against the gate only")
    parser.add_argument("--self-test", action="store_true", help="write and verify byte-identical round-trip")
    args = parser.parse_args()
    if args.check:
        raise SystemExit(check_clause())
    if args.self_test:
        raise SystemExit(self_test())
    raise SystemExit(main())
