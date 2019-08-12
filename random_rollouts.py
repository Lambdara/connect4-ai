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
    Node,
    Player,
)
import random


class RandomRollout(Player):
    """
    For each move, observes the winrate under random behavior, makes the move
    with the highest winrate
    """
    walks = 100
    printing = False

    def move(self, state):
        tree = Node(state=state)
        tree.expand()

        best_move = None
        best_count = -1
        for child in tree.children:
            count = 0
            for _ in range(self.walks):
                if self.random_walk(child).state.winner() == state.player:
                    count += 1
            if self.printing:
                print('%d: %f' % (child.move, count/self.walks))
            if count > best_count:
                best_count = count
                best_move = child.move
        return best_move

    def random_walk(self,node):
        while node.state.winner() is None:
            node.expand()
            node = random.choice(node.children)
        return node
