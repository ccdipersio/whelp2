from random import randrange


class Character:

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

    # INITIALIZATION FUNCTION
    def __init__(self):
        # SET STATS
        self.name = input("Name: ").upper()  # GET NAME
        self.hp = randrange(65, 101)  # SET HP
        self.mp = randrange(65, 101)  # SET MP
        self.attack = randrange(1, 11)  # SET ATTACK
        self.defense = randrange(1, 11)  # SET DEFENSE
        self.magic_attack = randrange(1, 11)  # SET MAGIC_ATTACK
        self.magic_defense = randrange(1, 11)  # SET MAGIC_DEFENSE
        self.speed = randrange(1, 11)  # SET SPEED
        self.evasion = randrange(1, 11)  # SET EVASION
        self.accuracy = randrange(1, 11)  # SET ACCURACY
        self.level = 1  # SET INITIAL LEVEL
        self.experience_points = 0  # ZERO OUT EXPERIENCE POINTS

        self.inventory = []
        self.weapon = 0
        self.armor = 0

        # SET JOB
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

    # PRINTER
    def __str__(self):
        return "\nName: " + self.name + "\nJob: " + self.job + "\nHP: " + str(self.hp) + "\nMP: " + str(
            self.mp) + "\nAttack: " + str(self.attack) + "\nDefense: " + str(
            self.defense) + "\nMagic Attack: " + str(
            self.magic_attack) + "\nMagic Defense: " + str(self.magic_defense) + "\nSpeed: " + str(
            self.speed) + "\nEvasion: " + str(self.evasion) + "\n"

    # PRINT INVENTORY
    def print_inventory(self, parser):
        if len(self.inventory) == 0:
            print("Inventory is empty!")
        else:
            print("Inventory:")
            for item_index in self.inventory:
                print("\t" + parser.reverse_lists[1][item_index])

    # PROCESS PLAYER MOVE FOR BATTLES
    def process_player_move(self, player_move, enemy):
        if player_move < 0 or player_move == 1 or player_move == 2:  # DAMAGE MOVES
            if 0 > player_move > -100:  # APPLY ITEM DAMAGE TO ENEMY HP
                enemy.hp += player_move
            elif -99 > player_move > -200:  # APPLY ITEM DAMAGE TO ENEMY MP
                enemy.mp -= player_move + 100
            else:
                if player_move == 1:
                    enemy.hp -= self.attack
                else:
                    enemy.hp -= self.magic_attack
        elif 2 < player_move < 100:  # APPLY ITEM HEAL TO PLAYER HP
            self.hp += player_move
        else:  # APPLY ITEM HEAL TO PLAYER MP
            self.mp += player_move - 100
        if enemy.hp <= 0:  # ENEMY DIED
            return False
        else:
            return True


class Enemy(Character):

    # INITIALIZATION FUNCTION
    def __init__(self, enemy_index):
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


    # GET ENEMY MOVE FOR BATTLES
    def enemy_move(self):
        if self.attack != 0 and self.magic_attack == 0:  # ONLY PHYSICAL ATTACK
            return 1
        elif self.magic_attack != 0 and self.attack == 0:  # ONLY MAGIC ATTACK
            return 2
        else:
            attack_denominator = self.attack + self.magic_attack  # CREATE DENOMINATOR FROM ATTACK VALUES
            attack_selector = randrange(1, attack_denominator + 1)  # FIND RANDOM NUMBER USING DENOMINATOR
            if self.magic_attack <= self.attack:  # FIND LOWEST ATTACKING VALUE
                lowest_attack_value = self.magic_attack
                lowest_attack_type = 2
            else:
                lowest_attack_value = self.attack
                lowest_attack_type = 1
            if attack_selector <= lowest_attack_value:  # IF ATTACK SELECTED IS LOWEST VALUE
                return lowest_attack_type
            else:  # IF ATTACK SELECTED IS HIGHEST VALUE
                if lowest_attack_type == 1:
                    return 2
                else:
                    return 1

    # PROCESS ENEMY MOVE FOR BATTLES
    def process_enemy_move(self, enemy_move, player):
        if enemy_move == 1:  # PHYSICAL ATTACK
            player.hp -= self.attack
        else:  # MAGIC ATTACK
            player.hp -= self.magic_attack
        if player.hp <= 0:  # PLAYER DIED
            return False
        else:
            return True

    # PASS ITEM TO PLAYER
    def give_item(self, parser, player):
        if self.item_held == 0:
            print(self.name + " doesn't have an item to take!")
        else:
            player.inventory.append(self.item_held)
            print(str(parser.reverse_lists[1][self.item_held]) + " taken!")
