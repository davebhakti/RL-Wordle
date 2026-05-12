from collections import Counter


def compute_feedback(guess, target):
    guess = guess.lower()
    target = target.lower()

    feedback = [0] * 5
    remaining = Counter(target)

    for i in range(5):
        if guess[i] == target[i]:
            feedback[i] = 2
            remaining[guess[i]] -= 1

    for i in range(5):
        if feedback[i] == 2:
            continue

        if remaining[guess[i]] > 0:
            feedback[i] = 1
            remaining[guess[i]] -= 1

    return feedback