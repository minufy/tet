import multiprocessing as mp
import pygame
import random
from stuff.bot import Bot
from stuff.game import Game
from stuff.utils import *
# from stuff.result import up, down

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
            "well_depth_sum": -random.random(),
        }
        weights_downstack = {
            "lines": random.random(),
            "change_rate": -random.random(),
            "holes": -random.random(),
            "avg_height": -random.random(),
            "well_depth_sum": -random.random(),
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

RATE = 0.2
TEST_DEPTH = 3
TEST_COUNT = 2
TEST_DURATION = 2000

def run_game(bot, game):
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

def run_test(args):
    i, prev_result = args
    game = Game()
    bot = Bot(game, 1)
    test = Test(game, bot, TEST_DURATION, prev_result.weights_upstack, prev_result.weights_downstack)
    
    run_game(bot, game)
    # score = game.attack
    score = game.attack+sum(bot.get_scores(game.board))
    print(f"{i+1}/{TEST_COUNT}")
    print(f"score: {score}")
    return Result(score, test.weights_upstack, test.weights_downstack)

def run(prev_result, depth=0):
    print(f"depth: {depth}")
    if depth > TEST_DEPTH:
        return prev_result
    
    results = [prev_result]
    args = [(i, prev_result) for i in range(TEST_COUNT)]
    with mp.Pool(processes=3) as pool:
        new_results = pool.map(run_test, args)
    results += new_results
        
    results.sort(key=lambda x: x.score)
    return run(results[-1], depth+1)

if __name__ == "__main__":
    mp.freeze_support()
    
    result = run(Result(0, None, None))
    with open("stuff/result.py", "a") as file:
        file.writelines("\n")
        file.writelines(f"# score: {result.score}\n")
        file.writelines(f"up = {result.weights_upstack}\n")
        file.writelines(f"down = {result.weights_downstack}\n")