from CharacterUtils import *
import os


class TextParser:
    """The TextParser object"""

    def __init__(self):
        """Initializes the TextParser object.

        This creates several dictionaries for use in the object on the whole, they are:
            files: A list of file names from which to load words.
            lists: A dictionary of dictionaries which are words and their indexes for the TextParser to process.
            reverse_lists: The same as the lists dictionary but instead of the key being the word and the index the
                value, it's reversed, so the index can be used to look up the word.
            words: A dictionary to save the word indexes from the user-given string
        The order of the word lists is vitally important as it's mirrored across all four lists/dictionaries listed
            above. That order is as follows:
                0: Verbs
                1: Items
                2: Directions
                3: Quantities
                4: Locations
                5: Objects
                6: Battle Commands
        The words dictionary adds 2 more entries: 7: Help Command and 8: Equip Command.
        Finally, one last dictionary is created for item strengths. Once all this is done, the files are opened and
        their contents are dumped into lists, reverse_lists, and item_strengths.
        """
        relative_path = os.path.dirname(__file__)
        lib = "LibraryFiles"

        self.files = [
            "verbs",
            "items",
            "directions",
            "quantities",
            "locations",
            "objects",
            "battle_commands"
        ]
        self.lists = {
            0: {},
            1: {},
            2: {},
            3: {},
            4: {},
            5: {},
            6: {},
        }
        self.reverse_lists = {
            0: {},
            1: {},
            2: {},
            3: {},
            4: {},
            5: {},
            6: {},
        }
        self.words = {
            0: -1,
            1: -1,
            2: -1,
            3: -1,
            4: -1,
            5: -1,
            6: -1,
            7: -1,
            8: -1,
        }
        self.item_strengths = {}

        for index in range(len(self.files)):
            with open(os.path.join(relative_path, lib, self.files[index]), "r") as file:
                for line in file:
                    line = line.strip()
                    split_line = line.split(",")
                    self.lists[index][split_line[0]] = int(split_line[1])
                    self.reverse_lists[index][int(split_line[1])] = split_line[0]
                    if index == 1:
                        self.item_strengths[int(split_line[1])] = int(split_line[2])

    def reset_words(self):
        """Clears out the words in the words dictionary to prep the TextParser for new input."""
        for index in range(len(self.words)):
            self.words[index] = -1

    def get_new_string(self):
        """Resets the words dictionary, asks for a new string, splits it along spaces, and passes it to parse_words"""
        self.reset_words()
        input_string = input("\nCommand: ").lower()
        split_string = input_string.split(" ")
        self.parse_words(split_string)

    def parse_words(self, split_string):
        """Runs through the words in the split_string list and attempts to match them to entries in the lists dictionary
            if a match is found, the current word's index from the lists dictionary is saved in the words dictionary.

        Args:
            split_string: List of user-defined words passed in from get_new_string
        """
        for word in split_string:
            if word == "help":
                self.words[7] = 1
                return
            for index in range(len(self.lists)):
                for key in self.lists[index]:
                    if word == key:
                        self.words[index] = self.lists[index][key]

    def parse_battle(self, player):
        """Determines the player's desired battle command based on parsing from get_new_string.

        Args:
            player: The instance of the Player character object.

        Returns:
            Index of the battle command from words[6] or the strength of the item if an item was used.
        """
        while True:
            print("Use SWORD, SPELL, or ITEM?")
            self.get_new_string()

            if self.words[7] == 1:
                self.help_me(2)
                continue
            elif self.words[6] == -1:
                if self.words[0] != 3 and self.words[0] != 4:
                    print("Can't use this command in battle; try again...")
                    continue
                else:
                    if self.words[0] == 3:
                        if self.words[5] != 1:
                            print("Didn't understand what you want to select or view; try again...")
                            continue
                        else:
                            player.print_inventory(self)
                            continue
                    if self.words[0] == 4:
                        if self.words[1] == -1:
                            print("Didn't understand the item; try again...")
                            continue
                        else:
                            index_in_inventory = self.check_inventory(self.words[1], player.inventory)
                            if index_in_inventory == -1:
                                continue
                            else:
                                item_strength = self.item_strengths[self.words[1]]
                                if item_strength == 0:
                                    print("Can't use that item in battle; try again...")
                                    continue
                                else:
                                    print(str(self.reverse_lists[1][self.words[1]]) + " used!")
                                    del player.inventory[index_in_inventory]
                                    return item_strength
            else:
                return self.words[6]

    def battle_set(self, player, enemy_index):
        """Runs the battle.

        Args:
            player: The instance of the Player character object.
            enemy_index: Integer index of the desired enemy to fight.

        Returns:
            True is player character lives. False if player character died.
        """
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

    def parse_json_room(self, room, player):
        """Determines the player's desired action with the room context. The function is called parse_json_room to
            differentiate it from parse_room which is an older version of the function implemented before a JSON array
            was used for the dungeon file. The old function is now located in OldComponents/Random\ Pieces\ of\ Old\
            Code.txt.

        Args:
            room: Current room dictionary passed in from dungeon_control.
            player: The instance of the Player character object.

        Returns: An integer which will either be 20 to 23 for movement commands or 12 if the player character died.
        """
        while True:
            self.print_room(room)
            self.get_new_string()

            if self.words[7] == 1:
                self.help_me(1)
                continue

            elif self.words[0] == 1:
                if room["item"] == 0:
                    print("No item to take...")
                    continue
                elif self.words[1] == -1:
                    print("Didn't understand item's name...")
                    continue
                elif self.words[1] != room["item"]:
                    print("That item isn't here...")
                    continue
                else:
                    player.inventory.append(room["item"])
                    print(str(self.reverse_lists[1][room["item"]]) + " added to inventory!")
                    room["item"] = 0
                    continue

            elif self.words[0] == 2:
                return 20 + self.words[2]

            elif self.words[0] == 3:
                if 0 < self.words[5] < 3:
                    if self.words[5] == 1:
                        player.print_inventory(self)
                    elif self.words[5] == 2:
                        print(player)
                else:
                    print("Didn't understand what you wanted to look at...")
                    continue

            elif self.words[0] == 4:
                if self.words[1] == -1:
                    print("Didn't understand item's name...")
                    continue
                else:  # VALID ITEM PASSED
                    index_in_inventory = self.check_inventory(self.words[1], player.inventory)
                    if index_in_inventory == -1:
                        continue
                    else:
                        item_strength = self.item_strengths[self.words[1]]
                        if item_strength < 0:
                            print("Can't use that item right now...")
                            continue
                        else:
                            if self.words[1] == 3:
                                if self.words[5] != 3:
                                    print("Can only use a key on a door...")
                                    continue
                                elif self.words[2] == -1:
                                    print("Need to specify a which door on which to use the key...")
                                    continue
                                elif room["doors"][self.convert_integer_to_direction(self.words[2]) + "_locked"] == 0:
                                    print("This door isn't locked...")
                                    continue
                                else:
                                    print(self.convert_integer_to_direction(self.words[2]) + " door is unlocked!")
                                    room["doors"][self.convert_integer_to_direction(self.words[2]) + "_locked"] = 0
                                    del player.inventory[index_in_inventory]

                            elif self.words[1] % 4 == 0 or self.words[1] % 5 == 0:
                                print("Must equip " + str(self.reverse_lists[1][self.words[1]]) + "...")
                                continue

                            else:
                                print(str(self.reverse_lists[1][self.words[1]]) + " used!")
                                if 0 < item_strength < 100:
                                    player.hp += item_strength
                                elif 99 < item_strength < 200:
                                    player.mp += item_strength - 100
                                del player.inventory[index_in_inventory]

            elif self.words[0] == 5:
                if room["enemy"] == 0:
                    print("No enemy to fight...")
                    continue
                else:
                    winner = self.battle_set(player, room["enemy"])
                    if winner:
                        print("Winner!")
                        room["enemy"] = 0
                    else:
                        print("Game Over!")
                        return 12

            elif self.words[0] == 8:
                if self.words[1] != -1:
                    index_in_inventory = self.check_inventory(self.words[1], player.inventory)
                    if index_in_inventory == -1:
                        continue
                    elif self.words[1] % 4 != 0 and self.words[1] % 5 != 0:
                        print("Cannot equip this item...")
                        continue
                    else:
                        if self.words[1] % 4 == 0:
                            if player.weapon != 0:
                                player.attack -= player.weapon * 5
                                player.inventory.append(player.weapon)
                                player.weapon = self.words[1]
                                player.attack += player.weapon * 5
                            else:
                                player.weapon = self.words[1]
                                player.attack += player.weapon * 5
                        elif self.words[1] % 5 == 0:
                            if player.armor != 0:
                                player.defense -= player.armor * 5
                                player.inventory.append(player.armor)
                                player.armor = self.words[1]
                                player.defense += player.armor * 5
                            else:
                                player.armor = self.words[1]
                                player.defense += player.armor * 5
                        del player.inventory[index_in_inventory]

            else:
                print("Didn't understand command...")
                continue

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
        door_index = 0
        while door_index < 4:
            if room["doors"][self.convert_integer_to_direction(door_index)] != -1:
                if room["doors"][self.convert_integer_to_direction(door_index)] < room["index"]:
                    print("\tCan move " + self.convert_integer_to_direction(door_index) + " back a room...")
                else:
                    print("\tCan move " + self.convert_integer_to_direction(door_index) + " forward a room...")
            door_index += 1

    @staticmethod
    def check_inventory(item_index, inventory):
        index_in_inventory = -1
        for index in range(len(inventory)):
            if item_index == inventory[index]:
                index_in_inventory = index
        if index_in_inventory == -1:
            print("Item isn't in inventory...")
        return index_in_inventory

    @staticmethod
    def help_me(mode):
        if mode == 1:
            print("POSSIBLE COMMANDS\n\tTAKE + ITEM IN ROOM\n\tMOVE + DIRECTION\n\tVIEW + INVENTORY/STATS\n\t"
                  "USE/SELECT + ITEM IN INVENTORY\n\tFIGHT")
        elif mode == 2:
            print("POSSIBLE COMMANDS IN BATTLE\n\tVIEW + INVENTORY/STATS\n\tUSE/SELECT + ITEM IN INVENTORY\n\t"
                  "BATTLE COMMAND")

    @staticmethod
    def convert_integer_to_direction(direction_index):
        if direction_index == 0:
            return "left"
        elif direction_index == 1:
            return "forward"
        elif direction_index == 2:
            return "right"
        elif direction_index == 3:
            return "backward"
