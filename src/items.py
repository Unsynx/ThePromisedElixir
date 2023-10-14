UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


class Range:
    ATTACK = 1
    CENTER = 2
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def __init__(self, pattern):
        self.pattern = pattern
        self.center_x, self.center_y = self.get_pattern_center()

    def get_pattern_center(self):
        for y in range(len(self.pattern)):
            for x in range(len(self.pattern[0])):
                if self.pattern[y][x] == self.CENTER:
                    return x, y

    def in_range(self, x1, y1, x2, y2):
        dy = y2 - y1
        dx = x2 - x1

        return self.pattern[self.center_y + dy][self.center_x + dx] == 1

    def get_list_of_positions(self, attack_dir):
        lis = []
        for y in range(len(self.pattern)):
            for x in range(len(self.pattern[0])):
                if self.pattern[y][x] == self.ATTACK:
                    match attack_dir:
                        case self.RIGHT:
                            lis.append([self.center_x + x, self.center_y + y])
                        case self.LEFT:
                            lis.append([self.center_x - x, self.center_y + y])
                        case self.UP:
                            lis.append([self.center_y + y, self.center_x + x])
                        case self.DOWN:
                            lis.append([self.center_y - y, self.center_x + x])
        return lis

    def get_hit_enemies(self, player_x, player_y, attack_dir, group):
        lis = []
        for pos in self.get_list_of_positions(attack_dir):
            e = group.get_entity_at(player_x + pos[0], player_y + pos[1])
            if e is not None:
                lis.append(e)

        return lis


class Attack:
    def __init__(self, damage: int, attack_range: Range, effect):
        self.damage = damage
        self.attack_range = attack_range
        self.effect = effect


class Weapon:
    def __init__(self, icon_path: str, normal_attack: Attack, special_attack: Attack):
        self.name = type(self).__name__
        self.icon_path = icon_path
        self.special_attack = special_attack
        self.normal_attack = normal_attack

    def attack(self, player_x, player_y, attack_dir, group):
        enemies = self.normal_attack.attack_range.get_hit_enemies(player_x, player_y, attack_dir, group)

        for e in enemies:
            e.attack(self.normal_attack.damage)


class DoubleReach(Range):
    def __init__(self):
        super().__init__([
            [2, 1, 1]
        ])


class SpearNormalAttack(Attack):
    def __init__(self):
        super().__init__(2, DoubleReach(), None)


class SimpleSpearWeapon(Weapon):
    def __init__(self):
        super().__init__(None, SpearNormalAttack(), None)
