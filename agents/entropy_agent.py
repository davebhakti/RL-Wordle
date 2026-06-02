import random

from utils.entropy import expected_information_gain
from utils.feedback_cache import FeedbackCache


class EntropyAgent:

    def __init__(self, word_list, sample_size=200):
        self.word_list = word_list
        self.sample_size = sample_size
        self.cache = None

    def choose_guess(self, env, state):

        candidates = state["candidates"]

        if self.cache is None:
            self.cache = FeedbackCache(env)

        if len(candidates) == 0:
            return self.word_list[0]

        if len(candidates) == 1:
            return candidates[0]

        best_guess = None
        best_score = -1

        # unbiased candidate sampling
        if len(candidates) > 150:
            possible_guesses = random.sample(candidates, 150)
        else:
            possible_guesses = candidates

        for guess in possible_guesses:

            score = expected_information_gain(
                env,
                guess,
                candidates,
                cache=self.cache,
                sample_size=self.sample_size
            )

            if score > best_score:
                best_score = score
                best_guess = guess

        return best_guess