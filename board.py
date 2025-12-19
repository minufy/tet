import pygame
from minos import *
from utils import *

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
        count = 0
        for y in range(self.h):
            for x in range(self.w):
                if self.grid[y][x] == " ":
                    break
            else:
                count += 1
                self.grid.pop(y)
                self.grid.insert(0, [" "]*self.w)
        return count

    def place(self, mino):
        for y, row in enumerate(MINO_SHAPES[mino.type][str(mino.rotation)]):
            for x, dot in enumerate(row):
                if dot:
                    self.grid[mino.y+y][mino.x+x] = mino.type
        self.line_clear()
