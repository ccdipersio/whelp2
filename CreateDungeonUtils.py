import os


class DungeonCreator:
    def __init__(self):
        self.createdDungeon = {}

    def generate_dungeon(self, parser, player):

        dungeon_name = input("Dungeon Name: ").upper()  # GET DUNGEON NAME

        self.createdDungeon = {  # CREATE SKELETON OF DICTIONARY FOR DUNGEON
            "NAME": dungeon_name,
            "SIZE": 0,
            "ROOMS": {}

        }

        go = True  # BOOLEAN FOR WHILE LOOP
        while go:
            choice = None  # VARIABLE FOR CHOICE
            while choice != "Y" and choice != "N":
                choice = input("Add Room? (Y/N): ").upper()  # GET CHOICE
                if choice == "Y":  # IF YES
                    self.createdDungeon["SIZE"] += 1  # INCREMENT SIZE

                    room_name = input("Room Name: ")  # GET ROOM NAME

                    for index in range(len(parser.reverse_lists[1])):  # PRINT POSSIBLE ITEMS
                        print(str((index + 1)) + ". " + parser.reverse_lists[1][index + 1])
                    item = "$"
                    while not item.isdigit() or int(item) < 1 or int(item) > len(parser.reverse_lists[1]):  # GET ITEM
                        item = input("Number of Item (1-" + str(len(parser.reverse_lists[1])) + "): ")
                    room_item = int(item)  # ADD TO ROOM

                    index = 5
                    while index < len(player.jobs) + 1:  ## PRINT POSSIBLE ENEMIES
                        print(str((index - 4)) + ". " + player.jobs[index])
                        index += 1
                    enemy = "$"
                    while not enemy.isdigit() or int(enemy) < 1 or int(enemy) > (len(player.jobs) - 4):  # GET ENEMY
                        enemy = input("Number of enemy (1-" + str(len(player.jobs) - 4) + "): ")
                    room_enemy = int(enemy) + 4

                    doors = {  # CREATE SKELETON OF DICTIONARY FOR DOORS
                        "left": -1,
                        "forward": -1,
                        "right": -1,
                        "backward": -1,
                        "left_locked": 0,
                        "forward_locked": 0,
                        "right_locked": 0,
                        "backward_locked": 0
                    }

                    door_choice = "-1"
                    while int(door_choice) != 5:  # PRINT DOOR OPTIONS
                        while not door_choice.isdigit() or int(door_choice) < 1 or int(door_choice) > 5:
                            door_choice = input("1. left\n2. forward\n3. right\n4. backward\n5. done\nDoor Choice "
                                                "(1-5): ")
                        if int(door_choice) < 5:  # IF ADD DOOR
                            destination_room = "-1"
                            while not destination_room.isdigit() or int(destination_room) < 0:  # GET DESTINATION ROOM
                                destination_room = input("Destination Room: ")
                                doors[parser.convert_integer_to_direction(int(door_choice) - 1)] = int(destination_room)
                                locked = "$"
                                while locked != "Y" and locked != "N":  # ASK IF DOOR IS LOCKED
                                    locked = input("Is door locked? (Y/N): ").upper()
                                if locked == "Y":
                                    doors[parser.convert_integer_to_direction(int(door_choice) - 1) + "_locked"] = 1
                            door_choice = "-1"

                    room_description = input("Room Description: ")  # GET ROOM DESCRIPTION
                    self.createdDungeon["ROOMS"][self.createdDungeon["SIZE"] - 1] = {  # DUMP DATA INTO ROOM
                        "index": self.createdDungeon["SIZE"] - 1, "name": room_name, "item": room_item,
                        "enemy": room_enemy, "doors": {"left": doors["left"], "forward": doors["forward"],
                                                       "right": doors["right"], "backward": doors["backward"],
                                                       "left_locked": doors["left_locked"],
                                                       "forward_locked": doors["forward_locked"],
                                                       "right_locked": doors["right_locked"],
                                                       "backward_locked": doors["backward_locked"]},
                        "description": room_description}
                else:  # IF NO, QUIT LOOP
                    go = False
        self.dump_data_to_file()  # PRINT DATA INTO FILE

    # PRINT DATA INTO FILE
    def dump_data_to_file(self):
        file_name = input("File Name (without extension): ")
        file_name_ext = file_name + ".json"
        relative_path = os.path.dirname(__file__)
        file = open(os.path.join(relative_path, "UserDefinedFiles", file_name_ext), "w+")
        file.write('{\n')
        file.write('  "NAME": ' + '"' + self.createdDungeon["NAME"] + '",\n')
        file.write('  "SIZE": ' + str(self.createdDungeon["SIZE"]) + ',\n')
        file.write('  "ROOMS": [\n')
        for index in range(len(self.createdDungeon["ROOMS"])):
            file.write('    {\n')
            file.write('      "index": ' + str(self.createdDungeon["ROOMS"][index]["index"]) + ',\n')
            file.write('      "name": "' + self.createdDungeon["ROOMS"][index]["name"] + '",\n')
            file.write('      "item": ' + str(self.createdDungeon["ROOMS"][index]["item"]) + ',\n')
            file.write('      "enemy": ' + str(self.createdDungeon["ROOMS"][index]["enemy"]) + ',\n')
            file.write('      "doors": {\n')
            file.write('        "left": ' + str(self.createdDungeon["ROOMS"][index]["doors"]["left"]) + ',\n')
            file.write('        "forward": ' + str(self.createdDungeon["ROOMS"][index]["doors"]["forward"]) + ',\n')
            file.write('        "right": ' + str(self.createdDungeon["ROOMS"][index]["doors"]["right"]) + ',\n')
            file.write('        "backward": ' + str(self.createdDungeon["ROOMS"][index]["doors"]["backward"]) + ',\n')
            file.write('        "left_locked": ' + str(self.createdDungeon["ROOMS"][index]["doors"]["left_locked"])
                       + ',\n')
            file.write('        "forward_locked": ' + str(self.createdDungeon["ROOMS"][index]["doors"]
                                                          ["forward_locked"]) + ',\n')
            file.write('        "right_locked": ' + str(self.createdDungeon["ROOMS"][index]["doors"]["right_locked"])
                       + ',\n')
            file.write('        "backward_locked": ' + str(self.createdDungeon["ROOMS"][index]["doors"]
                                                           ["backward_locked"]) + '\n')
            file.write('      },\n')
            file.write('      "description": "' + self.createdDungeon["ROOMS"][index]["description"] + '"\n')
            if index == len(self.createdDungeon["ROOMS"]) - 1:
                file.write('    }\n')
            else:
                file.write('    },\n')
        file.write('  ]\n')
        file.write('}')
        file.close()
