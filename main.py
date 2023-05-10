import pygame
import math
from random import randint
from tkinter import messagebox

pygame.init()

screen_size = (800, 800)  # Размер экрана
screen = pygame.display.set_mode(screen_size)

game = False

ball_cords = [30, 30]
enemies_ball_cords = [[randint(0, 800), randint(0, 800)], [randint(0, 800), randint(0, 800)],
                      [randint(0, 800), randint(0, 800)], [randint(0, 800), randint(0, 800)]]

enemy_colour = (50, 205, 50)  # Цвет врагов
color = (0, 128, 255)  # Цвет игрока

player_speed = 3  # Скорость игрока
enemy_speed = 1.7  # Скорость врагов

clock = pygame.time.Clock()

mines = []  # Координаты мин
bullets = []  # Координаты пуль

mines_delay = 0  # Задержка мин


def distance(lst1, lst2):
    """Функция находит расстояние между обьектами на координатной плоскости."""
    return math.sqrt(math.pow(lst2[0] - lst1[0], 2) + math.pow(lst2[1] - lst1[1], 2))


while not game:  # Цикл игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Выход из игры.
            game = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3 and not mines_delay:
                mines.append(tuple(ball_cords))  # Установка мины.
                mines_delay = 60

    pressed = pygame.key.get_pressed()  # Движение игрока.
    if pressed[pygame.K_UP] and ball_cords[1] > 20: ball_cords[1] -= player_speed
    if pressed[pygame.K_DOWN] and ball_cords[1] < 780: ball_cords[1] += player_speed
    if pressed[pygame.K_LEFT] and ball_cords[0] > 20: ball_cords[0] -= player_speed
    if pressed[pygame.K_RIGHT] and ball_cords[0] < 780: ball_cords[0] += player_speed

    for i in enemies_ball_cords:  # Движение врагов.
        if ball_cords[1] < i[1]: i[1] -= enemy_speed
        if ball_cords[1] > i[1]: i[1] += enemy_speed
        if ball_cords[0] < i[0]: i[0] -= enemy_speed
        if ball_cords[0] > i[0]: i[0] += enemy_speed

    if len(mines) > 3:  # Проверка количества мин.
        mines.remove(mines[0])

    for i in mines:  # Проверяем: наступили ли враги на мины.
        for z in enemies_ball_cords:
            if distance(z, i) < 20: enemies_ball_cords.remove(z); mines.remove(i)

    for i in enemies_ball_cords:  # Проверяем: догнали ли игрока враги.
        if distance(i, ball_cords) < 35: messagebox.showinfo(title="Игра", message="Вы проиграли."); game = True

    screen.fill((255, 255, 255))

    for i in mines:  # Рисовка мин.
        pygame.draw.circle(screen, (255, 69, 0), i, 5)

    pygame.draw.circle(screen, color, (ball_cords[0], ball_cords[1]), 20)  # Рисовка игрока

    for i in enemies_ball_cords:
        pygame.draw.circle(screen, enemy_colour, (i[0], i[1]), 20)  # Рисовка врагов.

    if not enemies_ball_cords: messagebox.showinfo(title="Игра",
                                                   message="Вы выиграли."); game = True  # Проверяем наличие врагов

    if mines_delay: mines_delay -= 1  # Уменьшаем задержку использования мин.

    pygame.display.flip()
    clock.tick(60)
