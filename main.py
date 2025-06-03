import pygame as pg
import random as rnd

class Tile(pg.sprite.Sprite):
    def __init__(self, value, x_pos, y_pos, size, padding, callback): # -1 is bomb, then we have 0-8
        super().__init__()

        self.tile_size = size
        self.padding = padding

        self.callback = callback

        self.image = pg.image.load('./images/unflipped-tile.png')

        # x_pos and y_pos here refer to the grid coordinates, not pixel coordinates
        self.x_pos = x_pos
        self.y_pos = y_pos

        # Calculate pixel position for the rect
        pixel_x = x_pos * (self.tile_size + self.padding)
        pixel_y = y_pos * (self.tile_size + self.padding)
        self.rect = pg.Rect(pixel_x, pixel_y, size, size)

        self.value = value
        self.flipped = False
        self.flagged = False

    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    if event.button == 1: # Left click
                        self.callback(self, True)
                    elif event.button == 3: # Right click
                        self.callback(self, False)


def on_click(tile, fliporflag):
    if fliporflag:
        if not tile.flagged and not tile.flipped:
            tile.flipped = True
            name = str(tile.value) if 0 < tile.value else ('bomb' if tile.value == -1 else 'empty')
            tile.image = pg.image.load(f'./images/{name}-tile.png')
    else:
        if not tile.flipped:
            tile.flagged = not tile.flagged
            if tile.flagged:
                tile.image = pg.image.load('images/flagged-tile.png')
            else:
                tile.image = pg.image.load('./images/unflipped-tile.png')


def init_grid(rows, cols):
    grid = [[-1 if rnd.randint(0, 100) > 85 else 0 for _ in range(cols)] for _ in range(rows)]

    for r_idx in range(rows): # Iterate through rows
        for c_idx in range(cols): # Iterate through columns
            if grid[r_idx][c_idx] != -1: # If it's not a bomb
                bomb_count = 0
                neighbor_coords = get_neighbour_coords(grid, r_idx, c_idx)
                for nr, nc in neighbor_coords:
                    if grid[nr][nc] == -1:
                        bomb_count += 1
                grid[r_idx][c_idx] = bomb_count # Assign the count to the tile

    return grid

def get_neighbour_coords(grid, r, c): # r is row, c is column
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    neighbor_coords = []
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in offsets:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbor_coords.append((nr, nc))
    return neighbor_coords

if __name__ == '__main__':
    pg.init()

    pg.display.set_caption("Minesweeper")

    tiles = pg.sprite.Group()

    rows = 35
    cols = 50

    tile_size = 16
    padding = 0

    grid = init_grid(rows, cols)

    for r_idx in range(rows):
        for c_idx in range(cols):
            tiles.add(Tile(grid[r_idx][c_idx], c_idx, r_idx, tile_size, padding, on_click))

    width = cols * (tile_size + padding)
    height = rows * (tile_size + padding)

    screen = pg.display.set_mode((width, height))

    running = True
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False

        tiles.update(events)

        screen.fill((0, 0, 0))

        tiles.draw(screen)

        pg.display.flip()

    pg.quit()
