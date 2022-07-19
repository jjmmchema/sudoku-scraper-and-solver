import requests
import re
import numpy as np


def scrape_all() -> dict:

    """
        Scrapes the daily easy, medium and hard sudoku from\n
        https://www.nytimes.com/puzzles/sudoku (with solutions)
    """

    url = "https://www.nytimes.com/puzzles/sudoku"
    r = requests.get(url)

    difficulties = ["easy", "medium", "hard"]
    sudokus = {}

    # (.*?<) -> .* matches the next character whatever it 0 or unlimited times and it's lazy thanks to the ?, so it
    # stops after the first < that's found 
    sudoku_data = re.findall(r"window.gameData = (.*?<)", r.text)[0]

    for difficulty in difficulties:

        # \"                -> don't interpretate the " as a python string
        # .*?               -> . match the next character whatever it is, * repeat the . from 0 to unlimited times, ? make 
    #                               the * lazy i.e. stop at first match of what's after the ?
        # (?=}})            -> positive look ahead, match everything before }}
        # (?<=puzzle\":)    -> positive look behind, match everything after puzzle":
        # (?=,)             -> positive look ahead, match everything before a ,
        # (?<=solution\":)  -> positive look behind, match everything after solution"
        # [.*]              -> get everything inside square brackets, including the brackets

        sudoku_info = re.findall(r"\"{}\":.*?(?=}})".format(difficulty), sudoku_data)[0]
        sudoku_game = re.findall(r"(?<=puzzle\":)\[.*](?=,)", sudoku_info)[0]
        sudoku_sol = re.findall(r"(?<=solution\":)\[.*]", sudoku_info)[0]

        # [1:-1] excludes both square brackets
        sudoku_game = [int(x) for x in sudoku_game[1:-1].split(",")]
        sudoku_sol = [int(x) for x in sudoku_sol[1:-1].split(",")]

        f = lambda arr: np.reshape(arr, (9, 9))
        sudokus[difficulty] = {"puzzle": f(sudoku_game), "solution": f(sudoku_sol)}

    return sudokus
