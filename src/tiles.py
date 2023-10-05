from math import floor, ceil, dist
import pygame
import threading


class Camera:
    def __init__(self, screensize, x=0, y=0):
        (self.screen_width, self.screen_height) = screensize
        self.center_offset_x = self.screen_width / 2
        self.center_offset_y = self.screen_height / 2
        self.x = x
        self.y = y
        self.rel_x = self.x - self.center_offset_x
        self.rel_y = self.y - self.center_offset_y

    def update(self):
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
            self.surface.blit(chunk.surface, (chunk.x * self.chunk_size_px - self.cam.rel_x - self.chunk_size_px / 2,
                                              chunk.y * self.chunk_size_px - self.cam.rel_y - self.chunk_size_px / 2))

    def update(self):

        self.cam.update()
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

        return self.chunks[self.chunk_positions.index([chunk_x, chunk_y])].get_tile(x % self.chunk_size, y % self.chunk_size )


class Tile:
    def __init__(self, name, image):
        self.name = name
        self.image = pygame.image.load(image)


class Chunk:
    tile = pygame.image.load("../assets/tiles/tile.png")
    tile2 = pygame.image.load("../assets/tiles/start_tile.png")

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
                tile = pygame.Surface((0, 0))
                match self.tiles[y][x]:
                    case 1:
                        tile = self.tile
                    case 2:
                        tile = self.tile2
                    case _:
                        pass

                self.surface.blit(tile, (x * self.tile_size, y * self.tile_size))

    def get_tile(self, x, y):
        return self.tiles[y][x]
