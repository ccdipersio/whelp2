from TextParser import *
from CharacterUtils import *
from json_RoomUtils import *

#TESTING

parser = TextParser()
player = Player()
dungeon = Dungeon()
dungeon.dungeon_control(parser, player)