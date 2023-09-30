'''CS 108 Final Project: Battleship Game -- Submitted on 12/15/2022

Authors:
    Musa Kwong (mak66)
    Landon Faber (lrf24)'''

from guizero import App, Drawing, PushButton, Box, Slider, Waffle, Text, ListBox
from random import randint
from Battleship_Engine import *
import time
import copy


class Battleship_Game:

    def __init__(self, app):
        app.title = 'Battleship'
        window_size = 475
        self.box_size = 210
        app.width = window_size
        app.height = window_size
        self.game = Game_Engine(7)

        #Sets the game settings
        self.enemy_difficulty = app.yesno('Setup', 'More advanced enemy?')
        self.player_turn = True
        self.aim_choice = False

        self.enemy_grid = Grid(app, [0, 0], 7, self.box_size)
        self.implement_fire_controls()

        #adds the boxes
        spacer1 = Box(app, grid=[0, 1], height=10, width=1)
        self.player_grid = Grid(app, [0, 2], 7, self.box_size)
        spacer2 = Box(app, grid=[1, 0], height=1, width=10)
        self.log_box = Box(app,
                           grid=[2, 2],
                           layout='grid',
                           height=self.box_size,
                           width=self.box_size * 1.2,
                           border=True)

        #Sets the initial log box information
        self.instructions_display = [
            " Select the coordinates using the sliders above,",
            ' then press the fire button.'
        ]
        self.implement_log_box()

        #Determines the ships and draws them
        self.game.determine_player_ships(False)
        self.draw_ships(self.game.player_ships, self.player_grid)

    def implement_log_box(self):
        '''[Musa] Initializes the report box with all the text items'''
        if not self.aim_choice:
            self.instructions1 = ListBox(self.log_box,
                                         grid=[0, 0],
                                         width=self.box_size * 1.19,
                                         enabled=False,
                                         height=36,
                                         items=self.instructions_display)
            self.game_turn_text = Text(self.log_box,
                                       grid=[0, 1],
                                       text='Player Turn...')
            self.shot_text = Text(self.log_box,
                                  grid=[0, 2],
                                  text=self.game.shot_report)
            self.hit_text = Text(self.log_box,
                                 grid=[0, 3],
                                 text=self.game.hit_report)
            self.sunk_text = Text(self.log_box,
                                  grid=[0, 4],
                                  text="Sunk ships:",
                                  align='left')
            self.sunken_list = ListBox(self.log_box,
                                       grid=[0, 5],
                                       width=self.box_size * 1.18,
                                       height=75,
                                       enabled=False,
                                       items=self.game.sunk_report)

    def update_log_box(self):
        '''[Musa] Updates the report box with current information'''
        if self.player_turn:
            turn = 'Player:'
        else:
            turn = 'Enemy:'
        if not self.aim_choice:
            #self.instructions1 = ListBox(self.log_box, grid = [0,0], width = 'fill', enabled = False,height = 36,items=self.instructions_display)
            self.game_turn_text.value = turn
            self.shot_text.value = self.game.shot_report
            self.hit_text.value = self.game.hit_report
            self.sunken_list = ListBox(self.log_box,
                                       grid=[0, 5],
                                       width=self.box_size * 1.18,
                                       height=75,
                                       enabled=False,
                                       items=self.game.sunk_report)

    def implement_fire_controls(self):
        '''[Musa] Implements the control scheme for firing'''
        self.firing_space = Box(app,
                                grid=[2, 0],
                                layout='grid',
                                height=self.box_size * 1.1,
                                width=self.box_size * 1.1,
                                border=True)
        self.crosshair = Drawing(self.firing_space,
                                 grid=[0, 0],
                                 width=int(self.box_size),
                                 height=int(self.box_size))

        if not self.aim_choice:
            self.max_x = 7
            self.max_y = 7
        #self.crosshair.rectangle(0,0,int(self.box_size),int(self.box_size))
        self.sliderx = Slider(self.firing_space,
                              grid=[0, 1],
                              start=1,
                              width=int(self.box_size),
                              height=int(self.box_size * .04),
                              align='left',
                              end=self.max_x,
                              horizontal=True,
                              command=self.move_line)
        self.slidery = Slider(self.firing_space,
                              grid=[1, 0],
                              start=self.max_y,
                              height=int(self.box_size),
                              width=int(self.box_size * .04),
                              align='top',
                              end=1,
                              horizontal=False,
                              command=self.move_line)
        fire_button = PushButton(self.firing_space,
                                 text='Fire',
                                 grid=[1, 1],
                                 width=1,
                                 height=1,
                                 pady=0,
                                 command=self.process_player_shot)
        self.crosshair.line(0, self.box_size * 13 / 14, self.box_size,
                            self.box_size * 13 / 14)
        self.crosshair.line(self.box_size / 14, 0, self.box_size / 14,
                            self.box_size)

    def move_line(self):
        '''[Musa] Moves the crosshair to match with the sliders'''
        self.crosshair.clear()
        self.shot_y = (self.max_y + .5 -
                       self.slidery.value) * self.box_size / 7
        self.shot_x = (self.sliderx.value - 0.5) * self.box_size / 7
        self.crosshair.line(0, self.shot_y, self.box_size, self.shot_y)
        self.crosshair.line(self.shot_x, 0, self.shot_x, self.box_size)

    def process_player_shot(self):
        '''[Musa] Process a player shot when the fire button is pressed based on the slider values. Also checks if the  player has shot at the coordinates, not activating if they have'''
        if self.player_turn == True:
            if not self.aim_choice:
                x = self.sliderx.value - 1
                y = self.slidery.value - 1
            if self.game.player_shots[x][y] == 0:
                self.enemy_grid.shot_marker(x, y, self.game.enemy_board)
                self.game.make_shot(x, y, self.game.enemy_board)
                self.game.player_shots[x][y] = 1
                self.update_log_box()
                if self.game.hit_report == 'Miss':
                    self.player_turn = not self.player_turn
                    self.win()
                    app.update()
                    self.process_enemy_shot(self.enemy_difficulty)
                    self.win()
                self.win()

    def process_enemy_shot(self, difficulty):
        while not self.player_turn:
            time.sleep(1)
            app.update()
            old_board = copy.deepcopy(self.game.player_board)
            shot_coords = self.game.make_enemy_shot(difficulty)
            x = shot_coords[0]
            y = shot_coords[1]
            self.update_log_box()
            self.player_grid.shot_marker(x, y, old_board)
            if self.game.hit_report == 'Miss':
                #self.win()
                self.player_turn = not self.player_turn
                break
            #self.win()

    def draw_ships(self, ships, grid):
        '''[Musa] Draws a given list of ships onto one of the grids'''
        for i in range(4):
            x = ships[i][0]
            y = ships[i][1]
            length = ships[i][2]
            orientation = ships[i][3]
            grid.draw_ship(x, y, orientation, length)

    def win(self):
        '''[Landon] checks either the player board or the enemy board and if that whole board is empty then the game ends'''
        c = 0
        v = 0
        for x in range(7):
            for y in range(7):
                if self.game.enemy_board[x][y] != 0:
                    c += 1
                if self.game.player_board[x][y] != 0:
                    v += 1
        if c == 0:
            #Enemy board was cleared
            self.log_box.destroy()
            text = Text(app, grid=[2, 2], text="GG YOU WON", size=20)
            app.display()
        if v == 0:
            #Player board was cleared
            self.log_box.destroy()
            text = Text(app, grid=[2, 2], text="GG YOU LOST", size=20)
            app.display()


#Grid for ships to be on
class Grid:

    def __init__(self, app, pos, size, box_size):
        '''[Musa] Creates a grid of drawing objects at a given location, initializing them with blue boxes'''
        self.grid_space = box_size / size
        self.grid = Box(app,
                        layout="grid",
                        grid=pos,
                        align='top',
                        border=1,
                        height=int((size) * self.grid_space) + 2,
                        width=int((size) * self.grid_space) + 2)
        self.board = []
        for x in range(size):
            boardline = []
            for y in range(size):
                a = Drawing(self.grid,
                            grid=[x, 6 - y],
                            width=self.grid_space,
                            height=self.grid_space)
                a.rectangle(0,
                            0,
                            self.grid_space - 1,
                            self.grid_space - 1,
                            color=(0, 80, 140),
                            outline=True)
                #a.rectangle(10,10,17,17,color="black",outline=True)
                boardline.append(a)
            self.board.append(boardline)

    def draw_ship(self, x, y, orient, length):
        '''[Musa] draws a ship based on given coordinate and orientation'''
        if orient == 'h':
            self.board[x][y].triangle(self.grid_space / 6,
                                      self.grid_space / 2,
                                      self.grid_space,
                                      self.grid_space / 6,
                                      self.grid_space,
                                      self.grid_space * 5 / 6,
                                      color='white',
                                      outline=True)
            for i in range(length - 2):
                self.board[x + i + 1][y].rectangle(0,
                                                   self.grid_space / 6,
                                                   self.grid_space,
                                                   5 * self.grid_space / 6,
                                                   color='white',
                                                   outline=True)
            self.board[x + length - 1][y].triangle(5 * self.grid_space / 6,
                                                   self.grid_space / 2,
                                                   0,
                                                   self.grid_space / 6,
                                                   0,
                                                   5 * self.grid_space / 6,
                                                   color='white',
                                                   outline=True)
        if orient == 'v':
            self.board[x][y + length - 1].triangle(self.grid_space / 2,
                                                   self.grid_space / 6,
                                                   self.grid_space / 6,
                                                   self.grid_space,
                                                   5 * self.grid_space / 6,
                                                   self.grid_space,
                                                   color='white',
                                                   outline=True)
            for i in range(length - 2):
                self.board[x][y + i + 1].rectangle(self.grid_space / 6,
                                                   0,
                                                   5 * self.grid_space / 6,
                                                   self.grid_space,
                                                   color='white',
                                                   outline=True)
            self.board[x][y].triangle(self.grid_space / 2,
                                      5 * self.grid_space / 6,
                                      self.grid_space / 6,
                                      0,
                                      5 * self.grid_space / 6,
                                      0,
                                      color='white',
                                      outline=True)

    def shot_marker(self, x, y, target):
        '''[Musa] Puts a shot marker on the given board with the color being red for hits and whites for misses'''
        if target[x][y] != 0:
            marker_color = 'red'
        else:
            marker_color = 'white'
        self.board[x][y].oval(self.grid_space / 4,
                              self.grid_space / 4,
                              self.grid_space * 3 / 4,
                              self.grid_space * 3 / 4,
                              color=marker_color)


app = App(layout="grid")
battleship_game = Battleship_Game(app)
app.display()
