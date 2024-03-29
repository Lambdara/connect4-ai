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
    Game,
    Player,
)
from random_rollouts import RandomRollout
from mcts import MCTS

# Enable this to have a game of randomrollout against itself
# game = Game(RandomRollout(),RandomRollout())

# Enable this to play against RandomRollout yourself
# game = Game(Player(), RandomRollout())

# Enable this to have MCTS-10 against MCTS-1000
# game = Game(MCTS(walks=10),MCTS(walks=1000))

# MCTS vs random rollouts
game = Game(RandomRollout(),MCTS())

game.play_game()
