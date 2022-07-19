import pygame as pg
import threading
from collections import Counter

import settings as stgs
import functions as fncs
from grid import Grid


class Application:

    def __init__(self):
        pg.init()

        # Get useful paths
        self.paths = fncs.paths()

        # Initialize window
        self.window = pg.display.set_mode(stgs.WIN_DIMENSION)
        self.icon = pg.image.load(self.paths["icon"])
        pg.display.set_caption("Sudoku")
        pg.display.set_icon(self.icon)

        self.clock = pg.time.Clock() # Clock for fps

        self.sprites = pg.sprite.Group() # Sprite container for drawing all tiles
        self.Grid = Grid(stgs.ROWS, stgs.COLUMNS, False) # Instanciate and populate grid
        self.sprites.add(self.Grid.grid) # Add all grid tiles to sprite group

        self.font = pg.font.Font(self.paths["font"], 48)
        self.text = self.font.render("", True, stgs.COLORS["gold"])
        self.textpos = self.text.get_rect(centerx=stgs.WIN_WIDTH/2, centery=(stgs.WIN_HEIGHT - stgs.GRID_H)/2)
        self.window.blit(self.text, self.textpos)

        self.difficulties = {pg.K_e: "easy", pg.K_m: "medium", pg.K_h: "hard"}

    def change_bottom_text(self, text = ""):
        self.window.fill("black", self.textpos)
        self.text = self.font.render(text, True, stgs.COLORS["gold"])
        self.textpos = self.text.get_rect(centerx=stgs.WIN_WIDTH/2, 
                                          centery=stgs.GRID_H + (stgs.WIN_HEIGHT - stgs.GRID_H)/2)
        self.window.blit(self.text, self.textpos)

    def start(self):

        while True: 

            for event in pg.event.get():
                fncs.handle_app_exit(event)
                
                # Handle tile clicked
                if event.type == pg.MOUSEBUTTONDOWN:
                    try:
                        row, column = fncs.mouse_xy_to_grid_index()
                        tile = self.Grid.grid[row, column]
                        if tile.is_editable:
                            value = fncs.wait(tile) # Wait for user input and return key name
                            if value != tile.number: # Check if the input isn't equal to the tile's number 
                                tile.update(value) # Call the Tile class' update method
                    except IndexError:
                        pass
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_s and self.Grid.difficulty != None:
                        t = threading.Thread(target=self.Grid.solve, args=())
                        t.start()
                    if event.key in self.difficulties.keys():
                        self.change_bottom_text()
                        difficulty = self.difficulties[event.key]
                        self.Grid.load_sudoku(difficulty)

                    if event.key == pg.K_r:
                        self.Grid.reset()
                    if event.key == pg.K_c: 
                        if self.Grid.difficulty != None:
                            if self.Grid.check_solution():
                                text = "Solved"
                            else:
                                text = "Not solved"
                            self.change_bottom_text(text)
                        else:
                            print("Checking rows...")
                            for i in range(stgs.ROWS):
                                print(f"\tRow {i}: ", Counter(fncs.grid_values(self.Grid.grid)[i, :]))
                            print("Checking columns...")
                            for i in range(stgs.COLUMNS):
                                print(f"\tColumn {i}: ", Counter(fncs.grid_values(self.Grid.grid)[:, i]))


            self.sprites.draw(self.window) # Draw all sprites in group
            pg.display.flip() # Update display

            self.clock.tick(60) 
            

if __name__ == "__main__":
    app = Application()
    app.start()

# Change color of hovered tile (WIP): 
# Need to find a way to detect when the mouse has exited the tile to draw again it's white border

# if event.type == pg.MOUSEMOTION:
#     row, column = fncs.mouse_xy_to_grid_index()
#     try:
#         tile = self.Grid.grid[row, column]
#     except IndexError:
#         continue
#     # Only runs if no error is raised
#     if tile.editable:
#         tile.update(tile.number, (0, 0, 0))
