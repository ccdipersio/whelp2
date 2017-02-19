<b>whelp2</b>
"whelp2" is the Python component of my coding sample for my University of Washington application for the master’s degree program in Computational Linguistics.

The program itself is a text parser placed in the context of a text adventure game. The design of the dungeon through which the player can move using the test parser can either be the default one or it can be user-generated. This generation can either be done by using the builtin generator function or simply by editing the default JSON file. One important note is the generator function won’t check if the doors in the dungeon actually line up properly meaning the player may be able to move from room 1 to 2 but not back from room 2 to 1 if the user doesn’t make it that way.

Usable commands in the text parser can be found in each of the applicable text files. The language can also be extended from within each one because they are loaded into the function upon the TextParser object’s initialization. 
