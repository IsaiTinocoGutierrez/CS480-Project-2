import math
import random

class MCTSNode:
    def __init__(self, parent=None, state=None):
        self.parent = parent
        self.state = state  # game state at this node
        self.children = []
        self.visits = 0
        self.wins = 0

    def add_child(self, child_node):
        self.children.append(child_node)

    def is_fully_expanded(self):
        return len(self.children) >= 1000  # example cap

    def ucb1(self, exploration_constant=math.sqrt(2)):
        if self.visits == 0:
            return float('inf')  # Always explore unvisited nodes

        parent_visits = self.parent.visits if self.parent else 1
        win_rate = self.wins / self.visits
        ucb_value = win_rate + exploration_constant * math.sqrt(
            math.log(parent_visits) / self.visits
        )
        return ucb_value

def select_best_child(node, exploration_constant=math.sqrt(2)):
    return max(node.children, key=lambda child: child.ucb1(exploration_constant))
