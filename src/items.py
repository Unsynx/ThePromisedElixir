import constants as c


class Range:
    ATTACK = 1
    CENTER = 2

    def __init__(self, pattern):
        self.pattern = pattern
        self.center_x, self.center_y = self.get_pattern_center()

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


class Attack:
    def __init__(self, damage: int, attack_range: Range, effect=None):
        self.damage = damage
        self.attack_range = attack_range
        self.effect = effect


class Weapon:
    def __init__(self, icon_path: str, normal_attack: Attack, special_attack=None):
        self.name = type(self).__name__
        self.icon_path = icon_path
        self.special_attack = special_attack
        self.normal_attack = normal_attack

    def __get__(self, instance, owner):
        return self.name

    def for_non_hit(self, not_hit_positions, group):
        pass

    def attack(self, player_x, player_y, attack_dir, group):
        hit_enemies, not_hit_positions = self.normal_attack.attack_range.get_hit_enemies(player_x, player_y, attack_dir, group)

        for e in hit_enemies:
            if not e.intractable:
                e.attack(self.normal_attack.damage)

        self.for_non_hit(not_hit_positions, group)


class DoubleReach(Range):
    def __init__(self):
        super().__init__([
            [2, 1, 1]
        ])


class NormalReach(Range):
    def __init__(self):
        super().__init__([
            [2, 1]
        ])


class SpearNormalAttack(Attack):
    def __init__(self):
        super().__init__(2, DoubleReach())


class Fists(Attack):
    def __init__(self):
        super().__init__(1, NormalReach())


class SimpleSpearWeapon(Weapon):
    def __init__(self):
        super().__init__("", SpearNormalAttack())


class StarReach(Range):
    def __init__(self):
        super().__init__([
            [0, 0, 1, 0],
            [2, 1, 1, 1],
            [0, 0, 1, 0]
        ])


class BigAttack(Attack):
    def __init__(self):
        super().__init__(5, StarReach())


class FunnyExplosion(Weapon):
    def __init__(self):
        super().__init__("", BigAttack())


class NoWeapon(Weapon):
    def __init__(self):
        super().__init__("", Fists())

