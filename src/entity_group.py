import json
import os
import sys
from tiles import Camera, TileManager
import pygame.surface
from items import *
from entity import *


class EntityGroup:
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, tile_size: int):
        self.camera = camera
        self.screen = screen
        self.tile_manager = tile_manager
        self.tile_size = tile_size

        self.entities = []

    def __get__(self):
        return self.entities

    def __getitem__(self, item):
        return self.entities[item]

    def add_entity(self, entity, *args, **kwargs):
        e = entity(self.camera, self.screen, self.tile_manager, self.tile_size, *args)
        for item, value in kwargs.items():
            setattr(e, item, value)

        e.group = self
        self.entities.append(e)
        return e

    def remove(self, e):
        self.entities.remove(e)

    def get_entity_at(self, x, y):
        for e in self.entities:
            if e.tile_x == x and e.tile_y == y:
                return e
        return None

    def on_player_move(self, player):
        for e in self.entities:
            e.on_player_move(player)

    def load(self):
        self.entities = []
        for file in os.listdir("../assets/saves"):
            if file.endswith(".json"):
                with open(f"../assets/saves/{file}", "r") as f:
                    data = json.load(f)

                    e = self.add_entity(getattr(sys.modules[__name__], data["type"]))
                    e.set_position(data["tile_x"], data["tile_y"])

                    for item, value in data.items():
                        setattr(e, item, value)

    def save(self):
        # Delete current saved data
        dir_name = "../assets/saves"
        test = os.listdir(dir_name)
        for item in test:
            if item.endswith(".json"):
                os.remove(os.path.join(dir_name, item))

        for i, e in enumerate(self.entities):
            data = {
                "tile_x": e.tile_x,
                "tile_y": e.tile_y,
                "health": e.health,
                "type": e.type,
                "intractable": e.intractable
            }

            try:
                data["weapon"] = e.weapon.name
            except AttributeError:
                data["weapon"] = None

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
