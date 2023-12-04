import random

import pygame
import time


class ParticleSystem:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.particle_x = []
        self.particle_y = []
        self.vel_x = []
        self.vel_y = []
        self.lifetime = []

        self.screen = None
        self.camera = None

    def add_particle(self, x, y, vel_x, vel_y, lifetime):
        self.particle_x.append(x)
        self.particle_y.append(y)
        self.vel_x.append(vel_x)
        self.vel_y.append(vel_y)
        self.lifetime.append(lifetime + time.time())

    def delete_particle(self, index):
        self.particle_x.pop(index)
        self.particle_y.pop(index)
        self.vel_x.pop(index)
        self.vel_y.pop(index)
        self.lifetime.pop(index)

    def update(self):
        for i in range(len(self.particle_x)):
            try:
                if self.lifetime[i] < time.time():
                    self.delete_particle(i)
                    i -= 1
                    continue
                self.tick(i)
                print(f"p: {self.particle_x[i] - self.camera.rel_x, self.particle_y[i] - self.camera.rel_y}")
                self.screen.blit(self.image, (int(self.particle_x[i]) - self.camera.rel_x,
                                              int(self.particle_y[i]) - self.camera.rel_y))
            except IndexError:
                return

    def tick(self, index):
        self.particle_x[index] = self.particle_x[index] + self.vel_x[index]
        self.vel_x[index] = self.vel_x[index] * 0.9
        self.particle_y[index] = self.particle_y[index] + self.vel_y[index]
        self.vel_x[index] = self.vel_x[index] * 0.9


class ParticleManager:
    def __init__(self, screen, camera):
        self.systems = []
        self.screen = screen
        self.camera = camera

    def render(self):
        i = 0
        while i < len(self.systems):
            if len(self.systems[i].particle_x) == 0:
                self.remove_system(self.systems[i])
                i -= 1
                continue
            self.systems[i].update()
            print(f"updated {i}")

    def add_system(self, system: ParticleSystem):
        self.systems.append(system)
        system.screen = self.screen
        system.camera = self.camera

    def remove_system(self, system: ParticleSystem):
        self.systems.remove(system)


class HitEffect(ParticleSystem):
    def __init__(self, x, y):
        super().__init__("../assets/tiles/stairs.png")

        for _ in range(10):
            self.add_particle(x, y, 0.1, 0.1, 3)
