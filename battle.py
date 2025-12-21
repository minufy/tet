import pygame
pygame.init()

import sys
import time
from stuff.bot import Bot
from stuff.game import Game
from stuff.minos import *
from stuff.utils import *
from stuff.result import up, down

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

clock = pygame.time.Clock()

seed = time.time()
player_game = Game(seed)
bot_game = Game(seed)
bot = Bot(bot_game, 1000)
bot.set_weights(up, down)

while True:
    screen.fill("#333333")
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player_game.restart()
                bot_game.restart()
                bot.restart()
            player_game.keydown(event.key)
        if event.type == pygame.KEYUP:
            player_game.keyup(event.key)

    for event in bot.get_events():
        if event.type == pygame.KEYDOWN:
            bot_game.keydown(event.key)
        if event.type == pygame.KEYUP:
            bot_game.keyup(event.key)

    player_game.draw(screen, (-UNIT*12, 0))
    bot_game.draw(screen, (UNIT*12, 0))

    dt = clock.tick(120)

    player_game.update(dt)
    bot_game.update(dt)
    
    bot_game.add_garbage(player_game.get_garbage())
    player_game.add_garbage(bot_game.get_garbage())

    bot.update(dt)

    pygame.display.update()