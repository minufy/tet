import pygame
import sys
import random
pygame.init()
from bot import Bot
from game import Game
from minos import *
from utils import *

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

clock = pygame.time.Clock()

class Test:
    def __init__(self, game, bot, game_time=5000):
        self.game = game
        self.bot = bot
        self.game_time = game_time
        self.active = True
        self.restart()

    def draw(self, screen):
        if self.active:
            depth_text = render_text(f"depth: {DEPTH}", MINO_COLORS["I"])
            screen.blit(depth_text, (10, 10+font.get_height()*5))
            best_count_text = render_text(f"best_count: {BEST_COUNT}", MINO_COLORS["I"])
            screen.blit(best_count_text, (10, 10+font.get_height()*6))

            attack_text = render_text(f"attack: {game.attack}", MINO_COLORS["Z"])
            screen.blit(attack_text, (10, 10+font.get_height()*8))

            pygame.draw.rect(screen, "#ffffff", (0, 0, self.game_timer/self.game_time*SCREEN_W, 5))

    def restart(self):
        self.game_timer = 0
        self.weights = {
            "line": random.randint(0, 100)/100,
            "change_rate": -random.randint(5, 100)/50,
            "holes": -random.randint(5, 100)/50,
            "well_depth": random.randint(0, 4)/100,
        }
        self.bot.set_weights(self.weights)
        
    def update(self, dt):
        if self.active:
            self.game_timer += dt
            if self.game_timer > self.game_time:
                print(game.attack, self.weights)
                self.game.restart()
                self.bot.restart()
                self.restart()
            
game = Game(-1)
bot = Bot(game, 10)
test = Test(game, bot)
test.active = False
 
while True:
    screen.fill("#333333")
     
    for event in pygame.event.get()+bot.get_events():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game = Game(-1)
            game.keydown(event.key)
        if event.type == pygame.KEYUP:
            game.keyup(event.key)

    game.draw(screen)
    test.draw(screen)
    bot.draw(screen)

    dt = clock.tick(120)
    
    game.update(dt)
    test.update(dt)
    bot.update(dt)

    pygame.display.update()