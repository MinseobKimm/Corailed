class Agent:
    def __init__(self):
        pass

    def input_key(self, key, delta_time):
        raise NotImplementedError()

    def input_move(self, key):
        raise NotImplementedError()

    def get_path(self, start, obj, game, last):
        raise NotImplementedError()

    def move(self, obj, game, draw, player_pos, last):
        raise NotImplementedError()

    def do_break(self, obj, game, player_pos):
        raise NotImplementedError()

    def rnd(self, r):
        raise NotImplementedError()