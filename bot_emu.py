import zmq

class BotEmu:
    def __init__(self, game, socket):
        self.game = game
        self.socket = socket
        self.events = []

    def update(self, dt):
        try:
            self.events = self.socket.recv_json(flags=zmq.NOBLOCK)["events"]
            game_state = {
                "grid": self.game.board.grid,
                "queue": self.game.queue,
                "mino_type": self.game.mino.type
            }
            self.socket.send_json(game_state)
        except zmq.Again:
            pass

    def get_events(self):
        events = self.events
        self.events = []
        return events