# connect4-ai
# Copyright (C) 2019 Uwila

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from connect4 import (
    State,
    Player,
    TIE,
)
import random
from math import log


class MCTS(Player):
    printing = False

    c = 2**0.5

    def __init__(self, walks=100):
        self.walks = walks

    def move(self, state):
        tree = Node(state=state)
        tree.expand()

        best_move = None
        best_w = 0
        
        for child in tree.children:
            for walk in range(self.walks):
                node = self.selection(child, walk)
                node.expand()
                result_state = self.simulate(node)
                self.backpropagate(state, node, result_state)

                
            if self.printing:
                print('%s: %f' % (child.move, child.w))
            if child.w > best_w:
                best_w = child.w
                best_move = child.move
        return best_move
    
    def selection(self, node, walk):
        # TODO: Replace random.choice with some good formula
        while node.fully_expanded() and node.children:
            best_uct = 0
            best_child = None
            for child in node.children:
                uct = child.w/child.n + self.c * (log(walk)/child.n) ** 0.5
                if uct > best_uct:
                    best_uct = uct
                    best_child = child
            node = best_child
            
        if node.children:
            # The node is not fully expanded but has children, so look for one
            # of the unused children and use it
            node = random.choice([c for c in node.children if c.n == 0])
        return node

    def simulate(self, node):
        # TODO: Maybe replace random.choice with some good formula?
        state = node.state.copy()
        while state.winner() is None:
            state.move(random.choice(state.available_moves()))
        return state

    def backpropagate(self, current_state, node, result_state):
        while True:
            winner = result_state.winner()
            if winner == TIE:
                value = 0.5
            # node.state.player is the player whose turn it is on that board,
            # the exact opposite of the winrate for the player who chooses to
            # go to that state
            elif winner != node.state.player:
                value = 1
            else:
                value = 0
            node.n += 1
            node.w += value

            if node.parent is None:
                break
            else:
                node = node.parent


class Node():
    """
    For building a gametree

    It is initialized with children being None. This means that the children
    arent generated yet. Calling expand will replace children with the list of
    the actual children ([] in case it is a leaf node).
    """

    def __init__(self, parent=None, state=None, move=None):
        self.parent = parent
        self.state = state.copy() if state is not None else State()
        self.children = None
        self.move = move # The move to get here from the previous node
        self.w = 0
        self.n = 0


    def expand(self):
        # Replaces children with a list of nodes, one for each available move

        if self.children is not None:
            # Already ran, nothing to do
            return

        self.children = []

        for move in self.state.available_moves():
            state = self.state.copy()
            state.move(move)

            node = Node(parent=self, state=state, move=move)
            self.children.append(node)

    def fully_expanded(self):
        self.expand()
        if not self.children:
            return True
        return all(child.n > 0 for child in self.children)

    def __str__(self):
        return self.state.__str__()
