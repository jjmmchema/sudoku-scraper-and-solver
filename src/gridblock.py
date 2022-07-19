import numpy as np

import functions as fncs
from tile import Tile

class GridBlock():
    """
        Sudoku grid 3x3 section
    """

    def __init__(self, grid_id, start_row, end_row, start_col, end_col):
        self.grid_id = grid_id
        self.start_row = start_row
        self.end_row = end_row
        self.start_col = start_col
        self.end_col = end_col
        self.block = np.zeros((3, 3), dtype=object)

    def add(self, tile : Tile):

        row = tile.row_idx % 3
        col = tile.column_idx % 3

        self.block[row, col] = tile

    def block_values(self) -> np.ndarray:
        extract_values = np.vectorize(lambda t: int(t.number))
        return np.ravel(extract_values(self.block))

    def __str__(self) -> str:
        print("Gridblock #", self.grid_id, ", ", 
                (self.start_row, self.start_col), " to ", (self.end_row, self.end_col), ":")
        for row in self.block:
            for column in row:
                print(column)
        return "Gridblock end"