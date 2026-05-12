import math
from collections import defaultdict

_feedback_cache = {}

def get_cached_feedback(env, guess, target):
    key = (guess, target)

    if key not in _feedback_cache:
        _feedback_cache[key] = tuple(env.simulate_feedback(guess, target))

    return _feedback_cache[key]






def expected_information_gain(env, guess, candidates):
    """
    Higher score means the guess is expected to split the candidate list better.
    This is Shannon entropy over possible feedback patterns.
    """

    partitions = defaultdict(int)

    for target in candidates:
        feedback = get_cached_feedback(env, guess, target)
        partitions[feedback] += 1

    total = len(candidates)
    entropy = 0.0

    for count in partitions.values():
        probability = count / total
        entropy -= probability * math.log2(probability)

    return entropy