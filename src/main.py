#!/usr/bin/env python3

#
# EPITECH PROJECT, 2024
# HouseBurn
# File description:
# houseBurn
#

import pygame
import sys

WIN_SIZE = 1000, 1000
PLAYER_SIZE = 80, 80
PLAYER_INIT_POS = 470, 845

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

def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            character_rect.x -= character_speed
            if not map_rect.contains(character_rect):
                character_rect.x += character_speed

        if keys[pygame.K_RIGHT]:
            character_rect.x += character_speed
            if not map_rect.contains(character_rect):
                character_rect.x -= character_speed

        if keys[pygame.K_UP]:
            character_rect.y -= character_speed
            if not map_rect.contains(character_rect):
                character_rect.y += character_speed

        if keys[pygame.K_DOWN]:
            character_rect.y += character_speed
            if not map_rect.contains(character_rect):
                character_rect.y -= character_speed

        screen.fill((0, 0, 0))
        screen.blit(map_image, map_rect.topleft)
        screen.blit(character_image, character_rect.topleft)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()