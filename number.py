import pygame as pg

class Number(pg.sprite.Sprite):
    def __init__(self, value, pixel_x, pixel_y, width, height, number_images):
        super().__init__()

        self.value = value
        self.number_images = number_images
        self.image = number_images[str(value)]

        self.rect = pg.Rect(pixel_x, pixel_y, width, height)

    def update_image(self, new_val):
        self.image = self.number_images[str(new_val)]
