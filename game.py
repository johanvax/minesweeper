import pygame as pg
import random as rnd

from happyface import HappyFace
from tile import Tile

class Game:
    def __init__(self, rows, cols, path):
        self.rows = rows
        self.cols = cols
        self.tile_size = 16
        self.padding = 0
        self.extra_height = 50

        self.path = path

        self.width = self.cols * (self.tile_size + self.padding)
        self.height = self.rows * (self.tile_size + self.padding)
        self.screen_width = self.width
        self.screen_height = self.height + self.extra_height

        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption("Minesweeper")

        self.tiles = pg.sprite.Group()
        self.happy_faces = pg.sprite.Group()

        self.init_game_elements()

    def init_game_elements(self):
        self.tiles.empty()
        self.happy_faces.empty()

        grid, bomb_count = self._init_grid(self.rows, self.cols)

        for r_idx in range(self.rows):
            for c_idx in range(self.cols):
                self.tiles.add(Tile(grid[r_idx][c_idx], c_idx, r_idx, self.tile_size, self.padding, self.on_click, self.path))

        happy_pixel_x = (self.width // 2) - 16
        happy_pixel_y = self.height + ((self.extra_height - 32) // 2)


        self.happy_faces.add(HappyFace(happy_pixel_x, happy_pixel_y, self.reset_game, self.path))

    def on_click(self, tile, fliporflag):
        if fliporflag:
            if not tile.flagged and not tile.flipped:
                tile.flipped = True
                name = str(tile.value) if 0 < tile.value else ('bomb' if tile.value == -1 else 'empty')
                tile.image = pg.image.load(f'{tile.path}images/{name}-tile.png')
        else:
            if not tile.flipped:
                tile.flagged = not tile.flagged
                if tile.flagged:
                    tile.image = pg.image.load(f'{tile.path}images/flagged-tile.png')
                else:
                    tile.image = pg.image.load(f'{tile.path}images/unflipped-tile.png')

    def _init_grid(self, rows, cols):
        grid = [[-1 if rnd.randint(0, 100) > 85 else 0 for _ in range(cols)] for _ in range(rows)]

        total_bombs = 0
        for r_idx in range(rows):
            for c_idx in range(cols):
                if grid[r_idx][c_idx] != -1:
                    bomb_count = 0
                    neighbor_coords = self._get_neighbour_coords(grid, r_idx, c_idx)
                    for nr, nc in neighbor_coords:
                        if grid[nr][nc] == -1:
                            bomb_count += 1
                    grid[r_idx][c_idx] = bomb_count
                else:
                    total_bombs += 1
        return grid, total_bombs

    def _get_neighbour_coords(self, grid, r, c):
        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0
        neighbor_coords = []
        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in offsets:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_coords.append((nr, nc))
        return neighbor_coords

    def reset_game(self):
        self.init_game_elements()

    def run(self):
        running = True
        while running:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.reset_game()

            self.tiles.update(events)
            self.happy_faces.update(events)

            self.screen.fill((200, 200, 200)) # Light grey background

            self.tiles.draw(self.screen)
            self.happy_faces.draw(self.screen)

            pg.display.flip()

        pg.quit()
