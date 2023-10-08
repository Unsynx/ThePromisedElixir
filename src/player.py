import pygame.surface

from tiles import Camera, TileManager
from math import ceil


class Entity:
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, tile_size: int):
        self.camera = camera
        self.screen = screen
        self.tile_manager = tile_manager
        self.tile_size = tile_size

        self.x = 0
        self.y = 0

        self.tile_x = 0
        self.tile_y = 0

        self.surface = pygame.surface.Surface((tile_size, tile_size))

    def render(self):
        self.screen.blit(self.surface, (int(self.x) - self.camera.rel_x, int(self.y) - self.camera.rel_y))

    def update(self):
        self.x += (self.tile_x * self.tile_size - self.x) * 0.3
        self.y += (self.tile_y * self.tile_size - self.y) * 0.3


class EntityGroup:
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, tile_size: int):
        self.camera = camera
        self.screen = screen
        self.tile_manager = tile_manager
        self.tile_size = tile_size

        self.entities = []

    def add_entity(self, entity: Entity):
        self.entities.append(entity)
        entity.camera = self.camera
        entity.screen = self.screen
        entity.tile_manager = self.tile_manager
        entity.tile_size = self.tile_size
        return entity

    def update(self):
        for e in self.entities:
            e.update()

    def render(self):
        # Add depth sorting option
        for e in self.entities:
            e.render()


class Player(Entity):
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, tile_size: int):
        super().__init__(camera, screen, tile_manager, tile_size)

        self.input_x = 0
        self.input_y = 0

        self.recent_input_x = False
        self.recent_input_y = False

        self.surface = pygame.image.load("../assets/player/frog3.png")

    def input(self, pressed):
        self.input_x = pressed[pygame.K_RIGHT] - pressed[pygame.K_LEFT]
        if self.recent_input_x and self.input_x != 0:
            if self.tile_manager.get_tile(self.tile_x + self.input_x, self.tile_y) != 0:
                self.tile_x += self.input_x

            self.recent_input_x = False
        elif self.input_x == 0:
            self.recent_input_x = True

        self.input_y = pressed[pygame.K_DOWN] - pressed[pygame.K_UP]
        if self.recent_input_y and self.input_y != 0:
            if self.tile_manager.get_tile(self.tile_x, self.tile_y + self.input_y) != 0:
                self.tile_y += self.input_y

            self.recent_input_y = False
        elif self.input_y == 0:
            self.recent_input_y = True


class Enemy(Entity):
    def __init__(self):
        super().__init__()
