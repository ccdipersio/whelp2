import os
import json
import re


class Dungeon:

    def __init__(self, file_path):
        if file_path == "":
            relative_path = os.path.dirname(__file__)  # RELATIVE FILE PATH TO USE TO OPEN FILES LATER
            lib = "LibraryFiles"  # SHORTENING OF NAME OF LIBRARY FILES FOLDER TO FIT WITH PEP 8 CONVENTIONS
            file_path = os.path.join(relative_path, lib, "json_Dungeon.json")

            line_number = self.verify_dungeon_file(file_path)
            if line_number != 0:
                print("ERROR AT LINE " + str(line_number) + " in file at path " + file_path + "!!!")
                return
            with open(file_path, "r") as file:
                self.json_dungeon = json.load(file)  # LOAD IN JSON FILE
        else:
            line_number = self.verify_dungeon_file(file_path)
            if line_number != 0:
                print("ERROR AT LINE " + str(line_number) + " in file at path " + file_path + "!!!")
                return
            with open(file_path, "r") as file:
                self.json_dungeon = json.load(file)

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

    @staticmethod
    def verify_dungeon_file(file_path):
        line_number = 1
        with open(file_path, "r") as file:
            if not re.search(r'\{', file.readline()):  # {
                return line_number
            line_number += 1
            if not re.search(r'"NAME": "[A-Z]+",', file.readline()):  # NAME
                return line_number
            line_number += 1
            if not re.search(r'"SIZE": \d+,', file.readline()):  # SIZE
                return line_number
            line_number += 1
            if not re.search(r'"ROOMS": \[', file.readline()):  # ROOMS
                return line_number
            line_number += 1

            line = file.readline()
            while line != ']':
                if not re.search(r'{', line):  # {
                    return line_number
                line_number += 1
                if not re.search(r'"index": \d+,', file.readline()):  # index
                    return line_number
                line_number += 1
                if not re.search(r'"name": "[A-Za-z]+",', file.readline()):  # name
                    return line_number
                line_number += 1
                if not re.search(r'"item": \d,', file.readline()):  # item
                    return line_number
                line_number += 1
                if not re.search(r'"enemy": \d,', file.readline()):  # enemy
                    return line_number
                line_number += 1
                if not re.search(r'"doors": \{', file.readline()):  # doors
                    return line_number
                line_number += 1
                if not re.search(r'"left": -?\d,', file.readline()):  # left
                    return line_number
                line_number += 1
                if not re.search(r'"forward": -?\d,', file.readline()):  # forward
                    return line_number
                line_number += 1
                if not re.search(r'"right": -?\d,', file.readline()):  # right
                    return line_number
                line_number += 1
                if not re.search(r'"backward": -?\d,', file.readline()):  # backward
                    return line_number
                line_number += 1
                if not re.search(r'"left_locked": 0|1,', file.readline()):  # left_locked
                    return line_number
                line_number += 1
                if not re.search(r'"forward_locked": 0|1,', file.readline()):  # forward_locked
                    return line_number
                line_number += 1
                if not re.search(r'"right_locked": 0|1,', file.readline()):  # right_locked
                    return line_number
                line_number += 1
                if not re.search(r'"backward_locked": 0|1,', file.readline()):  # backward_locked
                    return line_number
                line_number += 1
                if not re.search(r'},', file.readline()):  # }
                    return line_number
                line_number += 1
                if not re.search(r'"description": ".+"', file.readline()):  # description
                    return line_number
                line_number += 1
                prev_line = file.readline()
                line = file.readline().strip()
                if not re.search(r']', line):
                    if not re.search(r'}', prev_line):  # },
                        return line_number
                else:
                    if not re.search(r'}', prev_line):  # }
                        return line_number
                line_number += 1
            if not re.search(r']', line):  # ]
                return line_number
            line_number += 1
            if not re.search(r'}', file.readline()):  # }
                return line_number
            line_number += 1

            return 0
