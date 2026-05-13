from collections import Counter


class FrequencyAgent:

    def choose_guess(self, env, state):

        candidates = state["candidates"]

        if not candidates:
            return env.word_list[0]

        # Count how often each letter appears
        letter_counts = Counter()

        for word in candidates:

            unique_letters = set(word)

            for letter in unique_letters:
                letter_counts[letter] += 1

        best_word = None
        best_score = -1

        # Score each candidate word
        for word in candidates:

            score = 0
            used_letters = set()

            for letter in word:

                # Avoid double-counting repeated letters
                if letter not in used_letters:
                    score += letter_counts[letter]
                    used_letters.add(letter)

            if score > best_score:
                best_score = score
                best_word = word

        return best_word
        