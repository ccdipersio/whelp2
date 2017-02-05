from random import randrange


class Character:
    """A placeholder class for Player and Enemy to inherit.

    Attributes:
        jobs: A dictionary of possible job (think RPG classes) settings for both the player character and enemy
            characters
    """

    jobs = {
        1: 'WARRIOR',
        2: 'MAGE',
        3: 'KNIGHT',
        4: 'SAGE',
        5: 'GOBLIN',
        6: 'ORC',
        7: 'OGRE',
        8: 'DRAGON',
    }


class Player(Character):
    """The class for the player character.

    Besides functions to initialize and an override to print specific details, this also deals with the player's inventory
        and the player's commands in a battle.
    """

    def __init__(self):
        """Initializes the player character's various stats and job and zeroes out inventory, weapon and armor."""
        self.name = input("Name: ").upper()
        self.hp = randrange(65, 101)
        self.mp = randrange(65, 101)
        self.attack = randrange(1, 11)
        self.defense = randrange(1, 11)
        self.magic_attack = randrange(1, 11)
        self.magic_defense = randrange(1, 11)
        self.speed = randrange(1, 11)
        self.evasion = randrange(1, 11)
        self.accuracy = randrange(1, 11)
        self.level = 1
        self.experience_points = 0

        self.inventory = []
        self.weapon = 0
        self.armor = 0

        job_input_string = ""
        while not job_input_string.isdigit() or int(job_input_string) < 1 or int(job_input_string) > 4:
            job_input_string = input("1 - Warrior\n2 - Mage\n3 - Knight\n4 - Sage\n\tChoice: ")
        job_input = int(job_input_string)
        self.job = self.jobs[job_input]
        if job_input == 1:
            self.attack += 5
            self.hp += 15
        elif job_input == 2:
            self.magic_attack += 5
            self.mp += 15
        elif job_input == 3:
            self.defense += 5
        elif job_input == 4:
            self.magic_defense += 5
            self.mp += 15

    def __str__(self):
        return "\nName: " + self.name + "\nJob: " + self.job + "\nHP: " + str(self.hp) + "\nMP: " + str(
            self.mp) + "\nAttack: " + str(self.attack) + "\nDefense: " + str(
            self.defense) + "\nMagic Attack: " + str(
            self.magic_attack) + "\nMagic Defense: " + str(self.magic_defense) + "\nSpeed: " + str(
            self.speed) + "\nEvasion: " + str(self.evasion) + "\n"

    def print_inventory(self, parser):
        if len(self.inventory) == 0:
            print("Inventory is empty!")
        else:
            print("Inventory:")
            for item_index in self.inventory:
                print("\t" + parser.reverse_lists[1][item_index])

    def process_player_move(self, player_move, enemy):
        """Applies the player's battle command choice to either the player or the enemy.

        Args:
            player_move: An integer referring to the player's desired move. Less than 0 is an item that harms the enemy.
                One is a physical attack. Two is a magic attack. Greater than 2 is an item that heals the player.
            enemy: The instance of the Enemy character class

        Returns:
            False if the enemy's HP is zero.
            True if the enemy's HP is greater than zero.
        """
        if player_move < 0 or player_move == 1 or player_move == 2:
            if 0 > player_move > -100:
                enemy.hp += player_move
            elif -99 > player_move > -200:
                enemy.mp -= player_move + 100
            else:
                if player_move == 1:
                    enemy.hp -= self.attack
                else:
                    enemy.hp -= self.magic_attack
        elif 2 < player_move < 100:
            self.hp += player_move
        else:
            self.mp += player_move - 100
        if enemy.hp <= 0:
            return False
        else:
            return True


class Enemy(Character):
    """The class for the enemy character.

    Besides functions to initialize and an override to print specific details, this also deals with determining what the
        enemy's move will be in a battle and passing off items to the player if the enemy is defeated.
    """

    def __init__(self, enemy_index):
        """Initializes the enemy character based on enemy_index and sets exact stats based on enemy_index.

        Args:
            enemy_index: An integer which must be 5 or higher that is used to reference back to the jobs dictionary in
                the parent class
        """
        self.name = self.jobs[enemy_index]
        self.job = self.name

        if self.name == 'GOBLIN':
            self.hp = 10
            self.mp = 0
            self.attack = 3
            self.defense = 1
            self.magic_attack = 0
            self.magic_defense = 1
            self.speed = 3
            self.evasion = 2
            self.accuracy = 4
            self.experience_to_pass = 10
            self.item_held = randrange(1, 4)
        elif self.name == 'ORC':
            self.hp = 15
            self.mp = 5
            self.attack = 5
            self.defense = 2
            self.magic_attack = 5
            self.magic_defense = 2
            self.speed = 4
            self.evasion = 4
            self.accuracy = 6
            self.experience_to_pass = 15
            self.item_held = randrange(1, 4)
        elif self.name == 'OGRE':
            self.hp = 20
            self.mp = 8
            self.attack = 7
            self.defense = 4
            self.magic_attack = 0
            self.magic_defense = 3
            self.speed = 5
            self.evasion = 5
            self.accuracy = 8
            self.experience_to_pass = 20
            self.item_held = randrange(1, 4)
        elif self.name == 'DRAGON':
            self.hp = 30
            self.mp = 10
            self.attack = 15
            self.defense = 10
            self.magic_attack = 18
            self.magic_defense = 10
            self.speed = 10
            self.evasion = 8
            self.accuracy = 12
            self.experience_to_pass = 40
            self.item_held = randrange(1, 6)

    def enemy_move(self):
        """Determines what the enemy's move will be in a battle.

        The entire goal here is to choose which attacking value is best. If both attacking values aren't zero, a roll is
            performed by adding both attacking values together, generating a random number between 1 and that resulting
            number, and determining if it is lower than the lowest of the two attacking values.

        Returns:
            One for a physical attack or two for a magic attack.
        """
        if self.attack != 0 and self.magic_attack == 0:
            return 1
        elif self.magic_attack != 0 and self.attack == 0:
            return 2
        else:
            attack_denominator = self.attack + self.magic_attack
            attack_selector = randrange(1, attack_denominator + 1)
            if self.magic_attack <= self.attack:
                lowest_attack_value = self.magic_attack
                lowest_attack_type = 2
            else:
                lowest_attack_value = self.attack
                lowest_attack_type = 1
            if attack_selector <= lowest_attack_value:
                return lowest_attack_type
            else:
                if lowest_attack_type == 1:
                    return 2
                else:
                    return 1

    def process_enemy_move(self, enemy_move, player):
        """Applies the enemy's battle command choice to either the player.

        Args:
            enemy_move: An integer referring to the enemy's move. One is a physical attack. Two is a magic attack.
            player: The instance of the Player character class

        Returns:
            False if the player's HP is zero.
            True if the player's HP is greater than zero.
        """
        if enemy_move == 1:  # PHYSICAL ATTACK
            player.hp -= self.attack
        else:  # MAGIC ATTACK
            player.hp -= self.magic_attack
        if player.hp <= 0:  # PLAYER DIED
            return False
        else:
            return True

    def give_item(self, parser, player):
        if self.item_held == 0:
            print(self.name + " doesn't have an item to take!")
        else:
            player.inventory.append(self.item_held)
            print(str(parser.reverse_lists[1][self.item_held]) + " taken!")
