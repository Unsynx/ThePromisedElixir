import pygame.surface
from tiles import Camera, TileManager
from scene_manager import SceneManager
import os
import json
import sys
from entity import *
from chests import Chest
from particles import ParticleManager


class EntityGroup:
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, scene_manager: SceneManager, particle_manager: ParticleManager, tile_size: int):
        self.camera = camera
        self.screen = screen
        self.tile_manager = tile_manager
        self.scene_manager = scene_manager
        self.particle_manager = particle_manager
        self.tile_size = tile_size

        self.entities = []

    def __get__(self):
        return self.entities

    def __getitem__(self, item):
        return self.entities[item]

    def add_entity(self, entity, *args, **kwargs):
        e = entity(*args)
        for item, value in kwargs.items():
            setattr(e, item, value)

        e.group = self
        e.camera = self.camera
        e.screen = self.screen
        e.tile_manager = self.tile_manager
        e.scene_manager = self.scene_manager
        e.particle_manager = self.particle_manager
        e.tile_size = self.tile_size

        self.entities.append(e)
        e.on_entity_ready()
        return e

    def remove(self, e):
        try:
            self.entities.remove(e)
        except ValueError:
            print(f"Tried to delete {e} from the group, but was not in list")

    def get_entity_at(self, x, y):
        for e in self.entities:
            if e.tile_x == x and e.tile_y == y:
                return e
        return None

    def on_player_move(self, player):
        for e in self.entities:
            e.on_player_move(player)

    def load(self, player_only=False):
        self.entities = []
        for file in os.listdir("../assets/saves"):
            if file.endswith(".json"):
                with open(f"../assets/saves/{file}", "r") as f:
                    data = json.load(f)
                    e = self.add_entity(getattr(sys.modules[__name__], data["type"]))

                    for item, value in data.items():
                        e.load(item, value)

                    if player_only:
                        return

    def save(self):
        # Delete current saved data
        dir_name = "../assets/saves"
        test = os.listdir(dir_name)
        for item in test:
            if item.endswith(".json"):
                os.remove(os.path.join(dir_name, item))

        for i, e in enumerate(self.entities):
            if e.ignore:
                continue

            data = {}
            for var in e.serialized_vars:
                data[var] = e.serialized_vars[var]()

            with open(f"../assets/saves/entity_{i}.json", "x") as f:
                json.dump(data, f)

    def input(self, pressed):
        for e in self.entities:
            e.input(pressed)

    def update(self, dt):
        for e in self.entities:
            e.update(dt)

    def render(self):
        # Add depth sorting option
        for e in self.entities:
            e.render()
