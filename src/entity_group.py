import time

import pygame.surface
from tiles import Camera, TileManager
from scene_manager import SceneManager
import os
import json
import sys
from entity import *
from chests import Chest
from dialogue import Dialogue, FinalDialogue
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

        self.queue = []
        self.queue_timer = []
        self.queue_args = []

        self.scene_queue_func = []
        self.scene_queue_scenes = []
        self.scene_queue_args = []

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

    def get_entity_at(self, x, y, return_all=False):
        li = []

        for e in self.entities:
            if e.tile_x == x and e.tile_y == y:
                if return_all:
                    li.append(e)
                else:
                    return e
        if return_all:
            return li
        else:
            return None

    def get_entity(self, t: object):
        for e in self.entities:
            if type(e) == t:
                return e

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

    def add_to_queue(self, func, delay, *args):
        self.queue.append(func)
        self.queue_timer.append(time.time() + delay)
        self.queue_args.append(args)

    def execute_on_scene_start(self, func, scene, *args):
        self.scene_queue_func.append(func)
        self.scene_queue_scenes.append(scene)
        self.scene_queue_args.append(args)

    def on_scene_start(self, scene):
        for i, sc in enumerate(self.scene_queue_scenes):
            if sc == scene:
                self.scene_queue_func[i](*self.scene_queue_args[i])
                self.scene_queue_scenes.pop(i)
                self.scene_queue_func.pop(i)
                self.scene_queue_args.pop(i)
                i -= 1

    def remove_from_queue(self, i):
        self.queue.pop(i)
        self.queue_timer.pop(i)
        self.queue_args.pop(i)

    def update(self, dt):
        delete = []
        for i, timer in enumerate(self.queue_timer):
            if time.time() > timer:
                self.queue[i](*self.queue_args[i])
                delete.append(i)
        delete.reverse()
        for i in delete:
            self.remove_from_queue(i)

        for e in self.entities:
            e.update(dt)

    def render(self):
        # Simple sort order
        movable_entity_classes = MobileEntity.__subclasses__()
        movable_entity_classes.extend(Enemy.__subclasses__())
        follower_entity_classes = Follower.__subclasses__()
        movable_entities = []
        follower_entities = []

        for e in self.entities:
            if type(e) in movable_entity_classes:
                movable_entities.append(e)
            elif type(e) in follower_entity_classes:
                follower_entities.append(e)
            else:
                e.render()

        for e in movable_entities:
            e.render()

        for e in follower_entities:
            e.render()
