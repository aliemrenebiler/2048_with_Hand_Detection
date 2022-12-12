import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 100
HEIGHT = 100

# This sets the margin between each cell
MARGIN = 5


# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [525, 525]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("2048")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()


# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            # User pressed a key
            if event.key == pygame.K_LEFT:
                # Move the current tile left
                pass
            elif event.key == pygame.K_RIGHT:
                # Move the current tile right
                pass
            elif event.key == pygame.K_UP:
                # Move the current tile up
                pass
            elif event.key == pygame.K_DOWN:
                # Move the current tile down
                pass

    # Set the screen background
    screen.fill(BLACK)

    # Draw the grid
    for row in range(4):
        for column in range(4):
            color = WHITE
            if grid[row][column] == 0:
                color = RED
            pygame.draw.rect(
                screen,
                color,
                [
                    (MARGIN + WIDTH) * column + MARGIN,
                    (MARGIN + HEIGHT) * row + MARGIN,
                    WIDTH,
                    HEIGHT,
                ],
            )

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
