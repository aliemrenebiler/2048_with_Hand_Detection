import pygame
import random
import os


import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

from statistics import mode
from argparse import ArgumentParser

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

# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 12:44:45 2022

@author: Bengi
"""

ap = ArgumentParser()
ap.add_argument("-rec", "--record", default=False, action="store_true", help="Record?")
ap.add_argument(
    "-pscale",
    "--pyr_scale",
    default=0.5,
    type=float,
    help="Image scale (<1) to build pyramids for each image",
)
ap.add_argument("-l", "--levels", default=3, type=int, help="Number of pyramid layers")
ap.add_argument("-w", "--winsize", default=15, type=int, help="Averaging window size")
ap.add_argument(
    "-i",
    "--iterations",
    default=3,
    type=int,
    help="Number of iterations the algorithm does at each pyramid level",
)
ap.add_argument(
    "-pn",
    "--poly_n",
    default=5,
    type=int,
    help="Size of the pixel neighborhood used to find polynomial expansion in each pixel",
)
ap.add_argument(
    "-psigma",
    "--poly_sigma",
    default=1.1,
    type=float,
    help="Standard deviation of the Gaussian that is used to smooth derivatives used as a basis for the polynomial expansion",
)
ap.add_argument(
    "-th", "--threshold", default=10.0, type=float, help="Threshold value for magnitude"
)
ap.add_argument(
    "-p", "--plot", default=False, action="store_true", help="Plot accumulators?"
)
ap.add_argument(
    "-rgb", "--rgb", default=False, action="store_true", help="Show RGB mask?"
)
ap.add_argument(
    "-s", "--size", default=10, type=int, help="Size of accumulator for directions map"
)

args = vars(ap.parse_args())

directions_map = np.zeros([args["size"], 5])

text = "WAIT"

cap = cv.VideoCapture(0)
if args["record"]:
    h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    codec = cv.VideoWriter_fourcc(*"MPEG")
    out = cv.VideoWriter("out.avi", codec, 10.0, (w, h))

if args["plot"]:
    plt.ion()

frame_previous = cap.read()[1]
gray_previous = cv.cvtColor(frame_previous, cv.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame_previous)
hsv[:, :, 1] = 255
param = {
    "pyr_scale": args["pyr_scale"],
    "levels": args["levels"],
    "winsize": args["winsize"],
    "iterations": args["iterations"],
    "poly_n": args["poly_n"],
    "poly_sigma": args["poly_sigma"],
    "flags": cv.OPTFLOW_LK_GET_MIN_EIGENVALS,
}


def detect_movement():
    global gray_previous, directions_map
    grabbed, frame = cap.read()
    if grabbed:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        flow = cv.calcOpticalFlowFarneback(gray_previous, gray, None, **param)
        mag, ang = cv.cartToPolar(flow[:, :, 0], flow[:, :, 1], angleInDegrees=True)
        ang_180 = ang / 2
        gray_previous = gray

        move_sense = ang[mag > args["threshold"]]
        if len(move_sense) != 0:
            move_mode = mode(move_sense)
            if 10 < move_mode <= 100:
                directions_map[-1, 0] = 1
                directions_map[-1, 1:] = 0
                directions_map = np.roll(directions_map, -1, axis=0)
            elif 100 < move_mode <= 190:
                directions_map[-1, 1] = 1
                directions_map[-1, :1] = 0
                directions_map[-1, 2:] = 0
                directions_map = np.roll(directions_map, -1, axis=0)
            elif 190 < move_mode <= 280:
                directions_map[-1, 2] = 1
                directions_map[-1, :2] = 0
                directions_map[-1, 3:] = 0
                directions_map = np.roll(directions_map, -1, axis=0)
            elif 280 < move_mode or move_mode < 10:
                directions_map[-1, 3] = 1
                directions_map[-1, :3] = 0
                directions_map[-1, 4:] = 0
                directions_map = np.roll(directions_map, -1, axis=0)
        else:
            directions_map[-1, -1] = 1
            directions_map[-1, :-1] = 0
            directions_map = np.roll(directions_map, 1, axis=0)

        if args["plot"]:
            plt.clf()
            plt.plot(directions_map[:, 0], label="Down")
            plt.plot(directions_map[:, 1], label="Right")
            plt.plot(directions_map[:, 2], label="Up")
            plt.plot(directions_map[:, 3], label="Left")
            plt.plot(directions_map[:, 4], label="Waiting")
            plt.legend(loc=2)
            plt.pause(1e-5)
            plt.show()

        loc = directions_map.mean(axis=0).argmax()
        if loc == 0:
            text = "DOWN"
        elif loc == 1:
            text = "RIGHT"
        elif loc == 2:
            text = "UP"
        elif loc == 3:
            text = "LEFT"
        else:
            text = "WAIT"

        hsv[:, :, 0] = ang_180
        hsv[:, :, 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
        rgb = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)

        frame = cv.flip(frame, 1)
        cv.putText(
            frame,
            text,
            (30, 90),
            cv.FONT_HERSHEY_COMPLEX,
            frame.shape[1] / 500,
            (0, 0, 255),
            2,
        )

        # k = cv.waitKey(1) & 0xff
        # if k == ord('q'):
        #     break
        if args["record"]:
            out.write(frame)
        if args["rgb"]:
            cv.imshow("Mask", rgb)
        cv.imshow("Frame", frame)
        # k = cv.waitKey(1) & 0xff
        # if k == ord('q'):
        #     break
        return text


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
    prev = "WAIT"
    # Oyun Dongusu
    while not ended:
        timer.tick(fps)

        direction = detect_movement()
        # for event in pygame.event.get():
        # Eger oyun kapatildiysa en yuksek skoru kaydet ve cik
        k = cv.waitKey(1) & 0xFF
        if k == ord("q"):
            high_score = check_score(score, high_score)
            save_high_score(high_score, "high_score")
            ended = True
        # Eger bir tusa basildiysa
        elif not stuck and not win and prev != direction:
            prev = direction
            moved = False
            # Sol
            if direction == "LEFT":
                score, grid, moved = Swipe.left(score, grid)
            # Sağ
            elif direction == "RIGHT":
                score, grid, moved = Swipe.right(score, grid)
            # Yukari
            elif direction == "UP":
                score, grid, moved = Swipe.up(score, grid)
            # Asagi
            elif direction == "DOWN":
                score, grid, moved = Swipe.down(score, grid)

            # Eger hareket varsa
            if moved:
                grid = create_random(grid)
                draw_board(score, high_score)
                draw_the_grid(grid)

            # Takilma ve kazanma kontrolleri
            stuck = stuck_control(grid)
            win = win_control(grid)

        if k == ord("r"):
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
cap.release()
if args["record"]:
    out.release()
if args["plot"]:
    plt.ioff()
cv.destroyAllWindows()
