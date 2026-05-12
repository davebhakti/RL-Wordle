import random

class RandomAgent:

    def choose_guess(self, env, state):
        candidates = state["candidates"]

        if not candidates:
            return random.choice(env.word_list)

        return random.choice(candidates)