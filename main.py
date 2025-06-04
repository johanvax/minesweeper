#!/usr/bin/env python3

import sys

from game import Game
import pygame as pg

if __name__ == '__main__':
    pg.init()

    args = sys.argv
    rows = int(args[1]) if len(args) > 1 else 30
    cols = int(args[2]) if len(args) > 1 else 40

    path = __file__[:-7] # remove "main.py", if you run the code yourself
    # path = './'
    game = Game(rows, cols, path)
    game.run()
