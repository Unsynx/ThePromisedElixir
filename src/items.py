import pygame.mixer
import constants as c


R_FRONT = [[2, 1]]
R_STAR = [[0, 0, 1, 0],
          [2, 1, 1, 1],
          [0, 0, 1, 0]]
R_SHIELD = [[1, 1, 0],
            [0, 1, 1],
            [2, 1, 1],
            [0, 1, 1],
            [1, 1, 0]]
R_DOUBLE = [[2, 1, 1]]
R_LONG = [[0, 1, 0, 0],
          [2, 1, 1, 1],
          [0, 1, 0, 0]]
R_SWIRL = [[1, 1, 1],
          [1, 2, 1],
          [1, 1, 1]]
R_MUKE = [[0, 0, 1, 1, 1, 0, 0],
          [0, 1, 1, 1, 1, 1, 0],
          [1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 2, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1],
          [0, 1, 1, 1, 1, 1, 0],
          [0, 0, 1, 1, 1, 0, 0]]
R_SWIPE = [[0, 1],
           [2, 1],
           [0, 1]]


class Weapon:
    ATTACK = 1
    CENTER = 2

    def __init__(self, icon_path: str, damage: int, pattern):
        self.name = type(self).__name__
        self.pretty_name = ""
        i = 0
        for le in self.name:
            if le.isupper() and i != 0:
                self.pretty_name += " "
            self.pretty_name += le
            i += 1

        self.icon_path = icon_path
        self.damage = damage
        self.pattern = pattern
        self.center_x, self.center_y = self.get_pattern_center()
        self.sound_path = "../assets/sfx/attack.wav"

        self.tier = None

        self.offset_x = 0
        self.offset_y = 0

        self.effect_excluded = []

    def get_pattern_center(self):
        for y in range(len(self.pattern)):
            for x in range(len(self.pattern[0])):
                if self.pattern[y][x] == self.CENTER:
                    return x, y

    def get_hit_enemies(self, player_x, player_y, attack_dir, group):
        hit_positions = []
        for y in range(len(self.pattern)):
            for x in range(len(self.pattern[0])):
                if self.pattern[y][x] == self.ATTACK:
                    match attack_dir:
                        case c.RIGHT:
                            hit_positions.append([x - self.center_x, self.center_y - y])
                        case c.LEFT:
                            hit_positions.append([self.center_x - x, self.center_y - y])
                        case c.UP:
                            hit_positions.append([self.center_y - y, self.center_x - x])
                        case c.DOWN:
                            hit_positions.append([self.center_y - y, x - self.center_x])

        enemies = []
        not_hit_positions = []
        for pos in hit_positions:
            e = group.get_entity_at(player_x + pos[0], player_y + pos[1], True)
            if len(e) == 0:
                not_hit_positions.append([pos[0] + player_x, pos[1] + player_y])
            else:
                enemies.extend(e)

        return enemies, not_hit_positions

    def for_non_hit(self, not_hit_positions, group):
        pass

    def attack(self, player_x, player_y, attack_dir, group, target):
        # Sound
        from entity import Player
        if type(group.get_entity_at(player_x, player_y)) == Player:
            s = pygame.mixer.Sound(self.sound_path)
            s.set_volume(c.SFX_VOLUME)
            s.play()

        # logic
        hit_enemies, not_hit_positions = self.get_hit_enemies(player_x, player_y, attack_dir, group)

        x = target.tile_x
        y = target.tile_y

        entities = group.get_entity_at(x, y, return_all=True)
        # Checks if multiple entities on attacked position
        if len(entities) > 1:
            from entity import Trap
            for e in entities:
                if type(e) == Trap:
                    hit_enemies.remove(e)
                    print("removed trap")
        else:
            from entity import Trap
            print(f"Attacking one enemy. {entities}")
            if type(entities[0]) == Trap:
                print(f"{entities} is trap")
                # don't attack anything but trap when stepping on trap
                not_hit_positions = []
                hit_enemies = entities

        # No infinite IceCubes
        if type(target) not in self.effect_excluded:
            print(f"effect {not_hit_positions}")
            self.for_non_hit(not_hit_positions, group)

        # attack all hit enemies
        attacker = group.get_entity_at(player_x, player_y)
        for e in hit_enemies:
            if e != target and e.must_be_attacked_directly:
                continue

            e.attack(attacker, self.damage)

    def effect(self, effect_entity, positions, group):
        for pos in positions:
            _, collider = group.tile_manager.get_tile(pos[0], pos[1])
            if not collider:
                group.add_entity(effect_entity).set_position(pos[0], pos[1])


class SimpleSpear(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/spear.png", 2, R_DOUBLE)
        self.offset_x = 25
        self.tier = c.TIER_0


class IceWand(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/ice_staff.png", 5, R_SHIELD)
        from entity import IceCube
        self.effect_excluded.append(IceCube)
        self.offset_x = 50
        self.tier = c.TIER_3

    def for_non_hit(self, not_hit_positions, group):
        from entity import IceCube
        self.effect(IceCube, not_hit_positions, group)


class NoWeapon(Weapon):
    def __init__(self):
        super().__init__(None, 1, R_FRONT)
        self.sound_path = "../assets/sfx/punch.wav"


class FireKnife(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/flaming_knife.png", 3, R_SWIPE)
        self.offset_x = 50
        self.tier = c.TIER_1

        from entity import Fire
        self.effect_excluded.append(Fire)

    def for_non_hit(self, not_hit_positions, group):
        from entity import Fire
        self.effect(Fire, not_hit_positions, group)


class MilesMuke(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/MassiveMuke.png", 100, R_MUKE)
        from entity import Fire
        self.effect_excluded.append(Fire)
        self.offset_y = -100
        self.offset_x = -10
        self.tier = c.TIER_4

    def for_non_hit(self, not_hit_positions, group):
        from entity import Fire
        self.effect(Fire, not_hit_positions, group)


class MorningStar(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/Morningstar.png", 3, R_SWIRL)
        self.offset_x = 80
        self.tier = c.TIER_1


class Knife(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/knife.png", 2, R_FRONT)
        self.tier = c.TIER_0
        self.offset_x = 20


class Sword(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/sword.png", 3, R_DOUBLE)
        self.tier = c.TIER_0
        self.offset_x = 50


class FlameStaff(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/fire_staff.png", 4, R_SHIELD)
        from entity import Fire
        self.effect_excluded.append(Fire)
        self.offset_x = 50
        self.tier = c.TIER_2

    def for_non_hit(self, not_hit_positions, group):
        from entity import Fire
        self.effect(Fire, not_hit_positions, group)


class Sabre(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/miles_mighty_sword.png", 3, R_SWIPE)
        self.offset_x = 60
        self.tier = c.TIER_1


class Hammer(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/Hammer.png", 4, R_STAR)
        self.offset_x = 45
        self.tier = c.TIER_1


class Icicle(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/Iceicle.png", 3, R_DOUBLE)
        self.offset_x = 35
        self.tier = c.TIER_1

        from entity import IceCube
        self.effect_excluded.append(IceCube)

    def for_non_hit(self, not_hit_positions, group):
        from entity import IceCube
        self.effect(IceCube, not_hit_positions, group)


class LargeAxe(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/LargeAxe.png", 4, R_SWIRL)
        self.offset_x = 55
        self.tier = c.TIER_2


class LooseSpear(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/LooseSpear.png", 5, R_LONG)
        self.offset_x = 55
        self.tier = c.TIER_2


class RustyAxe(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/RustyAxe.png", 5, R_FRONT)
        self.offset_x = 55
        self.tier = c.TIER_1


class SpectreBlade(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/SpectreBlade.png", 7, R_SWIPE)
        self.offset_x = 45
        self.tier = c.TIER_3


class WoodenClub(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/WoodenClub.png", 5, R_STAR)
        self.offset_x = 65
        self.tier = c.TIER_2


class FirePolearm(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/FirePolarm.png", 4, R_LONG)
        self.offset_x = 45
        self.tier = c.TIER_2

        from entity import Fire
        self.effect_excluded.append(Fire)

    def for_non_hit(self, not_hit_positions, group):
        from entity import Fire
        self.effect(Fire, not_hit_positions, group)


class FireKatana(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/FireKatana.png", 7, R_SWIPE)
        self.offset_x = 45
        self.offset_y = -10
        self.tier = c.TIER_3

        from entity import Fire
        self.effect_excluded.append(Fire)

    def for_non_hit(self, not_hit_positions, group):
        from entity import Fire
        self.effect(Fire, not_hit_positions, group)
