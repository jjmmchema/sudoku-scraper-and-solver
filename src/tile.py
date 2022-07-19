import math
import pygame as pg
from sqlalchemy import column

import settings as stgs
import functions as fncs

class Tile(pg.sprite.Sprite):
    """
        Single tile of a sudoku board
    """
    
    def __init__(self, x : int, y : int, width : int, height : int, number = "0"):
        """
            Create a tile with a white border and a number at it's center
        """
        super().__init__()

        self.width = width
        self.height = height
        self.row_idx = int(y/height)
        self.column_idx = int(x/width)
        self.is_editable = True
        self.block = (self.row_idx//3)*3 + (self.column_idx//3) # int(self.row_idx/3)*3 + int(self.column_idx/3)

        self.number = str(number)
        self.font_path = fncs.paths()["font"]
        self.font = pg.font.Font(self.font_path, 32) # Create a font object
        if self.number == "0":
            self.text = self.font.render("", True, "white") # Render some text
        else:
            self.text = self.font.render(number, True, "white") # Render some text
        self.textpos = self.text.get_rect(centerx=width/2, centery=height/2) # Specify pos of the text with a rect

        self.image = pg.Surface([width, height]) # Create the tile surface to draw on
        # Get the rect of the surface and set it's position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Draw the white border around the tile
        pg.draw.rect(self.image, "white", [0, 0, width, height], 1)

        # Draw the text on the tile
        self.image.blit(self.text, self.textpos)

    # Can take parameters
    def update(self, number : str, text_color = "white", border_color = "white"):
        """
            Change the number that the tile displays
            and optionally change it's border color.
        """

        self.image.fill("black") # Erase the number already in the tile and it's border
        self.number = number # Update the number that will be shown
        pg.draw.rect(self.image, border_color, [0, 0, self.width, self.height], 1) # Create the border again
        self.text = self.font.render(self.number if self.number != "0" else "", True, text_color) # Render the number
        self.textpos = self.text.get_rect(centerx=self.width/2, centery=self.height/2) # Update the position
        self.image.blit(self.text, self.textpos) # Draw the text

    def reset(self):
        self.update("0")

    def change_fill(self):
        self.image.fill(stgs.COLORS["silver"])

    def __str__(self):
        return f"{self.row_idx}, {self.column_idx} : {self.number} in block {self.block}"
