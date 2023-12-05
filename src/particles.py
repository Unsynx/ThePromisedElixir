import random

import pygame
import time
from gui import Text


class ParticleSystem:
    def __init__(self, image: pygame.Surface):
        self.image = image
        self.particle_x = []
        self.particle_y = []
        self.vel_x = []
        self.vel_y = []
        self.lifetime = []

        self.manager = None
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
        if len(self.particle_x) == 0:
            self.manager.remove_system(self)
            print("deleted system")
            return

        for i in range(len(self.particle_x)):
            self.tick(i)
            print(f"Particle drawn at {int(self.particle_x[i]) - self.camera.rel_x, int(self.particle_y[i]) - self.camera.rel_y}")
            self.screen.blit(self.image, (int(self.particle_x[i]) - self.camera.rel_x,
                                          int(self.particle_y[i]) - self.camera.rel_y))

        for i in range(len(self.particle_x)):
            if self.lifetime[i] < time.time():
                self.delete_particle(i)
                i -= 1
                if i < 0:
                    return

    def tick(self, index):
        self.particle_x[index] = self.particle_x[index] + self.vel_x[index]
        self.vel_x[index] = self.vel_x[index] * 0.95
        self.particle_y[index] = self.particle_y[index] + self.vel_y[index]
        self.vel_y[index] = self.vel_y[index] * 0.95


class ParticleManager:
    def __init__(self, screen, camera):
        self.systems = []
        self.screen = screen
        self.camera = camera

    def render(self):
        for p in self.systems:
            p.update()

    def add_system(self, system: ParticleSystem):
        self.systems.append(system)
        system.screen = self.screen
        system.camera = self.camera
        system.manager = self

    def remove_system(self, system: ParticleSystem):
        self.systems.remove(system)


class HitEffect(ParticleSystem):
    def __init__(self, x, y, damage):
        t = Text(f"-{damage}hp", Text.FONT_BASE, 48, (255, 255, 255))
        super().__init__(t.surface)

        for _ in range(1):
            self.add_particle(x, y, random.randint(-5, 5), random.randint(-5, 5), 1)
