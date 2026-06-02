from collections import Counter


class FrequencyAgent:

    def choose_guess(self, env, state):

        candidates = state["candidates"]

        if not candidates:
            return env.word_list[0]

        # Count letter frequencies in remaining candidate answers
        letter_counts = Counter()

        for word in candidates:
            for letter in word:      # raw frequency count
                letter_counts[letter] += 1

        best_word = None
        best_score = -1

        # Only score candidate words
        for word in candidates:

            score = 0

            for letter in word:
                score += letter_counts[letter]

            if score > best_score:
                best_score = score
                best_word = word

        return best_word