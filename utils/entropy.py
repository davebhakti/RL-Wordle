import math
from collections import defaultdict


def expected_information_gain(env, guess, candidates):
    """
    Higher score means the guess is expected to split the candidate list better.
    This is Shannon entropy over possible feedback patterns.
    """

    partitions = defaultdict(int)

    for target in candidates:
        feedback = tuple(env.simulate_feedback(guess, target))
        partitions[feedback] += 1

    total = len(candidates)
    entropy = 0.0

    for count in partitions.values():
        probability = count / total
        entropy -= probability * math.log2(probability)

    return entropy