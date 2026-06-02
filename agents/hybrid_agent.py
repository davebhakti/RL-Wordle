import random
from collections import Counter

from utils.entropy import expected_information_gain
from utils.feedback_cache import FeedbackCache


class HybridAgent:

    def __init__(
        self,
        word_list,
        endgame_threshold=5,
        max_entropy_guesses=75
    ):
        self.word_list = word_list
        self.endgame_threshold = endgame_threshold
        self.max_entropy_guesses = max_entropy_guesses
        self.cache = None

        print("Hybrid threshold =", self.endgame_threshold)

    def choose_guess(self, env, state):

        if self.cache is None:
            self.cache = FeedbackCache(env)

        candidates = state["candidates"]
        guesses_used = state["guess_number"]
        guesses_left = env.MAX_GUESSES - guesses_used

        if len(candidates) == 0:
            return self.word_list[0]

        if len(candidates) == 1:
            return candidates[0]

        # strong opener
        if guesses_used == 0 and "slate" in self.word_list:
            return "slate"

        # final guess
        if guesses_left == 1:
            return self._frequency_choice(candidates)

        # endgame
        if len(candidates) <= self.endgame_threshold:
            return self._minimax_choice(candidates)

        # entropy phase
        return self._entropy_choice(env, candidates)

    def _entropy_choice(self, env, candidates):

        best_guess = None
        best_score = -1

        # unbiased sample
        if len(candidates) > self.max_entropy_guesses:
            possible_guesses = random.sample(
                candidates,
                self.max_entropy_guesses
            )
        else:
            possible_guesses = candidates

        for guess in possible_guesses:

            score = expected_information_gain(
                env,
                guess,
                candidates,
                cache=self.cache
            )

            if score > best_score:
                best_score = score
                best_guess = guess

        return best_guess

    def _minimax_choice(self, candidates):

        best_guess = None
        best_worst_case = float("inf")

        for guess in candidates:

            partitions = {}

            for target in candidates:

                feedback = self.cache.get(
                    guess,
                    target
                )

                partitions[feedback] = (
                    partitions.get(feedback, 0) + 1
                )

            worst_case = max(partitions.values())

            if worst_case < best_worst_case:
                best_worst_case = worst_case
                best_guess = guess

        return best_guess

    def _frequency_choice(self, candidates):

        letter_counts = Counter()

        for word in candidates:
            for letter in set(word):
                letter_counts[letter] += 1

        best_word = None
        best_score = -1

        for word in candidates:

            score = sum(
                letter_counts[letter]
                for letter in set(word)
            )

            if score > best_score:
                best_score = score
                best_word = word

        return best_word