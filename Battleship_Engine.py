"""
The engine for the battleship game, needs to be imported by the Battleship_gui program.

@author: Musa Kwong (mak66)
@author: Landon Faber (lrf24)
@date: Fall, 2022
"""

from random import randint


class Game_Engine:

    def __init__(self, grid):
        #initializes empty arrays to hold the gamestate
        self.enemy_board = []
        self.player_board = []
        self.enemy_shots = []
        self.player_shots = []
        self.enemy_ships = []
        self.player_ships = []
        self.shot_report = ''
        self.hit_report = ''
        self.sunk_report = []
        self.previously_sunken_ships = []
        self.player_sunken_ships = []
        self.sunk_num = 0
        self.valid_directions = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        self.creep = 2
        for i in range(grid):
            self.enemy_board.append([])
            self.player_board.append([])
            self.enemy_shots.append([])
            self.player_shots.append([])

        for x in range(7):
            for y in range(7):
                self.enemy_board[x].append(0)
                self.player_board[x].append(0)
                self.enemy_shots[x].append(0)
                self.player_shots[x].append(0)
        self.determine_enemy_ships()

    def make_shot(self, x, y, board):
        '''[Musa] Makes a shot onto a given board, updating the location fired at, the hit result, and the ships already sunk. [Edit by Landon] Returns a "Hit" or a "Miss" for enemy_ai processing '''
        ships = ["Destroyer(2)", "Submarine(3)", "Cruiser(3)", "Battleship(4)"]
        self.shot_report = (f'Shot made at ({x+1},{y+1})')
        self.hit_report = "Miss"
        shot_result = 'Miss'
        if board[x][y] != 0:
            self.hit_report = f'Hit the {ships[board[x][y]-1]}'
            board[x][y] = 0
            shot_result = 'Hit'
        self.sunk_report = self.check_ships(board)
        return (shot_result)

    def check_ships(self, board):
        '''[Musa] Scans through the given board and returns a list of the sunken ships'''
        ships = [0, 0, 0, 0]
        list_ships = [
            "Destroyer(2)", "Submarine(3)", "Cruiser(3)", "Battleship(4)"
        ]
        sunken = []
        if board == self.player_board:
            sunken_list = self.player_sunken_ships
        else:
            sunken_list = self.previously_sunken_ships
        for x in board:
            for y in x:
                for i in range(1, 5):
                    if y == i:
                        ships[i - 1] += 1
        for i in range(len(ships)):
            if ships[i] == 0 and list_ships[i] not in sunken_list:
                sunken_list.append(list_ships[i])
        return (sunken_list)

    def populate_board(self, board, x, y, orientation, length, type):
        '''[Musa] Populates a given board with ship chunks based on the type, length of the ship, and starting coordinates'''
        if orientation == 'h':
            for i in range(length):
                #print(str(x+i) + ', '+ str(y))
                board[x + i][y] = type
        if orientation == 'v':
            for i in range(length):
                #print(str(x) +', '+ str(y+i))
                board[x][y + i] = type

    def randomize_ships(self, board):
        '''[Musa] Creates a random arrangement of ships on a given board, returns a list of ships for the gui constructor. Earlier version of function by [Landon]'''
        num_of_ships = 1
        ship_list = []
        while num_of_ships < 5:
            x_mult = 0
            y_mult = 0
            o = randint(0, 1)
            displacement = num_of_ships
            if num_of_ships <= 2:
                displacement += 1
            if o == 0:
                orientation = 'h'
                x_mult = 1
            if o == 1:
                orientation = 'v'
                y_mult = 1
            coord1 = randint(0, 6 - (x_mult * displacement))
            coord2 = randint(0, 6 - (y_mult * displacement))
            space = True
            for i in range(displacement):
                if board[coord1 + (x_mult * i)][coord2 + (y_mult * i)] != 0:
                    space = False
            if space != False:
                self.populate_board(board, coord1, coord2, orientation,
                                    displacement, num_of_ships)
                ship_list.append([coord1, coord2, displacement, orientation])
                num_of_ships += 1
        return ship_list

    def determine_enemy_ships(self):
        '''[Musa] Calls the randomize ship function on the enemy board'''
        self.enemy_ships = self.randomize_ships(self.enemy_board)

    def get_board(self, board):
        '''[Musa] prints the given board into the console'''
        for x in board:
            print(x)

    def determine_player_ships(self, choice):
        '''[Musa] Randomizes the player ships as long as the input is false'''
        if choice == False:
            self.player_ships = self.randomize_ships(self.player_board)

    def make_enemy_shot(self, difficulty):
        '''[Musa] Makes a shot for the enemy, if difficulty is False, makes a random, non-repeating shot on the board, if difficulty is True, makes a more calculated shot given board data. Note: Earlier iterations of the advanced shooting was done by [Landon].'''
        shot = False
        if difficulty == True:
            directions = [[-1, 0], [0, -1], [1, 0], [0, 1]]
            while True:
                shot = False
                for x in range(7):
                    for y in range(7):
                        if self.enemy_shots[x][y] > 1:
                            #If a given point is a ship chunk, looks around the point of interest
                            if len(self.valid_directions) == 1:
                                #If there is a valid direction, shoots in that direction
                                xo = y + self.valid_directions[0] * self.creep
                                yo = y + self.valid_directions[1] * self.creep
                                self.creep += 1
                                s = False
                                for b in range(2):
                                    if 0 <= xo <= 6 and 0 < (yo) < 6:
                                        if s == True:
                                            continue
                                        if self.enemy_shots[xo][yo] == 0:
                                            shot = True
                                            if self.make_shot(
                                                    xo, yo, self.player_board
                                            ) != 'Hit':
                                                self.enemy_shots[xo][yo] = 1
                                                return ([xo, yo])
                                                self.valid_directions = directions
                                            else:
                                                self.enemy_shots[xo][
                                                    yo] = self.player_board[
                                                        xo][yo] + 2
                                                return ([xo, yo])
                                    else:
                                        s = True
                                        self.valid_directions[
                                            0] = -self.valid_directions[0]
                                        self.valid_directions[
                                            1] = -self.valid_directions[1]

                            else:
                                #If no single valid direction, just shoots around the point of interest
                                for i in range(len(directions)):
                                    xo = x + directions[i][0]
                                    yo = y + directions[i][1]
                                    if 0 <= xo <= 6 and 0 <= (yo) <= 6:
                                        if self.enemy_shots[xo][yo] == 0:
                                            shot = True
                                            if self.make_shot(
                                                    xo, yo, self.player_board
                                            ) != 'Hit':
                                                self.enemy_shots[xo][yo] = 1
                                                if directions[
                                                        i] in self.valid_directions:
                                                    self.valid_directions.remove(
                                                        directions[i])
                                                return ([xo, yo])
                                            else:
                                                self.enemy_shots[xo][
                                                    yo] = self.player_board[
                                                        xo][yo] + 2
                                                self.valid_directions = directions[
                                                    i]
                                                return ([xo, yo])

                if self.sunk_num < len(self.check_ships(self.player_board)):
                    #If a ship was sunk, removes its ship chunks from being valid points of interest
                    if self.sunk_report[-1][1] == 'B':
                        num = 6
                    if self.sunk_report[-1][1] == 'C':
                        num = 5
                    if self.sunk_report[-1][1] == 'S':
                        num = 4
                    else:
                        num = 3
                    for x in range(len(self.enemy_shots)):
                        for y in range(len(self.enemy_shots[x])):
                            if self.enemy_shots[x][y] == num:
                                self.enemy_shots[x][y] = 1

                if shot == False:
                    #In case no shot was made by the above section, makes a random, valid shot
                    while shot == False:
                        x = randint(0, 6)
                        y = randint(0, 6)
                        if self.enemy_shots[x][y] == 0:
                            if self.make_shot(x, y,
                                              self.player_board) == 'Hit':
                                self.enemy_shots[x][y] = int(
                                    self.hit_report[-2])
                            else:
                                self.enemy_shots[x][y] = 1
                            shot = True

                if shot:
                    return ([x, y])
                    break

        elif difficulty == False:
            '''[Landon] Added an random firing mode for if the difficulty was not selected to be advanced'''
            while shot == False:
                x = randint(0, 6)
                y = randint(0, 6)
                if self.enemy_shots[x][y] == 0:
                    if self.make_shot(x, y, self.player_board) == 'Hit':
                        self.enemy_shots[x][y] = int(
                            self.player_board[x][y]) + 2
                    else:
                        self.enemy_shots[x][y] = 1
                    shot = True
                if shot == True:
                    return ([x, y])
                    break
