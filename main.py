#!/usr/bin/env python3

import sys
import os # Import os module

from game import Game
import pygame as pg

if __name__ == '__main__':
    pg.init()

    args = sys.argv
    rows = int(args[1]) if len(args) > 1 else 30
    cols = int(args[2]) if len(args) > 1 else 40

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))


    image_path = os.path.join(base_path, 'images') + os.sep

    game = Game(rows, cols, image_path)
    game.run()
