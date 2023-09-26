import math
import pygame
import random


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
        self.chunks_per_width = math.ceil(self.cam.screen_width / self.chunk_size_px) + 3
        self.chunks_per_height = math.ceil(self.cam.screen_height / self.chunk_size_px) + 3
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
                    self.new_chunk(chunk_x, chunk_y)

        for chunk in self.chunk_positions:
            if math.dist([chunk[0], chunk[1]], [self.cam.x // self.chunk_size_px, self.cam.y // self.chunk_size_px]) > self.chunk_del_range:
                self.del_chunk(self.chunk_positions.index([chunk[0], chunk[1]]))


class Tile:
    def __init__(self, name, image):
        self.name = name
        self.image = pygame.image.load(image)


class Chunk:
    tile = pygame.image.load("../assets/tiles/tile1.png")

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

        chunk = []
        for x in range(self.size):
            row = []
            for y in range(self.size):
                row.append(random.randint(0, 1))
            chunk.append(row)
        return chunk

    def render(self):
        self.surface.fill((255, 100, 255))

        for x in range(self.size):
            for y in range(self.size):
                if self.tiles[y][x] == 0:
                    self.surface.blit(self.tile, (x * self.tile_size, y * self.tile_size))
