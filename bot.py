import pygame

def keydown(key):
    return pygame.event.Event(pygame.KEYDOWN, {
        "key": key
    })

def keyup(key):
    return pygame.event.Event(pygame.KEYUP, {
        "key": key
    })

class Bot:
    def __init__(self, game, pps):
        self.game = game
        self.pps = pps
        self.place_time = 0
        self.place_timer = 0

        self.holding = False
        self.hold_timer = 0
        self.hold_time = 0
        self.down_event = None
        self.up_event = None
        
    def evaluate(self):
        return

    def update(self, dt):
        self.place_timer += dt
        if self.place_timer > self.place_time:
            self.place_time += 1000/self.pps
        
        if self.holding:
            self.hold_timer += dt

    def hold(self, key, time):
        self.holding = True
        self.hold_time = time
        self.hold_timer = 0
        self.down_event = keydown(key)
        self.up_event = keyup(key)

    def get_events(self, dt):
        events = []
        if self.down_event:
            events.append(self.down_event)
            self.down_event = None
        
        if self.holding:
            if self.hold_timer > self.hold_time:
                events.append(self.up_event)
                self.holding = False
                self.up_event = None

        return events