import time

from agents.random_agent import RandomAgent
from agents.frequency_agent import FrequencyAgent
from agents.entropy_agent import EntropyAgent
from agents.hybrid_agent import HybridAgent

from evaluation.evaluate import evaluate_agent, print_summary


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

print("Valid:", len(valid_words))
print("Answer:", len(answer_words))

agents = [
    ("Random Agent", RandomAgent()),
    ("Frequency Agent", FrequencyAgent()),
    ("Entropy Agent", EntropyAgent(valid_words)),
    ("Hybrid Agent", HybridAgent(valid_words)),
]


for name, agent in agents:

    start = time.time()

    summary = evaluate_agent(
        agent,
        valid_words,
        answer_words,
        max_games=None
    )

    end = time.time()

    print_summary(name, summary)

    print(f"Runtime: {end - start:.2f} seconds")