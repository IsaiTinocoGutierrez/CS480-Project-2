from mcts import MCTS

if __name__ == "__main__":
    state = {'hole_cards': ['Qs', 'Ks']}  # example input
    mcts = MCTS(root_state=state, num_simulations=1000)
    win_prob = mcts.run_search()
    print(f"Estimated win probability for {state['hole_cards']}: {win_prob:.4f}")
