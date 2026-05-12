import time

from wordle_env import WordleEnv

from agents.random_agent import RandomAgent
from agents.entropy_agent import EntropyAgent


def evaluate_agent(agent, words, max_games=100):
    """
    Evaluate an agent over multiple Wordle games.

    Args:
        agent: agent object with choose_guess(env, state)
        words: list of valid words
        max_games: number of games to evaluate

    Returns:
        summary dictionary
    """

    wins = 0
    losses = 0

    total_guesses = 0

    solve_distribution = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
    }

    env = WordleEnv(words)

    test_words = words[:max_games]

    for target_word in test_words:

        state = env.reset(target=target_word)

        done = False

        while not done:

            guess = agent.choose_guess(env, state)

            state, reward, done, info = env.step(guess)

        if info["won"]:

            wins += 1

            guesses_used = info["guess_number"]

            total_guesses += guesses_used

            solve_distribution[guesses_used] += 1

        else:
            losses += 1

    games_played = wins + losses

    win_rate = (wins / games_played) * 100

    average_guesses = (
        total_guesses / wins
        if wins > 0 else 0
    )

    summary = {
        "games": games_played,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "average_guesses": average_guesses,
        "solve_distribution": solve_distribution,
    }

    return summary


def print_summary(agent_name, summary):
    """
    Pretty-print evaluation metrics.
    """

    print("\n========================================")
    print(f"Results for {agent_name}")
    print("========================================")

    print(f"Games: {summary['games']}")
    print(f"Wins: {summary['wins']}")
    print(f"Losses: {summary['losses']}")

    print(f"Win Rate: {summary['win_rate']:.2f}%")

    print(
        f"Average Guesses on Wins: "
        f"{summary['average_guesses']:.2f}"
    )

    print("Solve Distribution:")

    for guesses, count in summary["solve_distribution"].items():
        print(f"  {guesses} guesses: {count}")

    print("========================================")


if __name__ == "__main__":

    # Load valid Wordle words
    with open("valid-wordle-words.txt") as f:
        words = f.read().splitlines()

    # ─────────────────────────────────────────────────────────────────────
    # Random Agent Evaluation
    # ─────────────────────────────────────────────────────────────────────

    random_agent = RandomAgent()

    start = time.time()

    random_summary = evaluate_agent(
        random_agent,
        words,
        max_games=100
    )

    end = time.time()

    print_summary("Constraint-Filtered Random Agent", random_summary)

    print(
        f"Evaluation Time: "
        f"{end - start:.2f} seconds"
    )

    # ─────────────────────────────────────────────────────────────────────
    # Entropy Agent Evaluation
    # ─────────────────────────────────────────────────────────────────────

    entropy_agent = EntropyAgent(
        words,
        use_full_word_list=False
    )

    start = time.time()

    entropy_summary = evaluate_agent(
        entropy_agent,
        words,
        max_games=100
    )

    end = time.time()

    print_summary("Entropy Agent", entropy_summary)

    print(
        f"Evaluation Time: "
        f"{end - start:.2f} seconds"
    )