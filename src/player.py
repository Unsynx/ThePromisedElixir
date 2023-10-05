import pygame.surface

from tiles import Camera
from math import ceil


class Entity:
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_size: int):
        self.camera = camera
        self.screen = screen
        self.tile_size = tile_size

        self.x = 0
        self.y = 0

        self.tile_x = 0
        self.tile_y = 0

        self.surface = pygame.surface.Surface((128, 128))
        self.surface.fill((255, 255, 255))

    def render(self):
        self.screen.blit(self.surface, (int(self.x) - self.camera.rel_x, int(self.y) - self.camera.rel_y))

    def update(self):
        self.x += (self.tile_x * self.tile_size - self.x) * 0.3
        self.y += (self.tile_y * self.tile_size - self.y) * 0.3


class Player(Entity):
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_size: int):
        super().__init__(camera, screen, tile_size)

        self.input_x = 0
        self.input_y = 0

        self.recent_input_x = False
        self.recent_input_y = False

    def input(self, pressed):
        # Not 100% accurate
        self.input_x = pressed[pygame.K_RIGHT] - pressed[pygame.K_LEFT]
        if not self.recent_input_x:
            self.tile_x += self.input_x
            self.recent_input_x = True
        elif self.input_x == 0:
            self.recent_input_x = False

        self.input_y = pressed[pygame.K_DOWN] - pressed[pygame.K_UP]
        if not self.recent_input_y:
            self.tile_y += self.input_y
            self.recent_input_y = True
        elif self.input_y == 0:
            self.recent_input_y = False
