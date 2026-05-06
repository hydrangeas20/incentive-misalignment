"""
Incentive Misalignment Simulation

Goal:
Simulate repeated Prisoner's Dilemma games and a toy reward-hacking environment
to show how incentive structures can lead to cooperation, defection, exploitation,
or optimization of the wrong objective.

Run experiments:
    python simulation.py

Run tests:
    python simulation.py --test

Outputs:
    Printed summaries in the terminal
    PNG charts saved in the results/ folder
    Markdown summaries saved in the results/ folder
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple
import random
import sys

import matplotlib.pyplot as plt


Action = str
RoundResult = Tuple[Action, Action, int, int]

COOPERATE = "C"
DEFECT = "D"


@dataclass
class PayoffMatrix:
    """Stores rewards for each pair of actions."""

    reward_both_cooperate: int = 3
    reward_defect_against_cooperator: int = 5
    reward_cooperate_against_defector: int = 0
    reward_both_defect: int = 1

    def get_rewards(self, action_a: Action, action_b: Action) -> Tuple[int, int]:
        if action_a == COOPERATE and action_b == COOPERATE:
            return self.reward_both_cooperate, self.reward_both_cooperate
        if action_a == DEFECT and action_b == COOPERATE:
            return self.reward_defect_against_cooperator, self.reward_cooperate_against_defector
        if action_a == COOPERATE and action_b == DEFECT:
            return self.reward_cooperate_against_defector, self.reward_defect_against_cooperator
        if action_a == DEFECT and action_b == DEFECT:
            return self.reward_both_defect, self.reward_both_defect
        raise ValueError(f"Invalid actions: {action_a}, {action_b}")


class Strategy:
    name = "Base Strategy"

    def choose_action(self, my_history: List[Action], opponent_history: List[Action]) -> Action:
        raise NotImplementedError


class AlwaysCooperate(Strategy):
    name = "Always Cooperate"

    def choose_action(self, my_history: List[Action], opponent_history: List[Action]) -> Action:
        return COOPERATE


class AlwaysDefect(Strategy):
    name = "Always Defect"

    def choose_action(self, my_history: List[Action], opponent_history: List[Action]) -> Action:
        return DEFECT


class RandomStrategy(Strategy):
    name = "Random"

    def choose_action(self, my_history: List[Action], opponent_history: List[Action]) -> Action:
        return random.choice([COOPERATE, DEFECT])


class TitForTat(Strategy):
    """Cooperates first, then copies the opponent's previous action."""

    name = "Tit For Tat"

    def choose_action(self, my_history: List[Action], opponent_history: List[Action]) -> Action:
        if not opponent_history:
            return COOPERATE
        return opponent_history[-1]


class SuspiciousTitForTat(Strategy):
    """Defects first, then copies the opponent's previous action."""

    name = "Suspicious Tit For Tat"

    def choose_action(self, my_history: List[Action], opponent_history: List[Action]) -> Action:
        if not opponent_history:
            return DEFECT
        return opponent_history[-1]


@dataclass
class SimulationResult:
    agent_a_name: str
    agent_b_name: str
    rounds: int
    history: List[RoundResult]

    @property
    def total_reward_a(self) -> int:
        return sum(result[2] for result in self.history)

    @property
    def total_reward_b(self) -> int:
        return sum(result[3] for result in self.history)

    @property
    def cooperation_rate_a(self) -> float:
        return sum(1 for result in self.history if result[0] == COOPERATE) / self.rounds

    @property
    def cooperation_rate_b(self) -> float:
        return sum(1 for result in self.history if result[1] == COOPERATE) / self.rounds

    @property
    def cumulative_rewards_a(self) -> List[int]:
        total = 0
        rewards = []
        for _, _, reward_a, _ in self.history:
            total += reward_a
            rewards.append(total)
        return rewards

    @property
    def cumulative_rewards_b(self) -> List[int]:
        total = 0
        rewards = []
        for _, _, _, reward_b in self.history:
            total += reward_b
            rewards.append(total)
        return rewards


class PrisonersDilemmaSimulation:
    def __init__(self, payoff_matrix: PayoffMatrix, rounds: int = 100):
        if rounds <= 0:
            raise ValueError("rounds must be positive")
        self.payoff_matrix = payoff_matrix
        self.rounds = rounds

    def run(self, strategy_a: Strategy, strategy_b: Strategy) -> SimulationResult:
        history: List[RoundResult] = []
        actions_a: List[Action] = []
        actions_b: List[Action] = []

        for _ in range(self.rounds):
            action_a = strategy_a.choose_action(actions_a, actions_b)
            action_b = strategy_b.choose_action(actions_b, actions_a)
            reward_a, reward_b = self.payoff_matrix.get_rewards(action_a, action_b)

            history.append((action_a, action_b, reward_a, reward_b))
            actions_a.append(action_a)
            actions_b.append(action_b)

        return SimulationResult(strategy_a.name, strategy_b.name, self.rounds, history)


def print_summary(result: SimulationResult) -> None:
    print("=" * 70)
    print(f"Agent A: {result.agent_a_name}")
    print(f"Agent B: {result.agent_b_name}")
    print(f"Rounds: {result.rounds}")
    print("-" * 70)
    print(f"Total reward A: {result.total_reward_a}")
    print(f"Total reward B: {result.total_reward_b}")
    print(f"Cooperation rate A: {result.cooperation_rate_a:.2%}")
    print(f"Cooperation rate B: {result.cooperation_rate_b:.2%}")
    print("=" * 70)
    print()


def safe_filename(name: str) -> str:
    return name.lower().replace(" ", "_").replace("/", "_")


def plot_cumulative_rewards(result: SimulationResult, output_dir: Path) -> None:
    rounds = list(range(1, result.rounds + 1))
    plt.figure(figsize=(10, 6))
    plt.plot(rounds, result.cumulative_rewards_a, label=result.agent_a_name)
    plt.plot(rounds, result.cumulative_rewards_b, label=result.agent_b_name)
    plt.xlabel("Round")
    plt.ylabel("Cumulative Reward")
    plt.title(f"Cumulative Rewards: {result.agent_a_name} vs {result.agent_b_name}")
    plt.legend()
    plt.tight_layout()

    filename = f"rewards_{safe_filename(result.agent_a_name)}_vs_{safe_filename(result.agent_b_name)}.png"
    plt.savefig(output_dir / filename)
    plt.close()


def plot_cooperation_rates(results: List[SimulationResult], output_dir: Path) -> None:
    labels = [f"{r.agent_a_name}\nvs\n{r.agent_b_name}" for r in results]
    rates_a = [r.cooperation_rate_a for r in results]
    rates_b = [r.cooperation_rate_b for r in results]
    x_positions = list(range(len(results)))
    width = 0.35

    plt.figure(figsize=(12, 6))
    plt.bar([x - width / 2 for x in x_positions], rates_a, width, label="Agent A")
    plt.bar([x + width / 2 for x in x_positions], rates_b, width, label="Agent B")
    plt.xticks(x_positions, labels, rotation=20, ha="right")
    plt.ylim(0, 1)
    plt.ylabel("Cooperation Rate")
    plt.title("Cooperation Rates Across Incentive Experiments")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "cooperation_rates.png")
    plt.close()


def write_markdown_summary(results: List[SimulationResult], output_dir: Path) -> None:
    lines = [
        "# Experiment Results",
        "",
        "This experiment compares simple strategies in a repeated Prisoner's Dilemma.",
        "The goal is to observe how different incentives and policies affect cooperation.",
        "",
        "| Agent A | Agent B | Total Reward A | Total Reward B | Cooperation A | Cooperation B |",
        "|---|---|---:|---:|---:|---:|",
    ]

    for result in results:
        lines.append(
            f"| {result.agent_a_name} | {result.agent_b_name} | "
            f"{result.total_reward_a} | {result.total_reward_b} | "
            f"{result.cooperation_rate_a:.2%} | {result.cooperation_rate_b:.2%} |"
        )

    lines.extend([
        "",
        "## Initial observations",
        "",
        "- Always Defect exploits Always Cooperate, showing how naive cooperation can be punished.",
        "- Tit For Tat can sustain cooperation when paired with another cooperative reciprocal strategy.",
        "- Initial distrust can reduce cooperation, even when both agents later mirror each other.",
        "- Random behaviour creates unstable outcomes because the opponent cannot reliably predict whether cooperation will be rewarded.",
    ])

    (output_dir / "experiment_results.md").write_text("\n".join(lines), encoding="utf-8")


RewardHackAction = str
MOVE_TO_GOAL = "move_to_goal"
COLLECT_COIN = "collect_coin"
LOOP_NEAR_START = "loop_near_start"


@dataclass
class RewardHackingResult:
    agent_name: str
    rounds: int
    history: List[Tuple[RewardHackAction, int, bool]]

    @property
    def total_reward(self) -> int:
        return sum(reward for _, reward, _ in self.history)

    @property
    def goal_completion_rate(self) -> float:
        return sum(1 for _, _, reached_goal in self.history if reached_goal) / self.rounds

    @property
    def action_counts(self) -> Dict[RewardHackAction, int]:
        counts = {MOVE_TO_GOAL: 0, COLLECT_COIN: 0, LOOP_NEAR_START: 0}
        for action, _, _ in self.history:
            counts[action] += 1
        return counts

    @property
    def cumulative_rewards(self) -> List[int]:
        total = 0
        rewards = []
        for _, reward, _ in self.history:
            total += reward
            rewards.append(total)
        return rewards


class RewardHackingEnvironment:
    """Tiny environment where the specified reward can diverge from the intended goal."""

    def __init__(self, reward_scheme: Dict[RewardHackAction, int], rounds: int = 100):
        if rounds <= 0:
            raise ValueError("rounds must be positive")
        required_actions = {MOVE_TO_GOAL, COLLECT_COIN, LOOP_NEAR_START}
        missing_actions = required_actions.difference(reward_scheme)
        if missing_actions:
            raise ValueError(f"reward_scheme is missing actions: {sorted(missing_actions)}")

        self.reward_scheme = reward_scheme
        self.rounds = rounds

    def step(self, action: RewardHackAction) -> Tuple[int, bool]:
        if action not in self.reward_scheme:
            raise ValueError(f"Unknown action: {action}")
        reward = self.reward_scheme[action]
        reached_goal = action == MOVE_TO_GOAL
        return reward, reached_goal

    def run(self, agent: "RewardHackAgent") -> RewardHackingResult:
        history: List[Tuple[RewardHackAction, int, bool]] = []
        for _ in range(self.rounds):
            action = agent.choose_action(self.reward_scheme)
            reward, reached_goal = self.step(action)
            history.append((action, reward, reached_goal))
        return RewardHackingResult(agent.name, self.rounds, history)


class RewardHackAgent:
    name = "Base Reward Hack Agent"

    def choose_action(self, reward_scheme: Dict[RewardHackAction, int]) -> RewardHackAction:
        raise NotImplementedError


class GoalDirectedAgent(RewardHackAgent):
    name = "Goal Directed Agent"

    def choose_action(self, reward_scheme: Dict[RewardHackAction, int]) -> RewardHackAction:
        return MOVE_TO_GOAL


class RewardMaximizingAgent(RewardHackAgent):
    name = "Reward Maximizing Agent"

    def choose_action(self, reward_scheme: Dict[RewardHackAction, int]) -> RewardHackAction:
        return max(reward_scheme, key=reward_scheme.get)


class MostlyGoalDirectedAgent(RewardHackAgent):
    name = "Mostly Goal Directed Agent"

    def __init__(self, goal_probability: float = 0.8):
        if not 0 <= goal_probability <= 1:
            raise ValueError("goal_probability must be between 0 and 1")
        self.goal_probability = goal_probability

    def choose_action(self, reward_scheme: Dict[RewardHackAction, int]) -> RewardHackAction:
        if random.random() < self.goal_probability:
            return MOVE_TO_GOAL
        return max(reward_scheme, key=reward_scheme.get)


def print_reward_hacking_summary(result: RewardHackingResult) -> None:
    print("=" * 70)
    print(f"Reward hacking experiment: {result.agent_name}")
    print(f"Rounds: {result.rounds}")
    print("-" * 70)
    print(f"Total specified reward: {result.total_reward}")
    print(f"Goal completion rate: {result.goal_completion_rate:.2%}")
    print(f"Action counts: {result.action_counts}")
    print("=" * 70)
    print()


def plot_reward_hacking_cumulative_rewards(results: List[RewardHackingResult], output_dir: Path) -> None:
    plt.figure(figsize=(10, 6))
    rounds = list(range(1, results[0].rounds + 1))
    for result in results:
        plt.plot(rounds, result.cumulative_rewards, label=result.agent_name)

    plt.xlabel("Round")
    plt.ylabel("Cumulative Specified Reward")
    plt.title("Reward Hacking: Specified Reward Over Time")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "reward_hacking_cumulative_rewards.png")
    plt.close()


def plot_reward_hacking_goal_completion(results: List[RewardHackingResult], output_dir: Path) -> None:
    labels = [result.agent_name for result in results]
    goal_rates = [result.goal_completion_rate for result in results]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, goal_rates)
    plt.ylim(0, 1)
    plt.ylabel("Goal Completion Rate")
    plt.title("Reward Hacking: Intended Goal Completion")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(output_dir / "reward_hacking_goal_completion.png")
    plt.close()


def write_reward_hacking_summary(results: List[RewardHackingResult], output_dir: Path) -> None:
    lines = [
        "# Reward Hacking Results",
        "",
        "This experiment shows a toy version of reward hacking.",
        "The intended goal is to reach the goal location, but the specified reward can make other actions more attractive.",
        "",
        "| Agent | Total Specified Reward | Goal Completion Rate | Action Counts |",
        "|---|---:|---:|---|",
    ]

    for result in results:
        lines.append(
            f"| {result.agent_name} | {result.total_reward} | "
            f"{result.goal_completion_rate:.2%} | {result.action_counts} |"
        )

    lines.extend([
        "",
        "## Initial observations",
        "",
        "- The goal-directed agent completes the intended task but may receive less specified reward.",
        "- The reward-maximizing agent receives high specified reward while failing the intended goal.",
        "- This demonstrates the core alignment problem: agents optimize what is measured, not necessarily what is meant.",
    ])

    (output_dir / "reward_hacking_results.md").write_text("\n".join(lines), encoding="utf-8")


def run_prisoners_dilemma_experiments(output_dir: Path) -> List[SimulationResult]:
    payoff_matrix = PayoffMatrix()
    simulation = PrisonersDilemmaSimulation(payoff_matrix=payoff_matrix, rounds=100)

    experiments = [
        (AlwaysCooperate(), AlwaysDefect()),
        (TitForTat(), AlwaysDefect()),
        (TitForTat(), TitForTat()),
        (SuspiciousTitForTat(), TitForTat()),
        (RandomStrategy(), TitForTat()),
    ]

    results = []
    for strategy_a, strategy_b in experiments:
        result = simulation.run(strategy_a, strategy_b)
        results.append(result)
        print_summary(result)
        plot_cumulative_rewards(result, output_dir)

    plot_cooperation_rates(results, output_dir)
    write_markdown_summary(results, output_dir)
    return results


def run_reward_hacking_experiments(output_dir: Path) -> List[RewardHackingResult]:
    bad_proxy_reward_scheme = {
        MOVE_TO_GOAL: 4,
        COLLECT_COIN: 6,
        LOOP_NEAR_START: 5,
    }

    environment = RewardHackingEnvironment(reward_scheme=bad_proxy_reward_scheme, rounds=100)
    agents = [
        GoalDirectedAgent(),
        RewardMaximizingAgent(),
        MostlyGoalDirectedAgent(goal_probability=0.8),
    ]

    results = []
    for agent in agents:
        result = environment.run(agent)
        results.append(result)
        print_reward_hacking_summary(result)

    plot_reward_hacking_cumulative_rewards(results, output_dir)
    plot_reward_hacking_goal_completion(results, output_dir)
    write_reward_hacking_summary(results, output_dir)
    return results


def run_tests() -> None:
    payoff_matrix = PayoffMatrix()
    assert payoff_matrix.get_rewards(COOPERATE, COOPERATE) == (3, 3)
    assert payoff_matrix.get_rewards(DEFECT, COOPERATE) == (5, 0)
    assert payoff_matrix.get_rewards(COOPERATE, DEFECT) == (0, 5)
    assert payoff_matrix.get_rewards(DEFECT, DEFECT) == (1, 1)

    simulation = PrisonersDilemmaSimulation(payoff_matrix=payoff_matrix, rounds=10)
    result = simulation.run(AlwaysCooperate(), AlwaysDefect())
    assert result.total_reward_a == 0
    assert result.total_reward_b == 50
    assert result.cooperation_rate_a == 1.0
    assert result.cooperation_rate_b == 0.0
    assert result.cumulative_rewards_b[-1] == 50

    tit_for_tat_result = simulation.run(TitForTat(), TitForTat())
    assert tit_for_tat_result.total_reward_a == 30
    assert tit_for_tat_result.total_reward_b == 30
    assert tit_for_tat_result.cooperation_rate_a == 1.0
    assert tit_for_tat_result.cooperation_rate_b == 1.0

    reward_scheme = {
        MOVE_TO_GOAL: 4,
        COLLECT_COIN: 6,
        LOOP_NEAR_START: 5,
    }
    environment = RewardHackingEnvironment(reward_scheme=reward_scheme, rounds=10)

    goal_result = environment.run(GoalDirectedAgent())
    assert goal_result.total_reward == 40
    assert goal_result.goal_completion_rate == 1.0
    assert goal_result.action_counts[MOVE_TO_GOAL] == 10

    reward_max_result = environment.run(RewardMaximizingAgent())
    assert reward_max_result.total_reward == 60
    assert reward_max_result.goal_completion_rate == 0.0
    assert reward_max_result.action_counts[COLLECT_COIN] == 10

    random.seed(42)
    mixed_result = environment.run(MostlyGoalDirectedAgent(goal_probability=1.0))
    assert mixed_result.goal_completion_rate == 1.0

    print("All tests passed.")


def main() -> None:
    if "--test" in sys.argv:
        run_tests()
        return

    random.seed(42)
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    print("\nRunning Prisoner's Dilemma experiments...\n")
    run_prisoners_dilemma_experiments(output_dir)

    print("\nRunning reward hacking experiments...\n")
    run_reward_hacking_experiments(output_dir)

    print(f"Saved charts and markdown summaries to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
