from board import *
import time

# the starting number of checkers for each player
CHECKERS = 12
PLAYERS = ["Black", "White"]
DEPTH_LIMIT = 5


class Game:
    def __init__(self, player=0):
        # initialize the board for the game
        self.board = Board()
        # number of checkers that are still on the board (for white and for black)
        self.checkers = [CHECKERS, CHECKERS]
        # initialize player (black or white)
        self.player = player
        # initialize whose turn is now
        self.turn = 0

    def run(self):
        total_time = 0
        total_comp_round = 0
        # check if the game is not ended after each turn
        while not self.game_over(self.board):
            # print the current state of the board
            self.board.print_board_state()
            # print the current player
            print("Turn: " + PLAYERS[self.turn])

            # if it is a turn of a player
            if self.turn == self.player:
                # list all possible moves
                possible_moves = self.board.define_possible_moves(self.turn)
                # check if a player can make a move
                if len(possible_moves) > 0:
                    move = self.choose_move(possible_moves)
                    self.make_move(move)
                else:
                    print("You are blocked, skipping turn!")

                # uncomment for computer vs computer
                '''
                # list all possible moves
                possible_moves = self.board.define_possible_moves(self.turn)

                # check if there are possible moves(move)
                if len(possible_moves) > 0:
                    if len(possible_moves) == 1:
                        choice = possible_moves[0]
                    else:
                        # we generate computer choice for current turn and board state
                        state = ComputerChoice(self.board, self.turn, self.turn)
                        # choice = self.alpha_beta(state)
                        choice = self.min_max(state)
                    self.make_move(choice)
                    print("Computer chooses (" + str(choice.start) + ", " + str(choice.end) + ")")
                '''

            # if it is a turn of a computer
            else:
                # list all possible moves
                possible_moves = self.board.define_possible_moves(self.turn)
                # print all possible moves
                '''
                print("Available moves: ")
                for i in range(len(possible_moves)):
                    print(str(i + 1) + ": ", end='')
                    print(str(possible_moves[i].start) + " " + str(possible_moves[i].end))
                '''

                # check if there are possible moves(move)
                if len(possible_moves) > 0:
                    start_time = time.time()
                    if len(possible_moves) == 1:
                        choice = possible_moves[0]
                    else:
                        # we generate computer choice for current turn and board state
                        state = ComputerChoice(self.board, self.turn, self.turn)
                        # choice = self.alpha_beta(state)
                        choice = self.min_max(state)
                    self.make_move(choice)
                    total_time += time.time() - start_time
                    total_comp_round += 1

                    print("Computer chooses (" + str(choice.start) + ", " + str(choice.end) + ")")

            # switch player after move
            self.turn = 1 - self.turn

        print("GAME OVER!")
        print("Total computer moves time: " + str(total_time))
        print("Average computer move time: " + str(total_time / total_comp_round))
        print("Black captured: " + str(CHECKERS - self.checkers[1]))
        print("White captured: " + str(CHECKERS - self.checkers[0]))
        score = self.define_score(self.board)
        print("Black score: " + str(score[0]))
        print("White score: " + str(score[1]))
        if score[0] > score[1]:
            print("Black wins!")
        elif score[0] < score[1]:
            print("White wins!")
        else:
            print("Draw!")
        self.board.print_board_state()

    # tests if the game is already over
    def game_over(self, board):
        # check if there is no more black or white checker
        if len(board.currState[0]) == 0 or len(board.currState[1]) == 0:
            return True
        # check if any player can move
        elif len(board.define_possible_moves(0)) == 0 and len(board.define_possible_moves(1)) == 0:
            return True
        # else the game is not ended
        else:
            return False

    # user selects the move
    def choose_move(self, possible_moves):
        move = -1
        # try until user choose legal move
        while move not in range(len(possible_moves)):
            print("Available moves: ")
            # print all available moves
            for i in range(len(possible_moves)):
                print(str(i + 1) + ": ", end='')
                print(str(possible_moves[i].start) + " " + str(possible_moves[i].end))

            usr_input = input("Pick a move number: ")
            # prompt user input until he picks valid and legal input
            if usr_input == '':
                move = -1
            else:
                move = int(usr_input) - 1

            if move not in range(len(possible_moves)):
                print("Illegal move!")

        return possible_moves[move]

    # make a move chosen by a player
    def make_move(self, move):
        # make a move on the board
        self.board.move_on_board(move, self.turn)

        # if the move was a jump
        if move.jump:
            # decrement remaining checkers from an opponent counter
            self.checkers[1 - self.turn] -= len(move.jump_over)
            # print the current number of checkers removed for a opponent player
            print("Removed: " + str(len(move.jump_over)) + " " + PLAYERS[1 - self.turn] + " pieces.")

    # starts min max algorithm with alpha beta pruning
    def alpha_beta(self, state):
        result = self.max_value(state, -999, 999, 0)
        return result.move

    # starts min max algorithm
    def min_max(self, state):
        result = self.max_value_no_ab(state, 0)
        return result.move

    # returns the best maximizing move
    def max_value(self, comp_state, alpha, beta, node):
        # find all possible moves
        possible_moves = comp_state.board_state.define_possible_moves(comp_state.player)
        # we generate a computer move, with the current move value and information about this move
        # (move_value, move, max_depth, total_nodes, max_cutoff, min_cutoff)
        move = ComputerMoveInfo(-999, None, node, 1, 0, 0)

        # if we are at the last possible node depth, then just return move with value for this state
        if node == DEPTH_LIMIT:
            # move.move_value = self.eval_jump(comp_state.player)
            move.move_value = self.eval_deff(comp_state.board_state, comp_state.origPlayer)
            return move

        # if we do not have any possible move in a given state
        if len(possible_moves) == 0:
            # then we calculate score for the current board state
            score = self.define_score(comp_state.board_state)
            # if the score of a player calling this function is bigger than opponent's
            if score[comp_state.origPlayer] > score[1 - comp_state.origPlayer]:
                # then define move value as 100 + 2 * player's score - opponent's score
                move.move_value = 100 + 2 * score[comp_state.origPlayer] - score[1 - comp_state.origPlayer]
            else:
                # else define move value as -100 + 2 * player's score - opponent's score
                move.move_value = -100 + 2 * score[comp_state.origPlayer] - score[1 - comp_state.origPlayer]
            # return current move and its value
            return move

        # now we should consider every possible move
        for move_choice in possible_moves:
            # now create new computer choice object, with current state, change maximizing player to minimizing player
            # and save original function caller
            new_state = ComputerChoice(deepcopy(comp_state.board_state), 1 - comp_state.player, comp_state.origPlayer)
            # change a state on the (copy) board with the current move
            new_state.board_state.move_on_board(move_choice, comp_state.player)
            # call the minimizing function (as we switched to minimizing player) and find the new move path, with
            # node + 1
            new_move = self.min_value(new_state, alpha, beta, node + 1)

            # increase node depth value if it is bigger for the new move than from original move
            if new_move.max_depth > move.max_depth:
                move.max_depth = new_move.max_depth
            # increase number of nodes and values of cutoffs by the new move values
            move.max_cutoff += new_move.max_cutoff
            move.min_cutoff += new_move.min_cutoff

            move.nodes += new_move.nodes

            # if the new move value is bigger than current move value
            if new_move.move_value > move.move_value:
                # update move and move value
                move.move_value = new_move.move_value
                move.move = move_choice

            # if the value of the current move is bigger or equal than current beta (min) value
            if move.move_value >= beta:
                # then we should stop considering that branch
                move.max_cutoff += 1
                return move
            # if current move's value is bigger than alpha (max) value then update alpha value
            if move.move_value > alpha:
                alpha = move.move_value

        # return the best maximizing move
        return move

    # returns the best minimizing move
    def min_value(self, comp_state, alpha, beta, node):
        # find all possible moves
        possible_moves = comp_state.board_state.define_possible_moves(comp_state.player)
        # we generate a computer move, with the current move value and information about this move
        # (move_value, move, max_depth, total_nodes, max_cutoff, min_cutoff)
        move = ComputerMoveInfo(999, None, node, 1, 0, 0)

        # if we are at the last possible node depth, then just return move with value for this state
        if node == DEPTH_LIMIT:
            # move.move_value = self.eval_jump(comp_state.player)
            move.move_value = self.eval_deff(comp_state.board_state, comp_state.origPlayer)
            return move

        # if we do not have any possible move in a given state
        if len(possible_moves) == 0:
            # then we calculate score for the current board state
            score = self.define_score(comp_state.board_state)
            # if the score of a player calling this function is bigger than opponent's
            if score[comp_state.origPlayer] > score[1 - comp_state.origPlayer]:
                # then define move value as 100 + 2 * player's score - opponent's score
                move.move_value = 100 + 2 * score[comp_state.origPlayer] - score[1 - comp_state.origPlayer]
            else:
                # else define move value as -100 + 2 * player's score - opponent's score
                move.move_value = -100 + 2 * score[comp_state.origPlayer] - score[1 - comp_state.origPlayer]
            # return current move and its value
            return move

        # now we should consider every possible move
        for move_choice in possible_moves:
            # now create new computer choice object, with current state, change maximizing player to minimizing player
            # and save original function caller
            new_state = ComputerChoice(deepcopy(comp_state.board_state), 1 - comp_state.player, comp_state.origPlayer)
            # change a state on the (copy) board with the current move
            new_state.board_state.move_on_board(move_choice, comp_state.player)
            # call the maximizing function (as we switched to maximizing player) and find the new move path, with
            # node + 1
            new_move = self.max_value(new_state, alpha, beta, node + 1)

            # increase node depth value if it is bigger for the new move than from original move
            if new_move.max_depth > move.max_depth:
                move.max_depth = new_move.max_depth
            # increase number of nodes and values of cutoffs by the new move values
            move.max_cutoff += new_move.max_cutoff
            move.min_cutoff += new_move.min_cutoff

            move.nodes += new_move.nodes

            # if the new move value is smaller than current move value
            if new_move.move_value < move.move_value:
                # update move and move value
                move.move_value = new_move.move_value
                move.move = move_choice

            # if the value of the current move is smaller or equal than current alpha (max) value
            if move.move_value <= alpha:
                # then we should stop considering that branch
                move.min_cutoff += 1
                return move
            # if current move's value is lower than beta (min) value then update beta value
            if move.move_value < beta:
                beta = move.move_value

        # return the best minimizing move
        return move

    # returns the best maximizing move without alpha beta pruning
    def max_value_no_ab(self, comp_state, node):
        # find all possible moves
        possible_moves = comp_state.board_state.define_possible_moves(comp_state.player)
        # we generate a computer move, with the current move value and information about this move
        # (move_value, move, max_depth, total_nodes, max_cutoff, min_cutoff)
        move = ComputerMoveInfo(-999, None, node, 1, 0, 0)

        # if we are at the last possible node depth, then just return move with value for this state
        if node == DEPTH_LIMIT:
            # move.move_value = self.eval_jump(comp_state.player)
            move.move_value = self.eval_deff(comp_state.board_state, comp_state.origPlayer)
            return move

        # if we do not have any possible move in a given state
        if len(possible_moves) == 0:
            # then we calculate score for the current board state
            score = self.define_score(comp_state.board_state)
            # if the score of a player calling this function is bigger than opponent's
            if score[comp_state.origPlayer] > score[1 - comp_state.origPlayer]:
                # then define move value as 100 + 2 * player's score - opponent's score
                move.move_value = 100 + 2 * score[comp_state.origPlayer] - score[1 - comp_state.origPlayer]
            else:
                # else define move value as -100 + 2 * player's score - opponent's score
                move.move_value = -100 + 2 * score[comp_state.origPlayer] - score[1 - comp_state.origPlayer]
            # return current move and its value
            return move

        # now we should consider every possible move
        for move_choice in possible_moves:
            # now create new computer choice object, with current state, change maximizing player to minimizing player
            # and save original function caller
            new_state = ComputerChoice(deepcopy(comp_state.board_state), 1 - comp_state.player, comp_state.origPlayer)
            # change a state on the (copy) board with the current move
            new_state.board_state.move_on_board(move_choice, comp_state.player)
            # call the minimizing function (as we switched to minimizing player) and find the new move path, with
            # node + 1
            new_move = self.min_value_no_ab(new_state, node + 1)

            # increase number of nodes
            move.nodes += new_move.nodes

            # if the new move value is bigger than current move value
            if new_move.move_value > move.move_value:
                # update move and move value
                move.move_value = new_move.move_value
                move.move = move_choice

        # return the best maximizing move
        return move

    # returns the best minimizing move without alpha-beta pruning
    def min_value_no_ab(self, comp_state, node):
        # find all possible moves
        possible_moves = comp_state.board_state.define_possible_moves(comp_state.player)
        # we generate a computer move, with the current move value and information about this move
        # (move_value, move, max_depth, total_nodes, max_cutoff, min_cutoff)
        move = ComputerMoveInfo(999, None, node, 1, 0, 0)

        # if we are at the last possible node depth, then just return move with value for this state
        if node == DEPTH_LIMIT:
            # move.move_value = self.eval_jump(comp_state.player)
            move.move_value = self.eval_deff(comp_state.board_state, comp_state.origPlayer)
            return move

        # if we do not have any possible move in a given state
        if len(possible_moves) == 0:
            # then we calculate score for the current board state
            score = self.define_score(comp_state.board_state)
            # if the score of a player calling this function is bigger than opponent's
            if score[comp_state.origPlayer] > score[1 - comp_state.origPlayer]:
                # then define move value as 100 + 2 * player's score - opponent's score
                move.move_value = 100 + 2 * score[comp_state.origPlayer] - score[1 - comp_state.origPlayer]
            else:
                # else define move value as -100 + 2 * player's score - opponent's score
                move.move_value = -100 + 2 * score[comp_state.origPlayer] - score[1 - comp_state.origPlayer]
            # return current move and its value
            return move

        # now we should consider every possible move
        for move_choice in possible_moves:
            # now create new computer choice object, with current state, change maximizing player to minimizing player
            # and save original function caller
            new_state = ComputerChoice(deepcopy(comp_state.board_state), 1 - comp_state.player, comp_state.origPlayer)
            # change a state on the (copy) board with the current move
            new_state.board_state.move_on_board(move_choice, comp_state.player)
            # call the maximizing function (as we switched to maximizing player) and find the new move path, with
            # node + 1
            new_move = self.max_value_no_ab(new_state, node + 1)

            # increase number of nodes
            move.nodes += new_move.nodes

            # if the new move value is smaller than current move value
            if new_move.move_value < move.move_value:
                # update move and move value
                move.move_value = new_move.move_value
                move.move = move_choice

        # return the best minimizing move
        return move

    # returns value of the possible move
    def eval_deff(self, board, currPlayer):
        # we define three situations for checkers of each player:
        # checkers at owns end, checker's at the opponent's half and at own half
        b_end, b_sec_half, b_fst_half = 0, 0, 0
        w_end, w_sec_half, w_fst_half = 0, 0, 0

        # we are scanning every player1's checkers position
        for position in range(len(board.currState[0])):
            # calculate every checker at enemy's end
            if board.currState[0][position][0] == 0:
                b_end += 1
            # calculate every checker at first half
            elif BOARD_SIZE / 2 <= board.currState[0][position][0] < BOARD_SIZE:
                b_fst_half += 1
            # calculate every checker at second half
            else:
                b_sec_half += 1

        # we are scanning every player2's checkers position
        for position in range(len(board.currState[1])):
            # calculate every checker at enemy's end
            if board.currState[1][position][0] == BOARD_SIZE - 1:
                w_end += 1
            # calculate every checker at first half
            elif 0 <= board.currState[1][position][0] < BOARD_SIZE / 2:
                w_fst_half += 1
            # calculate every checker at second half
            else:
                w_sec_half += 1

        # apply weights of each position and sum score
        w_score = 15 * w_end + 10 * w_fst_half + 5 * w_sec_half
        b_score = 15 * b_end + 10 * b_fst_half + 5 * b_sec_half

        # return the result as score of the player - score of the opponent
        if currPlayer == 0:
            return b_score - w_score
        else:
            return w_score - b_score

    # returns value of the possible move
    def eval_jump(self, currPlayer):
        score = 0
        # calculate score as a number of checkers captured by us * 2 - number of checkers lost
        if currPlayer == 0:
            score = 2 * self.checkers[0] - self.checkers[1]
        elif currPlayer == 1:
            score = 2 * self.checkers[1] - self.checkers[0]
        return score

    # returns value of the possible move
    def eval_attack(self, board, currPlayer):
        # we define three situations for checkers of each player:
        # checkers at opponent's end, checker's at the opponent's half and at own half
        b_end, b_sec_half, b_fst_half = 0, 0, 0
        w_end, w_sec_half, w_fst_half = 0, 0, 0

        # we are scanning every player1's checkers position
        for position in range(len(board.currState[0])):
            # calculate every checker at enemy's end
            if board.currState[0][position][0] == BOARD_SIZE - 1:
                b_end += 1
            # calculate every checker at first half
            elif BOARD_SIZE / 2 <= board.currState[0][position][0] < BOARD_SIZE:
                b_fst_half += 1
            # calculate every checker at second half
            else:
                b_sec_half += 1

        # we are scanning every player2's checkers position
        for position in range(len(board.currState[1])):
            # calculate every checker at enemy's end
            if board.currState[1][position][0] == 0:
                w_end += 1
            # calculate every checker at first half
            elif 0 <= board.currState[1][position][0] < BOARD_SIZE / 2:
                w_fst_half += 1
            # calculate every checker at second half
            else:
                w_sec_half += 1

        # apply weights of each position and sum score
        w_score = 15 * w_end + 10 * w_fst_half + 5 * w_sec_half
        b_score = 15 * b_end + 10 * b_fst_half + 5 * b_sec_half

        # return the result as score of the player - score of the opponent
        if currPlayer == 0:
            return b_score - w_score
        else:
            return w_score - b_score

    def define_score(self, board):
        score = [0, 0]
        # black pieces
        for cell in range(len(board.currState[0])):
            # black pieces at end of board - 2 pts
            if board.currState[0][cell][0] == 0:
                score[0] += 2
            # black pieces not at end - 1 pt
            else:
                score[0] += 1
        # white pieces
        for cell in range(len(board.currState[1])):
            # white pieces at end of board - 2 pts
            if board.currState[1][cell][0] == BOARD_SIZE - 1:
                score[1] += 2
            # white pieces not at end - 1 pt
            else:
                score[1] += 1

        # add to the score the number of checkers captured by a player
        score[0] += 2 * (CHECKERS - self.checkers[1])
        score[1] += 2 * (CHECKERS - self.checkers[0])
        return score


# the class keeps info about current state in a game for computer choice
class ComputerChoice:
    def __init__(self, boardState, currPlayer, originalPlayer):
        self.board_state = boardState
        self.player = currPlayer
        self.origPlayer = originalPlayer


# the class keeps info about possible move
class ComputerMoveInfo:
    def __init__(self, move_value, move, max_depth, child_nodes, max_cutoff, min_cutoff):
        self.move_value = move_value
        self.move = move
        self.max_depth = max_depth
        self.nodes = child_nodes
        self.max_cutoff = max_cutoff
        self.min_cutoff = min_cutoff