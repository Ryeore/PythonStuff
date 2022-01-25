from copy import deepcopy

BOARD_SIZE = 8


class Board:
    def __init__(self, board=[], currBlack=[], currWhite=[]):
        # if we do not have board, set default
        if not board == []:
            self.board_state = board
        else:
            self.reset_board()
        # member holds a position of every checker in a board
        self.currState = [[], []]
        # if the current blacks state is not empty, then save it in current state[0]
        # else calculate the blacks state
        if not currBlack == []:
            self.currState[0] = currBlack
        else:
            self.currState[0] = self.define_state(0)
        # if the current whites state is not empty, then save it in current state[1]
        if not currWhite == []:
            self.currState[1] = currWhite
        else:
            self.currState[1] = self.define_state(1)

    # initialize board to the default
    def reset_board(self):
        # reset board
        # -1 = empty, 0=black, 1=white
        self.board_state = [
            [-1, 1, -1, 1, -1, 1, -1, 1],
            [1, -1, 1, -1, 1, -1, 1, -1],
            [-1, 1, -1, 1, -1, 1, -1, 1],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1],
            [0, -1, 0, -1, 0, -1, 0, -1],
            [-1, 0, -1, 0, -1, 0, -1, 0],
            [0, -1, 0, -1, 0, -1, 0, -1]
        ]

    # check each position in matrix, return each position occupied by player 0 or 1
    def define_state(self, player):
        state = []
        # analyze each cell on the board, cell by cell
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                # if the current cell is black checker (0) or white checker (1) add to the state list
                if self.board_state[row][col] == player:
                    state.append((row, col))
        return state

    # set all possible moves
    def define_possible_moves(self, player):
        possible_moves = []
        can_jump = False

        # determine which player has move, as well as move direction and board limits
        if player == 0:
            move_dir = -1
            board_end = 0
        else:
            move_dir = 1
            board_end = BOARD_SIZE - 1

        # check each position of checkers of a player (row, col)
        for position in self.currState[player]:
            # if we are at the last row, we cannot go further, no possible moves
            if position[0] == board_end:
                continue

            # consider only if we are not at right edge - right diagonal moves
            if not position[1] == BOARD_SIZE - 1:
                # regular move, one position toward the enemy and to right, if that field is free (= -1)
                # and if we do not have jump possibility
                if self.board_state[position[0] + move_dir][position[1] + 1] == -1 and not can_jump:
                    # create possible move, right diagonal
                    temp_move = Move((position[0], position[1]), (position[0] + move_dir, position[1] + 1))
                    # add this move to possible moves
                    possible_moves.append(temp_move)

                # check if the right diagonal field is occupied by opposite player
                elif self.board_state[position[0] + move_dir][position[1] + 1] == 1 - player:
                    # create a list of possible jump-moves for the current cell (we are going to right)
                    jumps = self.check_jump((position[0], position[1]), False, player)
                    # if we have at least one jump
                    if not len(jumps) == 0:
                        # force to make jump move
                        if not can_jump:
                            can_jump = True
                            possible_moves = []
                        possible_moves.extend(jumps)

            # consider only if we are not at left edge - left diagonal moves
            if not position[1] == 0:
                # regular move, one position toward the enemy and to left, if that field is free (= -1)
                # and if we do not have jump possibility
                if self.board_state[position[0] + move_dir][position[1] - 1] == -1 and not can_jump:
                    # create possible move, left diagonal
                    temp_move = Move((position[0], position[1]), (position[0] + move_dir, position[1] - 1))
                    # add this move to possible moves
                    possible_moves.append(temp_move)

                # check if the left diagonal field is occupied by opposite player
                elif self.board_state[position[0] + move_dir][position[1] - 1] == 1 - player:
                    # check if the left diagonal field is occupied by opposite player
                    jumps = self.check_jump((position[0], position[1]), True, player)
                    # if we have at least one jump
                    if not len(jumps) == 0:
                        # if we not have any other jumps, then force to make this move
                        if not can_jump:
                            can_jump = True
                            possible_moves = []
                        possible_moves.extend(jumps)

        # return the list of all possible moves and jumps
        return possible_moves

    # set all possible jumps
    def check_jump(self, position, is_left, player):
        jumps = []
        # again, set the direction that we are going to move our checkers
        if player == 0:
            move_dir = -1
        else:
            move_dir = 1

        # if we are at the row one before the end, we can't jump forward
        if position[0] + move_dir == 0 or position[0] + move_dir == BOARD_SIZE - 1:
            return jumps

        # check if we are going left diagonal
        if is_left:
            # check if the field that we want to jump to is free (= -1) and is in the board
            if position[1] > 1 and self.board_state[position[0] + move_dir + move_dir][position[1] - 2] == -1:
                # create possible move - jump to diagonal left
                temp = Move(position, (position[0] + move_dir + move_dir, position[1] - 2), True)
                # add the position that we just jumped over to the jumpOver[]
                temp.jump_over = [(position[0] + move_dir, position[1] - 1)]

                # check if we still have rows forward, after jumping
                if temp.end[0] + move_dir > 0:
                    if temp.end[0] + move_dir < BOARD_SIZE - 1:
                        # check if the next possible diagonal field is occupied by the enemy and is in the board
                        if temp.end[1] > 1 and self.board_state[temp.end[0] + move_dir][temp.end[1] - 1] == 1 - player:
                            # check if there is possible jump in the same turn (double jump, to left)
                            double_temp = self.check_jump(temp.end, True, player)
                            # if yes (possible jumps not empty)
                            if not double_temp == []:
                                dbl_temp = deepcopy(temp)
                                # create possible move - double jump
                                dbl_temp.end = double_temp[0].end
                                # add the position that we just jumped over to the jumpOver[]
                                dbl_temp.jump_over.extend(double_temp[0].jump_over)
                                # add this double jump to the possible jumps
                                jumps.append(dbl_temp)

                        # check if the next possible diagonal field is occupied by the enemy and is in the board
                        if temp.end[1] < BOARD_SIZE - 2 and self.board_state[temp.end[0] + move_dir][temp.end[1] + 1] == 1 - player:
                            # check if there is possible jump in the same turn (double jump, to right)
                            double_temp = self.check_jump(temp.end, False, player)
                            # if yes (possible jumps not empty)
                            if not double_temp == []:
                                dbl_temp = deepcopy(temp)
                                # create possible move - double jump
                                dbl_temp.end = double_temp[0].end
                                # add the position that we just jumped over to the jumpOver[]
                                dbl_temp.jump_over.extend(double_temp[0].jump_over)
                                # add this double jump to the possible jumps
                                jumps.append(dbl_temp)
                # add single jump to the possible jumps
                jumps.append(temp)

        # we are going to the right edge
        else:
            # check if the field that we want to jump to is free (= -1) and is in the board
            if position[1] < BOARD_SIZE - 2 and self.board_state[position[0] + move_dir + move_dir][position[1] + 2] == -1:
                # create possible move - jump to diagonal right
                temp = Move(position, (position[0] + move_dir + move_dir, position[1] + 2), True)
                # add the position that we just jumped over to the jumpOver[]
                temp.jump_over = [(position[0] + move_dir, position[1] + 1)]

                # check if we still have rows forward, after jumping
                if temp.end[0] + move_dir > 0 and temp.end[0] + move_dir < BOARD_SIZE - 1:
                        # check if the move_dir possible jump field is occupied by the enemy and in the board
                        if temp.end[1] > 1 and self.board_state[temp.end[0] + move_dir][temp.end[1] - 1] == 1 - player:
                            # check if there is possible jump in the same turn (double jump, to left)
                            double_temp = self.check_jump(temp.end, True, player)
                            # if yes (possible jumps not empty)
                            if not double_temp == []:
                                dbl_temp = deepcopy(temp)
                                # create possible move - double jump
                                dbl_temp.end = double_temp[0].end
                                # add the position that we just jumped over to the jumpOver[]
                                dbl_temp.jump_over.extend(double_temp[0].jump_over)
                                # add this double jump to the possible jumps
                                jumps.append(dbl_temp)

                        # check if the move_dir possible jump field is occupied by the enemy and in the board
                        if temp.end[1] < BOARD_SIZE - 2 and self.board_state[temp.end[0] + move_dir][temp.end[1] + 1] == 1 - player:
                            # check if there is possible jump in the same turn (double jump, to right)
                            double_temp = self.check_jump(temp.end, False, player)
                            # if yes (possible jumps not empty)
                            if not double_temp == []:
                                dbl_temp = deepcopy(temp)
                                # create possible move - double jump
                                dbl_temp.end = double_temp[0].end
                                # add the position that we just jumped over to the jumpOver[]
                                dbl_temp.jump_over.extend(double_temp[0].jump_over)
                                # add this double jump to the possible jumps
                                jumps.append(dbl_temp)
                # add single jump to the possible jumps
                jumps.append(temp)
        # return the list of possible jumps
        return jumps

    # print the board
    def print_board_state(self):
        # print the number of column
        for col_num in range(BOARD_SIZE):
            print(str(col_num) + " ", end="")
        print("")
        # for each position print the B - black, W - white or _ - empty cell
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board_state[row][col] == -1:
                    print("_ ", end='')
                elif self.board_state[row][col] == 1:
                    print("W ", end='')
                elif self.board_state[row][col] == 0:
                    print("B ", end='')
            # print the number of row
            print(str(row))

    # update the state of the board after move
    def move_on_board(self, move_info, currPlayer):
        # prepare the info about the move picked by a player
        move = [move_info.start, move_info.end]
        jump = move_info.jump

        # make the old cell empty
        self.board_state[move[0][0]][move[0][1]] = -1
        # set the cell state that the player moved to
        self.board_state[move[1][0]][move[1][1]] = currPlayer
        # if the move was jump
        if jump:
            # remove the opponent's checkers
            for enemy in move_info.jump_over:
                self.board_state[enemy[0]][enemy[1]] = -1
            # update the current state of the board
        if jump:
            self.currState[0] = self.define_state(0)
            self.currState[1] = self.define_state(1)
        # update the current state of the board
        else:
            self.currState[currPlayer].remove((move[0][0], move[0][1]))
            self.currState[currPlayer].append((move[1][0], move[1][1]))


# class that defines possible move
class Move:
    def __init__(self, start, end, jump=False):
        self.start = start
        self.end = end
        self.jump = jump
        self.jump_over = []
