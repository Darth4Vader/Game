# -*- coding: utf-8 -*-

import pygame
import random
import time
import sys
import os
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
sound1 = pygame.mixer.Sound('shoot.wav')
sound2 = pygame.mixer.Sound('invaderkilled.wav')
sound3 = pygame.mixer.Sound('game_over.wav')

width = 1200
height = 600

color = [255,255,255]

count_font = pygame.font.SysFont("monospace", 30)

player_img = pygame.image.load("spaceShip.png")
player_img = pygame.transform.scale(player_img, (100,100))
player_rect = player_img.get_rect()
player_rect.y = 500


line_red = pygame.image.load("line_red.png")
line_red.fill(color)
line_red = pygame.transform.scale(line_red, (80, 100))
line_visible = False
line_position = [0, 0]


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
alien_position.append([50, 50])
alien_time.append(0)
alien_index.append(index)
index+=1


add_alien = False
alien_start = False


screen = pygame.display.set_mode((width, height))
screen.fill(color)
pygame.display.flip()

def rand():
    n = 0
    i = random.randint(0, 1130)
    #for pos in alien_position:
        #if (i + 50 <= pos[0] or i + 50 >= pos[0] + 50) and pos[1] >= 100:
            #n+=1
    while n is not index:
        for pos in alien_position:
            #if (i + 50 <= pos[0] or i + 50 >= pos[0] + 50):
            if ((i + 50) < pos[0] or i > pos[0] + 50):
                n+=1
            else:
                if pos[1] >= 120:
                    return i
        if n is not index:
            i = random.randint(0, 1150)
            n = 0
    return i


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
        line_position[1] -= 1.5
        if line_position[1] <= 0:
            shot_true = False
        for image, pos, vis, time, ind in zip(alien_img, alien_position, alien_visible, alien_time, alien_index):
                if (line_position[1] <= (pos[1] + 50) and line_position[1] >= pos[1]) or (pos[1] >= line_position[1] and pos[1] <= line_position[1] + 50):
                    if (line_position[0] <= pos[0] + 10 and line_position[0] >= (pos[0] - 50)):
                        sound2.play()
                        alien_img[ind].fill(color)
                        alien_visible[ind] = False
                        shot_true = False
                        count_kills += 1
                        alien_time[ind] = 0
                        if count_kills % 10 == 0:
                            move_faster_True = True
                        if count_kills % 5 == 0:
                            add_alien = True
                            alien_start = True

    #create a new alien after n kills
    if count_kills % 5 == 0 and add_alien is True and index is not 10:
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
    if count_kills % 10 == 0 and move_faster_True is True:
        move_faster += 0.005
        if move_faster_True is True:
            move_faster_True = False

    #refresh invisible aliens
    for vis, pos, ind in zip(alien_visible, alien_position, alien_index):
        if vis is False:
            alien_position[ind][0] = rand()
            alien_position[ind][1] = 50
            img = pygame.image.load("alien.png")
            img = pygame.transform.scale(img, (50, 50))
            alien_img[ind] = img
            alien_visible[ind] = True

    for pos, time, vis, ind in zip(alien_position, alien_time,alien_visible, alien_index):
        if vis is True:
            time += move_faster
            if pos[1] >= 550 or (pos[0] >= player_rect.x and (player_rect.x + 50) >= pos[0] and (pos[1] > 450)):
                play_game = False
            else:
                if player_rect.x > pos[0]:
                    if pos[0] + 50 >= player_rect.x and pos[1] > 450:
                        play_game = False
                    elif time >= 2:
                        alien_position[ind][1] += 10
                        time = 0
                else:
                    if player_rect.x < pos[0]:
                        if pos[0] <= player_rect.x + 100 and pos[1] > 450:
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
            sound1.play()
            line_position[0] = player_rect.x + 6
            line_position[1] = player_rect.centery - 146
            shot_true = True
            line_visible = True
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            x_speed = 0

    if player_rect.x < 0:
        player_rect.x=20
    if player_rect.x > 1100:
        player_rect.x= 1080

    screen.fill(color)
    player_rect = player_rect.move(x_speed, 0)
    screen.blit(player_img, player_rect)
    screen.blit(line_red, line_position)
    for image, pos, vis in zip(alien_img, alien_position, alien_visible):
        if vis is True:
            screen.blit(image, pos)
    text = count_font.render(str(count_kills) + " Kills", True, (100, 200, 100))
    screen.blit(text, (10, 20))
    pygame.display.flip()
    pygame.display.update()

sound3.play()

txt = open("BestGame.txt", "r")
line = txt.readline()
if int(line) < count_kills:
    txt.close()
    txt = open("BestGame.txt", "w+")
    txt.write(str(count_kills))
    txt.close()
txt = open("BestGame.txt", "r")
line = txt.readline()
txt.close()

count_font1 = pygame.font.SysFont("monospace", 80)
count_font2 = pygame.font.SysFont("monospace", 40)
text = count_font1.render("GAME OVER", True, (0, 0, 0))
text1= count_font2.render(str(count_kills) + " Kills", True, (100, 200, 100))
text2 = count_font2.render(str(line) + " BEST SCORE", True, (100, 200, 100))

while play_game is False:
    screen = pygame.display.set_mode((width, height))
    event = pygame.event.poll()
    if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
        pygame.quit()
        sys.exit()
    screen.fill(color)
    screen.blit(text, (400, 100))
    screen.blit(text1, (520, 250))
    screen.blit(text2, (520, 400))
    pygame.display.flip()

def main():

    pass  # Replace Pass with Your Code


if __name__ == '__main__':
    main()