import pygame
pygame.init()

import sys
import time
import zmq
from bot_emu import BotEmu
from tet_utils.game import Game
from tet_utils.minos import *

keys_to_code = {
    pygame.K_LSHIFT: "hold",
    pygame.K_UP: "cw",
    pygame.K_LCTRL: "ccw",
    pygame.K_a: "180",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
    pygame.K_SPACE: "harddrop",
    pygame.K_DOWN: "softdrop",
}

SCREEN_W = 1280
SCREEN_H = 720
UNIT = 24

handling = {
    "das": 117,
    "arr": 0,
    "sdf": 0
}
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

clock = pygame.time.Clock()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

seed = time.time()*1000
games = [
    Game(handling, seed),
    Game(handling, seed),
]
bots = [
    BotEmu(games[0]),
    BotEmu(games[1]),
]
ready = {}

while True:
    screen.fill("#333333")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                seed = time.time()*1000
                games[0].restart(seed)
                games[1].restart(seed)
            if event.key in keys_to_code:
                games[0].keydown(keys_to_code[event.key])
        if event.type == pygame.KEYUP:
            if event.key in keys_to_code:
                games[0].keyup(keys_to_code[event.key])

    for event in bots[0].get_events():
        type, key = event.split(".")
        if type == "keydown":
            games[0].keydown(key)
        if type == "keyup":
            games[0].keyup(key)

    for event in bots[1].get_events():
        type, key = event.split(".")
        if type == "keydown":
            games[1].keydown(key)
        if type == "keyup":
            games[1].keyup(key)

    games[0].draw(screen, UNIT, (-UNIT*12, 0))
    games[1].draw(screen, UNIT, (UNIT*12, 0))

    dt = clock.tick(60)

    games[0].update(dt)
    games[1].update(dt)

    try:
        data = socket.recv_json(flags=zmq.NOBLOCK)
        index = data["index"]
        if index not in ready:
            ready[index] = True
        if len(ready) == len(bots):
            game_state = bots[index].update(dt, data)
            socket.send_json(game_state)
        else:
            socket.send_json({
                "state": "not_started",
                "grid": [],
                "queue": [],
                "mino_type": "",
                "hold_mino_type": ""
            })
        
    except zmq.Again:
        pass

    games[0].add_garbage(games[1].get_garbage())
    games[1].add_garbage(games[0].get_garbage())

    pygame.display.update()