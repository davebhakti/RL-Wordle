import random
from collections import Counter


class WordleEnv:
    """
    Wordle game environment for RL training and evaluation.

    Feedback encoding:
        0 = gray   (letter not in word)
        1 = yellow (letter in word, wrong position)
        2 = green  (letter in correct position)
    """

    MAX_GUESSES = 6
    WORD_LENGTH = 5

    def __init__(self, word_list: list[str]):
        """
        Args:
            word_list: list of valid 5-letter words (loaded from your words.txt)
        """
        self.word_list = [w.strip().lower() for w in word_list if len(w.strip()) == 5]
        self.target = None
        self.guesses = []       # list of (guess, feedback) tuples
        self.done = False

    # ─────────────────────────────────────────────────────────────────────────
    # Core API
    # ─────────────────────────────────────────────────────────────────────────

    def reset(self, target: str = None) -> dict:
        """
        Start a new episode.

        Args:
            target: optional fixed target word (for evaluation); random if None
        Returns:
            Initial state dict
        """
        if target is not None:
            self.target = target.strip().lower()
        else:
            self.target = random.choice(self.word_list)
        self.guesses = []
        self.done = False
        return self.get_state()

    def step(self, guess: str) -> tuple[dict, float, bool, dict]:
        """
        Submit a guess and advance the game.

        Args:
            guess: 5-letter word string
        Returns:
            (state, reward, done, info)
        """
        if self.done:
            raise RuntimeError("Episode is finished. Call reset() to start a new game.")

        guess = guess.strip().lower()

        if len(guess) != self.WORD_LENGTH:
            raise ValueError(f"Guess must be {self.WORD_LENGTH} letters, got: '{guess}'")

        if guess not in self.word_list:
            # Penalise invalid guesses without ending the episode
            return self.get_state(), -0.5, False, {"invalid_guess": True}

        feedback = self.get_feedback(guess)
        self.guesses.append((guess, feedback))

        won = guess == self.target
        out_of_guesses = len(self.guesses) >= self.MAX_GUESSES

        self.done = won or out_of_guesses
        reward = self._compute_reward(feedback, won, out_of_guesses)

        info = {
            "won": won,
            "guess_number": len(self.guesses),
            "target": self.target if self.done else None,   # reveal only when over
        }
        return self.get_state(), reward, self.done, info

    # ─────────────────────────────────────────────────────────────────────────
    # Feedback
    # ─────────────────────────────────────────────────────────────────────────

    def get_feedback(self, guess: str) -> list[int]:
        """
        Compute green/yellow/gray feedback for a guess against self.target.

        Handles duplicate letters correctly:
            - Greens are awarded first.
            - Yellows are only awarded if the letter still has unmatched
              occurrences remaining in the target.

        Returns:
            List of 5 ints: 2=green, 1=yellow, 0=gray
        """
        target = self.target
        feedback = [0] * self.WORD_LENGTH
        target_remaining = Counter(target)

        # Pass 1: greens
        for i in range(self.WORD_LENGTH):
            if guess[i] == target[i]:
                feedback[i] = 2
                target_remaining[guess[i]] -= 1

        # Pass 2: yellows
        for i in range(self.WORD_LENGTH):
            if feedback[i] == 2:
                continue
            if guess[i] in target_remaining and target_remaining[guess[i]] > 0:
                feedback[i] = 1
                target_remaining[guess[i]] -= 1

        return feedback

    # ─────────────────────────────────────────────────────────────────────────
    # State
    # ─────────────────────────────────────────────────────────────────────────

    def get_state(self) -> dict:
        """
        Return a structured state dict.

        Fields:
            guess_number    : int, how many guesses have been made (0–6)
            guesses         : list of (word, feedback) tuples so far
            green_letters   : dict {position: letter} for confirmed placements
            yellow_letters  : dict {letter: set of positions where it is NOT}
            gray_letters    : set of letters confirmed absent
            candidates      : list of words still consistent with all feedback
        """
        green_letters = {}
        yellow_letters = {}
        gray_letters = set()

        for guess, feedback in self.guesses:
            for i, (letter, fb) in enumerate(zip(guess, feedback)):
                if fb == 2:
                    green_letters[i] = letter
                elif fb == 1:
                    if letter not in yellow_letters:
                        yellow_letters[letter] = set()
                    yellow_letters[letter].add(i)
                else:  # gray
                    # Only mark gray if not also green/yellow elsewhere
                    if letter not in green_letters.values() and letter not in yellow_letters:
                        gray_letters.add(letter)

        return {
            "guess_number": len(self.guesses),
            "guesses": list(self.guesses),
            "green_letters": green_letters,
            "yellow_letters": yellow_letters,
            "gray_letters": gray_letters,
            "candidates": self.get_candidates(),
        }

    def get_candidates(self) -> list[str]:
        """Return the list of words still consistent with all feedback so far."""
        state = self._get_constraints()
        return [w for w in self.word_list if self._is_consistent(w, state)]

    # ─────────────────────────────────────────────────────────────────────────
    # Reward
    # ─────────────────────────────────────────────────────────────────────────

    def _compute_reward(self, feedback: list[int], won: bool, out_of_guesses: bool) -> float:
        """
        Reward shaping:
            +10   for winning
            bonus for winning early (fewer guesses = bigger bonus)
            +0.1  per green tile (progress signal)
            +0.05 per yellow tile (partial progress)
            -1    for losing (used all 6 guesses)
            -0.1  per turn (encourages efficiency)
        """
        if won:
            guesses_used = len(self.guesses)
            efficiency_bonus = (self.MAX_GUESSES - guesses_used) * 0.5
            return 10.0 + efficiency_bonus

        if out_of_guesses:
            return -1.0

        # Intermediate shaping
        green_count = feedback.count(2)
        yellow_count = feedback.count(1)
        return (green_count * 0.1) + (yellow_count * 0.05) - 0.1

    # ─────────────────────────────────────────────────────────────────────────
    # Internal helpers
    # ─────────────────────────────────────────────────────────────────────────

    def _get_constraints(self) -> dict:
        """Summarise all feedback into constraint dicts (used by candidate filter)."""
        green = {}
        yellow = {}
        gray = set()

        for guess, feedback in self.guesses:
            for i, (letter, fb) in enumerate(zip(guess, feedback)):
                if fb == 2:
                    green[i] = letter
                elif fb == 1:
                    if letter not in yellow:
                        yellow[letter] = set()
                    yellow[letter].add(i)
                else:
                    if letter not in green.values() and letter not in yellow:
                        gray.add(letter)

        return {"green": green, "yellow": yellow, "gray": gray}

    def _is_consistent(self, word: str, constraints: dict) -> bool:
        """Return True if word satisfies all green/yellow/gray constraints."""
        green = constraints["green"]
        yellow = constraints["yellow"]
        gray = constraints["gray"]

        for i, letter in enumerate(word):
            # Must match greens
            if i in green and word[i] != green[i]:
                return False
            # Must not contain gray letters
            if letter in gray:
                return False

        # Yellow letters must appear, but not in the ruled-out positions
        for letter, bad_positions in yellow.items():
            if letter not in word:
                return False
            for i, ch in enumerate(word):
                if ch == letter and i in bad_positions:
                    return False

        return True

    # ─────────────────────────────────────────────────────────────────────────
    # Display
    # ─────────────────────────────────────────────────────────────────────────

    def render(self):
        """Print the current board to the terminal with color codes."""
        COLORS = {2: "\033[42m", 1: "\033[43m", 0: "\033[100m"}
        RESET = "\033[0m"

        print(f"\n{'─' * 25}")
        for guess, feedback in self.guesses:
            row = ""
            for letter, fb in zip(guess, feedback):
                row += f"{COLORS[fb]} {letter.upper()} {RESET}"
            print(row)

        remaining = self.MAX_GUESSES - len(self.guesses)
        if not self.done:
            print(f"  {remaining} guess(es) remaining")
        print(f"{'─' * 25}\n")


# ─────────────────────────────────────────────────────────────────────────────
# Quick manual test — run this file directly to verify everything works
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Minimal inline word list for testing (replace with your real words.txt)
    test_words = [
        "crane", "slate", "audio", "raise", "planet",
        "arose", "stare", "snare", "share", "spare",
        "scare", "glare", "flare", "blare", "flake",
        "brake", "shake", "shame", "shale", "shape",
    ]

    env = WordleEnv(test_words)

    # ── Test 1: feedback logic ─────────────────────────────────────────────
    env.reset(target="crane")
    assert env.get_feedback("crane") == [2, 2, 2, 2, 2], "Exact match should be all green"
    assert env.get_feedback("slate") == [0, 0, 2, 0, 2], "'a' green pos2, 'e' green pos4"
    assert env.get_feedback("arise") == [1, 2, 0, 0, 2], "'a' yellow, 'r' green, 'e' green"
    print("✓ Feedback logic tests passed")

    # ── Test 2: full episode ───────────────────────────────────────────────
    state = env.reset(target="crane")
    assert state["guess_number"] == 0

    state, reward, done, info = env.step("slate")
    assert not done
    assert info["guess_number"] == 1
    print(f"  slate → feedback: {env.guesses[-1][1]}, reward: {reward:.2f}")

    state, reward, done, info = env.step("crane")
    assert done and info["won"]
    print(f"  crane → WON in {info['guess_number']} guesses, reward: {reward:.2f}")
    env.render()

    # ── Test 3: loss path ──────────────────────────────────────────────────
    state = env.reset(target="shape")
    for word in ["crane", "slate", "audio", "raise", "arose", "stare"]:
        state, reward, done, info = env.step(word)
    assert done and not info["won"]
    print(f"✓ Loss path: game over after 6 guesses, reward: {reward:.2f}")

    # ── Test 4: candidates filter ──────────────────────────────────────────
    state = env.reset(target="spare")
    env.step("crane")   # c=gray, r=yellow pos2, a=yellow pos1, n=gray, e=green pos4
    candidates = state["candidates"]
    print(f"✓ Candidates after 'crane': {env.get_candidates()}")

    print("\nAll tests passed. wordle_env.py is ready to use.")