import pygame
import math
from tkinter import messagebox

pygame.init()

screen_size = (800, 800)
screen = pygame.display.set_mode(screen_size)

game = False
is_blue = True

ball_cords = [30, 30]
enemies_ball_cords = [[550, 490], [395, 427], [311, 329], [659, 475]]

enemy_colour = (50,205,50)
color = (0, 128, 255)

clock = pygame.time.Clock()

mines = []
bullets = []

mines_delay = 0

def distance(lst1, lst2):
    return math.sqrt(math.pow(lst2[0] - lst1[0], 2) + math.pow(lst2[1] - lst1[1], 2))

while not game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3 and not mines_delay:
                mines.append(tuple(ball_cords))
                mines_delay = 100

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP] and ball_cords[1] > 20: ball_cords[1] -= 3
    if pressed[pygame.K_DOWN] and ball_cords[1] < 780: ball_cords[1] += 3
    if pressed[pygame.K_LEFT] and ball_cords[0] > 20: ball_cords[0] -= 3
    if pressed[pygame.K_RIGHT] and ball_cords[0] < 780: ball_cords[0] += 3

    for i in enemies_ball_cords:
        if ball_cords[1] < i[1]: i[1] -= 1.7
        if ball_cords[1] > i[1]: i[1] += 1.7
        if ball_cords[0] < i[0]: i[0] -= 1.7
        if ball_cords[0] > i[0]: i[0] += 1.7

    if len(mines) > 3:
        mines.remove(mines[0])

    for i in mines:
        for z in enemies_ball_cords:
            if distance(z, i) < 20: enemies_ball_cords.remove(z); mines.remove(i)

    for i in enemies_ball_cords:
        if distance(i, ball_cords) < 35: messagebox.showinfo(title = "Игра", message = "Вы проиграли."); game = True

    screen.fill((255, 255, 255))

    for i in mines:
        pygame.draw.circle(screen, (255,69,0), i, 5)

    pygame.draw.circle(screen, color, (ball_cords[0], ball_cords[1]), 20)

    for i in enemies_ball_cords:
        pygame.draw.circle(screen, enemy_colour, (i[0], i[1]), 20)

    if not enemies_ball_cords: messagebox.showinfo(title = "Игра", message = "Вы выиграли."); game = True

    if mines_delay: mines_delay -= 1

    pygame.display.flip()
    clock.tick(60)