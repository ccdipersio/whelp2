import os
import json
import re


class Dungeon:
    """The Dungeon class to initialize and control activities within."""

    def __init__(self, file_path):
        """Initializes the dungeon.

        The function opens the file, passes it to a function checking its validity, and if all is good to go, loads the
            file using the JSON library.

        Args:
            file_path: A string for the path to a user defined file. It's possible to pass in "" rather than a full path
                if the use doesn't want to define his or her own file.
        """
        if file_path == "":
            relative_path = os.path.dirname(__file__)
            lib = "LibraryFiles"
            file_path = os.path.join(relative_path, lib, "json_Dungeon.json")

            line_number = self.verify_dungeon_file(file_path)
            if line_number != 0:
                print("ERROR AT LINE " + str(line_number) + " in file at path " + file_path + "!!!")
                self.json_dungeon = None
                return
            with open(file_path, "r") as file:
                self.json_dungeon = json.load(file)
        else:
            line_number = self.verify_dungeon_file(file_path)
            if line_number != 0:
                print("ERROR AT LINE " + str(line_number) + " in file at path " + file_path + "!!!")
                self.json_dungeon = None
                return
            with open(file_path, "r") as file:
                self.json_dungeon = json.load(file)

    def dungeon_control(self, parser, player):
        """Controls activities within the dungeon.

        This function mostly passes things off to the parse_json_room function from the TextParser object and takes
            integer it passes back to move through the dungeon or determine if the player died.

        Args:
            parser: The TextParser object.
            player: The instance of the Player character object.
        """
        current_room = 0
        control_index = 0
        while control_index != 12:
            enemies_remaining = 0
            for index in range(len(self.json_dungeon["ROOMS"])):
                if self.json_dungeon["ROOMS"][index]["enemy"] != 0:
                    enemies_remaining += 1
            control_index = parser.parse_json_room(self.json_dungeon["ROOMS"][current_room], player, enemies_remaining)
            if 19 < control_index < 24:
                direction = parser.convert_integer_to_direction(control_index - 20)
                locked = direction + "_locked"
                if self.json_dungeon["ROOMS"][current_room]["doors"][direction] == -1:
                    print("Cannot move that way...")
                    continue
                elif self.json_dungeon["ROOMS"][current_room]["doors"][locked] == 1:
                    print(direction + " door is locked!\n")
                    continue
                else:
                    current_room = self.json_dungeon["ROOMS"][current_room]["doors"][direction]
            elif control_index == 12:
                print("You have failed...")
                return
            elif control_index == 13:
                print("The dungeon has been purged of danger!")
                return

    @staticmethod
    def verify_dungeon_file(file_path):
        """Verifies the dungeon's JSON file using regular expressions

        Args:
            file_path: Path to the JSON file.

        Returns: A line_number in the JSON file is something is wrong, or a 0 if everything is fine.
        """
        line_number = 1
        with open(file_path, "r") as file:
            if not re.search(r'\{', file.readline()):
                return line_number
            line_number += 1
            if not re.search(r'"NAME": "[A-Z]+",', file.readline()):
                return line_number
            line_number += 1
            if not re.search(r'"SIZE": \d+,', file.readline()):
                return line_number
            line_number += 1
            if not re.search(r'"ROOMS": \[', file.readline()):
                return line_number
            line_number += 1

            line = file.readline()
            while line != ']':
                if not re.search(r'{', line):
                    return line_number
                line_number += 1
                if not re.search(r'"index": \d+,', file.readline()):
                    return line_number
                line_number += 1
                if not re.search(r'"name": "[A-Za-z\s]+",', file.readline()):
                    return line_number
                line_number += 1
                if not re.search(r'"item": \d,', file.readline()):
                    return line_number
                line_number += 1
                if not re.search(r'"enemy": \d,', file.readline()):
                    return line_number
                line_number += 1
                if not re.search(r'"doors": \{', file.readline()):
                    return line_number
                line_number += 1
                if not re.search(r'"left": -?\d,', file.readline()):
                    return line_number
                line_number += 1
                if not re.search(r'"forward": -?\d,', file.readline()):
                    return line_number
                line_number += 1
                if not re.search(r'"right": -?\d,', file.readline()):
                    return line_number
                line_number += 1
                if not re.search(r'"backward": -?\d,', file.readline()):
                    return line_number
                line_number += 1
                if not re.search(r'"left_locked": 0|1,', file.readline()):
                    return line_number
                line_number += 1
                if not re.search(r'"forward_locked": 0|1,', file.readline()):
                    return line_number
                line_number += 1
                if not re.search(r'"right_locked": 0|1,', file.readline()):
                    return line_number
                line_number += 1
                if not re.search(r'"backward_locked": 0|1,', file.readline()):
                    return line_number
                line_number += 1
                if not re.search(r'},', file.readline()):
                    return line_number
                line_number += 1
                if not re.search(r'"description": ".+"', file.readline()):
                    return line_number
                line_number += 1
                prev_line = file.readline()
                line = file.readline().strip()
                if not re.search(r']', line):
                    if not re.search(r'}', prev_line):
                        return line_number
                else:
                    if not re.search(r'}', prev_line):
                        return line_number
                line_number += 1
            if not re.search(r']', line):
                return line_number
            line_number += 1
            if not re.search(r'}', file.readline()):
                return line_number
            line_number += 1

            return 0
