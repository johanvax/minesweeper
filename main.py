#!/usr/bin/env python3

import sys
import os

from game import Game
import pygame as pg

if __name__ == '__main__':
    pg.init()

    DEFAULT_ROWS = 20
    DEFAULT_COLS = 15

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    args = sys.argv
    try:
        rows = None
        cols = None
        difficulty = None
        if len(args) == 2: # must be difficulty, or help
            if args[1] == '--help':
                print('Provide arguments like this:\n\t<[--easy, --medium, --hard]>, or\n\t<rows> <cols>, or\n\t<rows> <cols> <[--easy, --medium, --hard]>')
            else:
                difficulty = args[1]
                rows = DEFAULT_ROWS
                cols = DEFAULT_COLS
        elif len(args) == 3:
            difficulty = '--medium'
            rows = int(args[1])
            cols = int(args[2])
        elif len(args) == 4:
            difficulty = args[3]
            rows = int(args[1])
            cols = int(args[2])
        else:
            difficulty = '--medium'
            rows = DEFAULT_ROWS
            cols = DEFAULT_COLS

        image_path = os.path.join(base_path, 'images') + os.sep

        if rows and cols and image_path and difficulty:
            game = Game(rows, cols, image_path, difficulty)
            game.run()
    except:
        print("Error loading game. Use '--help' to see how to run.")
