import time
import numpy as np
import pygame as pg
import random

from gridblock import GridBlock

import settings as stgs
import functions as fncs
from tile import Tile

# DS#2
# Make that a tile that's in the same row & column, row & block,
# column & block or row & column & block appears in possible values?

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

        if read_grid: self.read_values("sudoku.txt")

        # Note: the x pos of the tile will be the column number times the width of the tile
        # and the y pos of the tile will be the row number times the height of the tile.
        # This is because selecting different columns of the same row will require a horizontal displacement
        # while selecting different rows of the same column will require a vertical displacement.
        # The "size step" of that displacement along each axis will be the respective dimension of the tile.

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
        
    def update_tile(self, tile : Tile, guess, values : np.array, text_color = "white"):
        values[tile.row_idx, tile.column_idx] = guess
        tile.update(f"{guess}", text_color)
        # Need to refactor but should fix problem 1 at DS#1
        # self.grid_blocks[tile.block].block[tile.row_idx % 3, tile.column_idx % 3] = tile

    def find_and_update_tile_value(self, tile : Tile, vals):
        i = tile.row_idx
        j = tile.column_idx
        tiles_block = self.grid_blocks[tile.block]

        row_values = vals[i, :]
        column_values = vals[:, j]
        block_values = tiles_block.block_values()
        available_values = fncs.available_values_for_tile(row_values, column_values, block_values)

        if available_values.size > 0:
            guess = random.choice(available_values)
            self.update_tile(tile, guess, vals)
            time.sleep(0.1)
        else:
            not_empty_row_values = fncs.exclude_zero(row_values) # row_values w/o 0 
            not_empty_col_values = fncs.exclude_zero(column_values) # column_values w/o 0
            not_empty_block_values = fncs.exclude_zero(block_values) # block_values w/o 0

            # Get ONLY the values that aren't repeated in the three arrays
            # diff1 = np.setdiff1d(not_empty_row_values, not_empty_col_values)
            # possible_values = np.setdiff1d(diff1, not_empty_block_values)
            possible_values = fncs.symmetric_3arr_diff(not_empty_row_values, 
                                                       not_empty_col_values, 
                                                       not_empty_block_values)

            editable_row_values = fncs.editable_values(self.grid[i, :])
            editable_col_values = fncs.editable_values(self.grid[:, j])
            editable_block_values = fncs.editable_values(self.grid[tiles_block.start_row : tiles_block.end_row+1, 
                                                                   tiles_block.start_col : tiles_block.end_col+1])
            editable_values = np.unique(np.concatenate((editable_row_values,
                                                        editable_col_values,
                                                        editable_block_values)))

            while True:
                try:
                    choice = random.choice(possible_values)
                except:
                    choice = random.randint(1, 9)
                    # choice = random.choice(editable_values)

                # Take the vals array and slice the entire i-th row and j-th column separately.
                # Apply a boolean operator to get only the values that match choice.
                # Then take the same row and column from self.grid (which contains Tile objects)
                # and use the mask to index the Tile(s).


                row_mask = vals[i, :] == choice
                col_mask = vals[:, j] == choice
                block_mask = vals[tiles_block.start_row : tiles_block.end_row+1, 
                                    tiles_block.start_col : tiles_block.end_col+1] == choice


                same_row_tile = self.grid[i, :][row_mask]
                same_col_tile = self.grid[:, j][col_mask]
                same_block_tile = self.grid[tiles_block.start_row : tiles_block.end_row+1, 
                                            tiles_block.start_col : tiles_block.end_col+1][block_mask]

                editable_same_row_tile = np.array([t for t in same_row_tile if t.is_editable])
                editable_same_col_tile = np.array([t for t in same_col_tile if t.is_editable])
                editable_same_block_tile = np.array([t for t in same_block_tile if t.is_editable])

                # Exceeds maximum recursion

                tiles_to_update = np.concatenate((editable_same_row_tile, 
                                                    editable_same_col_tile, 
                                                    editable_same_block_tile))
                                                    
                if tiles_to_update.size > 0:
                    self.update_tile(tile, choice, vals, "red")
                    for t in tiles_to_update:
                        self.find_and_update_tile_value(t, vals)
                    break
                else:
                    if possible_values.size > 0:
                        idx_to_remove = np.where(possible_values == choice)
                        possible_values = np.delete(possible_values, idx_to_remove)

    def solve(self):
        """
            Solves the sudoku grid.
        """
        vals = fncs.grid_values(self.grid)
        for row in self.grid:
            for tile in row:
                if tile.is_editable and tile.number == "0":
                    self.find_and_update_tile_value(tile, vals)
                   
    def __str__(self):
        for row in self.grid:
            for column in row:
                print(column)
        return "Grid end"
