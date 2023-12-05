import constants as c


R_FRONT = [[2, 1]]
R_STAR = [[0, 0, 1, 0],
          [2, 1, 1, 1],
          [0, 0, 1, 0]]
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

    # todo: Attack rotation is not working for some reason
    def get_hit_enemies(self, player_x, player_y, attack_dir, group):
        hit_positions = []
        for y in range(len(self.pattern)):
            for x in range(len(self.pattern[0])):
                if self.pattern[y][x] == self.ATTACK:
                    match attack_dir:
                        case c.RIGHT:
                            hit_positions.append([self.center_x + x, self.center_y - y])
                        case c.LEFT:
                            hit_positions.append([self.center_x - x, self.center_y - y])
                        case c.UP:
                            hit_positions.append([self.center_y - y, self.center_x - x])
                        case c.DOWN:
                            hit_positions.append([self.center_y - y, self.center_x + x])

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
                e.attack(self.damage)

        if type(target) not in self.effect_excluded:
            self.for_non_hit(not_hit_positions, group)


class SimpleSpearWeapon(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/spear.png", 2, R_DOUBLE)
        self.offset_x = 25


class IceWand(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/ice_staff.png", 5, R_STAR)
        from entity import IceCube
        self.effect_excluded.append(IceCube)
        self.offset_x = 50

    def for_non_hit(self, not_hit_positions, group):
        from entity import IceCube
        for pos in not_hit_positions:
            group.add_entity(IceCube).set_position(pos[0], pos[1])


class NoWeapon(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/sword.png", 1, R_FRONT)
        self.offset_x = 50


class FireKnife(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/flaming_knife.png", 3, R_SWIRL)
        self.offset_x = 50


class MilesMuke(Weapon):
    def __init__(self):
        super().__init__("../assets/weapons/MassiveMuke.png", 100, R_MUKE)
        from entity import IceCube
        self.effect_excluded.append(IceCube)
        self.offset_y = -100
        self.offset_x = -10

    def for_non_hit(self, not_hit_positions, group):
        from entity import IceCube
        for pos in not_hit_positions:
            group.add_entity(IceCube).set_position(pos[0], pos[1])
