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