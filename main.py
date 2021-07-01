import pygame
import requests
import time

response = requests.get("https://sugoku.herokuapp.com/board?difficulty=hard")
board = response.json()['board']

size = 550
background_color = (255, 255, 255)
original_element_color = (52, 31, 151)
new_element_color = (255, 0, 0)

# returns next empty cell
def nextEmpty (sdk):
    for row in range(9):
        for col in range (9):
            if (sdk[row][col] == 0):
                return True, row, col
    return False, None, None

# return the first position of the quadrant of a specific cell
def getQuad (x, y):
    return (int((x // 3) * 3), int((y // 3)) * 3)

# checks for constraints
def isValid(sdk, guess, guess_r, guess_c):
    # Row constraint
    for i in range(9):
        if guess in sdk[guess_r]:
            return False

    # Column constraint
    for i in range(9):
        if (guess == sdk[i][guess_c]):
            return False

    # Quadrant constraint
    x, y = getQuad(guess_r, guess_c)

    for i in range(x, (x + 3)):
        for j in range(y, (y + 3)):
            if guess == sdk[i][j]:
                return False

    return True

def solveSdk(sdk_puzzle, myFont, screen):
    # 1 - Checks to see if there are empty spots
    empty, x, y = nextEmpty(sdk_puzzle)

    time.sleep(0.01)

    # if empty spots found, proceeds to guess solution
    if not empty:
        return True

    # Generate guesses
    for guess in range(1, 10):
        # 2 - Verify if the guess is currently viable
        # if guess is viable, proceeds to save it on the position
        if isValid(sdk_puzzle, guess, x, y):
            sdk_puzzle[x][y] = guess
            guess_render = myFont.render(str(guess), True, new_element_color)
            screen.blit(guess_render, ((y + 1) * 50 + 15, (x + 1) * 50))
            pygame.display.update()

            # since the board changed, we try to solve it again (recursion)
            if solveSdk(sdk_puzzle, myFont, screen):
                # if the puzzle is completed, it will return True, so we just return True here as well
                return True
            else:
                # if guess is no good, we backtrack
                # resetting the value of the cell
                sdk_puzzle[x][y] = 0
                pygame.draw.rect(screen, (255, 255, 255), ((y + 1) * 50 + 5, (x + 1) * 50 + 5, 40, 40))
                pygame.display.update()
    # if we ran out of loops (guesses) and still haven't solved the puzzle, the puzzle is unsolvable
    return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((size, size))
    pygame.display.set_caption('Sudoku Solver Visualizer')
    screen.fill(background_color)
    myFont = pygame.font.SysFont('Comic Sans MS', 35)

    for i in range(10):
        pygame.draw.line(screen, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 2)
        pygame.draw.line(screen, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 2)
        if (i%3 == 0):
            pygame.draw.line(screen, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 4)
            pygame.draw.line(screen, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 4)
    pygame.display.update()

    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                value = myFont.render(str(board[i][j]), True, original_element_color)
                screen.blit(value, ((j+1) * 50 + 15, (i+1) * 50))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYUP:
                solveSdk(board, myFont, screen)

main()