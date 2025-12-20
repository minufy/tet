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
        self.active = False
        self.set()

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, "#ffffff", (0, 0, self.game_timer/self.game_time*SCREEN_W, 5))

    def restart(self):
        print(game.seed, game.attack, f"{self.weights_upstack}, {self.weights_downstack}")
        self.game.restart()
        self.bot.restart()
        self.set()

    def set(self):
        self.game_timer = 0
        change_rate = -random.randint(50, 1000)/750
        holes = -random.randint(50, 1000)/750
        lines = random.randint(0, 500)/1000
        self.weights_upstack = {
            "lines": lines,
            "change_rate": change_rate,
            "holes": holes,
            "avg_height": 0,
            "well_depth": random.randint(0, 40)/1000,
        }
        self.weights_downstack = {
            "lines": lines*2,
            "change_rate": change_rate,
            "holes": holes,
            "avg_height": -random.randint(0, 1000)/1000,
            "well_depth": -random.randint(0, 40)/1000,
        }
        for weight in self.weights_upstack:
            self.weights_upstack[weight] = round(self.weights_upstack[weight], 3)
        for weight in self.weights_downstack:
            self.weights_downstack[weight] = round(self.weights_downstack[weight], 3)

        self.bot.set_weights(self.weights_upstack, self.weights_downstack)
        
    def update(self, dt):
        if self.active:
            self.game_timer += dt
            if self.game_timer > self.game_time:
                self.restart()
            
game = Game()
bot = Bot(game, 100)
test = Test(game, bot, 10000)
test.active = True
# bot.set_weights(*WEIGHTS[2])
 
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
            # if event.key == pygame.K_BAC KSPACE:
            #     test.restart()
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