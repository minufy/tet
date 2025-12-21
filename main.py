import pygame
pygame.init()

import sys
from stuff.bot import Bot
from stuff.game import Game
from stuff.minos import *
from stuff.utils import *
from stuff.text import *
from stuff.result import up, down

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

clock = pygame.time.Clock()

game = Game()
bot = Bot(game, 20)
bot.set_weights(up, down)

def draw_hud(screen, bot, game):
    x = 15
    y = 20
    gap = 20

    weights_text = render_text(font_bold, "WEIGHTS", MINO_COLORS["O"])
    screen.blit(weights_text, (x, y))
    y += font_bold.get_height()

    weights = bot.get_weights(bot.game.board)
    for i, weight in enumerate(weights):
        text = render_text(font, f"{weight}: {weights[weight]}")
        screen.blit(text, (x, y))
        y += font.get_height()

    y += gap

    search_text = render_text(font_bold, "SEARCH", MINO_COLORS["I"])
    screen.blit(search_text, (x, y))
    y += font_bold.get_height()

    depth_text = render_text(font, f"depth: {DEPTH}")
    screen.blit(depth_text, (x, y))
    y += font.get_height()
    
    best_count_text = render_text(font, f"best_count: {BEST_COUNT}")
    screen.blit(best_count_text, (x, y))
    y += font.get_height()

    y += gap

    state_text = render_text(font_bold, "STATE", MINO_COLORS["Z"])
    screen.blit(state_text, (x, y))
    y += font_bold.get_height()

    attack_text = render_text(font, f"attack: {game.attack}")
    screen.blit(attack_text, (x, y))
    y += font.get_height()
    
    mode_text = render_text(font, f"mode: {bot.get_mode(game.board)}")
    screen.blit(mode_text, (x, y))
    y += font.get_height()

    avg_height_text = render_text(font, f"avg_height: {sum(bot.get_heights(game.board))/game.board.w}")
    screen.blit(avg_height_text, (x, y))
    y += font.get_height()

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