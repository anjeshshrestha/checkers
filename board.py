from sys import flags
from piece import Piece

# assume player 1 is white
# assume player 2 is red
class Board:
    def __init__(self):
        self.board = []
        self.moves = []
        self.player = 1
        self.rows = 8
        self.cols = 8

        self.playerColor = ["", "WHITE", "RED"]
        self.playerColorShort = [".", "w", "r"]
        self.playerColorKing = [".", "W", "R"]

        self.player1Pieces = []
        self.player1PiecesCount = 0
        self.player2Pieces = []
        self.player2PiecesCount = 0
        self.create_board()

    # returns a piece on the board
    def get_piece(self, row, col):
        return self.board[row][col]

    # creates the starting of board
    def create_board(self):
        for row in range(self.rows):
            self.board.append([])
            for col in range(self.cols):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:  # top half - player 1
                        temp_piece = Piece(row, col, self.playerColor[1], self.playerColorShort[1],
                                           self.playerColorKing[1])
                        self.board[row].append(temp_piece)
                        self.player1Pieces.append(temp_piece)
                        self.player1PiecesCount += 1
                    elif row > 4:  # bottom half - player 2
                        temp_piece = Piece(row, col, self.playerColor[2], self.playerColorShort[2],
                                           self.playerColorKing[2])
                        self.board[row].append(temp_piece)
                        self.player2Pieces.append(temp_piece)
                        self.player2PiecesCount += 1
                    else:
                        self.board[row].append(0)

                else:
                    self.board[row].append(0)

    # print board with padding of nubers
    def print_board(self):
        print("   0 1 2 3 4 5 6 7")
        print("   _______________")
        for row in range(self.rows):
            print(row, end="| ")
            for col in range(self.cols):
                if self.board[row][col] == 0:
                    print(". ", end="")
                elif self.board[row][col].king:
                    print(self.board[row][col].colorKing, end=" ")
                else:
                    print(self.board[row][col].colorShort, end=" ")
            print("")
        print()

    # move a piece from before to after
    def move(self, row, col, new_row, new_col):
        piece = self.board[row][col]
        # move the piece in pieces
        piece.move(new_row, new_col)
        # set new location to current piece
        self.board[new_row][new_col] = piece
        # set old position to free
        self.board[row][col] = 0

        # make it king if at end
        if self.player == 1 and new_row == self.rows - 1:
            piece.make_king()
        elif self.player == 2 and new_row == 0:
            piece.make_king()

        # record the move
        self.moves.append([(row, col), (new_row, new_col)])

    # change turn of play, should be called from move
    def change_turn(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    # return if speicied position is valid
    # no longer need i think
    def valid_position(self, row, col):
        return (row >= 0 and row < self.rows) and (col >= 0 and col < self.cols)

    # check who's turn it is to play
    def whose_turn(self):
        return self.player

    # check to see if there is a winner
    def has_winner(self):
        return self.player1PiecesCount == 0 or self.player2PiecesCount == 0 or len(self.get_all_valid_moves()) == 0

    # if there is no more pieces left return who won
    def get_winner(self):
        if self.player1PiecesCount == 0:
            return "Player 2 is Winner"
        elif self.player2PiecesCount == 0:
            return "Player 1 is Winner"
        elif self.player1PiecesCount == self.player2PiecesCount:
            p1King = 0
            p2King = 0
            for k in self.player1Pieces:
                if k.king:
                    p1King += 1
            for k in self.player2Pieces:
                if k.king:
                    p2King += 1
            if p1King == p2King:
                return "Game is Draw"

        return "Player " + str((self.player % 2) + 1) + " is Winner"

    def get_winner_code(self):
        # Return the player number of who won
        if self.player1PiecesCount == 0:
            return 2
        elif self.player2PiecesCount == 0:
            return 1
        elif self.player1PiecesCount == self.player2PiecesCount:
            p1King = 0
            p2King = 0
            for k in self.player1Pieces:
                if k.king:
                    p1King += 1
            for k in self.player2Pieces:
                if k.king:
                    p2King += 1
            if p1King == p2King:
                return 0

        return (self.player % 2) + 1

    def to_play_won(self):
        if self.whose_turn() == 1 and self.player2PiecesCount == 0:
            return True
        if self.whose_turn() == 2 and self.player1PiecesCount == 0:
            return True
        return False

    # itterate over all pieces of player that is not captured
    # find moves it can make and save it a list
    # if a piece can capture, only return moves of pieces that can capture
    # return dictionary
    # { (x,y) : [[(x,y),(a,b)],[(x,y),(g,d),(f,h)]]
    #   ....
    # }
    def get_all_valid_moves(self):
        only_moves = {}
        only_capture_moves = {}
        if self.player == 1:
            for piece in self.player1Pieces:
                if not piece.captured:
                    capture, moves_list = self.get_valid_moves(piece)
                    if capture:
                        only_capture_moves[(piece.row, piece.col)] = moves_list
                    elif moves_list != []:
                        only_moves[(piece.row, piece.col)] = moves_list
        else:
            for piece in self.player2Pieces:
                if not piece.captured:
                    capture, moves_list = self.get_valid_moves(piece)
                    if capture:
                        only_capture_moves[(piece.row, piece.col)] = moves_list
                    if moves_list != []:
                        only_moves[(piece.row, piece.col)] = moves_list
        if only_capture_moves != {}:
            return only_capture_moves
        else:
            return only_moves

    def get_all_valid_moves_as_list(self):
        # Gets all legal moves as list of lists of tuples
        # {(1, 0): [ [(1, 0), (2, 1)] ],
        # (1, 2): [ [(1, 2), (2, 1)] ],
        # (3, 2): [ [(3, 2), (4, 3)], [(3, 2), (4, 1)] ],
        # (2, 3): [ [(2, 3), (3, 4)] ],
        # (2, 5): [ [(2, 5), (3, 6)], [(2, 5), (3, 4)] ],
        # (2, 7): [ [(2, 7), (3, 6)] ]}
        moves_dict = self.get_all_valid_moves()
        moves_list = []
        for moves in moves_dict.values():
            for move in moves:
                moves_list.append(move)
        return moves_list

    # print all moves a piece can make
    def print_all_valid_moves(self):
        list_of_moves = self.get_all_valid_moves()
        for piece, moves in list_of_moves.items():
            print(piece, moves)
        return list_of_moves

    # given a piece find position it can move to
    # find places it can move to
    # if it can capture, return capture move only
    def get_valid_moves(self, piece):
        moves = []
        list_of_places = []
        # check for emptty space
        if piece.king or self.player == 1:  # look moving down
            if piece.row + 1 < self.rows and piece.col + 1 < self.cols and self.board[piece.row + 1][
                piece.col + 1] == 0:  # right
                moves.append([(piece.row, piece.col), (piece.row + 1, piece.col + 1)])
            if piece.row + 1 < self.rows and piece.col - 1 >= 0 and self.board[piece.row + 1][
                piece.col - 1] == 0:  # left
                moves.append([(piece.row, piece.col), (piece.row + 1, piece.col - 1)])
        if piece.king or self.player == 2:  # look moving up
            if piece.row - 1 >= 0 and piece.col + 1 < self.cols and self.board[piece.row - 1][
                piece.col + 1] == 0:  # right
                moves.append([(piece.row, piece.col), (piece.row - 1, piece.col + 1)])
            if piece.row - 1 >= 0 and piece.col - 1 >= 0 and self.board[piece.row - 1][piece.col - 1] == 0:  # left
                moves.append([(piece.row, piece.col), (piece.row - 1, piece.col - 1)])

        # check for capture pieces
        check_capture_list = [(piece.row, piece.col)]
        already_checked = []
        capture_directed_graph = {}
        while len(check_capture_list) != 0:
            row, col = check_capture_list.pop()
            if (row, col) in already_checked:  # we already checked that place
                continue

            new_check = self.can_capture(piece, row, col)
            already_checked.append((row, col))
            check_capture_list.extend(new_check)

            if new_check:
                for new in new_check:
                    copy_graph = dict(capture_directed_graph)
                    if (row, col) not in copy_graph:
                        copy_graph[(row, col)] = []
                    if new in copy_graph[(row, col)]:
                        continue
                    copy_graph[(row, col)].append(new)
                    if not self.cyclic(copy_graph):
                        if (row, col) not in capture_directed_graph:
                            capture_directed_graph[(row, col)] = []
                        capture_directed_graph[(row, col)].append(new)
        dump_value, move_path_dictionary = self.dfs((piece.row, piece.col), [], capture_directed_graph, [])

        ### un-nest the x
        temp_moves = []
        if (piece.row, piece.col) not in move_path_dictionary:
            for y in move_path_dictionary:
                temp_moves.append(self.get_unNested(y))

        if temp_moves != []:
            return (True, temp_moves)
        else:
            return (False, moves)

    def cyclic(self, g):
        # https://codereview.stackexchange.com/questions/86021/check-if-a-directed-graph-contains-a-cycle
        """Return True if the directed graph g has a cycle.
        g must be represented as a dictionary mapping vertices to
        iterables of neighbouring vertices. For example:
        >>> cyclic({1: (2,), 2: (3,), 3: (1,)})
        True
        >>> cyclic({1: (2,), 2: (3,), 3: (4,)})
        False
        """
        path = set()
        visited = set()

        def visit(vertex):
            if vertex in visited:
                return False
            visited.add(vertex)
            path.add(vertex)
            for neighbour in g.get(vertex, ()):
                if neighbour in path or visit(neighbour):
                    return True
            path.remove(vertex)
            return False

        return any(visit(v) for v in g)

    # unnest a nested list [[1,2,3]] -> [1,2,3]
    ### NO LONGER NEED I THINK - NO TEST HAS BEEN DONE
    def get_unNested(self, alist):
        if len(alist) == 1:
            return self.get_unNested(alist[0])
        else:
            return alist

    # checks if it can capture a piece next to it and jump to a empty spot
    def can_capture(self, piece, row, col):
        new_position_placement = []
        if piece.king or self.player == 1:  # look moving down
            if row + 1 < self.rows and col + 1 < self.cols:
                if self.board[row + 1][col + 1] != 0 and self.board[row + 1][
                    col + 1].color != piece.color and self.valid_position(row + 2, col + 2) and self.board[row + 2][
                    col + 2] == 0:
                    new_position_placement.append((row + 2, col + 2))  # right
            if row + 1 < self.rows and col - 1 >= 0:
                if self.board[row + 1][col - 1] != 0 and self.board[row + 1][
                    col - 1].color != piece.color and self.valid_position(row + 2, col - 2) and self.board[row + 2][
                    col - 2] == 0:
                    new_position_placement.append((row + 2, col - 2))  # left
        if piece.king or self.player == 2:  # look moving up
            if row - 1 >= 0 and col + 1 < self.cols:
                if self.board[row - 1][col + 1] != 0 and self.board[row - 1][
                    col + 1].color != piece.color and self.valid_position(row - 2, col + 2) and self.board[row - 2][
                    col + 2] == 0:
                    new_position_placement.append((row - 2, col + 2))  # right
            if row - 1 >= 0 and col - 1 >= 0:
                if self.board[row - 1][col - 1] != 0 and self.board[row - 1][
                    col - 1].color != piece.color and self.valid_position(row - 2, col - 2) and self.board[row - 2][
                    col - 2] == 0:
                    new_position_placement.append((row - 2, col - 2))  # left
        return new_position_placement

    # return all sequence of moves for captures from a graph/tree
    def dfs(self, node, visited, graph, path):
        list_of_paths = []
        if node not in visited:
            if node not in graph or graph[node] == []:
                visited.append(node)
                path.append(node)
                return (True, path)
            else:
                visited.append(node)
                path.append(node)
                for neighbour in graph[node]:
                    is_path, returned_path = self.dfs(neighbour, visited, graph, path.copy())
                    if returned_path != []:
                        if is_path:
                            list_of_paths.append(returned_path)
                        else:
                            list_of_paths.extend(returned_path)
        # temp = self.get_unNested(temp)
        return (False, list_of_paths)

    # handles sequence of moves and capturing
    def make_moves(self, moves):
        cur_row, cur_col = moves[0]
        for new_row, new_col in moves[1:]:
            #print("Moving", self.playerColorShort[self.player], "From", (cur_row, cur_col), "to", (new_row, new_col))
            # move the piece
            self.move(cur_row, cur_col, new_row, new_col)

            # condition check to see if there is piece in the way we have to capture
            if abs(cur_row - new_row) > 1 or abs(cur_col - new_col) > 1:
                mid_row = (new_row + cur_row) // 2
                mid_col = (new_col + cur_col) // 2
                #print("!!! Capturing", (mid_row, mid_col))
                remove_piece = self.board[mid_row][mid_col]
                remove_piece.capture()
                self.board[mid_row][mid_col] = 0
                if self.player == 1:
                    self.player2PiecesCount -= 1
                elif self.player == 2:
                    self.player1PiecesCount -= 1
            cur_row, cur_col = new_row, new_col
        # change turns
        self.change_turn()

    # make move with most captures or first found
    def get_best_move(self, moves):
        best = -1
        best_move = None
        for piece, move in moves.items():
            for sequence in move:
                if len(sequence) > best:
                    best = len(sequence)
                    best_move = sequence
        return best_move

    def get_king_count_for_player(self, player):
        king_count = 0
        if player == 1:
            pieces = self.player1Pieces
        else:
            pieces = self.player2Pieces
        for piece in self.player1Pieces:
            if piece.king:
                king_count += 1
        return king_count

    def count_pieces_on_home_row(self):
        # Return the count of the number of pieces on the home row
        count = 0
        if self.player == 1:
            for pos in self.board[0]:
                if pos != 0:
                    count += 1
        else:
            for pos in self.board[7]:
                if pos != 0:
                    count += 1
        return count

    def get_board_heuristic(self):
        # Return a heuristic of the state of the board for
        # the current player
        # Combination of the difference in the number of pieces and number
        # of kings between the two players
        p1_king_count = self.get_king_count_for_player(1)
        p2_king_count = self.get_king_count_for_player(2)
        pieces_on_home_row = self.count_pieces_on_home_row()
        if self.whose_turn() == 1:
            heuristic = (self.player1PiecesCount - self.player2PiecesCount) + 3 * (p1_king_count - p2_king_count) + pieces_on_home_row
        else:
            heuristic = (self.player2PiecesCount - self.player1PiecesCount) + 3 * (p2_king_count - p1_king_count) + pieces_on_home_row
        return heuristic
