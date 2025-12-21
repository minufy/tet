import pygame
pygame.init()

import sys
from stuff.bot import Bot
from stuff.game import Game
from stuff.minos import *
from stuff.utils import *
from stuff.result import up, down

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

clock = pygame.time.Clock()

game = Game()
bot = Bot(game, 1)
bot.set_weights(up, down)

while True:
    screen.fill("#333333")
     
    for event in pygame.event.get()+bot.get_events():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game.restart()
                bot.restart()
            game.keydown(event.key)
        if event.type == pygame.KEYUP:
            game.keyup(event.key)

    game.draw(screen)
    draw_hud(screen, bot, game)

    dt = clock.tick(120)

    game.update(dt)
    bot.update(dt)
    # print(bot.get_scores(game.board))

    pygame.display.update()