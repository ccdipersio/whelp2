from TextParser import *
from CharacterUtils import *
from json_RoomUtils import *

'''
parser = TextParser()

parser.get_new_string()
print(parser.words)

player = Player()
player.inventory.append(1)
player.inventory.append(2)

enemy = Enemy(5)

battle = BattleScene(parser, player, enemy)

parser.close_files()


parser = TextParser()
player = Player()
maze = Dungeon()
maze.dungeon_control(parser, player)
'''

parser = TextParser()
player = Player()
dungeon = Dungeon()
dungeon.dungeon_control(parser, player)