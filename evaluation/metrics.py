def summarize_results(results):
    games = results["games"]
    wins = results["wins"]
    losses = results["losses"]
    total_guesses_for_wins = results["total_guesses_for_wins"]
    solve_distribution = results["solve_distribution"]

    win_rate = wins / games if games > 0 else 0
    avg_guesses = total_guesses_for_wins / wins if wins > 0 else 0

    return {
        "games": games,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "avg_guesses": avg_guesses,
        "solve_distribution": solve_distribution,
    }


def print_summary(summary, agent_name):
    print("\n" + "=" * 40)
    print(f"Results for {agent_name}")
    print("=" * 40)
    print(f"Games: {summary['games']}")
    print(f"Wins: {summary['wins']}")
    print(f"Losses: {summary['losses']}")
    print(f"Win Rate: {summary['win_rate'] * 100:.2f}%")
    print(f"Average Guesses on Wins: {summary['avg_guesses']:.2f}")
    print("Solve Distribution:")

    for guesses, count in summary["solve_distribution"].items():
        print(f"  {guesses} guesses: {count}")

    print("=" * 40 + "\n")