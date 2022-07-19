import pygame as pg
import numpy as np
import sys
from pathlib import Path

from tile import Tile
import settings as stgs

def handle_app_exit(event : pg.event.Event):
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            sys.exit()
    if event.type == pg.QUIT:
        sys.exit()

def paths():
    p = Path(__file__)
    src_dir = p.parent
    icon = src_dir / "icons/sudoku.png"
    font = src_dir.parent / "timeburnerbold.ttf"
    return {"src" : src_dir, "icon" : icon, "font" : font}

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

