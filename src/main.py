#!/usr/bin/env python3

#
# EPITECH PROJECT, 2024
# HouseBurn
# File description:
# houseBurn
#

import pygame
import sys
import tkinter as tk
from tkinter import messagebox

WIN_SIZE = 1000, 1000
PLAYER_SIZE = 80, 80
PLAYER_INIT_POS = 470, 845
TILE_SIZE = 100

pygame.init()
screen = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption('House Burn')

map_image = pygame.image.load('resources/map.png')
map_rect = map_image.get_rect()
character_image = pygame.image.load('resources/player.png')
character_image = pygame.transform.scale(character_image, PLAYER_SIZE)
character_rect = character_image.get_rect()
character_rect.topleft = PLAYER_INIT_POS
character_speed = 5

font = pygame.font.Font(None, 50)
cans = 0
max_cans = 7

my_dict = {
    "2": False,
    "3": False,
    "4": False,
    "5": False,
    "6": False,
    "7": False,
    "8": False
}

def draw_score(score, max_score):
    score_text = f"{score}/{max_score}"
    text = font.render(score_text, True, (255, 0, 0))
    screen.blit(text, (10, 10))

def load_collision_map(filename):
    with open(filename, 'r') as file:
        return [list(line.strip()) for line in file]

def show_message(value):
    global cans
    if value == '9' and cans < max_cans:
        root = tk.Tk()
        root.withdraw()
        message = "You need to collect all the petrol cans before burning the house!"
        messagebox.showinfo("Warning", message)
        root.destroy()
        character_rect.x += 110
        return
    elif value == '9' and cans == max_cans:
        print("launching house burn mini game") #start the mini game here
    if my_dict[value] == False:
        cans += 1
        my_dict[value] = True
    if cans == max_cans:
        root = tk.Tk()
        root.withdraw()
        message = "You have collected all the petrol cans! You can now burn the house!"
        messagebox.showinfo("Congratulations", message)
        root.destroy()

def check_collision(collision_map, rect, tile_size):
    map_height = len(collision_map)
    map_width = len(collision_map[0])

    positions = [
        (rect.left // tile_size, rect.top // tile_size),
        (rect.right // tile_size, rect.top // tile_size),
        (rect.left // tile_size, rect.bottom // tile_size),
        (rect.right // tile_size, rect.bottom // tile_size)
    ]

    for pos in positions:
        if 0 <= pos[1] < map_height and 0 <= pos[0] < map_width:
            cell_value = collision_map[pos[1]][pos[0]]
            if cell_value == '1':
                return True
            elif cell_value in '23456789':
                show_message(cell_value)
                return False
    return False

collision_map = load_collision_map('resources/collisions.txt')

def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        old_position = character_rect.topleft

        if keys[pygame.K_LEFT]:
            character_rect.x -= character_speed
        if keys[pygame.K_RIGHT]:
            character_rect.x += character_speed
        if keys[pygame.K_UP]:
            character_rect.y -= character_speed
        if keys[pygame.K_DOWN]:
            character_rect.y += character_speed

        if not map_rect.contains(character_rect) or check_collision(collision_map, character_rect, TILE_SIZE):
            character_rect.topleft = old_position

        screen.fill((0, 0, 0))
        screen.blit(map_image, map_rect.topleft)
        screen.blit(character_image, character_rect.topleft)
        draw_score(cans, max_cans)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
