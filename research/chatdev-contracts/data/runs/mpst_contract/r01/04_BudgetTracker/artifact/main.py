from cli import run_cli
from tracker import BudgetTracker


def main():
    tracker = BudgetTracker("budget_data.json")
    run_cli(tracker)


if __name__ == "__main__":
    main()