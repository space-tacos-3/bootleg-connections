import pygame, sys, random, pyperclip
from pygame.locals import *
import pygame.freetype
#from pygame_emojis import load_emoji

pygame.init()

# Running the game in 60 frames per second
FPS = 60
fpsClock = pygame.time.Clock()

# The game will be displayed in a 1000x700 window.
DISPLAYSURF = pygame.display.set_mode((1000, 700))
pygame.display.set_caption('Bootleg Connections')

# Basic colors with their RGB values. Both the variables and the dictionary are used, which is smth that needs fixing.
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (128,128,128)
BEIGE = (245,245,220)
GREEN = (0,255,0)
BLUE = (0,0,128)
YELLOW = (255,255,0)
PURPLE = (255,0,255)

colors = {
    'White': (255,255,255),
    'Black': (0,0,0),
    'Gray': (190,190,190),
    'Beige': (245,245,220),
    'Green': (49,255,43),
    'Blue': (43,126,255),
    'Yellow': (255,245,43),
    'Purple': (175,43,255)
}

# Width and height of the basic buttons.
box_width=200
box_height=100

BASICFONT = pygame.font.SysFont('helveticaneue', 26)
seguisy64 = pygame.freetype.SysFont("segoeuisymbol", 64)
seguisy32 = pygame.freetype.SysFont("segoeuisymbol", 32)
#BASICFONT = pygame.font.Font('/Library/Fonts/Arial Unicode.ttf', 20)

# All the puzzles are stored in a .txt file
# We parse the file in blocks separated by a new line.
# The puzzles are added to a dictionary.
def parsePuzzles():
    puzzle_file = open('puzzles.txt', encoding='utf8')
    puzzles = {}
    current_puzzle = []

    for line in puzzle_file:
        if not line.strip():
            header = current_puzzle[0]
            yellow_group = (current_puzzle[1].split(': ')[0][2:], current_puzzle[1].split(': ')[1].split(', '))
            green_group = (current_puzzle[2].split(': ')[0][2:], current_puzzle[2].split(': ')[1].split(', '))
            blue_group = (current_puzzle[3].split(': ')[0][2:], current_puzzle[3].split(': ')[1].split(', '))
            purple_group = (current_puzzle[4].split(': ')[0][2:], current_puzzle[4].split(': ')[1].split(', '))
            puzzles[header] = {'Yellow': yellow_group, 'Green': green_group, 'Blue': blue_group, 'Purple': purple_group}
            current_puzzle = []
        elif line.strip():
            current_puzzle.append(line.strip())

    return puzzles

# We choose a random puzzle using the random library.
# We store all the important information about the current puzzle in separate variables for ease of access.
def choosePuzzle(puzzles):
    rand_puzzle = random.choice(list(puzzles.keys()))
    #rand_puzzle = 'Connections December 6, 2024'
    puzzle_title = rand_puzzle
    categories = {'Yellow':puzzles[rand_puzzle]['Yellow'][0],
                  'Green':puzzles[rand_puzzle]['Green'][0],
                  'Blue':puzzles[rand_puzzle]['Blue'][0],
                  'Purple':puzzles[rand_puzzle]['Purple'][0],
                  }
    yellow_words = puzzles[rand_puzzle]['Yellow'][1]
    green_words = puzzles[rand_puzzle]['Green'][1]
    blue_words = puzzles[rand_puzzle]['Blue'][1]
    purple_words = puzzles[rand_puzzle]['Purple'][1]

    return puzzle_title, categories, yellow_words, green_words, blue_words, purple_words

# Main function that updates the state of the board on every frame.
def drawBoard(puzzle_title, wordlist, chosen_boxes, solved_rows, categories, mistakes, player_moves, admire):
    x = 90
    y = 120

    # If the player has already solved one (or more) categories, we need to draw a big rectangle.
    # The create textSurf objects on top of it to show the category names and the words in each category.
    if len(solved_rows) > 0:
        for i, row in enumerate(solved_rows):
            pygame.draw.rect(DISPLAYSURF, colors[row[0]], (x,y+((box_height+5)*i),box_width*4+30,box_height))
            words = ', '.join(row[1])
            textSurf = BASICFONT.render(categories[row[0]], True, BLACK)
            textRect = textSurf.get_rect()
            textRect.center = x+415, y+(box_height+5)*i+25
            DISPLAYSURF.blit(textSurf, textRect)
            textSurf = BASICFONT.render(words, True, BLACK)
            textRect = textSurf.get_rect()
            textRect.center = x+415, y+(box_height+5)*i+75
            DISPLAYSURF.blit(textSurf, textRect)

    # The main loop for drawing the 4x4 button grid.
    # We use the number of solved categories to shift the starting y value.
    # We also draw less buttons depending on how many solved rows there are (so we draw a 4x3 grid, then 4x2, then 4x1).
    # The text content of the buttons is grabbed from the 'wordlist' list. This list only has as many words as there are left to guess, so we can just grab the info with each buttons index in the grid.
    # If the player has chosen one of the buttons, we draw a second rectangle on top of it, but in a different color (gray).
    for boxx in range(4):
        for boxy in range(len(solved_rows),4):
            box_color = WHITE
            boxy = boxy
            if (boxx, boxy) in chosen_boxes:
                box_color = GRAY
            pygame.draw.rect(DISPLAYSURF, box_color, (x+((box_width+10)*boxx),y+((box_height+5)*boxy),box_width,box_height))
            textSurf = BASICFONT.render(wordlist[boxx+boxy*4-(len(solved_rows)*4)], True, BLACK)
            textRect = textSurf.get_rect()
            textRect.center = x+(box_width+10)*boxx+100, y+(box_height+5)*boxy+50
            DISPLAYSURF.blit(textSurf, textRect)
    
    # We create several textSurf objects that show the date of the puzzle, remaining lives and the text on the buttons outside of the main 4x4 grid (Submit guess and Next puzzle).
    textSurf = BASICFONT.render(puzzle_title, True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = 500, 55
    DISPLAYSURF.blit(textSurf, textRect)

    pygame.draw.rect(DISPLAYSURF, WHITE, (400,550,box_width+10,box_height))
    textSurf = BASICFONT.render('Submit', True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = 505, 600
    DISPLAYSURF.blit(textSurf, textRect)

    #textSurf = load_emoji('❤️', (64,64))
    textSurf, textRect = seguisy64.render('❤', BLACK)
    #textRect = textSurf.get_rect()
    textRect.center = 120, 600
    DISPLAYSURF.blit(textSurf, textRect)
    textSurf = BASICFONT.render(str(4-mistakes), True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = 180, 600
    DISPLAYSURF.blit(textSurf, textRect)

    pygame.draw.rect(DISPLAYSURF, WHITE, (720,550,box_width,box_height))
    textSurf = BASICFONT.render('Next puzzle', True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = 825, 600
    DISPLAYSURF.blit(textSurf, textRect)

    # If the puzzle is solved we call another function to draw a window with the results.
    # Different function if the player lost.
    if len(solved_rows) == 4 and admire==False:
        drawResults(player_moves)

    if mistakes == 4 and admire==False:
        drawGameOver(player_moves)

# The results window shows all the player moves as emojis. Emojis are loaded using the pygame_emojis library.
# The window has two buttons. One copies the player history so that they can share them (as emojis).
# The other button closes the window.
def drawResults(player_moves):
    pygame.draw.rect(DISPLAYSURF, WHITE, (290,80,box_width*2+20,box_height*4+55))
    pygame.draw.rect(DISPLAYSURF, BLACK, (290,80,box_width*2+20,box_height*4+55), 2)
    textSurf = BASICFONT.render('You won!', True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = 500, 110
    DISPLAYSURF.blit(textSurf, textRect)
    for i, move in enumerate(player_moves.split('\n')):
        for j, emoji in enumerate(move):
            #textSurf = load_emoji(emoji, (32,32))
            #textRect = textSurf.get_rect()
            textSurf, textRect = seguisy32.render(emoji, BLACK)
            textRect.center = 412+35*(j+1), 120+30*(i+1)
            DISPLAYSURF.blit(textSurf, textRect)
    pygame.draw.rect(DISPLAYSURF, BEIGE, (300,400,box_width-10,box_height))
    textSurf = BASICFONT.render('Copy', True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = 395, 450
    DISPLAYSURF.blit(textSurf, textRect)
    pygame.draw.rect(DISPLAYSURF, BEIGE, (510,400,box_width-10,box_height))
    textSurf = BASICFONT.render('Close', True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = 605, 450
    DISPLAYSURF.blit(textSurf, textRect)

def drawGameOver(player_moves):
    pygame.draw.rect(DISPLAYSURF, WHITE, (290,80,box_width*2+20,box_height*4+55))
    pygame.draw.rect(DISPLAYSURF, BLACK, (290,80,box_width*2+20,box_height*4+55), 2)
    textSurf = BASICFONT.render('You lost!', True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = 500, 110
    DISPLAYSURF.blit(textSurf, textRect)
    for i, move in enumerate(player_moves.split('\n')):
        for j, emoji in enumerate(move):
            #textSurf = load_emoji(emoji, (32,32))
            #textRect = textSurf.get_rect()
            textSurf, textRect = seguisy32.render(emoji, BLACK)
            textRect = textSurf.get_rect()
            textRect.center = 412+35*(j+1), 120+30*(i+1)
            DISPLAYSURF.blit(textSurf, textRect)
    #300-490, 400-500
    pygame.draw.rect(DISPLAYSURF, BEIGE, (300,400,box_width-10,box_height))
    textSurf = BASICFONT.render('Copy', True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = 395, 450
    DISPLAYSURF.blit(textSurf, textRect)
    #510-700, 400-500
    pygame.draw.rect(DISPLAYSURF, BEIGE, (510,400,box_width-10,box_height))
    textSurf = BASICFONT.render('Close', True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = 605, 450
    DISPLAYSURF.blit(textSurf, textRect)

def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (200 + 10) + 90
    top = boxy * (100 + 5) + 120
    return (left, top)

# This function receives the current mouse coordinates and returns a tuple with the type of the button that the mouse hovers over (if any).
# If the mouse is over one of the buttons in the main 4x4 grid, we also return the top left coordinates of that button.
# The fact that we use different methods for these two cases is something that could use fixing.
def getBoxAtPixel(x, y, solved_rows):
    for boxx in range(4):
        for boxy in range(len(solved_rows),4):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, 200, 100)
            if boxRect.collidepoint(x, y):
                return ('word', (boxx, boxy))
    if 400 <= x <= 610 and 550 <= y <= 650:
        return ('submit', None)
    if 400 <= x <= 610 and 400 <= y <= 500:
        return ('copy', None)
    if 720 <= x <= 920 and 550 <= y <= 650:
        return ('next', None)
    return (None, None)

# This function draws a gray rectangle on top of the regular one for buttons from the 4x4 grid.
# We also need to create a new textSurf object on top of the new gray rectangle.
def drawHighlightBox(boxx, boxy, wordlist, solved_rows):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, GRAY, (left, top, 200, 100))
    textSurf = BASICFONT.render(wordlist[boxx+boxy*4-(len(solved_rows)*4)], True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = left+100, top+50
    DISPLAYSURF.blit(textSurf, textRect)

# This function is called once the player presses the submit button. It grabs the words that correspond to the chosen buttons in the 4x4 grid using the indexes to address 'wordlist'.
# Then we check if the set of the chosen words corresponds to any of the four categories.
# If the guess is correct we return the new wordlist, the info on the guessed category and the chosen words (the latter goes straight into player history).
def checkGuess(chosen_boxes, wordlist, yellow_words, green_words, blue_words, purple_words, solved_rows):
    chosen_words = []
    for boxx, boxy in chosen_boxes:
        word = wordlist[boxx+boxy*4-(len(solved_rows)*4)]
        chosen_words.append(word)
    if set(chosen_words) == set(yellow_words):
        return list(set(wordlist) - set(chosen_words)), ('Yellow', yellow_words), chosen_words
    elif set(chosen_words) == set(green_words):
        return list(set(wordlist) - set(chosen_words)), ('Green', green_words), chosen_words
    elif set(chosen_words) == set(blue_words):
        return list(set(wordlist) - set(chosen_words)), ('Blue', blue_words), chosen_words
    elif set(chosen_words) == set(purple_words):
        return list(set(wordlist) - set(chosen_words)), ('Purple', purple_words), chosen_words
    else:
        return None, None, chosen_words

# This function swaps the words from each category to a corresponding emoji.
# Each player move is then just 4 emojis.
def parseHistory(history, yellow_words, green_words, blue_words, purple_words):
    moves = ''
    for guess in history:
        move = ''
        for word in guess:
            if word in yellow_words:
                move += '🟨'
            elif word in green_words:
                move += '🟩'
            elif word in blue_words:
                move += '🟦'
            elif word in purple_words:
                move += '🟪'
        moves += move + '\n'
    return moves

# Basic function that closes the game if the player presses the close button and presses ESC.
def checkForQuit():
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        pygame.event.post(event)

# Main function that contains the basic loop.
def main():
    puzzles = parsePuzzles()
    puzzle_title, categories, yellow_words, green_words, blue_words, purple_words = choosePuzzle(puzzles)
    words = set(yellow_words + green_words + blue_words + purple_words)
    wordlist = list(words)
    chosen_boxes = []
    solved_rows = []
    mistakes = 0
    history = []
    player_moves = ''
    solved_flag = False
    admire = False

    # First off we load the background music (it can take a second).
    # The song loops forever.
    pygame.mixer.init()
    pygame.mixer.music.load('one_note_sampo.ogg')
    pygame.mixer.music.play(-1, 0.0)

    while True:
        try:
            mouseClicked = False

            # Every frame we draw the current game state. We also check for whether the player tried to close the game.
            DISPLAYSURF.fill(BEIGE)
            drawBoard(puzzle_title, wordlist, chosen_boxes, solved_rows, categories, mistakes, player_moves, admire)
            checkForQuit()

            # On every frame we check where the current mouse position is.
            for event in pygame.event.get():
                if event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
                elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouseClicked = True

            # Using that mouse position we check if the cursor is over one of the buttons.
            # If it is and we registered a click, we change the chosen_boxes list. It functions as the selector for buttons in the main 4x4 grid.
            box_type, box = getBoxAtPixel(mousex, mousey, solved_rows)
            if box_type == 'word' and not solved_flag:
                boxx, boxy = box
                drawHighlightBox(boxx, boxy, wordlist, solved_rows)
                if mouseClicked:
                    if (boxx, boxy) in chosen_boxes:
                        chosen_boxes.remove((boxx, boxy))
                    elif len(chosen_boxes) < 4:
                        chosen_boxes.append((boxx, boxy))

            # If the mouse is over the submit button we need to draw another rectangle to highlight it.
            # If the mouse is clicked, we launch the checkGuess function. It only works if the player selected 4 words exactly.
            elif box_type == 'submit' and not solved_flag:
                pygame.draw.rect(DISPLAYSURF, GRAY, (400, 550, 210, 100))
                textSurf = BASICFONT.render('Submit', True, BLACK)
                textRect = textSurf.get_rect()
                textRect.center = 405+100, 550+50
                DISPLAYSURF.blit(textSurf, textRect)
                if mouseClicked and len(chosen_boxes) == 4:
                    result = checkGuess(chosen_boxes, wordlist, yellow_words, green_words, blue_words, purple_words, solved_rows)
                    if result[0] != None:
                        wordlist = result[0]
                        solved_rows.append(result[1])
                        chosen_boxes = []
                    else:
                        mistakes += 1
                        chosen_boxes = []
                    history.append(result[2])

            # If the player clicked on the Next puzzle button we simply launch the choosePuzzle function again and reintroduce all the basic variables from the start of the main function.
            elif box_type == 'next':
                pygame.draw.rect(DISPLAYSURF, GRAY, (720, 550, 200, 100))
                textSurf = BASICFONT.render('Next puzzle', True, BLACK)
                textRect = textSurf.get_rect()
                textRect.center = 725+100, 550+50
                DISPLAYSURF.blit(textSurf, textRect)
                if mouseClicked:
                    puzzle_title, categories, yellow_words, green_words, blue_words, purple_words = choosePuzzle(puzzles)
                    words = set(yellow_words + green_words + blue_words + purple_words)
                    wordlist = list(words)
                    chosen_boxes = []
                    solved_rows = []
                    mistakes = 0
                    history = []
                    player_moves = ''
                    solved_flag = False
                    admire = False

            # The buttons from the result screen are checked simply by the current mouse coordinates.
            if 300 <= mousex <= 490 and 400 <= mousey <= 500 and solved_flag and not admire:
                pygame.draw.rect(DISPLAYSURF, GRAY, (300, 400, 190, 100))
                textSurf = BASICFONT.render('Copy', True, BLACK)
                textRect = textSurf.get_rect()
                textRect.center = 395, 400+50
                DISPLAYSURF.blit(textSurf, textRect)
                if mouseClicked:
                    pyperclip.copy(puzzle_title + '\n' + player_moves.strip())
            
            if 510 <= mousex <= 700 and 400 <= mousey <= 500 and solved_flag and not admire:
                pygame.draw.rect(DISPLAYSURF, GRAY, (510, 400, 190, 100))
                textSurf = BASICFONT.render('Close', True, BLACK)
                textRect = textSurf.get_rect()
                textRect.center = 605, 400+50
                DISPLAYSURF.blit(textSurf, textRect)
                if mouseClicked:
                    admire = True

            # If the player lost we still need to draw all the categories on the screen.
            # We add the remaining (unsolved) categories to the solved ones.
            if len(solved_rows) == 4 or mistakes == 4:
                if solved_flag == False:
                    if len(solved_rows) < 4:
                        solved_categories = []
                        for row in solved_rows:
                            category = row[0]
                            solved_categories.append(category)
                        for category in ['Yellow', 'Green', 'Blue', 'Purple']:
                            if not category in solved_categories:
                                if category == 'Yellow':
                                    solved_rows.append((category, yellow_words))
                                elif category == 'Green':
                                    solved_rows.append((category, green_words))
                                elif category == 'Blue':
                                    solved_rows.append((category, blue_words))
                                elif category == 'Purple':
                                    solved_rows.append((category, purple_words))
                    player_moves = parseHistory(history, yellow_words, green_words, blue_words, purple_words)
                    solved_flag = True

        # Sometimes the game crashes on startup if we can't locate the mouse cursor.
        # This exception catches that and just waits until the player moves the cursor to another place.
        except UnboundLocalError:
            pass

        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == '__main__':
    main()
