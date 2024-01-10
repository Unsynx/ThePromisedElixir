import pygame.surface
from tiles import Camera, TileManager, Chunk
from math import copysign
from random import randint, choice
from constants import *
from tween import Tween
import sys
from items import *
from particles import HitEffect, PotionEffect, ConfusedEffect, MaxHealthUp

MOVEMENT_RADIUS = 4
PLAYER_MOVEMENT_DELAY = 0.15

pygame.mixer.init()


class Entity:
    def __init__(self):
        # Vars needed by all entities. Set by EntityGroup
        self.camera = None
        self.screen = None
        self.tile_manager = None
        self.scene_manager = None
        self.particle_manager = None
        self.tile_size = None
        self.group = None
        self.type = type(self).__name__
        self.surface = None
        self.intractable = False
        self.visible = True
        self.can_walk_over = False
        self.must_be_attacked_directly = False

        self.serialized_vars = {}
        self.ignore = False
        self.health = None

        self.x = 0
        self.y = 0
        self.tile_x = 0
        self.tile_y = 0

        self.serialize("type", lambda: self.type) \
            .serialize("x", lambda: self.x) \
            .serialize("y", lambda: self.y) \
            .serialize("tile_x", lambda: self.tile_x) \
            .serialize("tile_y", lambda: self.tile_y)

    def serialize(self, name: str, var_func):
        self.serialized_vars[name] = var_func
        return self

    def load(self, name: str, value):
        setattr(self, name, value)

    def on_entity_ready(self):
        pass

    def set_position(self, tile_x, tile_y):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = self.tile_size * tile_x
        self.y = self.tile_size * tile_y
        return self

    def on_player_move(self, player):
        pass

    def on_interact(self, entity):
        pass

    def on_death(self):
        self.group.remove(self)

    def input(self, pressed):
        pass

    def render(self):
        self.screen.blit(self.surface, (int(self.x) - self.camera.rel_x, int(self.y) - self.camera.rel_y))

    def update(self, dt):
        pass

    def attack(self, entity, damage):
        if self.health is None:
            return

        self.health -= damage
        self.particle_manager.add_system(HitEffect(self.x + 64, self.y + 64, damage))

        if self.health <= 0:
            self.on_death()


class Follower(Entity):
    def __init__(self, target: Entity):
        super().__init__()
        self.target = target
        self.ignore = True

        self.offset_x = 0
        self.offset_y = 0

    def update(self, dt):
        self.x = self.target.x + self.offset_x
        self.y = self.target.y + self.offset_y


class HealthBar(Follower):
    def __init__(self, target):
        super().__init__(target)
        self.offset_y = -10
        self.offset_x = 14

        self.surface = pygame.surface.Surface((100, 10))
        self.redraw()

    def redraw(self):
        self.surface.fill((0, 0, 0))
        pygame.draw.rect(self.surface, (217, 33, 45),
                         (0, 0, int(100 * self.target.health / self.target.max_health), 10))


class WeaponVisual(Follower):
    def __init__(self, target: Entity, weapon: Weapon):
        super().__init__(target)
        if weapon.icon_path is None:
            self.surface = pygame.Surface((0, 0))
        else:
            self.surface = pygame.image.load(weapon.icon_path)
        self.offset_x = weapon.offset_x
        self.offset_y = weapon.offset_y


class MobileEntity(Entity):
    def __init__(self):
        super().__init__()

        self.max_health = None
        self.health = None
        self.weapon = NoWeapon()
        self.weapon_visual = None
        self.health_bar = None

        self.animation_x = None
        self.animation_y = None

        self.serialize("health", lambda: self.health) \
            .serialize("weapon", lambda: self.weapon.name)

    def on_entity_ready(self):
        self.set_weapon(self.weapon)
        self.health_bar = self.group.add_entity(HealthBar, self)

    def load(self, name: str, value):
        if name == "weapon":
            value = getattr(sys.modules[__name__], value)()
            self.set_weapon(value)
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
                    self.x += x * 48
                    self.animation_x = Tween(self.x, self.tile_x * self.tile_size, 75)
                    if e.can_walk_over:
                        self.tile_x += x
                        self.animation_x = Tween(self.x, self.tile_x * self.tile_size, 100)
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
                    self.y += y * 48
                    self.animation_y = Tween(self.y, self.tile_y * self.tile_size, 75)
                    if e.can_walk_over:
                        self.tile_y += y
                        self.animation_y = Tween(self.y, self.tile_y * self.tile_size, 100)

                return True

        return False

    def on_death(self):
        self.group.remove(self.weapon_visual)
        self.group.remove(self.health_bar)
        self.group.remove(self)

    def attack(self, entity, damage):
        if self.health is None:
            return

        self.health -= damage
        if self.health_bar:
            self.health_bar.redraw()
        self.particle_manager.add_system(HitEffect(self.x + 64, self.y + 64, damage))

        if self.health <= 0:
            self.on_death()

    def attack_logic(self, enemy, x, y):
        if self.weapon is None:
            enemy.attack(self, 1)
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

        self.weapon.attack(self.tile_x, self.tile_y, direction, self.group, enemy)

    def update(self, dt):
        if self.animation_x is not None:
            self.animation_x.update()
            self.x = self.animation_x.get_current_value()
        if self.animation_y is not None:
            self.animation_y.update()
            self.y = self.animation_y.get_current_value()

    def set_weapon(self, weapon):
        self.weapon = weapon
        self.group.remove(self.weapon_visual)
        self.weapon_visual = self.group.add_entity(WeaponVisual, self, self.weapon)


class Player(MobileEntity):
    steps = [
        pygame.mixer.Sound("../assets/sfx/footstep1.wav"),
        pygame.mixer.Sound("../assets/sfx/footstep2.wav"),
        pygame.mixer.Sound("../assets/sfx/footstep3.wav"),
        pygame.mixer.Sound("../assets/sfx/footstep4.wav")
    ]

    def __init__(self):
        super().__init__()
        self.health = 15
        self.max_health = self.health

        self.weapon = NoWeapon()

        self.input_x = 0
        self.input_y = 0

        # saves previous tile before move for enemy movement
        self.last_x = 0
        self.last_y = 0

        self.recent_input_x = False
        self.recent_input_y = False

        self.can_move = True

        self.surface = pygame.image.load("../assets/player/frog3.png")

    def on_entity_ready(self):
        self.set_weapon(self.weapon)
        self.health_bar = None
        self.can_move = False

        def set_can_move(val):
            self.can_move = val

        self.group.add_to_queue(set_can_move, PLAYER_MOVEMENT_DELAY, True)

    def input(self, pressed):
        if not self.can_move:
            return

        moved = False

        self.input_x = pressed[pygame.K_RIGHT] - pressed[pygame.K_LEFT]
        self.input_y = pressed[pygame.K_DOWN] - pressed[pygame.K_UP]

        if self.input_x != 0:
            if not self.recent_input_x:
                last_x_temp = self.tile_x
                if self.move(self.input_x, 0):
                    self.last_x = last_x_temp  # only sets last_x to old x if moved is True
                    moved = True

                self.recent_input_x = False
            elif self.input_x == 0:
                self.recent_input_x = True

        if self.input_y != 0 and not moved:
            if not self.recent_input_y:
                last_y_temp = self.tile_y
                if self.move(0, self.input_y):
                    self.last_y = last_y_temp
                    moved = True

                self.recent_input_y = False
            elif self.input_y == 0:
                self.recent_input_y = True

        if moved:
            s = choice(self.steps)
            s.set_volume(c.SFX_VOLUME)
            s.play()

            self.group.add_to_queue(self.group.on_player_move, PLAYER_MOVEMENT_DELAY, self)
            self.can_move = False

    def on_player_move(self, player):
        self.can_move = True


class Enemy(MobileEntity):
    def __init__(self):
        super().__init__()
        self.health = 5
        self.max_health = self.health

        self.surface = pygame.image.load("../assets/player/baddy.png")

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
        chance = 80  # 80% chance of moving toward player
        if randint(1, 100) in [*range(1, chance)]:
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
        else:
            self.particle_manager.add_system(ConfusedEffect(self.x + 60, self.y - 64))


class Potion(Entity):
    sound = pygame.mixer.Sound("../assets/sfx/gulp.wav")
    sound.set_volume(c.SFX_VOLUME)

    def __init__(self):
        super().__init__()
        self.surface = pygame.image.load("../assets/weapons/Potion.png")
        self.intractable = True

    def on_interact(self, entity):
        if not type(entity) is Player:
            return

        entity.health += 3
        if entity.health > entity.max_health:
            entity.health = entity.max_health

        self.sound.play()
        entity.particle_manager.add_system(PotionEffect(self.x + 64, self.y + 64, 3))
        self.on_death()


class Staircase(Entity):
    def __init__(self):
        super().__init__()
        self.surface = pygame.image.load("../assets/tiles/stairs2.png")
        self.intractable = True

    def on_interact(self, entity):
        if not type(entity) is Player:
            return

        self.group.save()
        self.scene_manager.set_scene("loadingScreen", True)


class IceCube(Entity):
    def __init__(self):
        super().__init__()
        self.surface = pygame.image.load("../assets/weapons/icecube2.png")
        self.health = None
        self.lifetime = 9
        self.must_be_attacked_directly = True

        self.serialize("lifetime", lambda: self.lifetime)

    def on_player_move(self, player):
        self.lifetime -= 1

        if self.lifetime < 0:
            self.visible = False
            self.group.add_to_queue(self.on_death, 0)
            return

        self.surface = pygame.image.load(f"../assets/weapons/icecube{self.lifetime // 3}.png")


class Fire(Entity):
    def __init__(self):
        super().__init__()
        self.surface = pygame.image.load("../assets/weapons/Fire.png")
        self.health = 1
        self.must_be_attacked_directly = True

    def attack(self, entity, damage):
        entity.attack(self, 2)
        self.on_death()


class Trap(Entity):
    sound = pygame.mixer.Sound("../assets/sfx/trap.wav")
    sound.set_volume(c.SFX_VOLUME)

    def __init__(self):
        super().__init__()
        self.surface = pygame.image.load("../assets/player/Trap1.png")
        self.can_walk_over = True
        self.health = None
        self.hits = 1
        self.must_be_attacked_directly = True

    def attack(self, entity, damage):
        if type(entity) not in MobileEntity.__subclasses__():
            return

        entity.attack(self, 3)
        self.sound.play()
        self.hits += 1
        if self.hits > 4:
            self.on_death()
            return
        self.surface = pygame.image.load(f"../assets/player/Trap{self.hits}.png")


class HealthUp(Entity):
    sound = pygame.mixer.Sound("../assets/sfx/gulp.wav")
    sound.set_volume(c.SFX_VOLUME)

    def __init__(self):
        super().__init__()
        self.surface = pygame.image.load("../assets/player/HealthUp.png")
        self.intractable = True

    def on_interact(self, entity):
        if not type(entity) is Player:
            return

        entity.max_health += 3
        entity.health = entity.max_health

        self.sound.play()
        entity.particle_manager.add_system(MaxHealthUp(self.x + 64, self.y + 64, 3))
        self.on_death()


class MiniBoss(Enemy):
    def __init__(self):
        super().__init__()
        self.health = 12
        self.max_health = self.health

        self.surface = pygame.image.load("../assets/player/Construct.png")

    def on_death(self):
        self.group.add_entity(HealthUp).set_position(self.tile_x, self.tile_y)

        self.group.remove(self.weapon_visual)
        self.group.remove(self.health_bar)
        self.group.remove(self)


class Rat(Enemy):
    def __init__(self):
        super().__init__()
        self.health = 3
        self.max_health = self.health

        self.surface = pygame.image.load("../assets/player/Rat.png")


class Enemy2(Enemy):
    def __init__(self):
        super().__init__()
        self.health = 8
        self.max_health = self.health

        self.surface = pygame.image.load("../assets/player/corrupt_enemy.png")
