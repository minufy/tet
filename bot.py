import pygame
from minos import *
from utils import *

LINE_TABLE = {
    0: 0,
    1: 0,
    2: 1,
    3: 2,
    4: 10
}

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
    def __init__(self, mino, score, board, hold):
        self.mino = mino
        self.score = score
        self.board = board
        self.hold = hold

class Input:
    def __init__(self, key, time):
        self.hold_time = time
        self.hold_timer = 0
        self.down_event = keydown(key)
        self.up_event = keyup(key)
    
    def update(self, dt):
        self.hold_timer += dt
 
class Bot:
    def __init__(self, game, input_time):
        self.game = game
        self.board = TestBoard(self.game.board.grid)
        self.queue = [self.game.mino.type]+self.game.queue.copy()
        self.last_queue = []
        self.inputs = []
        self.weights = {
            "line": 0,
            "change_rate": 0,
            "holes": 0,
            "well_depth": 0,
        }
        self.input_time = input_time
        self.input_timer = 0
        self.hold_type = None
        self.held = False
        self.depth = DEPTH
        self.best_count = BEST_COUNT

    def restart(self):
        self.board = TestBoard(self.game.board.grid)
        self.queue = [self.game.mino.type]+self.game.queue.copy()
        self.last_queue = []
        self.inputs = []
        self.input_timer = 0
        self.hold_type = None
        self.held = False
        self.depth = DEPTH
        self.best_count = BEST_COUNT

    def set_weights(self, weights):
        self.weights = weights

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

    def find_moves(self, mino_0, mino_1, grid):
        mino_types = [mino_0]
        if mino_1:
            mino_types.append(mino_1)
        moves = []
        for mino_type in mino_types:
            for r in [0, 1, 2, 3]:
                for x in range(-2, self.board.w-2):
                    mino = Mino(mino_type, x, self.game.board.margin_top-4, r)
                    board = TestBoard(grid)

                    if mino.check_collison(board):
                        continue
                    
                    self.hard_drop(mino, board)
                    score = self.get_score(board)
                    self.line_clear(board)
                    
                    hold = None
                    if mino_type != mino_0:
                        hold = mino_0
                    
                    moves.append(Move(mino, score, board, hold))
        return moves
 
    def exectue_move(self, move):
        if move.hold:
            self.input(pygame.K_LSHIFT, 1)
            self.hold_type = move.hold
            
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

    def get_heights(self, board):
        heights = [0]*board.w
        for x in range(board.w):
            heights[x] = board.h
            for y in range(board.h):
                if board.grid[y][x] == " ":
                    heights[x] -= 1
                else:
                    break
        return heights
                
    def get_well_depth(self, board):
        heights = self.get_heights(board)
        well_depth = 0
        for x in range(board.w):
            left = -1 if x == 0 else heights[x-1]
            right = -1 if x == board.w-1 else heights[x+1]
            if left == -1: left = right
            if right == -1: right = left
            h = heights[x]
            depth = left-h+right-h
            if depth < 8:
                continue
            well_depth = max(well_depth, depth)
        return well_depth

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
        heights = self.get_heights(board)
        diffs = []
        for i in range(board.w-1):
            diffs.append(abs(heights[i]-heights[i+1]))
        change_rate = sum(diffs)/board.w
        return change_rate

    def get_score(self, board):
        lines = LINE_TABLE[self.get_lines(board)]*self.weights["line"]
        change_rate = self.get_change_rate(board)*self.weights["change_rate"]
        holes = self.get_holes(board)*self.weights["holes"]
        well_depth = self.get_well_depth(board)*self.weights["well_depth"]
        return lines+change_rate+holes+well_depth

    def research(self, depth, move):
        mino_1 = None
        if depth >= len(self.queue):
            return 0
        if depth+1 < len(self.queue):
            mino_1 = self.queue[depth+1]
        return self.search_moves(self.queue[depth], move.hold or mino_1, move.board, depth).score 

    def search_moves(self, mino_0, mino_1, board, depth):
        moves = self.find_moves(mino_0, mino_1, board.grid)
        moves.sort(key=lambda x: x.score)
        if depth >= self.depth:
            if moves:
                return moves[-1]
            else:
                return Move(Mino("O", 0, 0, 0), 0, [], False)
        new_moves = sorted(moves[-self.best_count:], key=lambda x: self.research(depth+1, x))
        if new_moves:
            return new_moves[-1]
        return Move(Mino("O", 0, 0, 0), 0, [], False)
    
    def update(self, dt):
        if len(self.game.queue) == 11:
            bag = self.game.queue[-7:]
            if self.last_queue != bag:
                self.last_queue = bag
                self.queue += bag

        if len(self.queue) >= 2:
            move = self.search_moves(self.queue[0], self.hold_type or self.queue[1], self.board, 0)
            self.exectue_move(move)
            self.place(move.mino, self.board)
            self.line_clear(self.board)
            if move.hold and not self.held:
                self.held = True
                self.queue.pop(0)
            self.queue.pop(0)

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

    def get_events(self):
        events = []

        if self.input_timer > self.input_time:
            self.input_timer = 0
            if self.inputs:
                current_input = self.inputs[0]
                if current_input.down_event:
                    events.append(current_input.down_event)
                    current_input.down_event = None
                
                if current_input.hold_timer > current_input.hold_time:
                    events.append(current_input.up_event)
                    self.inputs.pop(0)

        return events
    
    def draw(self, screen):
        for i, weight in enumerate(self.weights):
            text = render_text(f"{weight}: {self.weights[weight]}", "#ffffff")
            screen.blit(text, (10, 10+font.get_height()*i))