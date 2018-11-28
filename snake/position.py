class Position:
    x = 0
    y = 1
    direction = None

    def __init__(self, x, y, direction = None):
        self.x = x
        self.y = y
        self.direction = direction

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"