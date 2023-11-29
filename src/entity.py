import pygame.surface
from random import randint
from constants import *
from tween import Tween
import sys
from items import *


class Entity:
    def __init__(self):
        # Vars needed by all entities. Set by EntityGroup
        self.camera = None
        self.screen = None
        self.tile_manager = None
        self.scene_manager = None
        self.tile_size = None
        self.group = None
        self.type = type(self).__name__
        self.surface = None
        self.intractable = False

        self.serialized_vars = {}

        self.x = 0
        self.y = 0
        self.tile_x = 0
        self.tile_y = 0

        self.serialize("type", lambda: self.type)\
            .serialize("x", lambda: self.x)\
            .serialize("y", lambda: self.y)\
            .serialize("tile_x", lambda: self.tile_x)\
            .serialize("tile_y", lambda: self.tile_y)

    def serialize(self, name: str, var_func):
        self.serialized_vars[name] = var_func
        return self

    def load(self, name: str, value):
        setattr(self, name, value)

    def set_position(self, tile_x, tile_y):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = self.tile_size * tile_x
        self.y = self.tile_size * tile_y

    def on_player_move(self):
        pass

    def on_interact(self, entity):
        pass

    def on_death(self):
        print("Entity Dead")
        self.group.entities.pop(self.group.entities.index(self))

    def input(self, pressed):
        pass

    def render(self):
        self.screen.blit(self.surface, (int(self.x) - self.camera.rel_x, int(self.y) - self.camera.rel_y))

    def update(self, dt):
        pass


class MobileEntity(Entity):
    def __init__(self):
        super().__init__()

        self.health = None
        self.weapon = NoWeapon()

        self.animation_x = None
        self.animation_y = None

        self.serialize("health", lambda: self.health)\
            .serialize("weapon", lambda: self.weapon.name)

    def load(self, name: str, value):
        if name == "weapon":
            value = getattr(sys.modules[__name__], value)()
        setattr(self, name, value)

    def move(self, x, y):
        if x != 0:
            _, collider = self.tile_manager.get_tile(self.tile_x + x, self.tile_y)
            if not collider:
                e = self.group.get_entity_at(self.tile_x + x, self.tile_y)
                if e is None:
                    self.tile_x += x
                    self.animation_x = Tween(self.x, self.tile_x * self.tile_size, 100)
                elif e.intractable:
                    e.on_interact(self)
                else:
                    self.attack_logic(e, x, 0)
                    self.x += x * 64
                return True

        if y != 0:
            _, collider = self.tile_manager.get_tile(self.tile_x, self.tile_y + y)
            if not collider:
                e = self.group.get_entity_at(self.tile_x, self.tile_y + y)
                if e is None:
                    self.tile_y += y
                    self.animation_y = Tween(self.y, self.tile_y * self.tile_size, 100)
                elif e.intractable:
                    e.on_interact(self)
                else:
                    self.attack_logic(e, 0, y)
                    self.y += y * 64
                return True

        return False

    def attack(self, damage):
        if self.health is None:
            return

        self.health -= damage

        if self.health <= 0:
            self.on_death()

    def attack_logic(self, enemy, x, y):
        if self.weapon is None:
            enemy.attack(1)
            return

        if x == -1:
            direction = LEFT
        elif x == 1:
            direction = RIGHT
        elif y == 1:
            direction = DOWN
        elif y == -1:
            direction = UP
        else:
            raise "Not a valid attack"

        self.weapon.attack(self.tile_x, self.tile_y, direction, self.group)

    def update(self, dt):
        if self.animation_x is not None:
            self.animation_x.update()
            self.x = self.animation_x.get_current_value()
        if self.animation_y is not None:
            self.animation_y.update()
            self.y = self.animation_y.get_current_value()

    def set_weapon(self, weapon):
        self.weapon = weapon


class Player(MobileEntity):
    def __init__(self):
        super().__init__()
        self.health = 10
        self.max_health = self.health

        self.input_x = 0
        self.input_y = 0

        self.recent_input_x = False
        self.recent_input_y = False

        self.surface = pygame.image.load("../assets/player/frog3.png")

    def input(self, pressed):
        moved = False

        self.input_x = pressed[pygame.K_RIGHT] - pressed[pygame.K_LEFT]
        self.input_y = pressed[pygame.K_DOWN] - pressed[pygame.K_UP]

        if self.recent_input_x and self.input_x != 0:
            if self.move(self.input_x, 0):
                moved = True

            self.recent_input_x = False
        elif self.input_x == 0:
            self.recent_input_x = True

        if self.recent_input_y and self.input_y != 0:
            if self.move(0, self.input_y):
                moved = True

            self.recent_input_y = False
        elif self.input_y == 0:
            self.recent_input_y = True

        if moved:
            self.group.on_player_move()


class Enemy(MobileEntity):
    def __init__(self):
        super().__init__()
        self.health = 5

        self.surface = pygame.image.load("../assets/player/baddy.png")

    def on_player_move(self):
        offset = randint(0, 3)
        for i in range(4):
            x = 0
            y = 0
            match (offset + i) % 4:
                case 0:
                    x = -1
                case 1:
                    x = 1
                case 2:
                    y = -1
                case 3:
                    y = 1

            tile, collider = self.tile_manager.get_tile(self.tile_x + x, self.tile_y + y)
            # instead of returning a tile index, it returns false when the chunk is not loaded
            if not tile:
                return

            if not collider:
                self.move(x, y)
                return

        print("I am stuck")


class Dummy(MobileEntity):
    def __init__(self):
        super().__init__()
        self.health = 1

        self.surface = pygame.image.load("../assets/player/baddy.png")


class Staircase(Entity):
    def __init__(self):
        super().__init__()
        self.surface = pygame.image.load("../assets/tiles/stairs.png")
        self.intractable = True

    def on_interact(self, entity):
        if not type(entity) is Player:
            return

        self.group.save()
        self.scene_manager.set_scene("loadingScreen", True)

