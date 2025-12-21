import pygame
import time
from stuff.board import Board
from stuff.handler import Handler
from stuff.rng import RNG
from stuff.minos import *
from stuff.utils import *

class Game:
    def __init__(self, seed=None):
        self.seed = round(time.time()*10000)
        if seed:
            self.seed = seed
        self.rng = RNG(self.seed)
        self.restart()

    def restart(self):
        self.board = Board(10, 40, 20)
        self.queue = []
        self.next()
        self.handler = Handler(DAS, ARR, SDF)
        self.hold_type = None
        self.held = False
        self.attack = 0

        self.send_garbage = 0
        self.take_garbage = 0

    def draw_mino(self, screen, pos, mx, my, mt, mr, color=None):
        if color == None:
            color = MINO_COLORS[mt]
        for y, row in enumerate(MINO_SHAPES[mt][str(mr)]):
            for x, dot in enumerate(row):
                if dot:
                    rect = ((mx+x)*UNIT+pos[0], (my+y)*UNIT+pos[1], UNIT, UNIT)
                    pygame.draw.rect(screen, color, rect)
    
    def next(self):
        if len(self.queue) <= 5:
            self.queue += self.rng.shuffleArray(MINO_TYPES.copy())
        self.mino = self.pop_queue()

    def draw_next(self, screen, pos):
        gap = 2.8
        for i in range(5):
            mino_type = self.queue[i]
            x = 0
            y = 0
            if mino_type == "I":
                y = -0.5
            if mino_type == "O":
                x = -0.5
            self.draw_mino(screen, pos, 11+x, y+1+i*gap, mino_type, 0, MINO_COLORS[mino_type])

    def hard_drop(self):
        self.board.add_garbage(self.take_garbage, round(self.rng.nextFloat()))
        self.take_garbage = 0
        self.held = False
        for _ in range(self.board.h):
            if self.mino.move(0, 1, self.board) == False:
                self.board.place(self.mino)
                
                attack = ATTACK_TABLE[self.board.line_clear()]
                self.send_garbage += attack
                self.attack += attack
                
                self.next()
                break

    def keydown(self, key):
        if key == pygame.K_RIGHT:
            self.handler.down_right()
            self.mino.move(1, 0, self.board)
        if key == pygame.K_LEFT:
            self.handler.down_left()
            self.mino.move(-1, 0, self.board)
        if key == pygame.K_DOWN:
            self.handler.down_soft_drop()
        if key == pygame.K_UP:
            self.mino.rotate(1, self.board)
        if key == pygame.K_LCTRL:
            self.mino.rotate(-1, self.board)
        if key == pygame.K_a:
            self.mino.rotate(2, self.board)
        if key == pygame.K_SPACE:
            self.hard_drop()
        if key == pygame.K_LSHIFT:
            self.hold()

    def keyup(self, key):
        if key == pygame.K_RIGHT:
            self.handler.up_right()
        if key == pygame.K_LEFT:
            self.handler.up_left()
        if key == pygame.K_DOWN:
            self.handler.up_soft_drop()

    def hold(self):
        if self.held:
            return
        old_type = self.mino.type
        if self.hold_type == None:
            self.next()
        else:
            self.mino = Mino(self.hold_type, 3, self.board.margin_top-4)
        self.hold_type = old_type
        self.held = True

    def update(self, dt):
        movement_queue = self.handler.update(dt, self.board)
        for x, y in movement_queue:
            self.mino.move(x, y, self.board)

    def draw_shadow(self, screen, pos):
        shadow_mino = Mino(self.mino.type, self.mino.x, self.mino.y, self.mino.rotation)
        for _ in range(self.board.h):
            if shadow_mino.move(0, 1, self.board) == False:
                break
        self.draw_mino(screen, pos, self.mino.x, shadow_mino.y, self.mino.type, self.mino.rotation, MINO_COLORS["X"])

    def draw(self, screen, offset=(0, 0)):
        pos = (SCREEN_W/2-UNIT*10/2+offset[0], SCREEN_H/2-UNIT*20/2+offset[1])
        pos_margin = (pos[0], pos[1]-self.board.margin_top*UNIT)
        self.board.draw(screen, pos_margin)
        self.draw_shadow(screen, pos_margin)
        self.draw_mino(screen, pos_margin, self.mino.x, self.mino.y, self.mino.type, self.mino.rotation)
        if self.hold_type:
            color = MINO_COLORS[self.hold_type]
            if self.held:
                color = MINO_COLORS["H"]
            self.draw_mino(screen, pos, -5, 1, self.hold_type, 0, color)
        self.draw_next(screen, pos)

    def fill_queue(self):
        self.queue += self.rng.shuffleArray(MINO_TYPES.copy())

    def pop_queue(self):
        return Mino(self.queue.pop(0), 3, self.board.margin_top-4)

    def get_garbage(self):
        garbage = self.send_garbage
        self.send_garbage = 0
        return garbage
    
    def set_garbage(self, amount):
        self.take_garbage += amount