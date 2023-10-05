import pygame.surface

from tiles import Camera


class Entity:
    def __init__(self, camera: Camera, screen: pygame.surface.Surface):
        self.camera = camera
        self.screen = screen

        self.x = 0
        self.y = 0

        self.surface = pygame.surface.Surface((128, 128))
        self.surface.fill((255, 255, 255))

    def render(self):
        self.screen.blit(self.surface, (self.x - self.camera.rel_x, self.y - self.camera.rel_y))


class Player(Entity):
    def __init__(self, camera: Camera, screen: pygame.surface.Surface):
        super().__init__(camera, screen)

    def move(self, x=0, y=0):
        self.x += x
        self.y += y
