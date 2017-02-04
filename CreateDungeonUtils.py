import json


class DungeonCreator:
    def __init__(self):
        self.createdDungeon = {}

    def generate_dungeon(self, parser, player):
        dungeon_name = input("Dungeon Name: ").upper()

        self.createdDungeon = {
            "NAME": dungeon_name,
            "SIZE": 0,
            "ROOMS": {}

        }

        go = True
        while go:
            choice = None
            while choice != "Y" and choice != "N":
                choice = input("Add Room? (Y/N): ").upper()
                if choice == "Y":
                    self.createdDungeon["SIZE"] += 1

                    room_name = input("Room Name: ")

                    for index in range(len(parser.reverse_lists[1])):
                        print(str((index + 1)) + ". " + parser.reverse_lists[1][index + 1])
                    item = "$"
                    while not item.isdigit() or int(item) < 1 or int(item) > len(parser.reverse_lists[1]):
                        item = input("Number of Item (1-" + str(len(parser.reverse_lists[1])) + "): ")
                    room_item = int(item)

                    index = 5
                    while index < len(player.jobs) + 1:
                        print(str((index - 4)) + ". " + player.jobs[index])
                        index += 1
                    enemy = "$"
                    while not enemy.isdigit() or int(enemy) < 1 or int(enemy) > (len(player.jobs) - 4):
                        enemy = input("Number of enemy (1-" + str(len(player.jobs) - 4) + "): ")
                    room_enemy = int(enemy) + 4

                    doors = {
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
                    while int(door_choice) != 5:
                        while not door_choice.isdigit() or int(door_choice) < 1 or int(door_choice) > 5:
                            door_choice = input("1. left\n2. forward\n3. right\n4. backward\n5. done\nDoor Choice "
                                                "(1-5): ")
                        if int(door_choice) < 5:
                            destination_room = "-1"
                            while not destination_room.isdigit() or int(destination_room) < 0:
                                destination_room = input("Destination Room: ")
                                doors[parser.convert_integer_to_direction(int(door_choice) - 1)] = int(destination_room)
                                locked = "$"
                                while locked != "Y" and locked != "N":
                                    locked = input("Is door locked? (Y/N): ").upper()
                                if locked == "Y":
                                    doors[parser.convert_integer_to_direction(int(door_choice) - 1) + "_locked"] = 1
                            door_choice = "-1"
                        print(str(room_item) + " " + str(room_enemy))
                        print(doors)

                    room_description = input("Room Description: ")
                    self.createdDungeon["ROOMS"][self.createdDungeon["SIZE"] - 1] = {"name": room_name, "item": room_item, "enemy": room_enemy,
                                                    "doors": {"left": doors["left"], "forward": doors["forward"],
                                                              "right": doors["right"], "backward": doors["backward"],
                                                              "left_locked": doors["left_locked"],
                                                              "forward_locked": doors["forward_locked"],
                                                              "right_locked": doors["right_locked"],
                                                              "backward_locked": doors["backward_locked"]},
                                                    "description": room_description}
                else:
                    go = False
            json_dungeon = json.dumps(self.createdDungeon)
            print(json_dungeon)

'''
"NAME": "DUNGEON",
  "SIZE": 9,
  "ROOMS": [
    {
      "index": 0,
      "name": "ONE",
      "item": 3,
      "enemy": 5,
      "doors": {
        "left": -1,
        "forward": 1,
        "right": -1,
        "backward": -1,
        "left_locked": 0,
        "forward_locked": 1,
        "right_locked": 0,
        "backward_locked": 0
      },
      "description": "this is the first room"
    },
'''