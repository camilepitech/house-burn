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
import time

WIN_SIZE = 1000, 1000
PLAYER_SIZE = 80, 80
PLAYER_INIT_POS = 470, 845
TILE_SIZE = 100

STATE_START_MENU = 0
STATE_PLAYING = 1
STATE_FINISHED = 2
STATE_DEAD = 3

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
bidon_image = pygame.image.load('resources/bidon.png')
bidon_image = pygame.transform.scale(bidon_image, (100, 100))
bidon_rect = bidon_image.get_rect()

font = pygame.font.Font(None, 50)
cans = 0
max_cans = 7
already_printed = False
start_time = None

my_dict = {
    "2": False,
    "3": False,
    "4": False,
    "5": False,
    "6": False,
    "7": False,
    "8": False,
    "9": True
}

def draw_score(score, max_score):
    score_text = f"{score}/{max_score}"
    text = font.render(score_text, True, (255, 0, 0))
    screen.blit(text, (10, 10))

def draw_timer(remaining_time):
    timer_text = f"Time: {remaining_time}"
    text = font.render(timer_text, True, (255, 0, 0))
    screen.blit(text, (WIN_SIZE[0] - text.get_width() - 10, 10))

def load_collision_map(filename):
    with open(filename, 'r') as file:
        return [list(line.strip()) for line in file]

def start_menu():
    screen.fill((0, 0, 0))
    title_text = font.render("House Burn", True, (255, 0, 0))
    prompt_text = font.render("Press ENTER to start", True, (255, 255, 255))
    screen.blit(title_text, (WIN_SIZE[0] // 2 - title_text.get_width() // 2, WIN_SIZE[1] // 2 - title_text.get_height() // 2 - 50))
    screen.blit(prompt_text, (WIN_SIZE[0] // 2 - prompt_text.get_width() // 2, WIN_SIZE[1] // 2 - prompt_text.get_height() // 2 + 50))
    pygame.display.flip()

def finish_screen():
    screen.fill((0, 0, 0))
    congrats_text = font.render("Congratulations!", True, (255, 255, 0))
    done_text = font.render("You have burned the house!", True, (255, 255, 255))
    screen.blit(congrats_text, (WIN_SIZE[0] // 2 - congrats_text.get_width() // 2, WIN_SIZE[1] // 2 - congrats_text.get_height() // 2 - 50))
    screen.blit(done_text, (WIN_SIZE[0] // 2 - done_text.get_width() // 2, WIN_SIZE[1] // 2 - done_text.get_height() // 2 + 50))
    prompt_text = font.render("Press ENTER to restart", True, (255, 255, 255))
    screen.blit(prompt_text, (WIN_SIZE[0] // 2 - prompt_text.get_width() // 2, WIN_SIZE[1] // 2 - prompt_text.get_height() // 2 + 150))
    pygame.display.flip()

def death_screen():
    screen.fill((0, 0, 0))
    death_text = font.render("You Died!", True, (255, 0, 0))
    screen.blit(death_text, (WIN_SIZE[0] // 2 - death_text.get_width() // 2, WIN_SIZE[1] // 2 - death_text.get_height() // 2))
    prompt_text = font.render("Press ENTER to restart", True, (255, 255, 255))
    screen.blit(prompt_text, (WIN_SIZE[0] // 2 - prompt_text.get_width() // 2, WIN_SIZE[1] // 2 - prompt_text.get_height() // 2 + 50))
    pygame.display.flip()

def show_message(value):
    global cans, already_printed, game_state
    if value == '9' and cans < max_cans:
        root = tk.Tk()
        root.withdraw()
        message = "You need to collect all the petrol cans before burning the house!"
        messagebox.showinfo("Warning", message)
        root.destroy()
        character_rect.x += 110
        return
    elif value == '9' and cans == max_cans:
        game_state = STATE_FINISHED
        return
    if my_dict[value] == False:
        cans += 1
        my_dict[value] = True
    if cans == max_cans and already_printed == False:
        already_printed = True
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

def print_bidon(collision_map, rect):
    map_height = len(collision_map)
    map_width = len(collision_map[0])

    for y in range(map_height):
        for x in range(map_width):
            cell_value = collision_map[y][x]
            if cell_value in '2345678' and not my_dict[cell_value]:
                screen.blit(bidon_image, (x * TILE_SIZE, y * TILE_SIZE))

def main():
    global cans, already_printed, game_state, start_time
    clock = pygame.time.Clock()
    game_state = STATE_START_MENU

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state == STATE_START_MENU:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_state = STATE_PLAYING
                    start_time = time.time()
            elif game_state == STATE_FINISHED:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_state = STATE_START_MENU
                    cans = 0
                    already_printed = False
                    my_dict = {str(i): False for i in range(2, 9)}
                    my_dict["9"] = True
                    character_rect.topleft = PLAYER_INIT_POS
            elif game_state == STATE_DEAD:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_state = STATE_START_MENU
                    cans = 0
                    already_printed = False
                    my_dict = {str(i): False for i in range(2, 9)}
                    my_dict["9"] = True
                    character_rect.topleft = PLAYER_INIT_POS

        if game_state == STATE_START_MENU:
            start_menu()
        elif game_state == STATE_PLAYING:
            current_time = time.time()
            elapsed_time = current_time - start_time
            remaining_time = max(0, int(25 - elapsed_time))

            if remaining_time <= 0:
                game_state = STATE_DEAD

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
            print_bidon(collision_map, bidon_rect)
            draw_score(cans, max_cans)
            draw_timer(remaining_time)

            pygame.display.flip()
            clock.tick(60)
        elif game_state == STATE_FINISHED:
            finish_screen()
        elif game_state == STATE_DEAD:
            death_screen()

if __name__ == "__main__":
    main()