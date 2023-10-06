from random import randint


class DrunkGeneration:
    def __init__(self, height: int, width: int, wall_countdown: int, padding: int):
        self.height = height
        self.width = width
        self.wall_countdown = wall_countdown
        self.padding = padding

        self.x = int(self.width / 2)
        self.y = int(self.height / 2)

        self.level = [self._get_level_row() for _ in range(self.height)]

    def _get_level_row(self):
        return ['#'] * self.width

    def generate_level(self):
        while self.wall_countdown >= 0:
            if self.level[self.y][self.x] == '#':
                self.level[self.y][self.x] = ' '
                self.wall_countdown -= 1

            roll = randint(1, 4)

            if roll == 1 and self.x > self.padding:
                self.x -= 1
            if roll == 2 and self.x < self.width - 1 - self.padding:
                self.x += 1
            if roll == 3 and self.y > self.padding:
                self.y -= 1
            if roll == 4 and self.y < self.height - 1 - self.padding:
                self.y += 1

    def get_level(self):
        for row in self.level:
            print(''.join(row))


dungeon = DrunkGeneration(55, 55, 600, 3)
dungeon.generate_level()
dungeon.get_level()
