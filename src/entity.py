import random
import pygame.surface
from tiles import Camera, TileManager, Chunk
from math import copysign
from random import randint
from constants import *
from items import SimpleSpearWeapon, FunnyExplosion
from tween import Tween

MOVEMENT_RADIUS = 3


class Entity:
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, tile_size: int):
        self.camera = camera
        self.screen = screen
        self.tile_manager = tile_manager
        self.tile_size = tile_size
        self.group = None
        self.type = type(self).__name__

        self.companions = []

        self.x = 0
        self.y = 0
        self.tile_x = 0
        self.tile_y = 0

        self.surface = pygame.surface.Surface((tile_size, tile_size))

        self.health = None
        self.weapon = None
        self.intractable = False

        self.animation_x = None
        self.animation_y = None

    def set_weapon(self, weapon):
        self.weapon = weapon

    def set_position(self, tile_x, tile_y):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = self.tile_size * tile_x
        self.y = self.tile_size * tile_y

    def on_player_move(self, player):
        pass

    def on_interact(self, entity):
        pass

    def attack(self, damage):
        if self.health is None:
            return

        self.health -= damage
        if any(isinstance(x, HealthBar) for x in self.companions):
            self.companions[0].set_var(current_value=self.health)

        print(f"Entity Attacked: {self.health}hp remaining")

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

    def on_death(self):
        print("Entity Dead")
        self.group.entities.pop(self.group.entities.index(self))

    def input(self, pressed):
        pass

    def render(self):
        self.screen.blit(self.surface, (int(self.x) - self.camera.rel_x, int(self.y) - self.camera.rel_y))

        for e in self.companions:
            e.render()

    def update(self, dt):
        if self.animation_x is not None:
            self.animation_x.update()
            self.x = self.animation_x.get_current_value()
        if self.animation_y is not None:
            self.animation_y.update()
            self.y = self.animation_y.get_current_value()

        for e in self.companions:
            e.update(dt, x=self.x, y=self.y)

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
                    # self.x += x * 64
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
                    # self.y += y * 64
                return True

        return False

    def add_companion_entity(self, companion, **kwargs):
        e = companion(self.camera, self.screen, self.tile_manager, self.tile_size)
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.companions.append(e)
        return e


class CompanionEntity(Entity):
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, tile_size: int):
        super().__init__(camera, screen, tile_manager, tile_size)

        self.parent_width = 0
        self.parent_height = 0

        self.offset_x = 0
        self.offset_y = 0

    def update(self, dt, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def center_on_parent_x(self, parent_width):
        self.offset_x = (parent_width - self.surface.get_width()) * 0.5
        return self

    def set_var(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            self.on_var_set(key)

    def render(self):
        self.screen.blit(self.surface, (
            int(self.x + self.offset_x) - self.camera.rel_x, int(self.y + self.offset_y) - self.camera.rel_y))

    def on_var_set(self, var):
        pass


class HealthBar(CompanionEntity):
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, tile_size: int):
        super().__init__(camera, screen, tile_manager, tile_size)

        self.offset_y = -10

        self.surface = pygame.surface.Surface((100, 10))

        self.current_value = 0
        self.max_value = 0

    def on_var_set(self, var):
        match var:
            case "current_value":
                self.surface.fill((0, 0, 0))
                pygame.draw.rect(self.surface, (255, 255, 255),
                                 [0, 0, self.current_value / self.max_value * self.surface.get_width(),
                                  self.surface.get_height()])


class DamageIndicator(CompanionEntity):
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, tile_size: int):
        super().__init__(camera, screen, tile_manager, tile_size)

        self.surface = pygame.surface.Surface((100, 20))

        self.offset_y = -40
        self.font = pygame.font.Font("../assets/gui/fonts/MondayDonuts.ttf", 20)
        self.text = None

    def on_var_set(self, var):
        match var:
            case "text":
                self.surface = self.font.render(self.text, False, (255, 255, 255))


class Player(Entity):
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, tile_size: int):
        super().__init__(camera, screen, tile_manager, tile_size)
        self.health = 10
        self.max_health = self.health

        self.input_x = 0
        self.input_y = 0

        # saves previous tile before move for enemy movement
        self.last_x = 0
        self.last_y = 0

        self.recent_input_x = False
        self.recent_input_y = False

        self.surface = pygame.image.load("../assets/player/frog3.png")

    def input(self, pressed):
        moved = False

        self.input_x = pressed[pygame.K_RIGHT] - pressed[pygame.K_LEFT]
        self.input_y = pressed[pygame.K_DOWN] - pressed[pygame.K_UP]

        if self.recent_input_x and self.input_x != 0:
            last_x_temp = self.tile_x
            if self.move(self.input_x, 0):
                self.last_x = last_x_temp  # only sets last_x to old x if moved is True
                moved = True

            self.recent_input_x = False
        elif self.input_x == 0:
            self.recent_input_x = True

        if self.recent_input_y and self.input_y != 0:
            last_y_temp = self.tile_y
            if self.move(0, self.input_y):
                self.last_y = last_y_temp
                moved = True

            self.recent_input_y = False
        elif self.input_y == 0:
            self.recent_input_y = True

        if moved:
            self.group.on_player_move(self)


class Enemy(Entity):
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, tile_size: int):
        super().__init__(camera, screen, tile_manager, tile_size)
        self.health = 5
        self.surface = pygame.image.load("../assets/player/baddy.png")
        self.add_companion_entity(HealthBar) \
            .center_on_parent_x(self.surface.get_width()) \
            .set_var(max_value=self.health, current_value=self.health)
        try:
            self.add_companion_entity(DamageIndicator).center_on_parent_x(self.surface.get_width()).set_var(
                text=f"{self.weapon.normal_attack.damage} dmg")
        except AttributeError:
            self.add_companion_entity(DamageIndicator).center_on_parent_x(self.surface.get_width()).set_var(
                text="1 atck")

    def on_player_move(self, player: Player):
        # last x and y for moving toward previous player tile
        d_x = player.tile_x - self.tile_x
        abs_x = abs(d_x)
        d_y = player.tile_y - self.tile_y
        abs_y = abs(d_y)

        x = int(copysign(1, d_x))
        y = int(copysign(1, d_y))

        if abs_x > MOVEMENT_RADIUS or abs_y > MOVEMENT_RADIUS:  # ARBITRARY VALUES: CHANGE FOR MORE/LESS DIFFICULTY
            return

        """
        movement logic:
        1) try to move toward player on furthest axis
        2) try to move toward player on closer axis
        3) try to move away from player on furthest axis
        4) try to move away from player on closest axis
        
        this should guarantee that an entity always moves, even if its course is blocked by walls
        """

        if abs_x >= abs_y:
            if not self.move(x, 0):
                if not self.move(0, y):
                    if not self.move(-x, 0):
                        self.move(0, -y)
        if abs_y > abs_x:
            if not self.move(0, y):
                if not self.move(x, 0):
                    if not self.move(0, -y):
                        self.move(-x, 0)


class Dummy(Entity):
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, tile_size: int):
        super().__init__(camera, screen, tile_manager, tile_size)
        self.health = 1
        self.surface = pygame.image.load("../assets/player/baddy.png")


class Chest(Entity):
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, tile_size: int):
        super().__init__(camera, screen, tile_manager, tile_size)
        self.surface = pygame.image.load("../assets/player/chest.png")
        self.intractable = True

    def on_interact(self, entity: Entity):
        if not type(entity) is Player:
            return

        # temp
        weapons = (
            SimpleSpearWeapon,
            FunnyExplosion
        )
        entity.set_weapon(random.choice(weapons)())
        self.group.remove(self)


class Staircase(Entity):
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, tile_size: int):
        super().__init__(camera, screen, tile_manager, tile_size)
        self.surface = pygame.image.load("../assets/tiles/stairs.png")
        self.intractable = True

        self.scene_manager = None

    def on_interact(self, entity):
        if not type(entity) is Player:
            return

        self.scene_manager.set_scene("win")


class Dialogue(Entity):
    def __init__(self, camera: Camera, screen: pygame.surface.Surface, tile_manager: TileManager, tile_size: int,
                 dialogue_scene):
        super().__init__(camera, screen, tile_manager, tile_size)
        self.dialogue_scene = dialogue_scene
        self.surface = pygame.image.load("../assets/player/wise_old_druid_or_maybe_a_potion_seller.png")
        self.intractable = True

        self.scene_manager = None

    def on_interact(self, entity):
        if not type(entity) is Player:
            return
        self.scene_manager.set_scene(f"{self.dialogue_scene}")
