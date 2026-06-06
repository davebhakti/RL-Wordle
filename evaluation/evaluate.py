import time
import random

from wordle_env import WordleEnv


def evaluate_agent(agent, valid_words, answer_words, max_games=None):

    wins = 0
    losses = 0

    total_guesses = 0
    total_time = 0.0

    failed_words = []

    solve_distribution = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
    }

    env = WordleEnv(valid_words, answer_words)

    # --------------------------------------------------
    # Choose evaluation set
    # --------------------------------------------------

    test_words = answer_words.copy()

    if max_games is not None:
        random.shuffle(test_words)
        test_words = test_words[:max_games]

    # --------------------------------------------------
    # Run games
    # --------------------------------------------------

    for i, target_word in enumerate(test_words):

        if i % 50 == 0:
            print(f"Game {i}/{len(test_words)}")

        start = time.time()

        state = env.reset(target=target_word)

        done = False
        info = {}

        while not done:

            guess = agent.choose_guess(env, state)

            state, reward, done, info = env.step(guess)

        end = time.time()

        total_time += (end - start)

        if info["won"]:

            wins += 1

            guesses_used = info["guess_number"]

            total_guesses += guesses_used

            solve_distribution[guesses_used] += 1

        else:

            losses += 1

            failed_words.append(target_word)

    games_played = wins + losses

    return {
        "games": games_played,
        "wins": wins,
        "losses": losses,
        "win_rate":
            (wins / games_played) * 100
            if games_played > 0 else 0,

        "average_guesses":
            total_guesses / wins
            if wins > 0 else 0,

        "average_runtime":
            total_time / games_played
            if games_played > 0 else 0,

        "solve_distribution":
            solve_distribution,

        "failed_words":
            failed_words,
    }


def print_summary(agent_name, summary):

    print("\n========================================")
    print(f"Results for {agent_name}")
    print("========================================")

    print(f"Games: {summary['games']}")
    print(f"Wins: {summary['wins']}")
    print(f"Losses: {summary['losses']}")

    print(f"Win Rate: {summary['win_rate']:.2f}%")

    print(f"\nTotal Failed Words: {len(summary['failed_words'])}")

    print(
        f"Average Guesses on Wins: "
        f"{summary['average_guesses']:.2f}"
    )

    print(
        f"Average Runtime Per Game: "
        f"{summary['average_runtime']:.4f} seconds"
    )

    print("Solve Distribution:")

    for guesses, count in summary["solve_distribution"].items():
        print(f"  {guesses} guesses: {count}")

    print("\nFirst 50 Failed Words:")

    for word in summary["failed_words"][:50]:
        print(word)

    print("========================================")


if __name__ == "__main__":

    from agents.random_agent import RandomAgent
    from agents.frequency_agent import FrequencyAgent
    from agents.entropy_agent import EntropyAgent
    from agents.hybrid_agent import HybridAgent

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

    agents = [
        ("Random Agent", RandomAgent()),
        ("Frequency Agent", FrequencyAgent()),
        ("Entropy Agent", EntropyAgent(valid_words)),
        ("Hybrid Agent", HybridAgent(valid_words)),
    ]

    for name, agent in agents:

        summary = evaluate_agent(
            agent,
            valid_words,
            answer_words,
            max_games=None
        )

        print_summary(name, summary)