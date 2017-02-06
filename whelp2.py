from TextParser import *
from CharacterUtils import *
from json_RoomUtils import *
from CreateDungeonUtils import *


def run_game():
    """This is the general controller function to run the game.
    First, it generates the TextParser and Player character. Second, it gives a choice to either run with default
        options or run a DungeonCreator.
    """
    parser = TextParser()
    player = Player()

    choice = ""
    while not choice.isdigit() or int(choice) < 1 or int(choice) > 2:
        choice = input("(1) Run with default Dungeon settings or (2) Generate Dungeon? (1/2): ")

    if int(choice) == 1:
        dungeon = Dungeon("")
        if dungeon.json_dungeon is not None:
            dungeon.dungeon_control(parser, player)
    else:
        dungeon_creator = DungeonCreator()
        file_name = dungeon_creator.generate_dungeon(parser, player)
        dungeon = Dungeon(os.path.join(os.path.dirname(__file__), "UserDefinedFiles", file_name))
        if dungeon.json_dungeon is not None:
            dungeon.dungeon_control(parser, player)

run_game()
