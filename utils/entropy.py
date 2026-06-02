import math
import random
from collections import defaultdict

def expected_information_gain(env, guess, candidates, cache=None, sample_size=50):
    # Sample candidates for speed when the pool is large
    if len(candidates) > sample_size:
        sample = random.sample(candidates, sample_size)
    else:
        sample = candidates

    partitions = defaultdict(int)
    for target in sample:
        feedback = (
            cache.get(guess, target)
            if cache is not None
            else tuple(env.simulate_feedback(guess, target))
        )
        partitions[feedback] += 1

    total = len(sample)
    entropy = 0.0
    for count in partitions.values():
        probability = count / total
        entropy -= probability * math.log2(probability)
    return entropy