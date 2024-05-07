import random

from src.constants.shapes_format import shapes, shape_colors

#* PIECE CREATION
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

#* SHAPE FORMAT
def convert_shape_format(shape):
    positions = []
    shape_format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

#* SHAPES
def get_shape():
    return Piece(5, 0, random.choice(shapes))
