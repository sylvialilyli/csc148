"""
Subclass StonehengeGame of Game
"""
from game import Game
from typing import Any
from stonehenge_state import StonehengeState


class StonehengeGame(Game):
    """
    Abstract class for a game to be played with two players.

    length: side length of a StonehengeGame that the player input
    current_state: the current game state of a StonehengeGame
    """
    length: int
    current_state: StonehengeState

    def __init__(self, p1_starts: bool) -> None:
        """
        Initialize this Game, using p1_starts to find who the first player is.
        Overrides Game.__init__(self, p1_starts)
        """
        length = input('Please input the side lenght of gameboard:')
        self.current_state = StonehengeState(p1_starts, int(length))

    def __eq__(self, other: Any) -> bool:
        """
        Return whether StonehengeGame self is equivalent to other.
        """
        return (type(self) == type(other)
                and self.current_state == other.current_state
                and self.length == other.length)

    def __str__(self) -> str:
        """
        Return a string representation of the StonehengeGame self.
        """
        return self.current_state.__str__()

    def get_instructions(self) -> str:
        """
        Return the instructions of this game.
        Overrrides Game.get_instructions(self)
        """
        instructions = "Stonehenge is played on a hexagonal grid formed by " \
                       'removing the corners from a triangular grid. Boards ' \
                       'can ' \
                       'have various sizes based on their side-length (the ' \
                       'number of cells in the grid along the bottom), but ' \
                       'are ' \
                       'always formed in a similar manner: For ' \
                       'side-length n, ' \
                       'the first row has 2 cells, and each row after has 1 ' \
                       "additional cell up until there's a row with n + 1 " \
                       "cells, after which the last row has only n cells in " \
                       "it. \n Players take turns claiming cells (in the " \
                       "diagram: circles labelled with a capital letter). " \
                       "When a player captures at least half of the cells " \
                       "in a " \
                       "ley-line (in the diagram: hexagons with a line " \
                       "connecting it to cells), then the player captures " \
                       "that ley-line. The first player to capture at least" \
                       " half " \
                       "of the ley-lines is the winner. A ley-line, once " \
                       "claimed, cannot be taken by the other player."
        return instructions

    def is_over(self, state: StonehengeState) -> bool:
        """
        Return whether or not this game is over.
        Override Game.is_over(self)
        """
        result = False
        if (state.p1_count / state.total_leylines >= 0.5
                or state.p2_count / state.total_leylines >= 0.5
                or self.current_state.get_possible_moves() == []):
            result = True
        return result

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.
        Precondition: player is 'p1' or 'p2'.
        Override Game.is_winner(self)
        """
        return (self.current_state.get_current_player_name() != player
                and self.is_over(self.current_state))

    def str_to_move(self, move_to_make: Any) -> str:
        """
        Return the move that string represents. If string is not a move,
        return an invalid move.
        Override Game.str_to_move(self, string)
        """
        result = str(move_to_make).upper().strip()
        while not result.isalpha() or len(result) != 1:
            result = input('Please enter a valid move:')
            self.string_to_move(result)
        return result


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
