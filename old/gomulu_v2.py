import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 80
HEIGHT = 80

# This sets the margin between each cell
MARGIN = 5

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(4):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(4):
        grid[row].append(0)  # Append a cell

# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)
grid[1][1] = 2

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [325, 325]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("2048")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 32)

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("Left arrow key pressed")
            elif event.key == pygame.K_RIGHT:
                print("Right arrow key pressed")
            elif event.key == pygame.K_UP:
                print("Up arrow key pressed")
            elif event.key == pygame.K_DOWN:
                print("Down arrow key pressed")

    # Set the screen background
    screen.fill(BLACK)

    # Draw the grid
    for row in range(4):
        for column in range(4):
            color = WHITE
            if grid[row][column] == 2:
                color = GREEN
            elif grid[row][column] == 4:
                color = RED
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

            text = font.render(str(grid[row][column]), True, BLACK)
            screen.blit(text,
                        [(MARGIN + WIDTH) * column + MARGIN,
                         (MARGIN + HEIGHT) * row + MARGIN])

    # Limit to 60 frames per second
