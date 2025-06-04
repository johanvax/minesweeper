import pygame as pg

class Tile(pg.sprite.Sprite):
    # Modified __init__ to accept pre-loaded images
    def __init__(self, value, x_pos, y_pos, size, padding, callback, tile_images):
        super().__init__()

        self.tile_size = size
        self.padding = padding

        self.callback = callback

        self.tile_images = tile_images

        self.image = self.tile_images['unflipped']

        self.x_pos = x_pos
        self.y_pos = y_pos

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
