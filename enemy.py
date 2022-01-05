# -*- coding: utf-8 -*-

import pygame
import random
import time
import sys
import os
from pygame.locals import *

pygame.init()

width = 1200
height = 600

color = [255,255,255]

count_font = pygame.font.SysFont("monospace", 30)

player_img = pygame.image.load("spaceShip.png")
player_img = pygame.transform.scale(player_img, (100,100))
player_rect = player_img.get_rect()
player_rect.y = 500

#line_red = pygame.image.load("line_red.png")
#line_red.fill(color)
#line_red = pygame.transform.scale(line_red, (80, 100))
#line_visible = False
#line_position = [0, 0]

line_img = []
line_visible = []
line_position = []
line_index = []
index_line = 0


#alien_img = pygame.image.load("alien.png")
#alien_img = pygame.transform.scale(alien_img, (50, 50))
#alien_visible = True
#alien_position = [60, 60]

alien_img = []
alien_visible = []
alien_position = []
alien_time = []
alien_index = []
index = 0

img = pygame.image.load("alien.png")
img = pygame.transform.scale(img, (50, 50))
alien_img.append(img)
alien_visible.append(True)
alien_position.append([50,50])
alien_time.append(0)
alien_index.append(index)
index+=1


add_alien = False
alien_start = False


screen = pygame.display.set_mode((width, height))
screen.fill(color)
pygame.display.flip()
#screen.blit(player_img, (30,50))


def shot():
    #line_red_rec.x = player_rect.centerx
    #line_red_rec.y = player_rect.centery + 90
    #screen.blit(line_red, line_red_rec)
    pygame.display.flip()
    pygame.display.update()

def alien():
    alien_position[1] += 10
    time.sleep(2)

def rand():
    n = 0
    i = random.randint(0, 1150)
    while n is not index:
        for pos in alien_position:
            if i + 50 <= pos[0] or i + 50 >= pos[0] + 50:
                n+=1
        if n is not index:
            i = random.randint(0, 1150)
            n = 0
    return i



playerLeft = 60
playerRight = 40
x_speed = 0
y_speed = 0
shot_true = False
alien_move = True
play_game = True
move_time = 0
move_faster = 0
move_faster_True = True
count_kills = 0
text1 = 0



while play_game:
    event = pygame.event.poll()
    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
        pygame.quit()
        sys.exit()

    if line_visible is True:
        line_red = pygame.image.load("line_red.png")
        line_red = pygame.transform.scale(line_red, (80, 100))
        line_visible = False

    if shot_true is True:
        line_position[1] -= 0.5
        if line_position[1] <= 0:
            shot_true = False
        for image, pos, vis, time, ind in zip(alien_img, alien_position, alien_visible, alien_time, alien_index):
            if vis is True:
                if line_position[1] <= (pos[1]  + 50) and line_position[1] >= pos[1]:
                    if line_position[0] <= pos[0] + 10 and line_position[0] >= (pos[0] - 50):
                        print "rocket"
                        alien_img[ind].fill(color)
                        alien_position[ind][1] = 60
                        alien_visible[ind] = False
                        shot_true = False
                        count_kills += 1
                        alien_time[ind] = 0
                        if count_kills % 5 == 0:
                            move_faster_True = True
                        if count_kills % 2 == 0:
                            add_alien = True
                            alien_start = True

    #create a new alien after n kills
    if count_kills % 2 == 0 and add_alien is True:
        img = pygame.image.load("alien.png")
        img = pygame.transform.scale(img, (50, 50))
        alien_img.append(img)
        alien_visible.append(True)
        alien_position.append([rand(), 50])
        alien_time.append(0)
        alien_index.append(index)
        index+=1
        add_alien = False

    #after kill hide the laser
    if shot_true is False:
        line_red.fill(color)
        line_visible = False

    #after t times make the aliens faster
    if count_kills % 5 == 0 and move_faster_True is True:
        move_faster += 0.005
        if move_faster_True is True:
            move_faster_True = False

    #refresh invisible aliens
    for vis, pos, ind in zip(alien_visible, alien_position, alien_index):
        if vis is False:
            alien_position[ind][0] = rand()
            img = pygame.image.load("alien.png")
            img = pygame.transform.scale(img, (50, 50))
            alien_img[ind] = img
            alien_visible[ind] = True

    for pos, time, vis, ind in zip(alien_position, alien_time,alien_visible, alien_index):
        if vis is True:
            time += move_faster
            if pos[1] >= 600:
                play_game = False
            elif time >= 2:
                alien_position[ind][1] += 10
                time = 0
            alien_time[ind] = time


    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            x_speed = -1
        elif event.key == pygame.K_RIGHT:
            x_speed = 1
        elif event.key == pygame.K_s and shot_true is False:
            line_position[0] = player_rect.x
            line_position[1] = player_rect.centery - 130
            shot_true = True
            line_visible = True
            #player_rect.right += 20
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            x_speed = 0

    if player_rect.x < 0:
        player_rect.x=20
    if player_rect.x > 1120:
        player_rect.x= 1100

    #player_rect = player_rect.move(x_speed,y_speed)
    screen.fill(color)
    player_rect = player_rect.move(x_speed, 0)
    screen.blit(player_img, player_rect)
    screen.blit(line_red, line_position)
    for image, pos in zip(alien_img, alien_position):
        screen.blit(image, pos)

    text = count_font.render(str(count_kills) + " Kills", True, (100, 200, 100))
    screen.blit(text, (10, 20))
    pygame.display.flip()
    pygame.display.update()

while play_game is False:
    screen = pygame.display.set_mode((width, height))
    event = pygame.event.poll()
    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
        pygame.quit()
        sys.exit()
    screen.fill(color)
    screen.blit(text, (600, 100))
    text = count_font.render(str(count_kills) + " Kills", True, (100, 200, 100))
    text1 = count_font.render("YOU LOST", True, (100, 200, 100))
    screen.blit(text1, (600, 300))
    pygame.display.flip()





def main():
    """
    Add Documentation here
    """
    pass  # Replace Pass with Your Code


if __name__ == '__main__':
    main()