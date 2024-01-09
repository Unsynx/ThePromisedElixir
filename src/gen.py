import copy
import random
import threading
import os
import math

import src.dialogue
from scene_manager import Scene, SceneManager
from gui import GuiManager, Guide, Text
from tiles import TILE_SIZE, TILE_DATA, CHUNK_SIZE
from entity import *
from chests import Chest, Loot
from dialogue import Dialogue
from entity_group import EntityGroup
from game import GameScene


class DrunkGeneration:
    def __init__(self, height: int, width: int, wall_countdown: int, padding: int):
        """
        Class to generate a random dungeon
        :param height: height of the dungeon in tiles
        :param width: width of the dungeon in tiles
        :param wall_countdown: how many tiles should be walkable
        :param padding: how many tiles to leave on each edge of the dungeon
        """
        self.height = height
        self.width = width
        self.wall_countdown = wall_countdown
        self.padding = padding

        self.x = int(self.width / 2)
        self.y = int(self.height / 2)

        self.level = [self._get_level_row() for _ in range(self.height)]

    def _get_level_row(self):
        return [0] * self.width

    def generate_level(self):
        """
        Generates a dungeon level with the initiated parameters
        :return: nothing
        """
        while self.wall_countdown >= 0:
            if self.level[self.y][self.x] == 0:
                self.level[self.y][self.x] = 1
                self.wall_countdown -= 1

            roll = randint(1, 4)
            if roll == 1 and self.x > self.padding:  # left
                self.x -= 1
            if roll == 2 and self.x < self.width - 1 - self.padding:  # right
                self.x += 1
            if roll == 3 and self.y > self.padding:  # up
                self.y -= 1
            if roll == 4 and self.y < self.height - 1 - self.padding:  # down
                self.y += 1

    def set_starting_square(self):
        """
        Sets the starting square for the player_only. Must be run after generating dungeon
        :return: the starting squares x and y coordinates
        """
        for tile_y in range(len(self.level)):
            for tile_x in range(len(self.level[tile_y])):
                if self.level[tile_y][tile_x] == 1:
                    return tile_x, tile_y

    def set_wall_top_tiles(self):
        duplicate = copy.deepcopy(self.level)
        """
        Sets the wall top tile positions
        :return: nothing
        """
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                if y != len(self.level) - 1 and x != len(self.level[0]) - 1:
                    if not self.level[y][x] == 0:
                        continue

                    # The most evil match case statement ever written
                    match (self.level[y - 1][x], self.level[y + 1][x], self.level[y][x - 1], self.level[y][x + 1]):
                        # Above, Below, Left, Right
                        # 1 - Ground
                        # 0 - Wall
                        case (1, 1, 1, 1):
                            # Center, capped
                            duplicate[y][x] = 14
                            duplicate[y + 1][x] = 4
                        case (0, 1, 1, 1):
                            # Center, extended
                            duplicate[y][x] = 9
                            duplicate[y + 1][x] = 4
                        case (0, 1, 0, 0):
                            # Continuous
                            duplicate[y][x] = 8
                            duplicate[y + 1][x] = 3
                        case (1, 1, 0, 0):
                            # Continuous topped
                            duplicate[y][x] = 7
                            duplicate[y + 1][x] = 3
                        case (0, 1, 0, 1):
                            # Right corner
                            duplicate[y][x] = 11
                            duplicate[y + 1][x] = 6
                        case (1, 1, 0, 1):
                            # Right corner topped
                            duplicate[y][x] = 13
                            duplicate[y + 1][x] = 6
                        case (1, 1, 0, 0):
                            # Continuous topped
                            duplicate[y][x] = 7
                            duplicate[y + 1][x] = 3
                        case (0, 1, 1, 0):
                            # Left corner
                            duplicate[y][x] = 10
                            duplicate[y + 1][x] = 5
                        case (1, 1, 1, 0):
                            # Left corner topped
                            duplicate[y][x] = 12
                            duplicate[y + 1][x] = 5
                        case (1, 0, 0, 0):
                            # Back continuous
                            duplicate[y][x] = 15
                        case (0, 0, 1, 1):
                            # Back extension
                            duplicate[y][x] = 16
                        case (0, 0, 0, 1):
                            # Back Rightfacing wall
                            duplicate[y][x] = 17
                        case (0, 0, 1, 0):
                            # Back left facing wall
                            duplicate[y][x] = 18
                        case (1, 0, 0, 1):
                            # Back left corner
                            duplicate[y][x] = 19
                        case (1, 0, 1, 0):
                            # Back right corner
                            duplicate[y][x] = 20
                        case (1, 0, 1, 1):
                            # Back cap
                            duplicate[y][x] = 21

        self.level = duplicate

        for y in range(len(self.level)):
            for x in range(len(self.level[0])):
                if randint(0, 8) == 1 and duplicate[y][x] == 1:
                    if randint(0, 5) == 0:
                        duplicate[y][x] = 23
                    else:
                        duplicate[y][x] = 22

        self.level = duplicate


class LoadingScreen(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "loadingScreen")

        self.guiManager = GuiManager(self.sceneManager.screen)

        self.center = self.guiManager.add_guideline(
            Guide("center", None, Guide.GL_VERTICAL, 0.5, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 0))
        self.loading_text = self.center.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))

        self.completion_event = None
        self.level = 0

    def on_scene_start(self, new, restart=False):
        if not new:
            self.sceneManager.set_scene("game", True)

        if restart:
            self.level = 0
        else:
            if self.level == 0:
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.load("../assets/music/ambience_cave_00.ogg")
                pygame.mixer.music.set_volume(c.MUSIC_VOLUME)
                pygame.mixer.music.play(-1)

        self.level += 1
        self.sceneManager.del_scene("game")
        self.sceneManager.add_scene(GameScene(self.sceneManager, self.level))
        self.completion_event = threading.Event()
        second_thread = threading.Thread(target=generate_dungeon, args=(CHUNK_SIZE, self.completion_event, self.level))
        second_thread.start()

    def update(self, dt):
        if self.completion_event.is_set():
            self.sceneManager.set_scene("game", True)

        self.loading_text.set_value(f"Loading{'.' * randint(3, 9)}")

    def render(self, screen: pygame.Surface):
        self.screen.fill((0, 0, 0))
        self.guiManager.render_guidelines()


class EntitySpawner:
    def __init__(self, width, height, chunk_size, group, world):
        self.width = width
        self.height = height
        self.chunk_size = chunk_size
        self.group = group
        self.world = world

    def spawn_entity(self, entity, count, can_spawn_on_other=False, neighbors=0, specific_spawn_tile=None):
        spawn_tile = []
        if specific_spawn_tile is not None:
            if type(specific_spawn_tile) is str:
                spawn_tile.append(specific_spawn_tile)
            else:
                spawn_tile.extend(specific_spawn_tile)

        print(spawn_tile)

        entities = []
        i = 0
        while i < count:
            r_x = randint(0, self.width * self.chunk_size - 1)
            r_y = randint(0, self.height * self.chunk_size - 1)

            if not TILE_DATA[self.world[r_y][r_x]].collider:
                if not can_spawn_on_other and self.group.get_entity_at(r_x, r_y) is not None:
                    continue
                if specific_spawn_tile is not None:
                    if TILE_DATA[self.world[r_y][r_x]].name not in spawn_tile:
                        continue

                e = self.group.add_entity(entity).set_position(r_x, r_y)
                entities.append(e)
                i += 1

                j = 0
                while j < neighbors:
                    if randint(0, 1) == 0:
                        r_x += 1
                    else:
                        r_y += 1
                    try:
                        if not TILE_DATA[self.world[r_y][r_x]].collider:
                            if not can_spawn_on_other and self.group.get_entity_at(r_x, r_y) is not None:
                                continue
                            if specific_spawn_tile is not None:
                                if TILE_DATA[self.world[r_y][r_x]].name not in spawn_tile:
                                    continue

                            e = self.group.add_entity(entity).set_position(r_x, r_y)
                            entities.append(e)

                            j += 1
                    except IndexError:
                        j = neighbors

        return entities


def generate_dungeon(chunk_size, event, level):
    # Delete current world
    dir_name = "../assets/world"
    for item in os.listdir(dir_name):
        if item.endswith(".txt"):
            os.remove(os.path.join(dir_name, item))

    # Level size
    match level:
        case 1:
            width = 3
            height = 3

        case _:
            width = min(10, level + 3)
            height = min(10, level + 3)

    dungeon = DrunkGeneration(height * CHUNK_SIZE, width * CHUNK_SIZE, int((4/6)*width*height*CHUNK_SIZE), 3)
    dungeon.generate_level()
    x, y = dungeon.set_starting_square()
    dungeon.set_wall_top_tiles()
    world = dungeon.level

    group = EntityGroup(None, None, None, None, None, TILE_SIZE)

    spawner = EntitySpawner(width, height, chunk_size, group, world)

    if level == 1:
        group.add_entity(Player).set_position(x, y)
    else:
        group.load(True)
        group[0].set_position(x, y)

    # Staircase
    spawner.spawn_entity(Staircase, 1, specific_spawn_tile="ground")

    # Chests
    match level:
        case 1:
            n = 1
        case 2:
            n = 2
        case 3:
            n = 2
        case 4:
            n = 4
        case _:
            n = min(math.floor(level * 1.25), 10)
    chest = spawner.spawn_entity(Chest, n)
    for e in chest:
        e.set_floor(level)

    # ------------------------- Enemies -------------------------
    # tier 1
    match level:
        case 1:
            n = 0
        case 2:
            n = 0
        case 3:
            n = 1
        case 4:
            n = 4
        case _:
            n = min(math.floor(level * 1.5), 12)

    enemies = spawner.spawn_entity(Enemy, n)
    loot = Loot()
    for e in enemies:
        if randint(0, 10) < level - 3:
            e.set_weapon(loot.get_weapon(level, 3))

    # Rats
    match level:
        case 2:
            spawner.spawn_entity(Rat, 1, neighbors=1)
        case 3:
            spawner.spawn_entity(Rat, 1, neighbors=2)
        case _:
            if level > 9:
                spawner.spawn_entity(Rat, 3, neighbors=2)

    # mini boss
    if level % 5 == 0:
        spawner.spawn_entity(MiniBoss, 1)

    # tier 2
    if level > 12:
        n = min(math.floor((level - 12) * 2), 12)

        enemies = spawner.spawn_entity(Enemy2, n)
        loot = Loot()
        for e in enemies:
            if randint(0, 10) < level - 9:
                e.set_weapon(loot.get_weapon(level, 9))

    # ------------------------------------------------------------
    # Traps
    if level > 5:
        spawner.spawn_entity(Trap, min(10, (level - 5) * 2), neighbors=2,
                             specific_spawn_tile=["ground", "ground2", "ground3"])

    if level in c.DIALOGUE.keys():
        book = spawner.spawn_entity(Dialogue, 1)
        book[0].set_dialogue_number(level)


    spawner.spawn_entity(Potion, max(0, min(math.floor((level - 2) * 1.25), 5)))

    group.save()

    # --------------------- REPLACE ABOVE --------------------- #

    # Save chunks to files
    for h in range(height):
        for w in range(width):
            with open(f"../assets/world/chunk_{w}_{h}.txt", "x") as f:
                for i in range(chunk_size):
                    row = world[(h * chunk_size) + i][(chunk_size * w):(chunk_size * (w + 1))]
                    for c1, li in enumerate(list(map(str, row))):
                        if c1 != 0:
                            f.write(", ")
                        f.write(f"{li}")
                    f.write("\n")

    event.set()
    return

"""
loot = Loot()
for i in range(25):
    tier0 = 0
    tier1 = 0
    tier2 = 0
    tier3 = 0
    tier4 = 0
    for j in range(100):
        w = loot.get_weapon(i + 1)
        match w.tier:
            case c.TIER_0:
                tier0 += 1
            case c.TIER_1:
                tier1 += 1
            case c.TIER_2:
                tier2 += 1
            case c.TIER_3:
                tier3 += 1
            case c.TIER_4:
                tier4 += 1

    print(f"Floor {i+1}: {tier0} Tier0, {tier1} Tier1, {tier2} Tier2, {tier3} Tier3, {tier4} Tier4")
"""

"""
loot = Loot()
for w in loot.tier0_weapons:
    w = w()
    print(f"tier0 {w.name}, {w.damage}dmg")
for w in loot.tier1_weapons:
    w = w()
    print(f"tier1 {w.name}, {w.damage}dmg")
for w in loot.tier2_weapons:
    w = w()
    print(f"tier2 {w.name}, {w.damage}dmg")
for w in loot.tier3_weapons:
    w = w()
    print(f"tier3 {w.name}, {w.damage}dmg")
for w in loot.tier4_weapons:
    w = w()
    print(f"tier4 {w.name}, {w.damage}dmg")
"""
