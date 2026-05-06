# 🧠 Incentive Misalignment Simulations

This project implements a lightweight AI alignment simulation project that explores how simple agents behave under different incentive structures. The project uses repeated game simulations and a toy reward-hacking environment to demonstrate how agents can optimize specified rewards while failing intended objectives.

## Overview

This project demonstrates how to build a research-style simulation workflow with:

- Agent-based incentive modeling
- Repeated strategic interaction experiments
- Reward hacking / proxy objective failure simulation
- Reproducible execution across environments
- Lightweight test coverage
- Chart and markdown artifact generation for analysis

Experiments included:

1. Repeated Prisoner’s Dilemma  
2. Reward Hacking Toy Environment  

## Problem Context: Incentive Misalignment

AI systems optimize objectives. However, the objective we specify is often only a proxy for what humans actually want.

When the reward function is misaligned with the intended goal, an agent may learn behaviour that performs well according to the metric while failing the real task.

This project simulates two alignment-relevant questions:

Can cooperation emerge or collapse based on incentives?

Can an agent maximize reward while failing the intended objective?

The key lesson from the reward hacking experiment:

> The agent that performs best according to the specified reward can perform worst according to the intended objective.

## Experiment 1: Repeated Prisoner’s Dilemma

The first experiment models repeated strategic interactions between agents.

Agents choose between:

- `C` → cooperate
- `D` → defect

The payoff matrix rewards mutual cooperation but also rewards exploiting a cooperative opponent.

This makes the environment useful for studying:

- cooperation
- defection
- trust
- exploitation
- strategic behaviour
- incentive design

Strategies included:

- Always Cooperate
- Always Defect
- Random
- Tit For Tat
- Suspicious Tit For Tat

## Experiment 2: Reward Hacking Toy Environment

The second experiment models reward mis-specification.

The intended goal is:

> Reach the goal location.

However, the specified reward function gives higher reward for collecting coins than reaching the goal:

```python
bad_proxy_reward_scheme = {
    "move_to_goal": 4,
    "collect_coin": 6,
    "loop_near_start": 5,
}
```

## Agents Included

- Goal Directed Agent  
- Reward Maximizing Agent  
- Mostly Goal Directed Agent  

The reward-maximizing agent receives the highest specified reward while failing the intended goal.

---

## Key Features

### Agent-Based Simulation

Defines agents as simple policies that choose actions based on strategy or reward incentives.

Included policies:

- always cooperate  
- always defect  
- reciprocal cooperation  
- random behaviour  
- reward maximization  
- goal-directed behaviour  

---

### Incentive Modeling

The project explicitly separates:

- intended objective  
- specified reward  
- observed behaviour  

This makes it possible to show how changing reward design changes agent behaviour.

---

### Reward Hacking Demonstration

The reward-hacking experiment shows how an agent can maximize reward while failing the true task.

#### Results:

| Agent                    | Total Specified Reward | Goal Completion Rate |
|-------------------------|----------------------:|--------------------:|
| Goal Directed Agent     | 400                   | 100%                |
| Reward Maximizing Agent | 600                   | 0%                  |
| Mostly Goal Directed    | 442                   | 79%                 |

---

### Reproducible Experiment Execution

The simulation uses a fixed random seed so results can be reproduced across runs.

Run experiments with:

```bash
python3 simulation.py
```
### Lightweight Test Coverage
The project includes built-in assertion tests to verify:

- payoff matrix logic
- cooperation rate calculations
- cumulative reward calculations
- reward-hacking behaviour
- goal completion outcomes

Run tests with:
``` bash
python3 simulation.py --test
```

Expected output:
``` bash
All tests passed.
```

### Visualization Outputs

The script generates visual artifacts for analysis and blog writing, including:
cumulative reward charts, cooperation rate comparisons, reward hacking cumulative reward chart,
goal completion chart

## Results Summary

### Prisoner’s Dilemma

The repeated Prisoner’s Dilemma experiments demonstrate how different incentive structures and behavioural policies influence long-term cooperation, exploitation, and trust dynamics between agents.

### Key observations:

- **Always Defect exploits Always Cooperate**

  The Always Defect strategy consistently maximizes short-term reward against Always Cooperate because the cooperative agent never retaliates. This creates a persistent asymmetric payoff structure where one agent benefits from exploitation while the other continually receives the lowest possible reward.

  This demonstrates how naive cooperation can become unstable in adversarial environments when there are no enforcement mechanisms, reputation systems, or reciprocal penalties.

---

- **Tit For Tat sustains cooperation with another reciprocal agent**

  When two Tit For Tat agents interact, both agents quickly converge toward stable mutual cooperation. Since each agent mirrors the opponent’s previous action, cooperative behaviour is rewarded while defection is punished immediately in subsequent rounds.

  This produces a cooperative equilibrium where both agents receive consistently high cumulative rewards over time.

  The result illustrates how reciprocity and conditional cooperation can stabilize multi-agent interactions under repeated strategic settings.

---

- **Suspicious Tit For Tat shows how initial distrust reduces cooperation**

  Suspicious Tit For Tat begins with defection before adopting reciprocal behaviour. Although cooperation may eventually emerge, the initial defection introduces early distrust and temporarily lowers collective reward.

  This demonstrates how initial conditions and early interaction dynamics can significantly influence long-term cooperative outcomes.

  Even when agents later become cooperative, early adversarial behaviour can reduce overall system efficiency and slow trust formation.

---

- **Random behaviour creates unstable cooperation patterns**

  RandomStrategy introduces unpredictability into the environment by selecting actions without a consistent policy. Reciprocal agents interacting with random behaviour struggle to establish stable cooperation because future actions become difficult to predict.

  This leads to oscillations between cooperation and defection, producing lower cumulative rewards and unstable interaction dynamics.

  The result highlights how noisy or inconsistent policies can destabilize coordination in multi-agent systems.

---

### Alignment-Relevant Insight

The experiments show that agent ur is not determined by intention alone, but by the interaction between:

- reward structure
- strategic incentives
- opponent behaviour
- policy design

Even simple environments can produce emergent cooperation, exploitation, retaliation, and instability depending on how incentives are structured.

This mirrors broader AI alignment concerns where optimizing agents may develop behaviours that are locally rational according to their objective function, but globally undesirable from a system-level perspective.


### Reward Hacking

<b>Key observations:</b>

Goal Directed Agent completes the intended task
Reward Maximizing Agent earns the highest specified reward
Reward Maximizing Agent fails the intended goal completely
Mostly Goal Directed Agent shows partial misalignment behaviour

### Central Finding
The agent is not trying to achieve the goal. It is trying to maximize the reward signal.

###  Tech Stack
<b>Language: Python </b>

<b>Visualization: Matplotlib </b>

<b>Testing: Built-in Python assertions </b>

<b>Experiment Type: Toy agent simulation </b>

<b> Research Area: AI alignment, reward hacking, incentive modeling, multi-agent behaviour </b>

<b> Version Control: Git / GitHub </b>

###  Repository Structure
``` bash
incentive-misalignment/
│
├── simulation.py              # Main experiment code
├── README.md                  # Project documentation
├── blog.md                    # Blog post draft
├── requirements.txt           # Python dependencies
├── .gitignore
└── results/
    └── .gitkeep               # Output folder placeholder
```

### Setup & Usage
Create and activate environment
```bash 
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run tests
``` bash
python3 simulation.py --test
```

### Run experiments
``` bash
python3 simulation.py
```

### Outputs

After running the experiments, the results/ folder contains:
cooperation_rates.png
reward_hacking_cumulative_rewards.png
reward_hacking_goal_completion.png
experiment_results.md
reward_hacking_results.md

### Experiment Architecture Summary

This project follows a simple research workflow:

Define environment rules
Define agent policies
Run repeated simulations
Track rewards and safety-relevant outcomes
Generate charts and markdown summaries
Interpret behaviour through an AI alignment lens


### Blog Post

This repository includes a blog-style writeup in:
[Read the full blog post on Substack](https://open.substack.com/pub/appliedalignment/p/when-agents-optimize-the-wrong-thing?r=6odc0x&utm_campaign=post-expanded-share&utm_medium=web)

The blog explains:

- What incentive misalignment means
- Why reward functions can fail
- How agents optimize specified rewards
- Why reward hacking matters for AI alignment

###  Key Takeaway

<b> The central insight is: AI systems do not optimize what we intend. They optimize what we specify. </b>

If the specification is wrong, even perfectly optimized behaviour can lead to the wrong outcome.

### Future Extensions
- Add Q-learning agents instead of fixed policies
- Compare multiple reward schemes
- Add noise or imperfect observation
- Run tournaments between strategies
- Add human feedback or corrective penalties
- Store experiment artifacts in Amazon S3
- Run experiments as scheduled AWS Batch jobs
- Add confidence intervals across multiple random seeds# incentive-misalignment
