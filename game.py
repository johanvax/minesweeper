import pygame as pg
import random as rnd
import os

from happyface import HappyFace
from tile import Tile
from number import Number

class Game:
    def __init__(self, rows, cols, image_dir_path, difficulty):
        self.rows = rows
        self.cols = cols
        self.tile_size = 16
        self.padding = 0
        self.extra_height = 50

        if difficulty == '--hard': self.bomb_percent = 25
        if difficulty == '--medium': self.bomb_percent = 15
        if difficulty == '--easy': self.bomb_percent = 10

        if not self.bomb_percent: self.bomb_percent = 15

        self.image_dir_path = image_dir_path # Store the image directory path

        self.width = self.cols * (self.tile_size + self.padding)
        self.height = self.rows * (self.tile_size + self.padding)
        self.screen_width = self.width
        self.screen_height = self.height + self.extra_height

        self.bomb_count = 0

        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption("Minesweeper")

        self.tiles = pg.sprite.Group()
        self.happy_faces = pg.sprite.Group()
        self.numbers = pg.sprite.Group()

        self.tile_images = {}
        self._load_tile_images()

        self.number_images = {}
        self._load_number_images()

        self.init_game_elements()

    def _load_tile_images(self):
        image_names = ['unflipped', 'flagged', 'bomb', 'empty'] + [str(i) for i in range(1, 9)]
        for name in image_names:
            try:
                # Use os.path.join to correctly build the file path
                image_file_path = os.path.join(self.image_dir_path, f'{name}-tile.png')
                self.tile_images[name] = pg.image.load(image_file_path).convert_alpha()
            except pg.error as e:
                print(f"Warning: Could not load image {image_file_path}: {e}")

        try:
            # Use os.path.join for the happyface image as well
            happyface_file_path = os.path.join(self.image_dir_path, 'happyface-tile.png')
            self.happyface_image = pg.image.load(happyface_file_path).convert_alpha()
        except pg.error as e:
            print(f"Warning: Could not load {happyface_file_path}: {e}")
            self.happyface_image = None

    def _load_number_images(self):
        image_names = [str(i) for i in range(10)]
        for name in image_names:
            try:
                image_file_path = os.path.join(self.image_dir_path, f'numbers/{name}.png')
                self.number_images[name] = pg.image.load(image_file_path).convert_alpha()
            except pg.error as e:
                print(f"Warning: Could not load image {image_file_path}: {e}")

    def init_game_elements(self):
        self.tiles.empty()
        self.happy_faces.empty()
        self.numbers.empty()

        self._tile_grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        grid, bomb_count = self._init_grid(self.rows, self.cols, self.bomb_percent)

        self.bomb_count = bomb_count

        for r_idx in range(self.rows):
            for c_idx in range(self.cols):
                tile = Tile(grid[r_idx][c_idx], c_idx, r_idx, self.tile_size, self.padding, self.on_click, self.tile_images)
                self.tiles.add(tile)
                self._tile_grid[r_idx][c_idx] = tile # Store tile in the 2D grid

        happy_pixel_x = (self.width // 2) - 16
        happy_pixel_y = self.height + ((self.extra_height - 32) // 2)

        if self.happyface_image:
            self.happy_faces.add(HappyFace(happy_pixel_x, happy_pixel_y, self.reset_game, self.happyface_image))
        else:
            print("HappyFace image not loaded, skipping happy face creation.")

        number_pixel_x = 10
        number_pixel_y = self.height + ((self.extra_height - 32) // 2)
        for i in range(3):
            self.numbers.add(Number(0, number_pixel_x + (i * 19), number_pixel_y, 19, 33, self.number_images))

    def on_click(self, tile, fliporflag):
        if fliporflag:
            if not tile.flagged and not tile.flipped:
                tile.flipped = True
                name = str(tile.value) if 0 < tile.value else ('bomb' if tile.value == -1 else 'empty')
                tile.image = self.tile_images.get(name, self.tile_images['unflipped'])

                if name == 'bomb':
                    print('You lost...', f'Score: {self.bomb_count}')
                    self.reset_game()

                if tile.value == 0:
                    self._reveal_empty_tiles(tile.y_pos, tile.x_pos)
        else:
            if not tile.flipped:
                if self.bomb_count > 0:
                    tile.flagged = not tile.flagged
                    if tile.flagged:
                        tile.image = self.tile_images['flagged']
                        self.bomb_count -= 1
                    else:
                        tile.image = self.tile_images['unflipped']
                        self.bomb_count += 1
                else:
                    if tile.flagged:
                        tile.flagged = not tile.flagged
                        tile.image = self.tile_images['unflipped']
                        self.bomb_count += 1

    def update_numbers(self, new_val):
        digits = list(str(new_val))
        while len(digits) < 3:
            digits.insert(0, '0')

        for i, n in enumerate(self.numbers):
            n.update_image(digits[i])

    def _reveal_empty_tiles(self, start_row, start_col):
        q = [(start_row, start_col)]
        visited = set()

        while q:
            r, c = q.pop(0)

            if (r, c) in visited:
                continue
            visited.add((r, c))

            current_tile = self._tile_grid[r][c]

            if current_tile.value == -1 or current_tile.flagged:
                continue

            if not current_tile.flipped:
                current_tile.flipped = True
                name = str(current_tile.value) if 0 < current_tile.value else 'empty'
                current_tile.image = self.tile_images.get(name, self.tile_images['unflipped'])

            # If the current tile is empty (value 0), add its unvisited and non-bomb neighbors to the queue
            if current_tile.value == 0:
                neighbor_coords = self._get_neighbour_coords_for_bfs(r, c)
                for nr, nc in neighbor_coords:
                    neighbor_tile = self._tile_grid[nr][nc]
                    # Only add if not visited, not a bomb, and not flagged
                    if (nr, nc) not in visited and neighbor_tile.value != -1 and not neighbor_tile.flagged:
                        q.append((nr, nc))


    def _get_neighbour_coords_for_bfs(self, r, c):
        neighbor_coords = []
        offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in offsets:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbor_coords.append((nr, nc))
        return neighbor_coords

    def _init_grid(self, rows, cols, percent):
        grid = [[-1 if rnd.randint(0, 100) > (100 - percent) else 0 for _ in range(cols)] for _ in range(rows)]

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
        clock = pg.time.Clock()
        FPS = 60 # You can adjust this

        while running:
            clock.tick(FPS)

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.reset_game()

            self.tiles.update(events)
            self.happy_faces.update(events)
            self.update_numbers(self.bomb_count)

            self.screen.fill((200, 200, 200))

            self.tiles.draw(self.screen)
            self.happy_faces.draw(self.screen)
            self.numbers.draw(self.screen)

            pg.display.flip()

        pg.quit()
