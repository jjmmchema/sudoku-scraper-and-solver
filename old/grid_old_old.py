import time
import numpy as np
import pygame as pg
import random

from sqlalchemy import null

import settings as stgs
import functions as fncs
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

        # Tile list
        self.grid = np.zeros((rows, columns), dtype=object)


        # Create a Tile(x, y, width, height, number) and add it to the index [x][y] of self.grid.
        for i in range(rows):
            for j in range(columns):
                self.grid[i][j] = Tile(j*stgs.TILE_W, i*stgs.TILE_H, stgs.TILE_W, stgs.TILE_H) #f"{randint(1, 9)}"

        if read_grid: self.read_values("sudoku.txt")

        # Note: the x pos of the tile will be the column number times the width of the tile
        # and the y pos of the tile will be the row number times the height of the tile.
        # This is because selecting different columns of the same row will require a horizontal displacement
        # while selecting different rows of the same column will require a vertical displacement.
        # The "size step" of that displacement along each axis will be the respective dimension of the tile.

    def grid_values(self) -> np.array:
        """
            Get the value of each tile in self.grid and store it in an array where
            the i,j-th element corresponds to the number of the i,j-th tile in self.grid.
        """
        vals = []
        for list in self.grid:
            vals.append([tile.number for tile in list])
        return np.array(vals, dtype=int)

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

    def find_and_update_tile_value(self, tile, vals):
        i = tile.row_idx
        j = tile.column_idx

        row_values = vals[i, :]
        column_values = vals[:, j]
        available_values = fncs.available_values_for_tile(row_values, column_values)

        if available_values.size > 0:
            guess = random.choice(available_values)
            self.update_tile(tile, guess, vals)
            time.sleep(0.1)
        else:
            not_empty_row_values = fncs.exclude_zero(row_values) # row_values w/o 0
            not_empty_col_values = fncs.exclude_zero(column_values) # column_values w/o 0
            possible_values = np.setdiff1d(not_empty_row_values, not_empty_col_values) # values not in 
                                                                                        # both arrays

            while True:
                try:
                    choice = random.choice(possible_values)
                except:
                    choice = random.randint(1, 9)

                # Take the vals array and slice the entire i-th row and j-th column separately.
                # Apply a boolean operator to get only the values that match choice.
                # Then take the same row and column from self.grid (which contains Tile objects)
                # and use the mask to index the Tile(s).
                row_mask = vals[i, :] == choice
                col_mask = vals[:, j] == choice
                same_row_tile = self.grid[i, :][row_mask]
                same_col_tile = self.grid[:, j][col_mask]

                editable_same_row_tile = np.array([t for t in same_row_tile if t.is_editable])
                editable_same_col_tile = np.array([t for t in same_col_tile if t.is_editable])

                # Error de lógica aquí?


                # Exceeds maximum recursion

                tiles_to_update = np.concatenate((editable_same_row_tile, editable_same_col_tile))

                if tiles_to_update.size > 0:
                    self.update_tile(tile, choice, vals, "red")
                    for t in tiles_to_update:
                        self.find_and_update_tile_value(t, vals)
                    break
                else:
                    if possible_values.size > 0:
                        idx_to_remove = np.where(possible_values == choice)
                        possible_values = np.delete(possible_values, idx_to_remove)


                # Fills the sudoku grid but there most of the time it's incorrect
                # if editable_same_row_tile.size > 0:
                #     t = editable_same_row_tile[0]
                #     self.update_tile(tile, t.number, vals, "red")
                #     self.find_and_update_tile_value(t, vals)
                #     break

                # if editable_same_col_tile.size > 0:
                #     t = editable_same_col_tile[0]
                #     self.update_tile(tile, t.number, vals, "red")
                #     self.find_and_update_tile_value(t, vals)
                #     break

                # Only runs if the tile t isn't editable
                # if possible_values.size > 0:
                #     idx_to_remove = np.where(possible_values == choice)
                #     possible_values = np.delete(possible_values, idx_to_remove)


                
    def solve(self):
        """
            Solves the sudoku grid.
        """
        vals = self.grid_values()
        for row in self.grid:
            for tile in row:
                if tile.is_editable and tile.number == "0":
                    self.find_and_update_tile_value(tile, vals)
                   
    def __str__(self):
        for row in self.grid:
            for column in row:
                print(column)
        return "Grid end"
