# Wordle Information-Theoretic Solver

## Project Overview

This project investigates different strategies for solving the game Wordle, with a primary focus on information-theoretic and constraint-based approaches.

Wordle is a sequential decision-making problem in which the player must identify a hidden five-letter word within six guesses. After each guess, the environment provides feedback for every letter:

- `0` = gray → letter is not in the target word
- `1` = yellow → letter exists in the target word but is in the wrong position
- `2` = green → letter is in the correct position

The goal of this project is to design and evaluate automated Wordle-solving agents that efficiently reduce uncertainty and solve puzzles in as few guesses as possible.

While the project initially explored Reinforcement Learning approaches, the primary focus shifted toward entropy-based search and information-gain strategies after observing that these methods are significantly more effective and computationally stable for Wordle.

---

# Information-Gain Approach

The main solver implemented in this repository is an entropy-based agent.

At each turn, the agent:

1. Simulates possible feedback patterns for candidate guesses
2. Computes the expected information gain (entropy reduction)
3. Selects the guess that maximally reduces uncertainty about the hidden word

This approach is inspired by information theory and search-based optimization techniques commonly used in Wordle solvers.

---

# Implemented Agents

## Constraint-Filtered Random Agent
Chooses randomly among words still consistent with all prior feedback.

## Frequency-Based Agent
Chooses words using letter-frequency heuristics to maximize coverage of common letters.

## Entropy Agent
Chooses guesses that maximize expected information gain using Shannon entropy.

## Archived RL Agents
Initial Reinforcement Learning scaffolding (REINFORCE and DQN) is preserved in the archive folder for comparison and future experimentation.

---

# Repository Structure

```text
wordle-project/
│
├── wordle_env.py
├── valid-wordle-words.txt
├── play.py
├── README.md
│
├── agents/
│   ├── random_agent.py
│   ├── frequency_agent.py
│   └── entropy_agent.py
│
├── evaluation/
│   ├── evaluate.py
│   ├── benchmark.py
│   └── metrics.py
│
├── utils/
│   ├── feedback.py
│   └── entropy.py
│
├── visualizations/
│
├── archive/
│   ├── reinforce_agent.py
│   ├── dqn_agent.py
│   └── train_rl.py
│
└── docs/