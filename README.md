# Wordle AI Project

## Project Overview

This project investigates different strategies for solving Wordle. The original idea was to build a Reinforcement Learning agent, but based on feedback, the project now focuses more strongly on comparing RL-based methods against information-gain based approaches.

Wordle is a sequential decision-making problem where the agent must guess a hidden five-letter word in at most six attempts. After each guess, the environment returns feedback:

- `0` = gray, letter is not in the target word
- `1` = yellow, letter is in the word but in the wrong position
- `2` = green, letter is in the correct position

## Current Repository Structure

```text
wordle-project/
│
├── wordle_env.py
├── valid-wordle-words.txt
│
├── agents/
│   ├── random_agent.py
│   ├── entropy_agent.py
│   ├── reinforce_agent.py
│   └── dqn_agent.py
│
├── evaluation/
│   ├── evaluate.py
│   └── metrics.py
│
├── utils/
│   ├── feedback.py
│   └── entropy.py
│
├── play.py
├── train_rl.py
└── README.md