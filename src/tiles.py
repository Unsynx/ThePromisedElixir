from math import floor, ceil, dist
import pygame
import threading


CHUNK_SIZE = 4
TILE_SIZE = 128


class Camera:
    ARROW_CONTROLS = 0
    CENTER_FIRST_ENTITY = 1
    CENTER_ENTITIES_SMOOTH = 2

    def __init__(self, screensize, x=0, y=0):
        (self.screen_width, self.screen_height) = screensize
        self.center_offset_x = self.screen_width / 2
        self.center_offset_y = self.screen_height / 2
        self.x = x
        self.y = y
        self.rel_x = self.x - self.center_offset_x
        self.rel_y = self.y - self.center_offset_y

        # Camera controls
        self.input_x = 0
        self.input_y = 0
        self.smooth_x = 0
        self.smooth_y = 0

        self.mode = self.CENTER_FIRST_ENTITY
        self.entities = []

    def input(self):
        pressed = pygame.key.get_pressed()

        self.input_x = pressed[pygame.K_RIGHT] - pressed[pygame.K_LEFT]
        self.input_y = pressed[pygame.K_DOWN] - pressed[pygame.K_UP]

    def update(self, dt):
        match self.mode:
            case self.ARROW_CONTROLS:
                self.x += int(self.input_x * dt * 10)
                self.y += int(self.input_y * dt * 10)

            case self.CENTER_ENTITIES_SMOOTH:
                x = 0
                y = 0
                for e in self.entities:
                    x += e.x
                    y += e.y

                x = int(x / len(self.entities))
                y = int(y / len(self.entities))

                # Temp
                self.smooth_x += (x - self.x) * 0.3
                self.smooth_y += (y - self.y) * 0.3

                self.x = int(self.smooth_x)
                self.y = int(self.smooth_y)

            case self.CENTER_FIRST_ENTITY:
                self.x = int(self.entities[0].x / len(self.entities)) + int(self.entities[0].surface.get_width() * 0.5)
                self.y = int(self.entities[0].y / len(self.entities)) + int(self.entities[0].surface.get_height() * 0.5)

        self.rel_x = self.x - self.center_offset_x
        self.rel_y = self.y - self.center_offset_y


class TileManager:
    def __init__(self, surface: pygame.Surface, tile_size: int, chunk_size: int, camera: Camera):
        self.surface = surface
        self.tile_size = tile_size
        self.chunk_size = chunk_size
        self.chunk_size_px = chunk_size * tile_size
        self.cam = camera
        self.chunks = []
        self.chunk_positions = []
        self.chunks_per_width = ceil(self.cam.screen_width / self.chunk_size_px) + 3
        self.chunks_per_height = ceil(self.cam.screen_height / self.chunk_size_px) + 3
        self.chunk_del_range = 10

    def new_chunk(self, x, y):
        self.chunks.append(Chunk(x, y, self.chunk_size, self.tile_size))
        self.chunk_positions.append([x, y])

    def del_chunk(self, i):
        self.chunks.pop(i)
        self.chunk_positions.pop(i)

    def render(self):
        for chunk in self.chunks:
            self.surface.blit(chunk.surface, (chunk.x * self.chunk_size_px - self.cam.x + self.cam.center_offset_x,
                                              chunk.y * self.chunk_size_px - self.cam.y + self.cam.center_offset_y))

    def update(self):
        for x in range(self.chunks_per_width):
            for y in range(self.chunks_per_height):

                chunk_x = x - self.chunks_per_width // 2 + self.cam.x // self.chunk_size_px
                chunk_y = y - self.chunks_per_height // 2 + self.cam.y // self.chunk_size_px

                if [chunk_x, chunk_y] not in self.chunk_positions:
                    thread = threading.Thread(target=self.new_chunk, args=(chunk_x, chunk_y))
                    thread.start()
                    # self.new_chunk(chunk_x, chunk_y)

        for chunk in self.chunk_positions:
            if dist([chunk[0], chunk[1]], [self.cam.x // self.chunk_size_px, self.cam.y // self.chunk_size_px]) > self.chunk_del_range:
                self.del_chunk(self.chunk_positions.index([chunk[0], chunk[1]]))

    def get_tile(self, x, y):
        chunk_x = floor(x/self.chunk_size)
        chunk_y = floor(y/self.chunk_size)

        if [chunk_x, chunk_y] not in self.chunk_positions:
            raise f"Chunk at {x}, {y} is not loaded"

        return self.chunks[self.chunk_positions.index([chunk_x, chunk_y])].get_tile(x % self.chunk_size, y % self.chunk_size)


class Tile:
    def __init__(self, num: int, path):
        self.name = num
        if path is None:
            self.image = pygame.surface.Surface((0, 0))
        else:
            self.image = pygame.image.load(path)


# Define tiles here
class Chunk:
    tile_images = [
        Tile(0, None),
        Tile(1, "../assets/tiles/ground.png"),
        Tile(2, "../assets/tiles/start_tile.png"),
        Tile(3, "../assets/tiles/wall.png"),
        Tile(4, "../assets/tiles/walltop.png")
    ]

    def __init__(self, x: int, y: int, size: int, tile_size: int):
        self.x = x
        self.y = y
        self.size = size
        self.tile_size = tile_size

        self.tiles = self.generate()
        self.surface = pygame.Surface((size * tile_size, size * tile_size))
        self.surface.set_colorkey((255, 100, 255))
        self.render()

    def generate(self):
        try:
            with open(f"../assets/world/chunk_{self.x}_{self.y}.txt", "r") as f:
                chunk = []
                for li in f.readlines():
                    chunk.append(list(map(int, li.split(", "))))
            return chunk

        except FileNotFoundError:
            return None

    def render(self):
        self.surface.fill((255, 100, 255))

        if self.tiles is None:
            return

        for x in range(self.size):
            for y in range(self.size):
                tile = self.tile_images[self.tiles[y][x]].image
                self.surface.blit(tile, (x * self.tile_size, y * self.tile_size))

    def get_tile(self, x, y):
        try:
            return self.tiles[y][x]
        except TypeError:
            return 0
