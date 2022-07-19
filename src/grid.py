import time
import numpy as np
import pygame as pg

from gridblock import GridBlock
import settings as stgs
import functions as fncs
import scrape
from tile import Tile

class Grid():
    """
        Matrix containing Tile objects for sudoku game
    """

    def __init__(self, rows : int, columns : int, read_grid = False):
        """
            Create a grid matrix with shape (rows*columns) which will contain Tile objects.\n
            If read_grid -> app will load a sudoku grid from a .txt file 
        """
        pg.init()

        self.difficulty = None
        self.rows = rows
        self.columns = columns
        # Tile list
        self.grid = np.zeros((rows, columns), dtype=object)
        # List of GridBlock objects (9 arrays that divide the grid in 9 3x3 sections) 
        self.grid_blocks = np.zeros(9, dtype=object)

        # Populate the self.grid_blocks array
        grid_id = 0
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                self.grid_blocks[grid_id] =  GridBlock(grid_id, i, i+2, j, j+2)
                grid_id += 1

        # Create a Tile(x, y, width, height, number) and add it to the index [x][y] of self.grid.
        # And to it's respective block
        for i in range(rows):
            for j in range(columns):
                self.grid[i, j] = Tile(j*stgs.TILE_W, i*stgs.TILE_H, stgs.TILE_W, stgs.TILE_H)
                block_id = (i//3)*3 + (j//3)
                self.grid_blocks[block_id].add(self.grid[i, j])

        if read_grid: 
            self.read_values("sudoku.txt")
        else:
            self.sudokus = scrape.scrape_all()

        # Note: the x pos of the tile will be the column number times the width of the tile
        # and the y pos of the tile will be the row number times the height of the tile.
        # This is because selecting different columns of the same row will require a horizontal displacement
        # while selecting different rows of the same column will require a vertical displacement.
        # The "size step" of that displacement along each axis will be the respective dimension of the tile.

    def reset(self):
        for row in self.grid:
            for tile in row:
                tile.reset()

    def load_sudoku(self, difficulty):
        self.reset()
        self.difficulty = difficulty
        puzzle = self.sudokus[difficulty]["puzzle"]
        for row in self.grid:
            for tile in row:
                i,  j = tile.row_idx, tile.column_idx
                value = puzzle[i, j]
                if value != 0:
                    tile.is_editable = False
                    tile.update(str(value), stgs.COLORS["gold"])

    def read_values(self, file):
        """
            Read a .txt file with values to load into the sudoku grid.
            Each value can be a number in the interval [1, 9] or a "-"
            to indicate a blank tile in the grid.
        """
        with open(f"src/load/{file}", "r") as f:
            i = 0                                           # Variable to loop through each row of self.grid.
            for line in f.readlines():                      # Loop through each line in the file.
                j = 0                                       # Variable to map each line value to the respective tile.
                t = line.split(",")[:-1]                    # Exclude the last character because it is \n.
                for tile in self.grid[i, :]:                # Loop through each tile in the i-th row.
                    val = t[j]
                    if (val != "-"):                        # If val == "-" the tile will be blank and that's the 
                                                            # default value so no need to update it.
                        tile.is_editable = False            # If the tile isn't a blank space, make it uneditable.
                        tile.update(val, stgs.COLORS["gold"])
                    j += 1
                i += 1
        
    def update_tile(self, tile : Tile, guess = "0", text_color = "white"):
        tile.update(f"{guess}", text_color)

    def findNextEmptyTile(self, i = 0, j = 0):
        for row in self.grid[i:, j:]:
            for tile in row:
                if tile.number == "0":
                    return tile
        # If this is reached sudoku should be solved and therefore there aren't any empty tiles left
        return None, None

    def isValid(self, guess, i, j, block_id):
        values = fncs.grid_values(self.grid)
        if guess not in values[i, :]:
            if guess not in values[:, j]:
                if guess not in self.grid_blocks[block_id].block_values():
                    return True
        return False

    def solve(self):
        """
            Solves the sudoku grid.
        """
        try:
            tile = self.findNextEmptyTile()
            i, j = tile.row_idx, tile.column_idx
            block_id = tile.block
        except AttributeError:
            # This runs if self.findNextEmptyTile() returns (None, None) as this is assigned to tile and therefore
            # doesn't have row_idx or column_idx attributes. When this happens the last cell has been solved
            return True

        # if i == None:
        #     print("y")
        #     return True
        
        for guess in range(1, 10):
            if self.isValid(guess, i, j, block_id):
                self.update_tile(tile, guess)
                # time.sleep(0.1)
                if self.solve():
                    return True
                self.update_tile(tile, "0")

    def check_solution(self):
        if self.difficulty:
            values = fncs.grid_values(self.grid)
            values == self.sudokus[self.difficulty]["solution"]
            return np.all(values)
            
    def __str__(self):
        for row in self.grid:
            for column in row:
                print(column)
        return "Grid end"
