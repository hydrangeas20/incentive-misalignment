# Reward Hacking Results

This experiment shows a toy version of reward hacking.
The intended goal is to reach the goal location, but the specified reward can make other actions more attractive.

| Agent | Total Specified Reward | Goal Completion Rate | Action Counts |
|---|---:|---:|---|
| Goal Directed Agent | 400 | 100.00% | {'move_to_goal': 100, 'collect_coin': 0, 'loop_near_start': 0} |
| Reward Maximizing Agent | 600 | 0.00% | {'move_to_goal': 0, 'collect_coin': 100, 'loop_near_start': 0} |
| Mostly Goal Directed Agent | 442 | 79.00% | {'move_to_goal': 79, 'collect_coin': 21, 'loop_near_start': 0} |

## Initial observations

- The goal-directed agent completes the intended task but may receive less specified reward.
- The reward-maximizing agent receives high specified reward while failing the intended goal.
- This demonstrates the core alignment problem: agents optimize what is measured, not necessarily what is meant.