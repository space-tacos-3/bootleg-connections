This is a study project that attempts to recreate New York Times' [Connections](https://www.nytimes.com/games/connections) puzzle in Python using the [pygame](https://github.com/pygame/pygame) library.
The first two chapters of Albert Sweigart's "[Making Games with Python and Pygame](https://inventwithpython.com/pygame/)" were a tremendous help.
The background track is "[One Note Sampo](https://www.youtube.com/watch?v=P82Qv74xYIs)" by Carioca.

## Installation
Requires Python >=3.10 (Windows users can use Python >=3.6, see below).
* Clone or download the repository
* Install the dependencies with
```
pip install -r requirements.txt
```
* Launch connections.py

Windows users will have issues with the [pygame_emojis](https://github.com/ScienceGamez/pygame_emojis) package that is used to render emojis in the game. There's no problem with installing it, but it will most likely crash on import due to not loading up libcairo-2.dll. The workarounds are [insane](https://stackoverflow.com/questions/73637315/oserror-no-library-called-cairo-2-was-found-from-custom-widgets-import-proje) and are too much to account for in a project like this (not to mention that they still don't fix the issue on my machine). So Windows users can skip installing pygames_emojis from the requirements.txt file and just launch connections_win.py. That version of the game renders emojis the way pygame can by default: in black and white 🤷.

## Few things of note
This is a study project, and knowing what I do now about the intricacies of game state tracking and rendering, I'd change a number of things in the code. As is it's quite messy. The comments inside try to make sense of it and point out some awkward bits.

This also wasn't meant to be a feature-complete clone of the original puzzle (God knows the NYT engineers are better at this than I am). That being said, there are a few things that *could* be added here that I won't add myself:
* Fix this whole emoji thing
* Write a puzzle update function that grabs the information from [this handy repository](https://github.com/Eyefyre/NYT-Connections-Answers)
* A mute button for the music
* An internal database for keeping track of solved puzzles between sessions
* A menu for proper puzzle selection in addition to the existing randomizer
* A text message for when the player is one word away from a correct answer

A very silly idea that I did not end up trying out:
* A mode wherein you take turns against an AI opponent who has a random chance of opening up one of the categories
