"""
subclass StonehengeState of Gamestate
"""
from typing import Any, List
from game_state import GameState
import copy


class Cellnode:
    """
    Representation of the cell in game Stonehenge

    value: the string value of a Cellnode
    left: the left cell of a Cellnode
    right_up: the right up cell of a Cellnode
    right_down: the right down cell of a Cellnode
    """
    value: str
    left: int or str
    right_up: int or str
    right_down: int or str

    def __init__(self, value, left: int or str, right_up: int or str,
                 right_down: int or str) -> None:
        """
        Initialize a cell node used in game Stonehenge

        >>> a = Cellnode(1, 15, 30, '@')
        >>> a.value
        1
        >>> a.left
        15
        >>> a.right_up
        30
        >>> a.right_down
        '@'
        """
        self.value = value
        self.left = left
        self.right_up = right_up
        self.right_down = right_down


class StonehengeState(GameState):
    """
    The state of a game Stonehenge at a certain point in time.

    length: side length of a game board
    p1_count: the number of leylines that player 1 captured
    p2_count: the number of leylines that player 2 captured
    total_leylines: the total number of leylines in a gameboard
    lines: line of cells in a gameboard
    lines_copy: the list copy of values of cells on the gameboard
    left_diagonal: list of cells forming left diagonal
    right_diagonal: list of cells forming right diagonal
    """
    length: int
    p1_count: int
    p2_count: int
    total_leylines: int
    lines: List[List[Cellnode]]
    lines_copy: List[List]
    left_diagonal: List[List[Cellnode]]
    right_diagonal: List[List[Cellnode]]

    def __init__(self, is_p1_turn: bool, length: int) -> None:
        """
        Initialize this game state and set the current player based on
        is_p1_turn.
        Extends GameState.__init__(self)

        >>> state = StonehengeState(True, 1)
        >>> line = state.lines_copy
        >>> line
        [['@', '@'], ['@', 'A', 'B'], ['@', 'C', '@'], ['@']]
        """
        GameState.__init__(self, is_p1_turn)
        self.length = length
        self.p1_count = 0
        self.p2_count = 0
        self.total_leylines = 0
        self.lines = []
        self.left_diagonal = []
        self.right_diagonal = []
        self.lines_copy = []

        # build up lines
        a = 65
        step = 2
        for i in range(self.length):
            self.lines.append([Cellnode(chr(a + j), 0, 0, 0) for j
                               in range(step)])
            self.lines_copy.append([chr(a+j) for j in range(step)])
            a += step
            step += 1
        self.lines.append([Cellnode(chr(a + i), 0, 0, 0)
                           for i in range(step - 2)])
        self.lines_copy.append([chr(a + i) for i in range(step - 2)])

        # add @
        for i in range(len(self.lines)):
            self.lines[i][0].left = '@'
            self.lines_copy[i] = ['@'] + self.lines_copy[i]
            self.total_leylines += 1
        self.lines[0][0].right_up = '@'
        self.lines_copy = [['@', '@']] + self.lines_copy
        for i in range(self.length):
            self.lines[i][-1].right_up = '@'
            self.total_leylines += 1
        if self.length >= 2:
            for i in range(1, self.length):
                self.lines_copy[i] += ['@']
        self.lines_copy[-1] += ['@']
        self.lines[-2][-1].right_down = '@'
        for node in self.lines[-1]:
            node.right_down = '@'
            self.total_leylines += 1
        self.lines_copy += [['@'] * self.length]
        self.total_leylines += 2

        # build up left_diagonal
        self.left_diagonal.append([self.lines[i][0]
                                   for i in range(self.length)])
        j = 1
        step_l = 0
        if self.length >= 2:
            for i in range(1, self.length + 1):
                self.left_diagonal.append([self.lines[z][j]
                                           for z in range(step_l,
                                                          self.length)])
                j += 1
                step_l += 1
        else:
            self.left_diagonal.append([self.lines[0][-1]])
        for i in range(1, len(self.left_diagonal)):
            self.left_diagonal[i].append(self.lines[-1][i - 1])

        # build up right_diagonal
        self.right_diagonal.append([self.lines[i][-1]
                                    for i in range(self.length)])
        step_r = 0
        for i in range(self.length - 1):
            self.right_diagonal.append([self.lines[j][-(i + 2)]
                                        for j in range(step_r, self.length)])
            step_r += 1
        if self.length >= 2:
            for i in range(self.length - 1):
                self.right_diagonal[i + 1] += [self.lines[-1][-(i + 1)]]
        self.right_diagonal.append([self.lines[-2][0], self.lines[-1][0]])

    def __eq__(self, other: Any) -> bool:
        """
        Return whether StonehengeState self is equivalent to other.

        >>> state = StonehengeState(True, 2)
        >>> state_1 = StonehengeState(True, 2)
        >>> state_2 = StonehengeState(True, 3)
        >>> state == state_1
        True
        >>> state == state_2
        False
        """
        return (type(self) == type(other)
                and self.p1_turn == other.p1_turn
                and self.length == other.length
                and self.lines_copy == other.lines_copy)

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        Override GameState.__str__(self)

        >>> state = StonehengeState(True, 1)
        >>> print(state)
                  @   @
                 /   /
            @ - A - B
                 \\ / \\
               @ - C   @
                   \\
                    @
        """
        template_1 = \
            """\
                  {}   {}
                 /   /
            {} - {} - {}
                 \\ / \\
              {} - {}   {}
                   \\
                    {}"""

        template_2 = \
            """\
                    {}   {}
                   /   /
              {} - {} - {}   {}
                 / \\ / \\ /
            {} - {} - {} - {}
                 \\ / \\ / \\
              {} - {} - {}   {}
                   \\   \\
                    {}   {}"""
        template_3 = \
            """\
                  {}   {}
                 /   /
            {} - {} - {}   {}
               / \\ / \\ /
          {} - {} - {} - {}   {}
             / \\ / \\ / \\ /
        {} - {} - {} - {} - {}
             \\ / \\ / \\ / \\
          {} - {} - {} - {}   {}
               \\   \\   \\
                {}   {}  {}"""
        template_4 = \
            """\
                  {}   {}
                /   /
           {} - {} - {}   {}
              / \\ / \\ /
         {} - {} - {} - {}   {}
            / \\ / \\ / \\ /
       {} - {} - {} - {} - {}   {}
          / \\ / \\ / \\ / \\ /
     {} - {} - {} - {} - {} - {}
          \\ / \\ / \\ / \\ / \\
       {} - {} - {} - {} - {}   {}
            \\   \\   \\   \\
             {}   {}   {}   {}"""
        template_5 = \
            """\
                  {}   {}
                 /   /
            {} - {} - {}   {}
               / \\ / \\ /
          {} - {} - {} - {}   {}
             / \\ / \\ / \\ /
        {} - {} - {} - {} - {}   {}
           / \\ / \\ / \\ / \\ /
       {} - {} - {} - {} - {} - {}   {}
          / \\ / \\ / \\ / \\ / \\ /
     {} - {} - {} - {} - {} - {} - {}
          \\ / \\ / \\ / \\ / \\ / \\
       {} - {} - {} - {} - {} -{}    {}
            \\   \\   \\   \\  \\
             {}   {}   {}   {}  {}"""
        lines = self.lines_copy
        lines_gather = sum([list_1 for list_1 in lines], [])
        if self.length == 1:
            return template_1.format(*lines_gather)
        if self.length == 2:
            return template_2.format(*lines_gather)
        if self.length == 3:
            return template_3.format(*lines_gather)
        if self.length == 4:
            return template_4.format(*lines_gather)
        if self.length == 5:
            return template_5.format(*lines_gather)

    def get_possible_moves(self) -> list:
        """
        Return all possible moves that can be applied to this state.
        Override GameState.get_possible_moves(self)

        >>> state = StonehengeState(True, 1)
        >>> state.get_possible_moves()
        ['A', 'B', 'C']
        >>> state_1 = StonehengeState(True, 2)
        >>> state_11 = state_1.make_move('A')
        >>> state_12 = state_11.make_move('F')
        >>> state_13 = state_12.make_move('D')
        >>> state_13.get_possible_moves()
        ['B', 'C', 'E', 'G']
        """
        result = []
        if (self.p1_count / self.total_leylines < 0.5
                and self.p2_count / self.total_leylines < 0.5):
            for line in self.lines:
                for item in line:
                    if item.value.isalpha():
                        result.append(item.value)
        return result

    # helper function to accumulate number of leylines gained
    def new_gain(self, current_player_name: str) -> None:
        """
        Accumulate the number of leylines gained by a player

        >>> state = StonehengeState(True, 1)
        >>> state.new_gain('p1')
        >>> state.p1_count
        1
        >>> state.p2_count
        0
        """
        if current_player_name == 'p1':
            self.p1_count += 1
        else:
            self.p2_count += 1

    def make_move(self, move: Any) -> "StonehengeState":
        """
        Return the GameState that results from applying move to this GameState.
        Override Gamestate.make_move(self)

        >>> state = StonehengeState(True, 1)
        >>> state_1 = state.make_move('A')
        >>> line_1 = state_1.lines_copy
        >>> line_1
        [['1', '@'], ['1', '1', 'B'], ['@', 'C', '@'], ['1']]

        """

        player_name = self.get_current_player_name()
        if player_name == 'p1':
            player = '1'
            p1_turn_mod = False
        else:
            player = '2'
            p1_turn_mod = True

        # create a new state
        new_state = StonehengeState(p1_turn_mod, self.length)
        new_state.p1_count = self.p1_count
        new_state.p2_count = self.p2_count
        new_state.total_leylines = self.total_leylines

        # change in lines
        line_result = copy.deepcopy(self.lines)
        line_copy_result = []
        index_node = 0
        index_list = 0
        gain = 0
        for line in line_result:
            for item in line:
                if item.value == move:
                    index_node = line.index(item)
                    index_list = line_result.index(line)
        line_result[index_list][index_node].value = player
        for i in line_result[index_list]:
            if i.value == player:
                gain += 1
        if gain / len(line_result[index_list]) >= 0.5:
            if line_result[index_list][0].left == '@':
                line_result[index_list][0].left = player
                new_state.new_gain(player_name)

        # lines in line_copy
        for i in range(len(line_result)):
            line_copy_result.append([line_result[i][j].value
                                    for j in range(len(line_result[i]))])
            line_copy_result[i] = [line_result[i][0].left] + line_copy_result[i]

        # change in left diagonal
        left_diagonal_result = copy.deepcopy(self.left_diagonal)
        index_node_l = 0
        index_list_l = 0
        gain_l = 0
        for diagonal in left_diagonal_result:
            for item_l in diagonal:
                if item_l.value == move:
                    index_node_l = diagonal.index(item_l)
                    index_list_l = left_diagonal_result.index(diagonal)
        left_diagonal_result[index_list_l][index_node_l].value = player
        for i in left_diagonal_result[index_list_l]:
            if i.value == player:
                gain_l += 1
        if gain_l / len(left_diagonal_result[index_list_l]) >= 0.5:
            if left_diagonal_result[index_list_l][0].right_up == '@':
                left_diagonal_result[index_list_l][0].right_up = player
                new_state.new_gain(player_name)

        # left diagonals in line_copy
        line_copy_result = ([[left_diagonal_result[0][0].right_up,
                            left_diagonal_result[1][0].right_up]]
                            + line_copy_result)
        for i in range(1, len(line_copy_result) - 2):
            line_copy_result[i].append(left_diagonal_result[i + 1][0].right_up)

        # change in right diagonal
        right_diagonal_result = copy.deepcopy(self.right_diagonal)
        index_node_r = 0
        index_list_r = 0
        gain_r = 0
        for diagonal_r in right_diagonal_result:
            for item_r in diagonal_r:
                if item_r.value == move:
                    index_node_r = diagonal_r.index(item_r)
                    index_list_r = right_diagonal_result.index(diagonal_r)
        right_diagonal_result[index_list_r][index_node_r].value = player
        for i in right_diagonal_result[index_list_r]:
            if i.value == player:
                gain_r += 1
        if gain_r / len(right_diagonal_result[index_list_r]) >= 0.5:
            if right_diagonal_result[index_list_r][-1].right_down == '@':
                right_diagonal_result[index_list_r][-1].right_down = player
                new_state.new_gain(player_name)

        # right diagonals in line_copy
        n1 = len(right_diagonal_result)
        line_copy_result[-1] += [right_diagonal_result[0][-1].right_down]
        line_copy_result.append([right_diagonal_result[i][-1].right_down
                                 for i in range(n1 - 1, 0, -1)])

        # return a new state
        new_state.lines = line_result
        new_state.left_diagonal = left_diagonal_result
        new_state.right_diagonal = right_diagonal_result
        new_state.lines_copy = line_copy_result
        return new_state

    def __repr__(self) -> str:
        """
        Return a representation of this state (which can be used for
        equality testing).
        Override GameState.__repr__(self)

        >>> state = StonehengeState(True, 1)
        >>> state
        P1's Turn: True
        Gameboard's side length: 1
        P1 gained: 0.0
        P2 gained: 0.0
        Unclaimed Leylines: 6
        """
        p1_points = self.p1_count / self.total_leylines
        p2_points = self.p2_count / self.total_leylines
        unclaimed_number = self.total_leylines - self.p1_count - self.p2_count
        return "P1's Turn: {} \nGameboard's side length: {} \n" \
               "P1 gained: {} \nP2 gained: {} \n" \
               "Unclaimed Leylines: {}".format(self.p1_turn,
                                               self.length,
                                               p1_points, p2_points,
                                               unclaimed_number)

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval [LOSE, WIN] of best outcome the current
        player can guarantee from state self.
        Override GameState.rough_outcome(self)

        >>> state = StonehengeState(True, 1)
        >>> state.rough_outcome()
        1.0
        >>> state_1 = StonehengeState(True, 2)
        >>> state_2 = state_1.make_move('A')
        >>> state_3 = state_2.make_move('D')
        >>> state_4 = state_3.make_move('F')
        >>> state_5 = state_4.make_move('G')
        >>> state_5.rough_outcome()
        1.0
        """
        moves = self.get_possible_moves()
        player_playing = self.get_current_player_name()
        if player_playing == 'p1':
            other_player = 'p2'
        else:
            other_player = 'p1'
        if self.game_over():
            if self.whos_winner(player_playing):
                return self.WIN
            else:
                return self.LOSE
        else:
            result = []
            for single_move in moves:
                state_new = self.make_move(single_move)
                if state_new.game_over():
                    if state_new.whos_winner(player_playing):
                        result.append(self.WIN)
                    elif state_new.whos_winner(other_player):
                        result.append(self.LOSE)
                    else:
                        result.append(self.DRAW)
                else:
                    moves_1 = state_new.get_possible_moves()
                    for single_move_1 in moves_1:
                        state_new_1 = state_new.make_move(single_move_1)
                        if state_new_1.game_over():
                            if state_new.whos_winner(player_playing):
                                result.append(self.WIN)
                            elif state_new.whos_winner(other_player):
                                result.append(self.LOSE)
                            else:
                                result.append(self.DRAW)
            return sum(result)/(len(result))

    # helper function to check if the game is over in current game state
    def game_over(self) -> bool:
        """
        Return if the game is over in current state.

        >>> state = StonehengeState(True, 1)
        >>> state.game_over()
        False
        >>> state_1 = state.make_move('A')
        >>> state_1.game_over()
        True
        """
        if (self.p1_count / self.total_leylines >= 0.5
                or self.p2_count / self.total_leylines >= 0.5
                or self.get_possible_moves() == []):
            return True
        else:
            return False

    # helper function to find winner if game is over
    def whos_winner(self, name: str) -> bool or str:
        """
        Return if the player name is a winner.

        >>> state = StonehengeState(True, 1)
        >>> state_1 = state.make_move('A')
        >>> state_1.whos_winner('p1')
        True
        """
        if self.game_over():
            if name == 'p1':
                return self.p1_count / self.total_leylines >= 0.5
            else:
                return self.p2_count / self.total_leylines >= 0.5


if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
