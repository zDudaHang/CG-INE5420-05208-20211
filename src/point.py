class Point2D:
    def __init__(self, x: float, y: float) -> None:
        self.coordinates = [[x, y, 1]]

    def get_x(self):
        return self.coordinates[0][0]

    def get_y(self):
        return self.coordinates[0][1]

    def __str__(self):
        return f'({self.get_x()},{self.get_y()})'