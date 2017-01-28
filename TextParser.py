from CharacterUtils import *
import os


class TextParser:

    def __init__(self):
        relative_path = os.path.dirname(__file__)  # RELATIVE FILE PATH TO USE TO OPEN FILES LATER
        lib = "LibraryFiles"  # SHORTENING OF NAME OF LIBRARY FILES FOLDER TO FIT WITH PEP 8 CONVENTIONS

        self.files = []  # LIST FOR FILES
        self.lists = {  # DICTIONARY OF DICTIONARIES FOR LISTS
            0: {},  # VERBS
            1: {},  # ITEMS
            2: {},  # DIRECTIONS
            3: {},  # QUANTITIES
            4: {},  # LOCATIONS
            5: {},  # OBJECTS
            6: {},  # BATTLE COMMANDS
        }
        self.reverse_lists = {
            0: {},  # VERBS
            1: {},  # ITEMS
            2: {},  # DIRECTIONS
            3: {},  # QUANTITIES
            4: {},  # LOCATIONS
            5: {},  # OBJECTS
            6: {},  # BATTLE COMMANDS
        }
        self.words = {  # DICTIONARY FOR WORDS
            0: -1,  # VERBS
            1: -1,  # ITEMS
            2: -1,  # DIRECTIONS
            3: -1,  # QUANTITIES
            4: -1,  # LOCATIONS
            5: -1,  # OBJECTS
            6: -1,  # BATTLE COMMANDS
            7: -1,  # HELP COMMAND
            8: -1,  # EQUIP COMMAND
        }
        self.item_strengths = {}

        self.files.append(open(os.path.join(relative_path, lib, "verbs"), "r"))  # VERBS FILE
        self.files.append(open(os.path.join(relative_path, lib, "items"), "r"))  # ITEMS FILE
        self.files.append(open(os.path.join(relative_path, lib, "directions"), "r"))  # DIRECTIONS FILE
        self.files.append(open(os.path.join(relative_path, lib, "quantities"), "r"))  # QUANTITIES FILE
        self.files.append(open(os.path.join(relative_path, lib, "locations"), "r"))  # LOCATIONS FILE
        self.files.append(open(os.path.join(relative_path, lib, "objects"), "r"))  # OBJECTS FILE
        self.files.append(open(os.path.join(relative_path, lib, "battle_commands"), "r"))  # BATTLE COMMANDS

        for index in range(len(self.files)):  # ITERATE THROUGH FILES LIST
            for line in self.files[index]:  # ITERATION THROUGH LINES IN CURRENT LIST
                line = line.strip()  # REMOVE '\n'
                split_line = line.split(",")  # SPLIT ALONG COMMA
                self.lists[index][split_line[0]] = int(split_line[1])  # COPY CONTENTS INTO CURRENT DICTIONARY
                self.reverse_lists[index][int(split_line[1])] = split_line[0]  # COPY WORD INTO REVERSE DICTIONARIES
                if index == 1:
                    self.item_strengths[int(split_line[1])] = int(split_line[2])
        for file in self.files:
            file.close()

    # RESET WORDS DICTIONARY
    def reset_words(self):
        for index in range(len(self.words)):
            self.words[index] = -1

    # GET NEW STRING
    def get_new_string(self):
        self.reset_words()  # RESET WORDS DICTIONARY
        input_string = input("\nCommand: ").lower()  # PROMPT FOR STRING
        split_string = input_string.split(" ")  # SPLIT ALONG SPACE
        self.parse_words(split_string)  # SEND TO PARSING FUNCTION

    # PARSE
    def parse_words(self, split_string):
        for word in split_string:  # ITERATE THROUGH PASSED-IN STRING
            if word == "help":
                self.words[7] = 1
                return
            for index in range(len(self.lists)):  # ITERATE THROUGH DICTIONARY OF DICTIONARIES
                for key in self.lists[index]:  # ITERATE THROUGH CURRENT DICTIONARY
                    if word == key:  # IF WORD MATCHES KEY IN DICTIONARY
                        self.words[index] = self.lists[index][key]  # SAVE INTEGER VALUE OF MATCHED KEY

    # GET BATTLE COMMAND
    def parse_battle(self, player):
        while True:
            print("Use SWORD, SPELL, or ITEM?")  # ASK FOR INPUT
            self.get_new_string()  # GET NEW STRING

            if self.words[7] == 1:
                self.help_me(2)
                continue
            elif self.words[6] == -1:  # BATTLE COMMAND NOT PASSED
                if self.words[0] != 3 and self.words[0] != 4:  # VIEW OR SELECT COMMAND NOT PASSED
                    print("Didn't understand command; try again...")
                    continue  # LOOP AGAIN
                else:
                    if self.words[0] == 3:  # VIEW COMMAND PASSED
                        if self.words[5] != 1:
                            print("Didn't understand command; try again...")
                            continue  # LOOP AGAIN
                        else:
                            player.print_inventory(self)  # PRINT INVENTORY
                            continue  # LOOP AGAIN
                    if self.words[0] == 4:  # SELECT COMMAND PASS
                        if self.words[1] == -1:  # DIDN'T PASS VALID ITEM
                            print("Didn't understand command; try again...")
                            continue  # LOOP AGAIN
                        else:  # VALID ITEM PASSED
                            index_in_inventory = self.check_inventory(self.words[1], player.inventory)
                            if index_in_inventory == -1:
                                continue
                            else:
                                item_strength = self.item_strengths[self.words[1]]  # GET ITEM STRENGTH
                                if item_strength == 0:  # CAN'T USE ITEM IN BATTLE
                                    print("Can't use that item in battle; try again...")
                                    continue
                                else:  # RETURN ITEM STRENGTH
                                    print(str(self.reverse_lists[1][self.words[1]]) + " used!")
                                    del player.inventory[index_in_inventory]
                                    return item_strength
            else:  # BATTLE COMMAND PASSED
                return self.words[6]

    # RUN BATTLE
    def battle_set(self, player, enemy_index):
        enemy = Enemy(enemy_index)
        print(player.name + " is fighting " + enemy.name + "!")
        while True:
            if player.speed >= enemy.speed:
                goes_first = True
            else:
                goes_first = False

            print(player.name + " HP: " + str(player.hp) + "\n")
            print(enemy.name + " HP: " + str(enemy.hp))

            player_move = self.parse_battle(player)
            enemy_move = enemy.enemy_move()

            if goes_first:
                if not player.process_player_move(player_move, enemy):
                    enemy.give_item(self, player)
                    return True
                if not enemy.process_enemy_move(enemy_move, player):
                    return False
            else:
                if not enemy.process_enemy_move(enemy_move, player):
                    return False
                if not player.process_player_move(player_move, enemy):
                    enemy.give_item(self, player)
                    return True

    # GET ROOM COMMAND (OLD)
    def parse_room(self, room, player):
        while True:
            room.print_room(self)
            self.get_new_string()

            if self.words[7] == 1:
                self.help_me(1)
                continue
            elif self.words[0] == 1:  # "TAKE" COMMAND
                if room.item_index == 0:  # NO ITEM
                    print("No item to take...")
                    continue
                elif self.words[1] == -1:  # INVALID ITEM PASSED
                    print("Didn't understand item's name...")
                    continue
                elif self.words[1] != room.item_index:
                    print("That item isn't here...")
                    continue
                else:  # ITEM PASSED IS GOOD
                    player.inventory.append(room.item_index)  # ADD ITEM TO INVENTORY
                    print(str(self.reverse_lists[1][room.item_index]) + " added to inventory!")
                    room.item_index = 0  # REMOVE ITEM FROM ROOM
                    continue

            elif self.words[0] == 2:  # "MOVE" COMMAND
                return 20 + self.words[2]  # RETURN "MOVE" COMMAND PLUS DIRECTION

            elif self.words[0] == 3:  # "LOOK" COMMAND
                if 0 < self.words[5] < 3:  # OBJECT PASSED IS GOOD
                    if self.words[5] == 1:  # VIEW INVENTORY
                        player.print_inventory(self)
                    elif self.words[5] == 2:  # VIEW PLAYER STATS
                        print(player)
                else:  # INCORRECT OBJECT PASSED
                    print(str(self.words[5]))
                    print("Didn't understand what you wanted to look at...")
                    continue

            elif self.words[0] == 4:  # "SELECT" COMMAND
                if self.words[1] == -1:
                    print("Didn't understand item's name...")
                else:
                    index_in_inventory = self.check_inventory(self.words[1], player.inventory)
                    if index_in_inventory == -1:
                        continue
                    else:
                        item_strength = self.item_strengths[self.words[1]]  # GET ITEM STRENGTH
                        if item_strength <= 0:  # CAN'T USE ITEM IN FIELD
                            print("Can't use that item right now; try again...")
                            continue
                        else:  # APPLY ITEM EFFECT
                            print(str(self.reverse_lists[1][self.words[1]]) + " used!")
                            if 0 < item_strength < 100:  # APPLY TO HP
                                player.hp += item_strength
                            elif 99 < item_strength < 200:  # APPLY TO MP
                                player.mp += item_strength - 100
                            del player.inventory[index_in_inventory]  # REMOVE ITEM FROM INVENTORY

            elif self.words[0] == 5:  # "FIGHT" COMMAND
                if room.enemy_index == 0:  # NO ENEMY
                    print("no enemy to fight...")
                    continue
                else:  # ENEMY PRESENT
                    winner = room.battle_set(self, player)
                    if winner:
                        print("Winner!")
                        room.enemy_index = 0
                    else:
                        print("Game Over!")
                        return 12

            elif self.words[0] == 8:  # "EQUIP" COMMAND
                if self.words[1] != -1:  # PASSED ITEM THROUGH TO COMMAND
                    index_in_inventory = self.check_inventory(self.words[1], player.inventory)
                    if index_in_inventory == -1:
                        continue
                    elif self.words[1] % 4 != 0 and self.words[1] % 5 != 5:
                        print("Cannot equip this item...")
                        continue
                    else:
                        if self.words[1] % 4 == 0:
                            player.weapon = self.words[1]
                            player.attack += player.weapon * 5
                        elif self.words[1] % 5 == 0:
                            player.armor = self.words[1]
                            player.defense = player.armor * 5
                        del player.inventory[index_in_inventory]

            else:  # BAD COMMAND
                print("Didn't understand command; try again...")
                continue

    # GET ROOM COMMAND (JSON)
    def parse_json_room(self, room, player):
        while True:
            self.print_room(room)  # PRINT ROOM CONTENTS
            self.get_new_string()  # GET COMMAND STRING

            if self.words[7] == 1:  # "HELP" COMMAND
                self.help_me(1)
                continue

            elif self.words[0] == 1:  # "TAKE" COMMAND
                if room["item"] == 0:  # NO ITEM
                    print("No item to take...")
                    continue
                elif self.words[1] == -1:  # INVALID ITEM PASSED
                    print("Didn't understand item's name...")
                    continue
                elif self.words[1] != room["item"]:  # ITEM PASSED ISN'T IN ROOM
                    print("That item isn't here...")
                    continue
                else:  # ITEM PASSED IS GOOD
                    player.inventory.append(room["item"])  # ADD ITEM TO INVENTORY
                    print(str(self.reverse_lists[1][room["item"]]) + " added to inventory!")
                    room["item"] = 0  # REMOVE ITEM FROM ROOM
                    continue

            elif self.words[0] == 2:  # "MOVE" COMMAND
                return 20 + self.words[2]  # RETURN "MOVE" COMMAND PLUS DIRECTION

            elif self.words[0] == 3:  # "LOOK" COMMAND
                if 0 < self.words[5] < 3:  # OBJECT PASSED IS GOOD
                    if self.words[5] == 1:  # VIEW INVENTORY
                        player.print_inventory(self)
                    elif self.words[5] == 2:  # VIEW PLAYER STATS
                        print(player)
                else:  # INCORRECT OBJECT PASSED
                    print("Didn't understand what you wanted to look at...")
                    continue

            elif self.words[0] == 4:  # "SELECT" COMMAND
                if self.words[1] == -1:  # BAD ITEM PASSED
                    print("Didn't understand item's name...")
                    continue
                else:  # VALID ITEM PASSED
                    index_in_inventory = self.check_inventory(self.words[1], player.inventory)  # GET INDEX OF ITEM
                    if index_in_inventory == -1:  # ITEM ISN'T IN INVENTORY
                        continue
                    else:
                        item_strength = self.item_strengths[self.words[1]]  # GET ITEM STRENGTH
                        if item_strength <= 0:  # CAN'T USE ITEM IN BATTLE
                            print("Can't use that item right now...")
                            continue
                        else:  # APPLY ITEM EFFECT
                            print(str(self.reverse_lists[1][self.words[1]]) + " used!")
                            if 0 < item_strength < 100:  # APPLY TO HP
                                player.hp += item_strength
                            elif 99 < item_strength < 200:  # APPLY TO MP
                                player.mp += item_strength - 100
                            del player.inventory[index_in_inventory]  # REMOVE ITEM FROM INVENTORY

            elif self.words[0] == 5:  # "FIGHT" COMMAND
                if room["enemy"] == 0:  # NO ENEMY
                    print("No enemy to fight...")
                    continue
                else:  # ENEMY PRESENT
                    winner = self.battle_set(player, room["enemy"])  # GET FIGHT RESULT
                    if winner:  # IF WON
                        print("Winner!")  # ANNOUNCE
                        room["enemy"] = 0  # REMOVE ENEMY FROM ROOM
                    else:  # IF LOST
                        print("Game Over!")  # ANNOUNCE
                        return 12  # RETURN DEAD INDEX

            elif self.words[0] == 8:  # "EQUIP" COMMAND
                if self.words[1] != -1:  # PASSED ITEM THROUGH TO COMMAND
                    index_in_inventory = self.check_inventory(self.words[1], player.inventory)
                    if index_in_inventory == -1:
                        continue
                    elif self.words[1] % 4 != 0 and self.words[1] % 5 != 0:  # CHECK IF ITEM IS ABLE TO BE EQUIPPED
                        print("Cannot equip this item...")
                        continue
                    else:
                        if self.words[1] % 4 == 0:  # IF WEAPON
                            player.weapon = self.words[1]  # EQUIP
                            player.attack += player.weapon * 5  # ALTER STATS
                        elif self.words[1] % 5 == 0:  # IF ARMOR
                            player.armor = self.words[1]  # EQUIP
                            player.defense = player.armor * 5  # ALTER STATS
                        del player.inventory[index_in_inventory]  # REMOVE FROM INVENTORY

            else:  # BAD COMMAND
                print("Didn't understand command...")
                continue

    # PRINT ROOM DETAILS
    def print_room(self, room):
        print("In " + room["name"] + "...")
        print(room["description"])
        if room["item"] == 0:
            print("\tThere isn't an item here...")
        else:
            print("\tThere's a(n) " + str(self.reverse_lists[1][room["item"]]) + "!")
        if room["enemy"] == 0:
            print("\tThere isn't an enemy here...")
        else:
            print("\tThere's an enemy here!")
        if room["doors"]["left"] != -1:
            print("\tCan move left...")
        if room["doors"]["forward"] != -1:
            print("\tCan move forward...")
        if room["doors"]["right"] != -1:
            print("\tCan move right...")
        if room["doors"]["backward"] != -1:
            print("\tCan move backward...")


    # CHECK IF ITEM IS IN INVENTORY
    @staticmethod
    def check_inventory(item_index, inventory):
        index_in_inventory = -1
        for index in range(len(inventory)):
            if item_index == inventory[index]:
                index_in_inventory = index
        if index_in_inventory == -1:
            print("Item isn't in inventory...")
        return index_in_inventory

    # HELP ME FUNCTION
    @staticmethod
    def help_me(mode):
        # MODES
        # 1 -> FIELD
        # 2 -> BATTLE
        if mode == 1:
            print("POSSIBLE COMMANDS\n\tTAKE + ITEM IN ROOM\n\tMOVE + DIRECTION\n\tVIEW + INVENTORY/STATS\n\t"
                  "USE/SELECT + ITEM IN INVENTORY\n\tFIGHT")
        elif mode == 2:
            print("POSSIBLE COMMANDS IN BATTLE\n\tVIEW + INVENTORY/STATS\n\tUSE/SELECT + ITEM IN INVENTORY\n\t"
                  "BATTLE COMMAND")
