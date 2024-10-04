#!/usr/bin/env python3
"""This script takes genomes from stdin (one per line) and performs a slip mutation on each, printing the results to stdout.
"""

import sys
import random
random.seed(1)


def try_slip_mutation(genome: str) -> str:
    orig_genome_len = len(genome)

    from_idx = random.randint(0, orig_genome_len)
    to_idx = random.randint(0, orig_genome_len + (from_idx != 0))

    return genome[:to_idx] + genome[from_idx:]

def force_slip_mutation(genome: str) -> str:
    result = genome
    while result == genome:
        result = try_slip_mutation(genome)
    return result


if __name__ == "__main__":
    for line in sys.stdin:
        genome = line.strip()
        print(force_slip_mutation(genome))
