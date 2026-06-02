from wordle_env import WordleEnv
from agents.hybrid_agent import HybridAgent


def main():

    with open("valid-wordle-words.txt") as f:
        valid_words = [
            w.strip().lower()
            for w in f
            if len(w.strip()) == 5
        ]

    with open("answer-words.txt") as f:
        answer_words = [
            w.strip().lower()
            for w in f
            if len(w.strip()) == 5
        ]

    env = WordleEnv(valid_words, answer_words)
    agent = HybridAgent(valid_words, endgame_threshold=5)

    state = env.reset()

    print("Target hidden. Starting Wordle game.")


    while not env.done:
        guess = agent.choose_guess(env, state)
        print(f"Agent guesses: {guess}")

        state, reward, done, info = env.step(guess)

        env.render()

        print("Target =", env.target)

        print(f"Remaining candidates: {len(state['candidates'])}")

        # Sanity check: make sure every remaining candidate is consistent
        # with the most recent feedback.
        latest_guess, latest_feedback = env.guesses[-1]

        for word in state["candidates"]:
            simulated_feedback = env.simulate_feedback(latest_guess, word)

            if simulated_feedback != latest_feedback:
                print("BAD CANDIDATE:", word)

    if info["won"]:
        print(f"Solved in {info['guess_number']} guesses!")
    else:
        print(f"Failed. Target was {info['target']}.")

        
    print("Target =", env.target)

if __name__ == "__main__":
    main()