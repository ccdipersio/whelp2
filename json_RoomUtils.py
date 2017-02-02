import os
import json


class Dungeon:

    def __init__(self):
        relative_path = os.path.dirname(__file__)  # RELATIVE FILE PATH TO USE TO OPEN FILES LATER
        lib = "LibraryFiles"  # SHORTENING OF NAME OF LIBRARY FILES FOLDER TO FIT WITH PEP 8 CONVENTIONS

        with open(os.path.join(relative_path, lib, "json_Dungeon.json"), "r") as file:
            self.json_dungeon = json.load(file)  # LOAD IN JSON FILE

    def dungeon_control(self, parser, player):
        current_room = 0
        control_index = 0  # VARIABLE FOR CONTROL INDEX
        while control_index != 12:  # 12 = DEATH
            control_index = parser.parse_json_room(self.json_dungeon["ROOMS"][current_room], player)
            if 19 < control_index < 24:  # "MOVE" COMMANDS
                direction = parser.convert_integer_to_direction(control_index - 20)  # REMOVE 20 AND CONVERT TO DIRECTION
                locked = direction + "_locked"  # CREATE STRING TO CHECK FOR LOCKED DOOR
                if self.json_dungeon["ROOMS"][current_room]["doors"][direction] == -1:  # CHECK FOR BAD MOVE
                    print("Cannot move that way...")
                    continue
                elif self.json_dungeon["ROOMS"][current_room]["doors"][locked] == 1:  # CHECK FOR LOCKED DOOR
                    print(direction + " door is locked!\n")
                    continue
                else:
                    current_room = self.json_dungeon["ROOMS"][current_room]["doors"][direction]  # MOVE


