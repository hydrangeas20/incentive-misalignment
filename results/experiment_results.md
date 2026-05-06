# Experiment Results

This experiment compares simple strategies in a repeated Prisoner's Dilemma.
The goal is to observe how different incentives and policies affect cooperation.

| Agent A | Agent B | Total Reward A | Total Reward B | Cooperation A | Cooperation B |
|---|---|---:|---:|---:|---:|
| Always Cooperate | Always Defect | 0 | 500 | 100.00% | 0.00% |
| Tit For Tat | Always Defect | 99 | 104 | 1.00% | 0.00% |
| Tit For Tat | Tit For Tat | 300 | 300 | 100.00% | 100.00% |
| Suspicious Tit For Tat | Tit For Tat | 250 | 250 | 50.00% | 50.00% |
| Random | Tit For Tat | 240 | 235 | 56.00% | 57.00% |

## Initial observations

- Always Defect exploits Always Cooperate, showing how naive cooperation can be punished.
- Tit For Tat can sustain cooperation when paired with another cooperative reciprocal strategy.
- Initial distrust can reduce cooperation, even when both agents later mirror each other.
- Random behavior creates unstable outcomes because the opponent cannot reliably predict whether cooperation will be rewarded.