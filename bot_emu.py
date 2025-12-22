class BotEmu:
    def __init__(self, game):
        self.game = game
        self.events = []

    def update(self, dt, data):
        self.events = data["events"]
        
        game_state = {
            "state": "started",
            "grid": self.game.board.grid,
            "queue": self.game.queue,
            "mino_type": self.game.mino.type,
            "hold_mino_type": self.game.hold_type
        }
        return game_state

    def get_events(self):
        events = self.events
        self.events = []
        return events