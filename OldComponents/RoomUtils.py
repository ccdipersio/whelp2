from CharacterUtils import Enemy
import os


class Room:

    def __init__(self, name, item_index, enemy_index, door_entered, door_exit):
        # SET VARIABLES
        self.name = name
        self.item_index = item_index
        self.enemy_index = enemy_index
        self.door_entered = door_entered
        self.door_exit = door_exit

        self.direction_indexes = {
            -1: "NO DOOR",
            0: "LEFT",
            1: "FORWARD",
            2: "RIGHT",
            3: "BACKWARD",
        }

    def print_room(self, parser):
        if self.item_index != 0:
            in_room = parser.reverse_lists[1][self.item_index]
            item = "\n\tThere's a(n) " + in_room + " here!"
        else:
            item = "\n\tNo item here..."
        if self.enemy_index != 0:
            enemy = "\n\tThere's an enemy here!"
        else:
            enemy = "\n\tNo enemy here..."
        if self.door_entered == -1:
            entered = ""
        else:
            entered = "\n\tEntered through " + self.direction_indexes[self.door_entered] + " door."
        if self.door_exit == -1:
            exited = ""
        else:
            exited = "\n\tExit seen " + self.direction_indexes[self.door_exit] + "."
        print("\nEntered " + self.name + item + enemy + entered + exited)

    def battle_set(self, parser, player):
        enemy = Enemy(self.enemy_index)
        print(player.name + " is fighting " + enemy.name + "!")
        while True:
            if player.speed >= enemy.speed:
                goes_first = True
            else:
                goes_first = False

            print(player.name + " HP: " + str(player.hp) + "\n")
            print(enemy.name + " HP: " + str(enemy.hp))

            player_move = parser.parse_battle(player)
            enemy_move = enemy.enemy_move()

            if goes_first:
                if not player.process_player_move(player_move, enemy):
                    enemy.give_item(parser, player)
                    return True
                if not enemy.process_enemy_move(enemy_move, player):
                    return False
            else:
                if not enemy.process_enemy_move(enemy_move, player):
                    return False
                if not player.process_player_move(player_move, enemy):
                    enemy.give_item(parser, player)
                    return True


class Dungeon:

    def __init__(self):
        relative_path = os.path.dirname(__file__)  # RELATIVE FILE PATH TO USE TO OPEN FILES LATER
        lib = "LibraryFiles"  # SHORTENING OF NAME OF LIBRARY FILES FOLDER TO FIT WITH PEP 8 CONVENTIONS

        self.maze_file = open(os.path.join(relative_path, lib, "maze"), "r")
        self.maze_list = []
        self.current_room = 0

        for line in self.maze_file:  # ITERATE THROUGH MAZE FILE
            line = line.strip()  # GET LINE FROM MAZE FILE
            line_split = line.split(",")  # SPLIT LINE ALONG COMMA
            self.maze_list.append(Room(line_split[0], int(line_split[1]), int(line_split[2]), int(line_split[3]),
                                       int(line_split[4])))
        self.maze_file.close()

    def dungeon_control(self, parser, player):
        control_index = 0  # VARIABLE FOR CONTROL INDEX
        while control_index != 12:  # 12 = DEATH
            control_index = parser.parse_room(self.maze_list[self.current_room], player)
            if 19 < control_index < 24:  # "MOVE" COMMANDS
                direction = control_index - 20  # REMOVE 20 TO GET DIRECTION
                if direction == self.maze_list[self.current_room].door_entered:  # DIRECTION MOVES BACK A ROOM
                    if self.current_room - 1 < 0:  # CAN'T MOVE BACK MORE
                        print("Cannot move out of dungeon!")
                        continue
                    else:
                        self.current_room -= 1
                        continue
                else:  # DIRECTION MOVES FORWARD A ROOM
                    if self.current_room + 1 >= len(self.maze_list):  # CAN'T MOVE FORWARD MORE
                        print("Cannot move more into dungeon!")
                        continue
                    else:
                        self.current_room += 1
                        continue
