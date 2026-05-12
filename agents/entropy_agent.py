from utils.entropy import expected_information_gain


class EntropyAgent:
    def __init__(self, word_list, use_full_word_list=True):
        self.word_list = word_list
        self.use_full_word_list = use_full_word_list

    def choose_guess(self, env, state):
        guesses = state.get("guesses", [])
        candidates = state["candidates"]

        if len(guesses) == 0:
            possible_guesses = self.word_list[:100]

        elif len(candidates) == 0:
            return self.word_list[0]

        if len(candidates) == 1:
            return candidates[0]
        
        elif len(candidates) == 1:
            return candidates[0]


        elif len(candidates) <= 5:
            return candidates[0]
        
        elif len(candidates) > 25:
            possible_guesses = self.word_list[:50]

        else:
            possible_guesses = candidates

        possible_guesses = candidates[:100]

        best_guess = None
        best_score = -1

        for guess in possible_guesses:
            score = expected_information_gain(
                env,
                guess,
                candidates
            )

            if score > best_score:
                best_score = score
                best_guess = guess

        return best_guess