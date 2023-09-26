#when you do hardwork you can always question god


#
# MCTS algorithm implementation
#selectiom , expandsion, simulation and backup
print('enter level')
level = int(input())
while True:
# packages
    import math
    import random
    print('level:' , level)

# tree node class defination
    class TreeNode():
        def __init__(self, board, parent):
            self.board = board

            # is node terminal (flag)
            if self.board.is_win() or self.board.is_draw():
                self.is_terminal = True
            else:
                self.is_terminal = False

            # set is fully expanded flag that means all the children it has is created in MCTS it is not done in ana instant
            self.is_fully_expanded = self.is_terminal
            # init parent node if available
            self.parent = parent

            # init the number of node visits
            self.visits = 0

            # init the total score of node
            self.score = 0
            # init current node's children
            self.children = {}

    class MCTS():
        # search for best move in current position
        def search(self, initial_state):
            # initial state is current state
            self.root = TreeNode(initial_state, None)

            # walk through iteration
            for iteration in range(level):
                # select a node
                node = self.select(self.root)
                # if node is not then we have to expand it
                # score of current node (simulation process)

                score = self.rollout(node.board)

                # rollout is a mcts  term two types of rollout light(random) and heavy (calculations are done)

                # backpropogate number of visits upto the root node

                self.backpropagate(node, score)

            # pick up the best move in the current position
            try:
                return self.get_best_move(self.root, 0)
            except:
                pass

        # select most promising node
        def select(self, node):
            # make sure that we 're dealing with non terminal nodes
            while not node.is_terminal:
                # case where the node is fully expanded
                if node.is_fully_expanded:
                    node = self.get_best_move(node, 2)

                #case where the node is not fully expanded
                else:
                    # otherwise expand the node
                    return self.expand(node)

            return node

        def expand(self, node):
            # generate legal states(moves) for the given node
            states = node.board.generate_states()
            # loop over generated states(moves)
            for state in states:
                # make sure current move is not present in child nodes
                if str(state.position) not in node.children:
                    print(str(state.position))
                    new_node = TreeNode(state, node)

                    node.children[str(state.position)] = new_node

                    if len(states) == len(node.children):
                        node.is_fully_expanded = True

                    # return newly created node
                    return new_node

            # debugging
            print('should not get here!!!')
        # simulate the game by making random moves until reach end of the game
        def rollout(self, board):
            # make randon moves for both sides until terminal state of game is reached
            while not board.is_win():
                try:
                    board = random.choice(board.generate_states())
                # no moves available
                except:
                    # return a draw score
                    return 0

            # return score from player 'x' perspective
            if board.player_2 == 'x':
                return 1
            elif board.player_2 == 'o':
                return -1

        # backpropgates the number of visits and score upto root node
        def backpropagate(self, node, score):
            # update node'svist count and score upto the root node
            while node is not None:
                # update node's visits
                node.visits += 1

                node.score += score

                node = node.parent



        # select the best node basing on ucb1 formula
        def get_best_move(self, node, exploration_constant):
           # define best score and best moves
            best_score = float('-inf')
            best_moves = []
            # loop over child nodes
            for child_node in node.children.values():

                # define current player
                if child_node.board.player_2 == 'x':
                    current_player = 1
                elif child_node.board.player_2 == 'o':
                    current_player = -1
                # formula
                move_score = current_player * child_node.score / child_node.visits + exploration_constant * math.sqrt(math.log(node.visits / child_node.visits))
                # better move has been found
                if move_score > best_score:
                    best_score = move_score
                    best_moves = [child_node]
                # found as good move as already available
                elif move_score == best_score:
                    best_moves.append(child_node)
                # return one of the best moves randomly
            return random.choice(best_moves)

    #
    #AI that learns to play Tic Tac Toe using
    #        reinforcement learning
    #            (MCTS + NN)

    #  Packages
    from copy import deepcopy
    #reason :  we would be copying the instance of entire board class  incase we need to generate a node for our opponent

    # Toc Tac Toe board class
    class Board():
        # create  constructor (inti board class instance)
        def __init__(self , board =None):
            #define Players
            self.player_1 = 'x'
            self.player_2 = 'o'
            self.empty_square = '_'

            #define board position
            self.position = {}

            # init (reset) board
            self.init_board()
            # create a copy of previous board state if available
            if board:
                self.__dict__ = deepcopy(board.__dict__)
                #__dict__ is a hack used to get all the internal field of a given class

        # init(reset) board
        def init_board(self):
            #loop over board rows
            for row in range(3):
                #loop over board columns
                for col in range(3):
                    self.position[row, col] = self.empty_square
        # make move
        def make_move(self, row, col):
            # create new board instance
            board = Board(self)
            # make move
            board.position[row, col] = self.player_1

            # swap players
            board.player_1, board.player_2 = board.player_2, board.player_1
            # return new board state
            return board

        # whether the game is drawn
        def is_draw(self):
            # loop over board squares
            for row, col in self.position:
                # empty square is available
                if self.position[row, col] == self.empty_square:
                    # this is not a draw
                    return False
            return True

        # wheather win
        def is_win(self):
            ###################################
            # vertical sequence detection
            ###################################
            for col in range(3):
                winning_sequence = []
                for row in range(3):
                    if self.position[row, col] == self.player_2:
                        #update winnig sequence
                        winning_sequence.append((row, col))
                    # if we have 3 element in athe row
                    if len(winning_sequence) == 3:
                        # game is won
                        return True
            ###################################
            # horizontal sequence detection
            ###################################
            for row in range(3):
                winning_sequence = []
                for col in range(3):
                    if self.position[row, col] == self.player_2:
                        #update winnig sequence
                        winning_sequence.append((row, col))
                    # if we have 3 element in athe row
                    if len(winning_sequence) == 3:
                        # game is won
                        return True
            ###################################
            # 1st diagonal sequence detection
            ###################################
            winning_sequence = []
            for col in range(3):
                row = col
                if self.position[row, col] == self.player_2:
                    # update winnig sequence
                    winning_sequence.append((row, col))
                # if we have 3 element in athe row
                if len(winning_sequence) == 3:
                    # game is won
                    return True
            ###################################
            # 2nd diagonal sequence detection
            ###################################
            winning_sequence = []
            for col in range(3):
                row = 2 - col
                if self.position[row, col] == self.player_2:
                    # update winnig sequence
                    winning_sequence.append((row, col))
                # if we have 3 element in athe row
                if len(winning_sequence) == 3:
                    # game is won
                    return True
            return False

        def generate_states(self):
            actions = []
            for row in range(3):
                for col in range(3):
                    if self.position[row, col] == self.empty_square:
                        actions.append(self.make_move(row, col))
            # list is necesssary for MCTS
            return actions

        def game_loop(self):
            global level
            print('   \n Tic Tac toe')
            print('type exit to quit the game')
            print('   enter move like: 1,1 for format [x][y]')
            # print(board)
            print(self)
            mcts = MCTS()
            #game loop
            while True:
                #get user input
                user_input = input('> ')
                if user_input == 'exit':
                    exit()
                if user_input == '':
                    continue
                try:
                    row = int(user_input.split(',')[0])  -1
                    col = int(user_input.split(',')[1]) -1
                    if self.position[row, col] != self.empty_square:
                        print(' Illegal move!')
                        continue
                    self = self.make_move(row, col)
                    print(self)

                    best_move = mcts.search(self)

                    # make AI move here
                    try:
                        self = best_move.board
                    except:
                        pass

                    # print board
                    print(self)
                    if self.is_win():
                        print('\n player "%s" has won the game!' % self.player_2)
                        if self.player_2 == 'o':
                            level -= 1
                        break
                    elif self.is_draw():
                        level -= 1
                        print('Game is Draw')
                        break
                except Expectation as e:
                    print('Error:', e)
                    print('illegal command!')
                    print(' Move format[x, y]: 1,2 wher 1 is column and 2 is row')
        # print board state
        def __str__(self):
            # is another hack of python
            # define board string representation
            board_string = ''
            # loop over board rows
            for row in range(3):
                # loop over board columns
                for col in range(3):
                    board_string += ' %s' % self.position[row, col]
                    #print new line every row
                board_string +='\n'
                #prepend side to move
            if self.player_1 == 'x':
                board_string = '\n\n-------------\n"x" to move\n------------\n\n' + board_string
            elif self.player_1 == 'o':
                board_string = '\n\n-------------\n"o" to move\n------------\n\n' + board_string
            # return board_string
            return board_string
    # main driver
    board = Board()
    mcts = MCTS()
    board.game_loop()
    level +=1


























































