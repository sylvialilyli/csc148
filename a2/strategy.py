"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from game import Game
from typing import Any, List
from game_state import GameState

# TODO: Adjust the type annotation as needed.
def interactive_strategy(game: Game) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)

def rough_outcome_strategy(game: Any) -> Any:
    """
    Return a move for game by picking a move which results in a state with
    the lowest rough_outcome() for the opponent.

    NOTE: game.rough_outcome() should do the following:
        - For a state that's over, it returns the score for the current
          player of that state.
        - For a state that's not over:
            - If there is a move that results in the current player winning,
              return 1.
            - If all moves result in states where the other player can
              immediately win, return -1.
            - Otherwise; return a number between -1 and 1 corresponding to how
              'likely' the current player will win from the current state.

        In essence: rough_outcome() will only look 1 or 2 states ahead to
        'guess' the outcome of the game, but no further. It's better than
        random, but worse than minimax.
    """
    current_state = game.current_state
    best_move = None
    best_outcome = -2 # Temporarily -- just so we can replace this easily later

    # Get the move that results in the lowest rough_outcome for the opponent
    for move in current_state.get_possible_moves():
        new_state = current_state.make_move(move)

        # We multiply the below by -1 since a state that's bad for the opponent
        # is good for us.
        guessed_score = new_state.rough_outcome() * -1
        if guessed_score > best_outcome:
            best_outcome = guessed_score
            best_move = move

    # Return the move that resulted in the best rough_outcome
    return best_move

# TODO: Implement a recursive version of the minimax strategy.


def minimax_recursive_strategy(game: Game) -> Any:
    """
    Return a move for game by running a minimax recursive strategy.
    """
    moves_to_make = game.current_state.get_possible_moves()
    result = [cal_scores(game, game.current_state.make_move(move)) for move in
              moves_to_make]
    return moves_to_make[result.index(max(result))]


def cal_scores(game: Game, game_state: GameState) -> int:
    """
    Calculate scores gained by players for possible moves in the game.
    """
    state_now = game.current_state
    current_player = game.current_state.get_current_player_name()
    if current_player == 'p1':
        other_player = 'p2'
    else:
        other_player = 'p1'
    if game.is_over(game_state):
        game.current_state = game_state
        if game.is_winner(current_player):
            game.current_state = state_now
            return game.current_state.WIN
        elif game.is_winner(other_player):
            game.current_state = state_now
            return game.current_state.LOSE
        game.current_state = state_now
        return game.current_state.DRAW
    a = [cal_scores(game, game_state.make_move(move)) for move in
         game_state.get_possible_moves()]
    return sum([score for score in a])


# TODO: Implement an iterative version of the minimax strategy.

def minimax_iterative_strategy(game: Game) -> Any:
    """
    Return a move for game by using iterative minimax.
    """
    state_now = game.current_state
    root_node = TreeNode(state_now)
    s = Stack()
    s.add(root_node)
    while not s.empty():
        removed_node = s.remove()
        state = removed_node.value
        if game.is_over(state):
            current_player = state.get_current_player_name()
            if current_player == 'p1':
                other_player = 'p2'
            else:
                other_player = 'p1'

            game.current_state = state
            if game.is_winner(current_player):
                removed_node.score = GameState.WIN
            elif game.is_winner(other_player):
                removed_node.score = GameState.LOSE
            else:
                removed_node.score = GameState.DRAW
            game.current_state = state_now
        elif removed_node.children == []:
            s.add(removed_node)
            for move in state.get_possible_moves():
                child_node = TreeNode(state.make_move(move))
                removed_node.children.append(child_node)
                s.add(child_node)
        else:
            removed_node.score = max([-1 * child.score for child in
                                      removed_node.children])
    moves = state_now.get_possible_moves()
    child_scores = [child.score for child in root_node.children]
    return moves[child_scores.index(root_node.score * -1)]


class TreeNode:
    """
    A TreeNode that stores a game's state and all possible moves from that
    state.

    value - the value of the TreeNode, which is a GameState
    children - the possible moves from the GameState value
    score - the score of the current state
    """
    value: GameState
    children: List["TreeNode"]
    score: int

    def __init__(self, value: GameState, children: List["TreeNode"] =
                 None, score: int = None) -> None:
        """
        Create TreeNode self with content value, 0 or more children,
        and a score.

        >>> state = GameState(True)
        >>> t1 = TreeNode(state, score=1)
        >>> t1.value == state
        True
        >>> t1.children
        []
        >>> t1.score
        1
        """
        self.value = value
        self.children = children[:] if children is not None else []
        self.score = score


class Stack:
    """ Last-in, first-out (LIFO) stack.
    """

    def __init__(self) -> None:
        """ Create a new, empty Stack self.

        >>> s = Stack()
        """
        self._contains = []

    def add(self, obj: TreeNode) -> None:
        """ Add object obj to top of Stack self.

        >>> state = GameState(True)
        >>> t1 = TreeNode(state, score = 1)
        >>> s = Stack()
        >>> s.add(t1)
        """
        self._contains.append(obj)

    def remove(self) -> TreeNode:
        """
        Remove and return top element of Stack self.

        Assume Stack self is not empty.

        >>> state = GameState(True)
        >>> t1 = TreeNode(state, score = 1)
        >>> s = Stack()
        >>> s.add(t1)
        >>> s.remove() == t1
        True
        """
        return self._contains.pop()

    def empty(self) -> bool:
        """
        Return whether Stack self is empty.

        >>> state = GameState(True)
        >>> t1 = TreeNode(state, score = 1)
        >>> s = Stack()
        >>> s.empty()
        True
        >>> s.add(t1)
        >>> s.empty()
        False
        """
        return len(self._contains) == 0


if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
