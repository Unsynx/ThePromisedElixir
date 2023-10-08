import pygame.surface

from tiles import Camera, TileManager
from random import randint


class Entity:
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, tile_size: int):
        self.camera = camera
        self.screen = screen
        self.tile_manager = tile_manager
        self.tile_size = tile_size
        self.group = None

        self.x = 0
        self.y = 0

        self.tile_x = 0
        self.tile_y = 0

        self.surface = pygame.surface.Surface((tile_size, tile_size))

        self.health = None

    def set_position(self, tile_x, tile_y):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = self.tile_size * tile_x
        self.y = self.tile_size * tile_y

    def on_player_move(self):
        pass

    def attack(self, damage):
        if self.health is None:
            return
        self.health -= damage
        print(f"Entity Attacked: {self.health}hp remaining")

        if self.health <= 0:
            self.on_death()

    def on_death(self):
        print("Entity Dead")
        self.group.entities.pop(self.group.entities.index(self))

    def input(self, pressed):
        pass

    def render(self):
        self.screen.blit(self.surface, (int(self.x) - self.camera.rel_x, int(self.y) - self.camera.rel_y))

    def update(self, dt):
        self.x += (self.tile_x * self.tile_size - self.x) * 0.3
        self.y += (self.tile_y * self.tile_size - self.y) * 0.3

    def move(self, x, y):
        if x != 0:
            if self.tile_manager.get_tile(self.tile_x + x, self.tile_y) != 0:
                e = self.group.get_entity_at(self.tile_x + x, self.tile_y)
                if e is None:
                    self.tile_x += x
                else:
                    e.attack(1)
                    self.x += x * 64  # Animation :)
                return True

        if y != 0:
            if self.tile_manager.get_tile(self.tile_x, self.tile_y + y) != 0:
                e = self.group.get_entity_at(self.tile_x, self.tile_y + y)
                if e is None:
                    self.tile_y += y
                else:
                    e.attack(1)
                    self.y += y * 64  # Animation :)
                return True

        return False


class EntityGroup:
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, tile_size: int):
        self.camera = camera
        self.screen = screen
        self.tile_manager = tile_manager
        self.tile_size = tile_size

        self.entities = []

    def add_entity(self, entity, *args):
        e = entity(self.camera, self.screen, self.tile_manager, self.tile_size, *args)
        e.group = self
        self.entities.append(e)
        return e

    def get_entity_at(self, x, y):
        for e in self.entities:
            if e.tile_x == x and e.tile_y == y:
                return e
        return None

    def on_player_move(self):
        for e in self.entities:
            e.on_player_move()

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


class Player(Entity):
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, tile_size: int):
        super().__init__(camera, screen, tile_manager, tile_size)
        self.health = 10

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


class Enemy(Entity):
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, tile_size: int):
        super().__init__(camera, screen, tile_manager, tile_size)
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

            if self.tile_manager.get_tile(self.tile_x + x, self.tile_y + y) != 0:
                self.move(x, y)
                return

        print("I am stuck")

