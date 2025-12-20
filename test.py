import pygame
pygame.init()

import random
from tqdm import tqdm
from stuff.bot import Bot
from stuff.game import Game
from stuff.utils import *

class Test:
    def __init__(self, game, bot, game_time, prev_weights_upstack=None, prev_weights_downstack=None):
        self.game = game
        self.bot = bot
        self.game_time = game_time
        self.active = False
        self.prev_weights_upstack = prev_weights_upstack
        self.prev_weights_downstack = prev_weights_downstack
        self.set()

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, "#ffffff", (0, 0, self.game_timer/self.game_time*SCREEN_W, 5))

    def restart(self):
        print(self.game.seed, self.game.attack, f"{self.weights_upstack}, {self.weights_downstack}")
        self.game.restart()
        self.bot.restart()
        self.set()

    def set(self):
        self.game_timer = 0
        weights_upstack = {
            "lines": random.random(),
            "change_rate": -random.random(),
            "holes": -random.random(),
            "avg_height": 0,
            "well_depth": random.random()*0.03,
        }
        weights_downstack = {
            "lines": random.random(),
            "change_rate": -random.random(),
            "holes": -random.random(),
            "avg_height": -random.random(),
            "well_depth": -random.random()*0.03,
        }

        if self.prev_weights_upstack:
            self.weights_upstack = self.prev_weights_upstack
            for weight in self.weights_upstack:
                self.weights_upstack[weight] += (weights_upstack[weight]-self.weights_upstack[weight])*RATE
        else:
            self.weights_upstack = weights_upstack

        if self.prev_weights_downstack:
            self.weights_downstack = self.prev_weights_downstack
            for weight in self.weights_downstack:
                self.weights_downstack[weight] += (weights_downstack[weight]-self.weights_downstack[weight])*RATE
        else:
            self.weights_downstack = weights_downstack

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
            
class Result:
    def __init__(self, score, weights_upstack, weights_downstack):
        self.score = score
        self.weights_upstack = weights_upstack
        self.weights_downstack = weights_downstack

RATE = 0.1
LEARN_DEPTH = 5
LEARN_COUNT = 10
TEST_DURATION = 1000

def run(prev_result, depth=0):
    print(f"depth: {depth}")
    if depth > LEARN_DEPTH:
        return prev_result
    
    results = [prev_result]
    for _ in tqdm(range(LEARN_COUNT)):
        game = Game()
        bot = Bot(game, 1)
        test = Test(game, bot, TEST_DURATION, prev_result.weights_upstack, prev_result.weights_downstack)

        for _ in range(TEST_DURATION):
            for event in bot.get_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.restart()
                        bot.restart()
                    game.keydown(event.key)
                if event.type == pygame.KEYUP:
                    game.keyup(event.key)

            game.update(1)
            bot.update(1)
            # test.update(1)

        score = game.attack
        print(f"\nscore: {score}")
        results.append(Result(score, test.weights_upstack, test.weights_downstack))
        
    results.sort(key=lambda x: x.score)
    return run(results[-1], depth+1)

result = run(Result(0, None, None))
with open("result.py", "a") as file:
    file.writelines("\n")
    file.writelines(f"# score: {result.score}\n")
    file.writelines(f"up = {result.weights_upstack}\n")
    file.writelines(f"down = {result.weights_downstack}\n")