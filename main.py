import math
import pygame
import sys
import time
from minos import *

pygame.init()
SCREEN_W = 1600
SCREEN_H = 900
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

clock = pygame.time.Clock()

UNIT = 32

class RNG:
    def __init__(self, seed):
        self.t = seed % 2147483647

        if self.t == 0:
            self.t += 2147483646

    def next(self):
        self.t = 16807 * self.t % 2147483647
        return self.t
    
    def nextFloat(self):
        return (self.next() - 1) / 2147483646

    def shuffleArray(self, array):
        if len(array) == 0:
            return array

        for i in range(len(array)-1, 0, -1):
            r = math.floor(self.nextFloat() * (i + 1))
            array[i], array[r] = array[r], array[i]

        return array

class Board:
    def __init__(self, w, h, margin_top):
        self.w = w
        self.h = h
        self.margin_top = margin_top
        self.grid = [[" "]*w for _ in range(h)]

    def draw(self, screen, pos):
        for y in range(self.h):
            for x in range(self.w):
                rect = (x*UNIT+pos[0], y*UNIT+pos[1], UNIT, UNIT)
                if self.grid[y][x] == " ":
                    if y >= self.margin_top:
                        pygame.draw.rect(screen, MINO_COLORS["X"], rect, 1)
                else:
                    pygame.draw.rect(screen, MINO_COLORS[self.grid[y][x]], rect)

    def line_clear(self):
        for y in range(self.h):
            for x in range(self.w):
                if self.grid[y][x] == " ":
                    break
            else:
                self.grid.pop(y)
                self.grid.insert(0, [" "]*self.w)

    def place(self, mino):
        for y, row in enumerate(MINO_SHAPES[mino.type][str(mino.rotation)]):
            for x, dot in enumerate(row):
                if dot:
                    self.grid[mino.y+y][mino.x+x] = mino.type
        self.line_clear()

class Handler:
    def __init__(self, das, arr, sdf):
        self.das = das
        self.arr = arr
        self.sdf = sdf

        self.held = []

        self.right_hold_ms = 0
        self.right_arr_timer = 0

        self.left_hold_ms = 0
        self.left_arr_timer = 0

        self.soft_drop_held = False
        self.soft_drop_sdf_timer = 0

    def down_right(self):
        self.held.append("right")
        self.right_hold_ms = 0
        self.right_arr_timer = 0

    def down_left(self):
        self.held.append("left")
        self.left_hold_ms = 0
        self.left_arr_timer = 0

    def down_soft_drop(self):
        self.soft_drop_held = True
        self.soft_drop_sdf_timer = 0

    def up_right(self):
        self.held.remove("right")

    def up_left(self):
        self.held.remove("left")

    def up_soft_drop(self):
        self.soft_drop_held = False

    def update(self, dt, board):
        movement_queue = []

        if self.soft_drop_held:
            self.soft_drop_sdf_timer += dt
            for _ in range(board.h):
                if self.soft_drop_sdf_timer >= self.sdf:
                    self.soft_drop_sdf_timer -= self.sdf
                    movement_queue.append((0, 1))
                else:
                    break

        if self.held == []:
            return movement_queue

        if self.held[-1] == "right":
            self.right_hold_ms += dt
            if self.right_hold_ms >= self.das:
                self.right_arr_timer += dt
                for _ in range(board.w):
                    if self.right_arr_timer >= self.arr:
                        self.right_arr_timer -= self.arr
                        movement_queue.append((1, 0))
                    else:
                        break
                    
        if self.held[-1] == "left":
            self.left_hold_ms += dt
            if self.left_hold_ms >= self.das:
                self.left_arr_timer += dt
                for _ in range(board.w):
                    if self.left_arr_timer >= self.arr:
                        self.left_arr_timer -= self.arr
                        movement_queue.append((-1, 0))
                    else:
                        break

        return movement_queue

class Game:
    def __init__(self):
        self.board = Board(10, 40, 20)
        self.rng = RNG(time.time()*1000)
        self.queue = []
        self.next()
        self.handler = Handler(117, 0, 0)
        self.hold_type = None
        self.held = False

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
            y = 0
            if mino_type == "I":
                y = -0.5
            self.draw_mino(screen, pos, 11, y+1+i*gap, mino_type, 0, MINO_COLORS[mino_type])

    def hard_drop(self):
        self.held = False
        for _ in range(self.board.h):
            if self.mino.move(0, 1, self.board) == False:
                self.board.place(self.mino)
                self.next()
                break

    def keydown(self, event):
        if event.key == pygame.K_RIGHT:
            self.handler.down_right()
            self.mino.move(1, 0, self.board)
        if event.key == pygame.K_LEFT:
            self.handler.down_left()
            self.mino.move(-1, 0, self.board)
        if event.key == pygame.K_DOWN:
            self.handler.down_soft_drop()
        if event.key == pygame.K_UP:
            self.mino.rotate(1, self.board)
        if event.key == pygame.K_LCTRL:
            self.mino.rotate(-1, self.board)
        if event.key == pygame.K_a:
            self.mino.rotate(2, self.board)
        if event.key == pygame.K_SPACE:
            self.hard_drop()
        if event.key == pygame.K_LSHIFT:
            self.hold()

    def keyup(self, event):
        if event.key == pygame.K_RIGHT:
            self.handler.up_right()
        if event.key == pygame.K_LEFT:
            self.handler.up_left()
        if event.key == pygame.K_DOWN:
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

    def draw(self, screen):
        pos = (SCREEN_W/2-UNIT*10/2, SCREEN_H/2-UNIT*20/2)
        pos_m = (pos[0], pos[1]-self.board.margin_top*UNIT)
        self.board.draw(screen, pos_m)
        self.draw_shadow(screen, pos_m)
        self.draw_mino(screen, pos_m, self.mino.x, self.mino.y, self.mino.type, self.mino.rotation)
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

game = Game()

while True:
    screen.fill("#333333")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game = Game()
            game.keydown(event)
        if event.type == pygame.KEYUP:
            game.keyup(event)

    game.draw(screen)
    dt = clock.tick(120)
    game.update(dt)

    pygame.display.update()