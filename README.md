# CS480-Project-2
CSC Project 2 "Poker"
# Poker Win Estimator using Monte Carlo Tree Search (MCTS)

This project estimates the pre-flop win probability of a given starting hand in Texas Hold’em Poker using **Monte Carlo Tree Search (MCTS)**.

Each simulation plays out a full poker hand to showdown (opponent cards + flop + turn + river) and evaluates the result. The MCTS bot uses the **UCB1** strategy to guide exploration and determine win rates based on random sampling.

From terminal or VSCode run:
- python main.py

It will output an estimated win probability for a hardcoded hand (default: ['As', 'Ks']):

Change the starting hand by going in the **main.py** and modify this line:
- state = {'hole_cards': ['Qs', 'Ks']}

You can change the number of simulations per estimate here in **main.py**:
- mcts = MCTS(root_state=state, num_simulations=10000)
