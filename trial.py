from wordle_env import WordleEnv

with open("valid-wordle-words.txt") as f:
    words = f.read().splitlines()

env = WordleEnv(words)
state = env.reset()
state, reward, done, info = env.step("crane")
env.render()