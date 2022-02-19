# Name: Charles Xu
# Date: 11/27/21
# Description: This program replicates the Hasami Shogi game in a Python program.
# Three classes help represent an abstract game board which follows the rules
# defined by Hasami Shogi Variant 1.


class HasamiShogiGame:
    """
    A class to represent the Hasami Shogi game which can make moves, check the
    current game state, and report on where the pawns are on the board. Creates
    a game board to represent pawns, squares, and keep count of the number of
    pawns each player has.

    Overview: Hasami Shogi is a 2-player game with one player
    moving the red pawns and one player moving the black pawns. Pawns can be
    captured if they are sandwiched either horizontally or vertically by the
    opponent’s pawns. Valid move returns True; false, otherwise. A player wins
    when the opponent has one or zero pawns left on the board.
    """

    def __init__(self) -> None:
        """
        Construct HasamiShogiGame object. Instantiate a Board object and set
        starting player's turn to the Black player.
        """
        self._board = Board()
        self._player_turn: str = 'BLACK'  # Black player starts first

    def get_board(self):
        """
        Return the Board.
        :return: Board
        """
        return self._board

    def set_board(self, new_board) -> None:
        """
        Set the Board to new_board.
        :return: None
        """
        self._board = new_board

    def get_player_turn(self) -> str:
        """
        Return active player's turn. Redundant with get_active_player but
        included so _player_turn has both a getter and a setter.
        :return: str
        """
        return self.get_active_player()

    def set_player_turn(self, color: str) -> None:
        """
        Set player's turn to either 'RED' or 'BLACK'.
        :param color: which player set as active
        :return: None
        """
        self._player_turn = color

    def get_active_player(self) -> str:
        """
        Return active player's turn.
        :return: str
        """
        return self._player_turn

    def switch_turns(self) -> None:
        """
        Switch player's turn from 'BLACK' to 'RED' and vice versa.
        :return: None
        """
        if self._player_turn == 'BLACK':
            self._player_turn = 'RED'
        else:
            self._player_turn = 'BLACK'

    def get_game_state(self) -> str:
        """
        Return one of three strings: 'UNFINISHED', 'RED_WON', or 'BLACK_WON'.
        Check if one player has one or zero pawns left; if so, that player lost.
        :return: str returned for the following game states:
        Black player has one or zero pawns left -> 'RED_WON'
        Red player has one or zero pawns left -> 'BLACK_WON'
        None of the players have one or zero pawns left -> 'UNFINISHED'
        """
        if self._board.get_num_pawns('BLACK') <= 1:
            return 'RED_WON'
        elif self._board.get_num_pawns('RED') <= 1:
            return 'BLACK_WON'
        else:
            return 'UNFINISHED'

    def get_num_captured_pieces(self, color: str) -> int:
        """
        Return number of pawns that have been captured with the specified color.
        :param color: str, which player's number of captured pawns to return
        :return: int between 0 - 9
        """
        result = self._board.get_num_pawns(color)
        return 9 - result

    def make_move(self, src_pos: str, dest_pos: str) -> bool:
        """
        Make a move by:
        [x] moving a pawn at src_pos to dest_pos
        [x] capturing any pawns in a captured state
        [x] updating the game state
        [x] updating which player's turn it is
        Return True if the move is legal; false, otherwise
        :param src_pos: str, location of the pawn being moved
        :param dest_pos: str, location of where to move the pawn
        :return: bool
        """
        this_pawn = self._board.get_square(src_pos)
        if not self.validate_move(src_pos, dest_pos):
            print("Move is not valid!")
            return False
        self._board.set_square(src_pos, Pawn(src_pos, 'NONE'))
        self._board.set_square(dest_pos, this_pawn)
        self.capture(dest_pos)
        if self.get_game_state() == 'BLACK_WON':
            print("BLACK WINS THE GAME!")
        if self.get_game_state() == 'RED_WON':
            print("RED WINS THE GAME")
        self.switch_turns()
        return True

    def validate_move(self, src_pos: str, dest_pos: str) -> bool:
        """
        Return True if
        (0) the game is not over
        (1) the pawn belongs to the player making the turn
        (2) the move is not off the board
        (3) the dest_pos is vacant
        (4) the pawn is only moving horizontally or vertically
        (5) the pawn can move legally without encountering pawns on its path
        Otherwise, return False.
        :param src_pos: str, location of pawn being moved
        :param dest_pos: str, location of where the pawn will be moved
        :return: bool
        """
        src_pawn = self._board.get_square(src_pos)
        dest_pawn = self._board.get_square(dest_pos)
        src_indices = self._board.translate(src_pos)
        dest_indices = self._board.translate(dest_pos)

        # (0) the game is not over
        if self.get_game_state() != 'UNFINISHED':
            print("Error: 0")
            return False
        # (1) the pawn belongs to the player making the turn
        elif src_pawn.get_color() != self.get_active_player():
            print("Error: 1")
            return False
        # (2) the move is not off the board
        elif 0 > src_indices[0] > 8 or 0 > src_indices[1] > 8 \
                or 0 > dest_indices[0] > 8 or 0 > dest_indices[1] > 8:
            print("Error: 2")
            return False
        # (3) the dest_pos is vacant
        elif dest_pawn.get_color() != "NONE":
            print("Error: 3")
            return False
        # (4) the pawn is only moving horizontally or vertically
        elif src_pos[0] != dest_pos[0] and src_pos[1] != dest_pos[1]:
            print("Error: 4")
            return False
        # (5) the pawn can move legally without encountering pawns on its path
        elif not self.check_if_clear_path(src_pos, dest_pos):
            print("Error: 5")
            return False
        else:
            return True

    def check_if_clear_path(self, src_pos: str, dest_pos: str) -> bool:
        """
        Return True if pawn at src_pos encounters no red or black pawns on the
        way to dest_pos. Otherwise, return False.
        :param src_pos: str, location of source square
        :param dest_pos: str, location of destination square
        :return: bool
        """
        src_indices = self._board.translate(src_pos)
        dest_indices = self._board.translate(dest_pos)
        the_list = self._board.get_board_list()

        # if move is horizontal
        if src_indices[0] == dest_indices[0]:
            lower_index = min(src_indices[1], dest_indices[1])
            max_index = max(src_indices[1], dest_indices[1])
            index = lower_index + 1
            while index < max_index:
                if the_list[src_indices[0]][index].get_color() != 'NONE':
                    return False
                index += 1

        # if move is vertical
        if src_indices[1] == dest_indices[1]:
            lower_index = min(src_indices[0], dest_indices[0])
            max_index = max(src_indices[0], dest_indices[0])
            index = lower_index + 1
            while index < max_index:
                if the_list[index][src_indices[1]].get_color() != 'NONE':
                    return False
                index += 1

        return True

    def capture(self, pos: str) -> bool:
        """
        Return True if the pawn at dest_pos
        (1) completes "sandwich" between 1 or more opponent pawns either
        horizontally or vertically
        (2) completes orthogonal capture of a corner square
        If True, remove captured pawn.
        Otherwise, return False.
        :param pos: str, location of where the pawn has been moved
        :return: bool
        """
        player_color = self._board.get_square(pos).get_color()
        opponent_color = ""
        if player_color == 'RED':
            opponent_color = 'BLACK'
        if player_color == 'BLACK':
            opponent_color = 'RED'

        left = self.left_capture(pos, player_color, opponent_color)
        right = self.right_capture(pos, player_color, opponent_color)
        top = self.top_capture(pos, player_color, opponent_color)
        bottom = self.bottom_capture(pos, player_color, opponent_color)
        corner = self.corner_capture()

        return left or right or top or bottom or corner

    def left_capture(self, pos: str, player_color: str, opponent_color: str) -> bool:
        """
        Return True if pos completes a left capture of one or more opponent pawns.
        :param pos: str
        :param player_color: str
        :param opponent_color: str
        :return: bool
        """
        captured_flag = False
        captured_list = []  # list of captured positions (in alg. notation)
        indices = self._board.translate(pos)
        row_index: int = indices[0] + 1
        col_index: int = indices[1] + 1
        if col_index >= 3:
            left_pos = pos[0] + str(col_index - 1)
            left_color = self._board.get_square(left_pos).get_color()
            if left_color == opponent_color:
                captured_list.append(left_pos)
                for index in range(col_index - 2, 0, -1):
                    temp_pos = pos[0] + str(index)
                    temp_pawn = self._board.get_square(temp_pos)
                    # if square is another opponent pawn
                    if temp_pawn.get_color() == opponent_color:
                        captured_list.append(temp_pos)
                    elif temp_pawn.get_color() == player_color:
                        for captured_pos in captured_list:
                            self._board.remove_pawn(captured_pos)
                            captured_flag = True
                        break
                    else:
                        break
            captured_list = []
            return captured_flag

    def right_capture(self, pos: str, player_color: str, opponent_color: str) -> bool:
        """
        Return True if pos completes a right capture of one or more opponent pawns.
        :param pos: str
        :param player_color: str
        :param opponent_color: str
        :return: bool
        """
        captured_flag = False
        captured_list = []  # list of captured positions (in alg. notation)
        indices = self._board.translate(pos)
        row_index: int = indices[0] + 1
        col_index: int = indices[1] + 1

        if col_index <= 7:
            right_pos = pos[0] + str(col_index + 1)
            right_color = self._board.get_square(right_pos).get_color()
            if right_color == opponent_color:
                captured_list.append(right_pos)
                for index in range(col_index + 2, 10):
                    temp_pos = pos[0] + str(index)
                    temp_pawn = self._board.get_square(temp_pos)
                    # if square is another opponent pawn
                    if temp_pawn.get_color() == opponent_color:
                        captured_list.append(temp_pos)
                    elif temp_pawn.get_color() == player_color:
                        for captured_pos in captured_list:
                            self._board.remove_pawn(captured_pos)
                            captured_flag = True
                        break
                    else:
                        break
            captured_list = []
            return captured_flag

    def top_capture(self, pos: str, player_color: str, opponent_color: str) -> bool:
        """
        Return True if pos completes a top capture of one or more opponent pawns.
        :param pos: str
        :param player_color: str
        :param opponent_color: str
        :return: bool
        """
        captured_flag = False
        captured_list = []  # list of captured positions (in alg. notation)
        indices = self._board.translate(pos)
        row_index: int = indices[0] + 1
        col_index: int = indices[1] + 1
        row_dict = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i'}

        if row_index >= 3:
            top_pos = row_dict.get(row_index - 1) + pos[1]
            top_color = self._board.get_square(top_pos).get_color()
            if top_color == opponent_color:
                captured_list.append(top_pos)
                for index in range(row_index - 2, 0, -1):
                    temp_pos = row_dict.get(index) + pos[1]
                    temp_pawn = self._board.get_square(temp_pos)
                    # if square is another opponent pawn
                    if temp_pawn.get_color() == opponent_color:
                        captured_list.append(temp_pos)
                    elif temp_pawn.get_color() == player_color:
                        for captured_pos in captured_list:
                            self._board.remove_pawn(captured_pos)
                            captured_flag = True
                        break
                    else:
                        break
            captured_list = []
            return captured_flag

    def bottom_capture(self, pos: str, player_color: str, opponent_color: str) -> bool:
        """
        Return True if pos completes a bottom capture of one or more opponent pawns.
        :param pos: str
        :param player_color: str
        :param opponent_color: str
        :return: bool
        """
        captured_flag = False
        captured_list = []  # list of captured positions (in alg. notation)
        indices = self._board.translate(pos)
        row_index: int = indices[0] + 1
        col_index: int = indices[1] + 1
        row_dict = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i'}

        if row_index <= 7:
            bottom_pos = row_dict.get(row_index + 1) + pos[1]
            bottom_color = self._board.get_square(bottom_pos).get_color()
            if bottom_color == opponent_color:
                captured_list.append(bottom_pos)
                for index in range(row_index + 2, 10):
                    temp_pos = row_dict.get(index) + pos[1]
                    temp_pawn = self._board.get_square(temp_pos)
                    # if square is another opponent pawn
                    if temp_pawn.get_color() == opponent_color:
                        captured_list.append(temp_pos)
                    elif temp_pawn.get_color() == player_color:
                        for captured_pos in captured_list:
                            self._board.remove_pawn(captured_pos)
                            captured_flag = True
                        break
                    else:
                        break
            captured_list = []
            return captured_flag

    def corner_capture(self) -> bool:
        """
        Return True and remove corner pawn if it is captured orthogonally.
        Otherwise, return False.
        :return: bool
        """
        top_left = self._board.get_square('a1')
        if self._board.get_square('b1').get_color() != top_left.get_color() and \
                self._board.get_square('b1').get_color() != 'NONE' and \
                self._board.get_square('a2').get_color() != top_left.get_color() and \
                self._board.get_square('a2').get_color() != 'NONE':
            self._board.remove_pawn('a1')
            return True
        top_right = self._board.get_square('a9')
        if self._board.get_square('a8').get_color() != top_right.get_color() and \
                self._board.get_square('a8').get_color() != 'NONE' and \
                self._board.get_square('b9').get_color() != top_right.get_color() and \
                self._board.get_square('b9').get_color() != 'NONE':
            self._board.remove_pawn('a9')
            return True
        bottom_left = self._board.get_square('i1')
        if self._board.get_square('h1').get_color() != bottom_left.get_color() and \
                self._board.get_square('h1').get_color() != 'NONE' and \
                self._board.get_square('i2').get_color() != bottom_left.get_color() and \
                self._board.get_square('i2').get_color() != 'NONE':
            self._board.remove_pawn('i1')
            return True
        bottom_right = self._board.get_square('i9')
        if self._board.get_square('h9').get_color() != bottom_right.get_color() and \
                self._board.get_square('h9').get_color() != 'NONE' and \
                self._board.get_square('i8').get_color() != bottom_right.get_color() and \
                self._board.get_square('i8').get_color() != 'NONE':
            self._board.remove_pawn('i9')
            return True
        return False

    def get_square_occupant(self, pos: str) -> str:
        """
        Return a string describing what is occupying the square at pos.
        :param pos: str
        :return: str of either 'RED', 'BLACK', or 'NONE'
        """
        return self._board.get_square(pos).get_color()

    def display(self) -> None:
        """
        Display the string representation of the Board.
        :return: None
        """
        print(self._board)
        print(f"{self.get_active_player()}'s Turn: ")
        print(f"BLACK pawns captured: {self.get_num_captured_pieces('BLACK')}")
        print(f"RED pawns captured: {self.get_num_captured_pieces('RED')}")


class Pawn:
    """
    A class to represent the pawns on the board. Each pawn can get and set its
    position and color. Used by the HasamiShogiGame class and Board class.
    """

    def __init__(self, current_pos: str, color: str) -> None:
        """
        Construct a Pawn object that takes a current_pos parameter to establish
        the location of the Pawn on the Board and a color parameter to keep
        track of which pawn belongs to whom.
        :param current_pos: str, algebraic notation of the pawn's position
        :param color: str, player color
        """
        self._current_pos = current_pos
        self._color = color

    def get_position(self) -> str:
        """
        Return the position of the Pawn.
        :return: str
        """
        return self._current_pos

    def set_position(self, new_pos: str) -> None:
        """
        Set the position of the Pawn
        :param new_pos: str, new position of Pawn
        :return: None
        """
        self._current_pos = new_pos

    def get_color(self) -> str:
        """
        Return the color of the Pawn.
        :return: str, Pawn color
        """
        return self._color

    def set_color(self, new_color: str) -> None:
        """
        Set the color of the Pawn.
        :param new_color: str, new color
        :return: None
        """
        self._color = new_color

    def __str__(self) -> str:
        """
        toString method; return string representation of the Pawn's color
        :return: str
        """
        if self._color == 'RED':
            return 'R'
        elif self._color == 'BLACK':
            return 'B'
        else:
            return '.'


class Board:
    """
    A class to represent the abstract game board for Hasami Shogi. A Board can
    create/remove Pawns, get/set squares, keep track of the number of Pawns on
    the board, and set the number of Pawns on the board. Used by the
    HasamiShogiGame class.
    """

    def __init__(self):
        """
        Construct a Board object of size 9 x 9 squares. The column will be
        labelled a-i and the row will be labelled 1-9. Each square will be
        empty, contain a Red Pawn, or contain a Black Pawn.
        Upon instantiation, 9 Red Pawns will be placed across row a and 9
        Black Pawns will be placed across row i.
        Each square is stored in a dictionary.
        Int num_pawns_red and int num_pawns_black are created to keep track of
        the number of pawns on the board for each player.
        """
        self._num_pawns_red = 9
        self._num_pawns_black = 9
        # create list representation of initial board setup
        self._board_list = self.starting_board_to_list()

    def starting_board_to_list(self) -> list:
        """
        Helper method to create a list of lists representing the starting 81
        squares on the game board. The outer list represents the columns and the
        inner lists represent the rows. Each list holds the following:
        (1) empty square: Pawn with color NONE
        (2) red Pawn with color RED
        (3) black Pawn with color BLACK
        :return: list of lists of Pawns
        """
        # THIS METHOD IS ONLY USED ONCE TO SET UP THE LIST REP. OF GAME BOARD
        row_and_column = []
        for letter in range(1, 10):
            row = []
            for number in range(1, 10):
                if letter == 1:
                    row.append(Pawn("", "RED"))
                elif letter == 9:
                    row.append(Pawn("", "BLACK"))
                else:
                    row.append(Pawn("", "NONE"))
            row_and_column.append(row)
        return row_and_column

    def get_board_list(self) -> list:
        """
        Return the list representation of the board.
        :return: list of lists of Pawns
        """
        return self._board_list

    def set_board_list(self, new_list) -> None:
        """
        Set the list representation of the board.
        :return: None
        """
        self._board_list = new_list

    def translate(self, notation: str) -> tuple:
        """
        Convert algebraic notation of a square (ex. 'a1') to the matching
        pair of indices in the list of lists. Return pair of indices as a tuple.
        :param notation: str consisting of one letter and one number
        :return: tuple of two ints
        """
        row_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7,
                    'h': 8, 'i': 9}
        row_index = int(row_dict.get(notation[0])) - 1
        col_index = int(notation[1]) - 1
        return row_index, col_index

    def get_square(self, pos: str) -> Pawn:
        """
        Return the Pawn at pos. If square is empty, return None.
        :param pos: str, algebraic notation of square
        :return: Pawn
        """
        indices = self.translate(pos)
        square = self._board_list[indices[0]][indices[1]]
        return square

    def set_square(self, pos: str, new_pawn: Pawn) -> None:
        """
        Add a new Pawn to position pos with color color.
        :param pos: str, algebraic notation of square
        :param new_pawn: Pawn, pawn that will occupy the square
        :return: None
        """
        indices = self.translate(pos)
        self._board_list[indices[0]][indices[1]] = new_pawn

    def remove_pawn(self, pos) -> None:
        """
        Remove the Pawn at pos. Decrement the number of pawns of that color.
        If there is no Pawn at pos, do nothing.
        :param pos: str
        :return: None
        """
        color = self.get_square(pos).get_color()
        if color == 'RED':
            self._num_pawns_red -= 1
        if color == 'BLACK':
            self._num_pawns_black -= 1
        empty_pawn = Pawn(pos, 'NONE')
        self.set_square(pos, empty_pawn)

    def get_num_pawns(self, color: str) -> int:
        """
        Return the number of pawns of color color.
        :param color: str
        :return: int
        """
        if color == 'RED':
            return self._num_pawns_red
        return self._num_pawns_black

    def set_num_pawns(self, color, new_num) -> None:
        """
        Set the number of pawns of color color to new_num.
        :param color: str
        :param new_num: int between 0-9
        :return: None
        """
        if color == 'RED':
            self._num_pawns_red = new_num
        else:
            self._num_pawns_black = new_num

    def __str__(self) -> str:
        """
        Override the __str__ method of the Pawn class to create a simpler
        board visualization for testing.
        :return: None
        """
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        line = ""

        print("  1 2 3 4 5 6 7 8 9")
        for row in range(9):
            lookup_key = alphabet[row]
            line += alphabet[row] + " "
            for col in range(9):
                lookup_key += str(col + 1)
                square_occupant: Pawn = self._board_list[row][col]
                line += str(square_occupant) + " "
                lookup_key = lookup_key[0]
            print(line)
            line = ""
        return ""


def main():
    """
    Main method to run and test the program.
    :return: None
    """
    game = HasamiShogiGame()
    board = Board()
    print("Welcome to Hasami Shogi!")
    print("GAME OVERVIEW: ")
    print("Hasami Shogi is a 2-player game with one player \
    moving the red pawns and one player moving the black pawns. Pawns can be\
    captured if they are sandwiched either horizontally or vertically by the\
    opponent’s pawns. Valid move returns True; false, otherwise. A player wins\
    when the opponent has one or zero pawns left on the board.")
    print("Enter QUIT when it is your turn to exit the game.")
    print("Game starting...\n\n\n")

    while game.get_game_state() != 'RED_WON' or \
            game.get_game_state() != 'BLACK_WON':
        game.display()
        source = input("Please select a pawn to move: ")
        dest = input("Please select where to move the pawn: ")
        if source == "QUIT" or dest == "QUIT":
            print("GAME OVER")
            break
        game.make_move(source, dest)




if __name__ == "__main__":
    main()
