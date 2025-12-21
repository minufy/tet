import pygame
from stuff.minos import *
from stuff.utils import *

class Board:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.grid = [[" "]*w for _ in range(h)]

    def draw(self, screen, pos):
        for y in range(self.h):
            for x in range(self.w):
                rect = (x*UNIT+pos[0], y*UNIT+pos[1], UNIT, UNIT)
                if self.grid[y][x] == " ":
                    if y >= self.h//2:
                        pygame.draw.rect(screen, MINO_COLORS["X"], rect, 1)
                else:
                    pygame.draw.rect(screen, MINO_COLORS[self.grid[y][x]], rect)

    def line_clear(self):
        count = 0
        for y in range(self.h-1, -1, -1):
            for x in range(self.w):
                if self.grid[y][x] == " ":
                    break
            else:
                count += 1
                self.grid.pop(y)
        for _ in range(count):
            self.grid.insert(0, [" "]*self.w)
        return count

    def place(self, mino):
        for y, row in enumerate(MINO_SHAPES[mino.type][str(mino.rotation)]):
            for x, dot in enumerate(row):
                if dot:
                    self.grid[mino.y+y][mino.x+x] = mino.type

    def add_garbage(self, amount, pos):
        garbage_line = ["X"]*self.w
        garbage_line[pos] = " "
        for _ in range(amount):
            self.grid.pop(0)
            self.grid.append(garbage_line.copy())

    def __repr__(self):
        s = "-"*self.w+"\n"
        for y in range(20, self.h):
            s += "".join(self.grid[y])+"\n"
        return s