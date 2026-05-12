from wordle_env import WordleEnv
from agents.entropy_agent import EntropyAgent


def main():
    with open("valid-wordle-words.txt") as f:
        words = [w.strip().lower() for w in f if len(w.strip()) == 5]

    env = WordleEnv(words)
    agent = EntropyAgent(words, use_full_word_list=False)

    state = env.reset()

    print(f"Target hidden. Starting Wordle game.")

    while not env.done:
        guess = agent.choose_guess(env, state)
        print(f"Agent guesses: {guess}")

        state, reward, done, info = env.step(guess)
        env.render()

    if info["won"]:
        print(f"Solved in {info['guess_number']} guesses!")
    else:
        print(f"Failed. Target was {info['target']}.")


if __name__ == "__main__":
    main()