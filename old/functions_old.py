import pygame as pg
import numpy as np
import sys

from tile import Tile
import settings as stgs

def handle_app_exit(event : pg.event.Event):
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            sys.exit()
    if event.type == pg.QUIT:
        sys.exit()

def wait(tile : Tile) -> str:
    """
        Takes a Tile object and waits for the user to input a key.\n
        If the key name is ESCAPE or BACKSPACE, return a blank string.\n
        If the key can be casted to an int and isn't equal to 0, return it's string name.\n
        If it can't be casted or if it's 0, return the number the Tile object already had.
    """

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()

            # Handle keydown event
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_BACKSPACE:
                    return ""
                try:
                    key = int(pg.key.name(event.key)) # Cast to int to check if it raises a ValueError.
                                                      # If it does, then the key name isn't a integer.
                    if (key == 0):
                        raise ValueError
                    return str(key)                   
                except ValueError:
                    return tile.number

def mouse_xy_to_grid_index() -> tuple:
    """
        Gets the mouse x,y position and converts it
        to an index usable on the grid matrix to access
        the tile at that position.
    """
    x, y = pg.mouse.get_pos() # Returns tuple of coordinates (x, y)
    column = int(x/stgs.TILE_W)
    row = int(y/stgs.TILE_H)
    return row, column
    # Note: 
    # x/stgs.TILE_W corresponds to the column containing the selected tile
    # y/stgs.TILE_H corresponds to the row containing the selected tile
    # int() rounds the quotient to the lowest integer
    # Therefore, self.Grid.grid[row][column] returns the selected tile from the grid list

def grid_values(tiles_array) -> np.ndarray:
    """
        Get the value of each tile in tiles_array and store it in an array where
        the i,j-th element corresponds to the number of the i,j-th tiles_array.
    """
    vals = []
    for list in tiles_array:
        vals.append([tile.number for tile in list])
    return np.array(vals, dtype=int)

def exclude_zero(arr : np.ndarray) -> np.ndarray:
    return arr[arr != 0]

def available_values_for(arr : np.ndarray) -> np.ndarray:
    """
        Takes and array, sorts it, excludes the 0s
        and returns it's difference with the set
        of possible values - i.e. the values
        that can be used - for a row or column of 
        the sudoku. 
    """
    possible_values = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]) # Posible values in a 9x9 sudoku
    arr = np.sort(exclude_zero(arr)) # Sort arr and exclude the empty tiles (0)
    return np.setdiff1d(possible_values, arr) # Return the values that are in possible_values but not in arr

def available_values_for_tile(row_vals : np.ndarray, col_vals : np.ndarray, block_vals : np.ndarray) -> np.ndarray:
    """
        row_vals -> Array of the values of every tile in a row
        col_vals -> Array of the values of every tile in a column
        block_vals -> Array of the values of every tile in a block

        Takes three arrays and returns a new array consisting of the
        intersection of the available values for each array.

    """
    available_row_vals = available_values_for(row_vals)
    available_column_vals = available_values_for(col_vals)
    available_block_vals = available_values_for(block_vals)

    intersect1 = np.intersect1d(available_row_vals, available_column_vals) 
    return np.intersect1d(intersect1, available_block_vals) # Return ONLY the values that are in both arrays

def symmetric_3arr_diff(a, b, c):
    """
        Returns an array with all elements that are exactly in one of the input arrays.
    """
    a = set(a)
    b = set(b)
    c = set(c)
    diff = (a ^ b ^ c) - (a & b & c)
    return np.array(list(diff))

def editable_values(tiles_arr : np.ndarray):
    return np.array([int(tile.number) for tile in tiles_arr.ravel() if (tile.is_editable and tile.number != "0")],
                    dtype=int)
