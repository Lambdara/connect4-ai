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
TIE = 3


class State():
    def __init__(self):
        self.data = np.zeros((BOARD_COLUMNS, BOARD_ROWS), dtype=np.int32)
        self.player = BOARD_RED

    def __str__(self):
        result = '-' * (BOARD_COLUMNS*2+1)
        for row in range(BOARD_ROWS-1,-1,-1):
            result += '\n|'
            for col in range(BOARD_COLUMNS):
                if col != 0:
                    result += ' '
                if self.data[col, row] == BOARD_RED:
                    result += '\033[1;37;41m'
                    colored = True
                elif self.data[col, row] == BOARD_YELLOW:
                    result += '\033[1;30;43m'
                    colored = True
                else:
                    colored = False
                result += str(self.data[col,row])
                if colored:
                    result += '\033[0m'
            result += '|'
        result += '\n' + '-' * (BOARD_COLUMNS*2+1)
        return result

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

        # Check for tie
        if BOARD_EMPTY not in self.data:
            return TIE

        # No winner
        return None

    def copy(self):
        state = State()
        state.data = self.data.copy()
        state.player = self.player

        return state

class Player():
    """
    Player is a class that defines behavior in a game. AI implementations can
    inherit from this to define behavior that the game will understand.
    """

    def move(self, state):
        print(
            'You are player %d, called %s' %\
            (state.player, 'Red' if state.player == BOARD_RED else 'Yellow')
        )
        print('Available moves: %s' % str([x+1 for x in state.available_moves()]))
        return int(input('Move (number): '))-1


class Game():
    def __init__(self, red_player, yellow_player):
        self.red_player = red_player
        self.yellow_player = yellow_player
        self.state = State()

    def play_turn(self, printing=True):
        if self.state.player == BOARD_RED:
            move = self.red_player.move(self.state.copy())
        else:
            move = self.yellow_player.move(self.state.copy())

        self.state.move(move)

        if printing:
            print(self.state)

    def play_game(self, printing=True):
        while self.state.winner() is None:
            self.play_turn(printing=printing)
        if printing:
            winner = self.state.winner()
            if winner == BOARD_RED:
                winner_text = 'Red'
            elif winner == BOARD_YELLOW:
                winner_text = 'Yellow'
            else:
                winner_text = 'tie'
            print('Winner: %s' % winner_text)
