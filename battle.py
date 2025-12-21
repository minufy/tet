import pygame
pygame.init()

import sys
import time
import zmq
from stuff.bot_emu import BotEmu
from stuff.game import Game
from stuff.minos import *
from stuff.utils import *

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

clock = pygame.time.Clock()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

seed = time.time()*1000
p1_game = Game(seed)
p2_game = Game(seed)
bot_2 = BotEmu(p2_game, socket)

while True:
    screen.fill("#333333")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                seed = time.time()*1000
                p1_game.restart(seed)
                p2_game.restart(seed)
            if event.key in keys_to_code:
                p1_game.keydown(keys_to_code[event.key])
        if event.type == pygame.KEYUP:
            if event.key in keys_to_code:
                p1_game.keyup(keys_to_code[event.key])

    for event in bot_2.get_events():
        type, key = event.split(".")
        if type == "keydown":
            p2_game.keydown(key)
        if type == "keyup":
            p2_game.keyup(key)

    p1_game.draw(screen, (-UNIT*12, 0))
    p2_game.draw(screen, (UNIT*12, 0))

    dt = clock.tick(60)

    p1_game.update(dt)
    p2_game.update(dt)
    
    p2_game.add_garbage(p1_game.get_garbage())
    p1_game.add_garbage(p2_game.get_garbage())

    bot_2.update(dt)

    pygame.display.update()