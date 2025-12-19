import pygame
import sys
import random
from bot import Bot
from game import Game
from minos import *
from utils import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

clock = pygame.time.Clock()

font = pygame.font.Font("Pretendard-Regular.ttf", 40)

def render_text(text, color):
    surface = font.render(text, True, color)
    return surface

game = Game(-1)

results = []

game_timer = 0
game_time = 5000
weights = {
    "line": random.randint(0, 100)/50,
    "change_rate": random.randint(0, 100)/50,
    "holes": random.randint(0, 100)/50,
}

{'line': 0.96, 'change_rate': 0.97, 'holes': 0.76}
{'line': 0.6, 'change_rate': 0.82, 'holes': 0.55}
{'line': 1.48, 'change_rate': 1.68, 'holes': 1.42}
{'line': 0.02, 'change_rate': 0.94, 'holes': 0.57}
{'line': 0.21, 'change_rate': 0.25, 'holes': 0.31}
{'line': 0.4, 'change_rate': 0.29, 'holes': 0.29}

input_time = 10
bot = Bot(game, input_time, weights)

while True:
    screen.fill("#333333")
    dt = clock.tick(120)
     
    for event in pygame.event.get()+bot.get_events(dt):
        if event.type == pygame.QUIT:
            results.sort()
            print(results[-1])
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game = Game(-1)
            game.keydown(event.key)
        if event.type == pygame.KEYUP:
            game.keyup(event.key)

    game.draw(screen)
    game.update(dt)
    bot.update(dt)

    for i, weight in enumerate(weights):
        text = render_text(f"{weight}: {weights[weight]}", "#ffffff")
        screen.blit(text, (10, 10+font.get_height()*i))
        
    depth_text = render_text(f"depth: {DEPTH}", MINO_COLORS["I"])
    screen.blit(depth_text, (10, 10+font.get_height()*4))
    best_count_text = render_text(f"best_count: {BEST_COUNT}", MINO_COLORS["I"])
    screen.blit(best_count_text, (10, 10+font.get_height()*5))

    attack_text = render_text(f"attack: {game.attack}", MINO_COLORS["Z"])
    screen.blit(attack_text, (10, 10+font.get_height()*7))

    pygame.draw.rect(screen, "#ffffff", (0, 0, game_timer/game_time*SCREEN_W, 5))

    game_timer += dt
    if game_timer > game_time:
        print(game.attack, weights)
        results.append((game.attack, weights))
        game_timer = 0
        game = Game(-1)
        weights = {
            "line": random.randint(0, 100)/100,
            "change_rate": random.randint(0, 100)/100,
            "holes": random.randint(0, 100)/100,
        }
        bot = Bot(game, input_time, weights)

    pygame.display.update()