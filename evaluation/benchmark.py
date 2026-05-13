import time

from agents.random_agent import RandomAgent
from agents.frequency_agent import FrequencyAgent
from agents.entropy_agent import EntropyAgent

from evaluation.evaluate import evaluate_agent, print_summary


with open("valid-wordle-words.txt") as f:
    words = f.read().splitlines()


agents = [
    ("Random Agent", RandomAgent()),
    ("Frequency Agent", FrequencyAgent()),
    ("Entropy Agent", EntropyAgent(words, use_full_word_list=False)),
]


for name, agent in agents:

    start = time.time()

    summary = evaluate_agent(
        agent,
        words,
        max_games=100
    )

    end = time.time()

    print_summary(name, summary)

    print(f"Runtime: {end - start:.2f} seconds")