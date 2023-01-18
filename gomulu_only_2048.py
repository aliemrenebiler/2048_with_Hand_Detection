import pygame
import random
import os

pygame.init()

# Define some colors
COLORS = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    "light_text": (249, 246, 242),
    "dark_text": (119, 110, 101),
    "other": (0, 0, 0),
    "background": (187, 173, 160),
}

screen_sizes = pygame.display.get_desktop_sizes()[0]
if screen_sizes[0] < screen_sizes[1]:
    SCREEN_SIZE = int(screen_sizes[0] / 2)
else:
    SCREEN_SIZE = int(screen_sizes[1] / 2)

MARGIN = SCREEN_SIZE / 50
FONT_SIZE = int(SCREEN_SIZE / 20)
SQUARE_SIZE = int((SCREEN_SIZE - MARGIN * 5) / 4)
TOP_BAR_HEIGHT = (FONT_SIZE + MARGIN) * 2

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + TOP_BAR_HEIGHT))
pygame.display.set_caption("2048 With Hands")

timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font("Roboto-Bold.ttf", FONT_SIZE)

# Hareketler
class Swipe:
    def up(score, grid):
        moved = False
        for i in range(4):
            # Sifirlari tara ve kaydir
            while grid[0][i] == 0 and (
                grid[1][i] != 0 or grid[2][i] != 0 or grid[3][i] != 0
            ):
                grid[0][i] = grid[1][i]
                grid[1][i] = grid[2][i]
                grid[2][i] = grid[3][i]
                grid[3][i] = 0
                moved = True
            while grid[1][i] == 0 and (grid[2][i] != 0 or grid[3][i] != 0):
                grid[1][i] = grid[2][i]
                grid[2][i] = grid[3][i]
                grid[3][i] = 0
                moved = True
            if grid[2][i] == 0 and grid[3][i] != 0:
                grid[2][i] = grid[3][i]
                grid[3][i] = 0
                moved = True

            # Ayni olan ciftleri topla ve kaydir
            if grid[0][i] == grid[1][i] and grid[0][i] != 0 and grid[1][i] != 0:
                grid[0][i] = grid[0][i] * 2
                grid[1][i] = grid[2][i]
                grid[2][i] = grid[3][i]
                grid[3][i] = 0
                score = score + grid[0][i]
                moved = True
            if grid[1][i] == grid[2][i] and grid[1][i] != 0 and grid[2][i] != 0:
                grid[1][i] = grid[1][i] * 2
                grid[2][i] = grid[3][i]
                grid[3][i] = 0
                score = score + grid[1][i]
                moved = True
            if grid[2][i] == grid[3][i] and grid[1][i] != 0 and grid[2][i] != 0:
                grid[2][i] = grid[2][i] * 2
                grid[3][i] = 0
                score = score + grid[2][i]
                moved = True

        return score, grid, moved

    def left(score, grid):
        moved = False
        for i in range(4):
            # Sifirlari tara ve kaydir
            while grid[i][0] == 0 and (
                grid[i][1] != 0 or grid[i][2] != 0 or grid[i][3] != 0
            ):
                grid[i][0] = grid[i][1]
                grid[i][1] = grid[i][2]
                grid[i][2] = grid[i][3]
                grid[i][3] = 0
                moved = True
            while grid[i][1] == 0 and (grid[i][2] != 0 or grid[i][3] != 0):
                grid[i][1] = grid[i][2]
                grid[i][2] = grid[i][3]
                grid[i][3] = 0
                moved = True
            if grid[i][2] == 0 and grid[i][3] != 0:
                grid[i][2] = grid[i][3]
                grid[i][3] = 0
                moved = True

            # Ayni olan ciftleri topla ve kaydir
            if grid[i][0] == grid[i][1] and grid[i][0] != 0 and grid[i][1] != 0:
                grid[i][0] = grid[i][0] * 2
                grid[i][1] = grid[i][2]
                grid[i][2] = grid[i][3]
                grid[i][3] = 0
                score = score + grid[i][0]
                moved = True
            if grid[i][1] == grid[i][2] and grid[i][1] != 0 and grid[i][2] != 0:
                grid[i][1] = grid[i][1] * 2
                grid[i][2] = grid[i][3]
                grid[i][3] = 0
                score = score + grid[i][1]
                moved = True
            if grid[i][2] == grid[i][3] and grid[i][2] != 0 and grid[i][3] != 0:
                grid[i][2] = grid[i][2] * 2
                grid[i][3] = 0
                score = score + grid[i][2]
                moved = True

        return score, grid, moved

    def down(score, grid):
        moved = False
        for i in range(4):
            # Sifirlari tara ve kaydir
            while grid[3][i] == 0 and (
                grid[0][i] != 0 or grid[1][i] != 0 or grid[2][i] != 0
            ):
                grid[3][i] = grid[2][i]
                grid[2][i] = grid[1][i]
                grid[1][i] = grid[0][i]
                grid[0][i] = 0
                moved = True
            while grid[2][i] == 0 and (grid[0][i] != 0 or grid[1][i] != 0):
                grid[2][i] = grid[1][i]
                grid[1][i] = grid[0][i]
                grid[0][i] = 0
                moved = True
            if grid[1][i] == 0 and grid[0][i] != 0:
                grid[1][i] = grid[0][i]
                grid[0][i] = 0
                moved = True

            # Ayni olan ciftleri topla ve kaydir
            if grid[3][i] == grid[2][i] and grid[3][i] != 0 and grid[2][i] != 0:
                grid[3][i] = grid[3][i] * 2
                grid[2][i] = grid[1][i]
                grid[1][i] = grid[0][i]
                grid[0][i] = 0
                score = score + grid[3][i]
                moved = True
            if grid[2][i] == grid[1][i] and grid[2][i] != 0 and grid[1][i] != 0:
                grid[2][i] = grid[2][i] * 2
                grid[1][i] = grid[0][i]
                grid[0][i] = 0
                score = score + grid[2][i]
                moved = True
            if grid[1][i] == grid[0][i] and grid[1][i] != 0 and grid[0][i] != 0:
                grid[1][i] = grid[1][i] * 2
                grid[0][i] = 0
                score = score + grid[1][i]
                moved = True

        return score, grid, moved

    def right(score, grid):
        moved = False
        for i in range(4):
            # Sifirlari tara ve kaydir
            while grid[i][3] == 0 and (
                grid[i][0] != 0 or grid[i][1] != 0 or grid[i][2] != 0
            ):
                grid[i][3] = grid[i][2]
                grid[i][2] = grid[i][1]
                grid[i][1] = grid[i][0]
                grid[i][0] = 0
                moved = True
            while grid[i][2] == 0 and (grid[i][0] != 0 or grid[i][1] != 0):
                grid[i][2] = grid[i][1]
                grid[i][1] = grid[i][0]
                grid[i][0] = 0
                moved = True
            if grid[i][1] == 0 and grid[i][0] != 0:
                grid[i][1] = grid[i][0]
                grid[i][0] = 0
                moved = True

            # Ayni olan ciftleri topla ve kaydir
            if grid[i][3] == grid[i][2] and grid[i][3] != 0 and grid[i][2] != 0:
                grid[i][3] = grid[i][3] * 2
                grid[i][2] = grid[i][1]
                grid[i][1] = grid[i][0]
                grid[i][0] = 0
                score = score + grid[i][3]
                moved = True
            if grid[i][2] == grid[i][1] and grid[i][2] != 0 and grid[i][1] != 0:
                grid[i][2] = grid[i][2] * 2
                grid[i][1] = grid[i][0]
                grid[i][0] = 0
                score = score + grid[i][2]
                moved = True
            if grid[i][1] == grid[i][0] and grid[i][1] != 0 and grid[i][0] != 0:
                grid[i][1] = grid[i][1] * 2
                grid[i][0] = 0
                score = score + grid[i][1]
                moved = True

        return score, grid, moved


# Diğer Fonksiyonlar
def reset_the_game():
    ended = False
    stuck = False
    win = False
    score = 0
    high_score = get_high_score("high_score")
    grid = [[0 for _ in range(4)] for _ in range(4)]

    create_random(grid)
    create_random(grid)

    return ended, stuck, win, score, high_score, grid


def get_high_score(file_name):
    if os.path.isfile(file_name):
        file = open(file_name, "r")
        high_score = int(file.readline())
        file.close()
        return high_score
    else:
        return 0


def save_high_score(high_score, file_name):
    file = open(file_name, "w+")
    file.write(str(high_score))
    file.close()
    return high_score


def check_score(score, high_score):
    if score > high_score:
        return score
    else:
        return high_score


def create_random(grid):
    rand_x = random.randint(0, 3)
    rand_y = random.randint(0, 3)
    while grid[rand_x][rand_y] != 0:
        rand_x = random.randint(0, 3)
        rand_y = random.randint(0, 3)

    rand_value = random.randint(0, 9)
    if rand_value == 0:
        rand_value = 4
    else:
        rand_value = 2
    grid[rand_x][rand_y] = rand_value

    return grid


def stuck_control(grid):
    stuck = True

    # Sifir kontrolu
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                stuck = False

    # Yan yana olan sayilarin kontrolu
    if stuck:
        for i in range(4):
            for j in range(3):
                if grid[i][j] == grid[i][j + 1] or grid[j][i] == grid[j + 1][i]:
                    stuck = False

    return stuck


def win_control(b):
    win = False

    i = 0
    while not win and i < 4:
        j = 0
        while not win and j < 4:
            if b[i][j] == 2048:
                win = True
            j += 1
        i += 1

    return win


# UI Elements
def draw_board(score, high_score):
    pygame.draw.rect(
        screen,
        COLORS["background"],
        [
            0,
            0,
            SCREEN_SIZE,
            SCREEN_SIZE + TOP_BAR_HEIGHT,
        ],
        0,
        0,
    )
    score_text = font.render(
        f"Score: {score}",
        True,
        COLORS["dark_text"],
    )
    high_score_text = font.render(
        f"High Score: {high_score}",
        True,
        COLORS["dark_text"],
    )
    screen.blit(high_score_text, (MARGIN, MARGIN))
    screen.blit(score_text, (MARGIN, MARGIN * 2 + FONT_SIZE))


def draw_the_grid(grid):
    # Draw the grid
    for i in range(4):
        for j in range(4):
            value = grid[i][j]
            if value > 8:
                text_color = COLORS["light_text"]
            else:
                text_color = COLORS["dark_text"]
            if value <= 2048:
                color = COLORS[value]
            else:
                color = COLORS["other"]
            pygame.draw.rect(
                screen,
                color,
                [
                    MARGIN + (MARGIN + SQUARE_SIZE) * j,
                    TOP_BAR_HEIGHT + MARGIN + (MARGIN + SQUARE_SIZE) * i,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                ],
                0,
                5,
            )
            if value > 0:
                value_text = font.render(str(value), True, text_color)
                text_rect = value_text.get_rect(
                    center=(
                        MARGIN + SQUARE_SIZE / 2 + (MARGIN + SQUARE_SIZE) * j,
                        TOP_BAR_HEIGHT
                        + MARGIN
                        + SQUARE_SIZE / 2
                        + (MARGIN + SQUARE_SIZE) * i,
                    )
                )
                screen.blit(value_text, text_rect)


def game_over_popup(score):
    top_space = int(
        (SCREEN_SIZE + TOP_BAR_HEIGHT - int(FONT_SIZE * 3 + MARGIN * 4)) / 2
    )
    pygame.draw.rect(
        screen,
        "black",
        [
            int(SCREEN_SIZE / 4),
            top_space,
            int(SCREEN_SIZE / 2),
            FONT_SIZE * 3 + MARGIN * 4,
        ],
        0,
        5,
    )
    game_over_text1 = font.render("Game Over!", True, COLORS["light_text"])
    game_over_text2 = font.render(f"Score: {score}", True, COLORS["light_text"])
    game_over_text3 = font.render("Press R to restart.", True, COLORS["light_text"])
    screen.blit(
        game_over_text1,
        game_over_text1.get_rect(
            midtop=(int(SCREEN_SIZE / 2), top_space + MARGIN),
        ),
    )
    screen.blit(
        game_over_text2,
        game_over_text2.get_rect(
            midtop=(int(SCREEN_SIZE / 2), top_space + MARGIN * 2 + FONT_SIZE),
        ),
    )
    screen.blit(
        game_over_text3,
        game_over_text3.get_rect(
            midtop=(int(SCREEN_SIZE / 2), top_space + MARGIN * 3 + FONT_SIZE * 2)
        ),
    )


def you_win_popup(score):
    top_space = int(
        (SCREEN_SIZE + TOP_BAR_HEIGHT - int(FONT_SIZE * 3 + MARGIN * 4)) / 2
    )
    pygame.draw.rect(
        screen,
        "white",
        [
            int(SCREEN_SIZE / 4),
            top_space,
            int(SCREEN_SIZE / 2),
            FONT_SIZE * 3 + MARGIN * 4,
        ],
        0,
        5,
    )
    game_over_text1 = font.render("You Win!", True, COLORS["dark_text"])
    game_over_text2 = font.render(f"Score: {score}", True, COLORS["dark_text"])
    game_over_text3 = font.render("Press R to restart.", True, COLORS["dark_text"])
    screen.blit(
        game_over_text1,
        game_over_text1.get_rect(
            midtop=(int(SCREEN_SIZE / 2), top_space + MARGIN),
        ),
    )
    screen.blit(
        game_over_text2,
        game_over_text2.get_rect(
            midtop=(int(SCREEN_SIZE / 2), top_space + MARGIN * 2 + FONT_SIZE),
        ),
    )
    screen.blit(
        game_over_text3,
        game_over_text3.get_rect(
            midtop=(int(SCREEN_SIZE / 2), top_space + MARGIN * 3 + FONT_SIZE * 2)
        ),
    )


# Main
def start_the_game():
    ended, stuck, win, score, high_score, grid = reset_the_game()

    draw_board(score, high_score)
    draw_the_grid(grid)

    # Oyun Dongusu
    while not ended:
        timer.tick(fps)

        for event in pygame.event.get():
            # Eger oyun kapatildiysa en yuksek skoru kaydet ve cik
            if event.type == pygame.QUIT:
                high_score = check_score(score, high_score)
                save_high_score(high_score, "high_score")
                ended = True
            # Eger bir tusa basildiysa
            elif event.type == pygame.KEYUP:
                if not stuck and not win:
                    moved = False
                    # Sol
                    if event.key == pygame.K_LEFT:
                        score, grid, moved = Swipe.left(score, grid)
                    # Sağ
                    elif event.key == pygame.K_RIGHT:
                        score, grid, moved = Swipe.right(score, grid)
                    # Yukari
                    elif event.key == pygame.K_UP:
                        score, grid, moved = Swipe.up(score, grid)
                    # Asagi
                    elif event.key == pygame.K_DOWN:
                        score, grid, moved = Swipe.down(score, grid)

                    # Eger hareket varsa
                    if moved:
                        grid = create_random(grid)
                        draw_board(score, high_score)
                        draw_the_grid(grid)

                    # Takilma ve kazanma kontrolleri
                    stuck = stuck_control(grid)
                    win = win_control(grid)
                if event.key == pygame.K_r:
                    ended, stuck, win, score, high_score, grid = reset_the_game()
                    draw_board(score, high_score)
                    draw_the_grid(grid)

        if win:
            high_score = check_score(score, high_score)
            save_high_score(high_score, "high_score")
            you_win_popup(score)
        elif stuck:
            high_score = check_score(score, high_score)
            save_high_score(high_score, "high_score")
            game_over_popup(score)

        pygame.display.flip()


start_the_game()
pygame.quit()
