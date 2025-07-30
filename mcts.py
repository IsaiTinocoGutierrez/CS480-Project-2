import random
from mcts_node import MCTSNode, select_best_child
from deck import Deck
from hand_evaluator import compare_hands


class MCTS:
    def __init__(self, root_state, num_simulations=1000):
        self.root = MCTSNode(state=root_state)
        self.num_simulations = num_simulations

    def run_search(self):
        for _ in range(self.num_simulations):
            node = self.root

            # Force full rollout to river
            while not self.is_terminal(node):
                if not node.is_fully_expanded():
                    node = self.expansion(node)
                else:
                    node = select_best_child(node)

            result = self.simulation(node)
            self.backpropagation(node, result)

        return self.root.wins / self.root.visits if self.root.visits > 0 else 0.0
    
    def is_terminal(self, node):
        state = node.state
        return all(key in state for key in ['opponent_cards', 'flop', 'turn', 'river'])

    def selection(self, node):
        while node.children and node.is_fully_expanded():
            node = select_best_child(node)
        return node

    def expansion(self, node):
        if node.is_fully_expanded():
            return node  # nothing to expand

        new_state = self.get_random_unseen_child_state(node)
        child = MCTSNode(parent=node, state=new_state)
        node.add_child(child)
        return child

    def simulation(self, node):
        return self.evaluate_random_hand(node.state)

    def backpropagation(self, node, result):
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent

    def get_random_unseen_child_state(self, node):
        deck = Deck()

        # Collect all known cards in the path from root to this node
        current = node
        known_cards = set()
        while current is not None:
            state = current.state
            if state:
                known_cards.update(state.get('hole_cards', []))
                known_cards.update(state.get('opponent_cards', []))
                known_cards.update(state.get('flop', []))
                known_cards.update(state.get('turn', []))
                known_cards.update(state.get('river', []))
            current = current.parent

        deck.mark_as_drawn(known_cards)
        parent_state = node.state
        child_state = parent_state.copy()

        if 'opponent_cards' not in parent_state:
            child_state['opponent_cards'] = deck.draw(2)
        elif 'flop' not in parent_state:
            child_state['flop'] = deck.draw(3)
        elif 'turn' not in parent_state:
            child_state['turn'] = deck.draw(1)
        elif 'river' not in parent_state:
            child_state['river'] = deck.draw(1)

        return child_state

    def evaluate_random_hand(self, state):
        required_keys = ['hole_cards', 'opponent_cards', 'flop', 'turn', 'river']
        if not all(k in state for k in required_keys):
            # Don't evaluate incomplete hands
            return 0.0

        my_hole = state['hole_cards']
        opp_hole = state['opponent_cards']
        flop = state['flop']
        turn = state['turn']
        river = state['river']
        board = flop + turn + river

        return compare_hands(my_hole, opp_hole, board)