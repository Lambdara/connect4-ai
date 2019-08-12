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


import numpy as np

# Settings
BOARD_COLUMNS = 7
BOARD_ROWS = 6


BOARD_EMPTY = 0
BOARD_RED = 1
BOARD_YELLOW = 2


class State():
    def __init__(self):
        self.data = np.zeros((BOARD_COLUMNS, BOARD_ROWS))
        self.player = BOARD_RED

    def __str__(self):
        return np.flipud(np.transpose(self.data)).__str__()

    def move(self, col, player=None):
        if player is None:
            player = self.player


        # First free location:
        free_spots = [
            row for row in range(BOARD_ROWS) if
            self.data[col,row] == BOARD_EMPTY
        ]

        if not free_spots:
            raise ValueError('Tried to make move at col %d which has no free spots' % col)

        row = free_spots[0]

        self.data[col,row] = self.player
        self.player = BOARD_YELLOW if self.player == BOARD_RED else BOARD_RED

    def available_moves(self):
        return [
            col for col in range(BOARD_COLUMNS) if
            BOARD_EMPTY in [self.data[col,row] for row in range(BOARD_ROWS)]
        ]

    def winner(self):
        # Check horizontal 4-in-a-rows
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS - 3):
                if self.data[col,row] != BOARD_EMPTY and\
                   self.data[col,row] ==\
                   self.data[col+1,row] ==\
                   self.data[col+2,row] ==\
                   self.data[col+3,row]:
                    return self.data[col,row]

        # Check vertical 4-in-a-rows
        for row in range(BOARD_ROWS-3):
            for col in range(BOARD_COLUMNS):
                if self.data[col,row] != BOARD_EMPTY and\
                   self.data[col,row] ==\
                   self.data[col,row+1] ==\
                   self.data[col,row+2] ==\
                   self.data[col,row+3]:
                    return self.data[col,row]

        # Check diagonal nw-se 4-in-a-rows
        for row in range(3, BOARD_ROWS):
            for col in range(BOARD_COLUMNS - 3):
                if self.data[col,row] != BOARD_EMPTY and\
                   self.data[col,row] ==\
                   self.data[col+1,row-1] ==\
                   self.data[col+2,row-2] ==\
                   self.data[col+3,row-3]:
                    return self.data[col,row]

        # Check diagonal sw-ne 4-in-a-rows
        for row in range(BOARD_ROWS-3):
            for col in range(BOARD_COLUMNS-3):
                if self.data[col,row] != BOARD_EMPTY and\
                   self.data[col,row] ==\
                   self.data[col+1,row+1] ==\
                   self.data[col+2,row+2] ==\
                   self.data[col+3,row+3]:
                    return self.data[col,row]

        # No winner
        return None

    def copy(self):
        state = State()
        state.data = self.data.copy()
        state.player = self.player

        return state


class Node():
    def __init__(self, parent=None, state=None):
        self.parent = parent
        self.state = state if state is not None else State()
        self.children = None

    def expand(self):
        # Replaces children with a list of nodes, one for each available move

        self.children = []

        for move in self.state.available_moves():
            state = self.state.copy()
            state.move(move)

            node = Node(parent=self, state=state)
            self.children.append(node)

    def __str__(self):
        return self.state.__str__()
