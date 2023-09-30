from Battleship_Engine import *

test = Game_Engine(7)
count = 0

#Tests that the enemy board is the right size
for x in range(len(test.enemy_board)):
    for y in range(len(test.enemy_board[x])):
        count += 1
assert count == 49 #enemy_board should have 49 (7 x 7) objects

#Tests that all ships are generated
assert len(test.check_ships(test.enemy_board)) == 0

test.make_shot(0, 0, test.player_board)
assert test.player_board[0][0] == 0

#makes a shot on every tile on player board and checks that all ships were sunk
for x in range(len(test.enemy_board)):
    for y in range(len(test.enemy_board[x])):
        test.make_shot(x, y, test.player_board)
assert len(test.check_ships(test.player_board)) == 4 #Should have sunken all ships
c = 0
for i in range(len(test.check_ships(test.player_board))):
    if test.check_ships(test.player_board)[i] == "Destroyer(2)":
        c += 1
    if test.check_ships(test.player_board)[i] == "Submarine(3)":
        c += 1
    if test.check_ships(test.player_board)[i] == "Cruiser(3)":
        c += 1
    if test.check_ships(test.player_board)[i] == "Battleship(4)":
        c += 1
assert c == 4 #Should have 4 ships with correct names spawned
