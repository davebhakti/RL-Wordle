from wordle_env import WordleEnv
from agents.reinforce_agent import ReinforceAgent
from agents.dqn_agent import DQNAgent


def main():
    with open("valid-wordle-words.txt") as f:
        words = [w.strip().lower() for w in f if len(w.strip()) == 5]

    env = WordleEnv(words)

    reinforce_agent = ReinforceAgent(words)
    dqn_agent = DQNAgent(words)

    print("Environment ready.")
    print(f"Loaded {len(words)} valid words.")

    reinforce_agent.train(episodes=1000)
    dqn_agent.train(episodes=1000)

    print("RL placeholder training complete.")


if __name__ == "__main__":
    main()