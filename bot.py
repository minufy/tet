import pygame
from minos import *

def keydown(key):
    return pygame.event.Event(pygame.KEYDOWN, {
        "key": key
    })

def keyup(key):
    return pygame.event.Event(pygame.KEYUP, {
        "key": key
    })

class TestBoard:
    def __init__(self, grid):
        self.grid = [row.copy() for row in grid]
        self.w = len(self.grid[0])
        self.h = len(self.grid)

    def __repr__(self):
        s = "-"*self.w+"\n"
        for y in range(20, self.h):
            s += "".join(self.grid[y])+"\n"
        return s

class Move:
    def __init__(self, mino, score):
        self.mino = mino
        self.score = score

class Input:
    def __init__(self, key, time):
        self.hold_time = time
        self.hold_timer = 0
        self.down_event = keydown(key)
        self.up_event = keyup(key)
    
    def update(self, dt):
        self.hold_timer += dt
 
class Bot:
    def __init__(self, game, input_time=100):
        self.game = game
        self.input_timer = 0
        self.input_time = input_time
        self.board = TestBoard(self.game.board.grid)
        self.queue = [self.game.mino.type]+self.game.queue.copy()
        self.last_queue = []
        self.inputs = []
        
    def place(self, mino, board):
        for y, row in enumerate(MINO_SHAPES[mino.type][str(mino.rotation)]):
            for x, dot in enumerate(row):
                if dot:
                    board.grid[mino.y+y][mino.x+x] = mino.type

    def hard_drop(self, mino, board):
        for _ in range(board.h):
            if mino.move(0, 1, board) == False:
                self.place(mino, board)
                break

    def find_moves(self, mino_type):
        moves = []
        for r in [0, 1, 2, 3]:
            for x in range(-2, self.board.w-2):
                mino = Mino(mino_type, x, self.game.board.margin_top-4)
                mino.rotation = r
                board = TestBoard(self.board.grid)

                if mino.check_collison(board):
                    continue
                self.hard_drop(mino, board)
                score = self.get_score(board)

                moves.append(Move(mino, score))
        return moves
 
    def exectue_move(self, move):
        if move.mino.rotation == 1:
            self.input(pygame.K_UP, 1)
        elif move.mino.rotation == 3:
            self.input(pygame.K_LCTRL, 1)
        elif move.mino.rotation == 2:
            self.input(pygame.K_a, 1)

        x = 3
        for _ in range(self.board.w):
            if move.mino.x == x:
                break
            elif move.mino.x > x:
                x += 1
                self.input(pygame.K_RIGHT, 1)
            else:
                x -= 1
                self.input(pygame.K_LEFT, 1)
             
        self.input(pygame.K_SPACE, 1)

    def get_height(self, board):
        height = 0
        for x in range(board.w):
            height -= board.h
            for y in range(board.h):
                if board.grid[y][x] == " ":
                    height += 1
                else:
                    break
        return height

    def get_lines(self, board):
        count = 0
        for y in range(board.h):
            for x in range(board.w):
                if board.grid[y][x] == " ":
                    break
            else:
                count += 1
        return count
    
    def get_holes(self, board):
        holes = 0
        for x in range(board.w):
            block = False
            for y in range(board.h):
                if board.grid[y][x] != " ":
                    block = True
                elif block and board.grid[y][x] == " ":
                    holes += 1
                    # break
        return holes

    def get_change_rate(self, board):
        heights = [0]*board.w
        for x in range(board.w):
            for y in range(board.h):
                if board.grid[y][x] == " ":
                    heights[x] += 1
                else:
                    break
        diffs = []
        for i in range(board.w-1):
            diffs.append(abs(heights[i]-heights[i+1]))
        change_rate = sum(diffs)/board.w
        return change_rate

    def get_score(self, board):
        lines = self.get_lines(board)
        change_rate = -self.get_change_rate(board)
        holes = -self.get_holes(board)
        # height = self.get_height(board)*0.02
        print(lines, change_rate, holes)
        # return lines+change_rate+holes+height
        return lines+change_rate+holes

    def update(self, dt):
        if len(self.game.queue) == 11:
            bag = self.game.queue[-7:]
            if self.last_queue != bag:
                self.last_queue = bag
                self.queue += bag

        if self.queue:
            # print(self.queue, self.game.queue)
            mino_type = self.queue.pop(0)
            # print(self.board)
            moves = self.find_moves(mino_type)
            moves.sort(key=lambda x: x.score)
            if moves:
                move = moves[-1]
                self.exectue_move(move)
                self.place(move.mino, self.board)
                self.line_clear(self.board)
                # print(move.mino.type)

        self.input_timer += dt

        if self.inputs:
            self.inputs[0].update(dt)

    def line_clear(self, board):
        for y in range(board.h):
            for x in range(board.w):
                if board.grid[y][x] == " ":
                    break
            else:
                board.grid.pop(y)
                board.grid.insert(0, [" "]*board.w)

    def input(self, key, time):
        self.inputs.append(Input(key, time))

    def get_events(self, dt):
        events = []

        # if self.input_timer > self.input_time:
        #     self.input_timer = 0
        if self.inputs:
            current_input = self.inputs[0]
            if current_input.down_event:
                events.append(current_input.down_event)
                current_input.down_event = None
            
            if current_input.hold_timer > current_input.hold_time:
                events.append(current_input.up_event)
                self.inputs.pop(0)

        return events