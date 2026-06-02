class FeedbackCache:
    def __init__(self, env):
        self.env = env
        self.cache = {}

    def get(self, guess, target):
        key = (guess, target)

        if key not in self.cache:
            self.cache[key] = tuple(
                self.env.simulate_feedback(guess, target)
            )

        return self.cache[key]

