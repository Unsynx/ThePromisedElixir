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
        self.icon_path = icon_path
        self.damage = damage
        self.pattern = pattern
        self.center_x, self.center_y = self.get_pattern_center()

        self.offset_x = 0
        self.offset_y = 0

        self.effect_excluded = []

    def get_pattern_center(self):
        for y in range(len(self.pattern)):
            for x in range(len(self.pattern[0])):
                if self.pattern[y][x] == self.CENTER:
                    return x, y

    def get_hit_enemies(self, player_x, player_y, attack_dir, group):
        print(self.center_x, self.center_y)
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
            e = group.get_entity_at(player_x + pos[0], player_y + pos[1])
            if e is None:
                not_hit_positions.append([pos[0] + player_x, pos[1] + player_y])
            else:
                enemies.append(e)

        return enemies, not_hit_positions

    def for_non_hit(self, not_hit_positions, group):
        pass

    def attack(self, player_x, player_y, attack_dir, group, target):
        hit_enemies, not_hit_positions = self.get_hit_enemies(player_x, player_y, attack_dir, group)

        for e in hit_enemies:
            if not e.intractable:
                # Cannot attack all the effects you spawned in
                if type(e) not in self.effect_excluded or e is target:
                    e.attack(group.get_entity_at(player_x, player_y), self.damage)

        # No infinite IceCubes
        if type(target) not in self.effect_excluded:
            self.for_non_hit(not_hit_positions, group)

    def effect(self, effect_entity, positions, group):
        for pos in positions:
            _, collider = group.tile_manager.get_tile(pos[0], pos[1])
            if not collider:
                group.add_entity(effect_entity).set_position(pos[0], pos[1])


class SimpleSpearWeapon(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/spear.png", 2, R_STAR)
        self.offset_x = 25


class IceWand(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/ice_staff.png", 5, R_SHIELD)
        from entity import IceCube
        self.effect_excluded.append(IceCube)
        self.offset_x = 50

    def for_non_hit(self, not_hit_positions, group):
        from entity import IceCube
        self.effect(IceCube, not_hit_positions, group)


class NoWeapon(Weapon):
    def __init__(self):
        super().__init__(None, 1, R_FRONT)


class FireKnife(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/flaming_knife.png", 3, R_SWIRL)
        self.offset_x = 50
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

    def for_non_hit(self, not_hit_positions, group):
        from entity import Fire
        self.effect(Fire, not_hit_positions, group)


class MorningStar(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/Morningstar.png", 3, R_SWIRL)
        self.offset_x = 80


class Knife(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/knife.png", 3, R_FRONT)
        self.offset_x = 20


class Sword(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/sword.png", 3, R_DOUBLE)
        self.offset_x = 50


class FlameStaff(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/fire_staff.png", 5, R_SHIELD)
        from entity import Fire
        self.effect_excluded.append(Fire)
        self.offset_x = 50

    def for_non_hit(self, not_hit_positions, group):
        from entity import Fire
        self.effect(Fire, not_hit_positions, group)


class Sabre(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/miles_mighty_sword.png", 3, R_SWIPE)
        self.offset_x = 60
