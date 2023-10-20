import os
from scene_manager import Scene, SceneManager
from gui import GuiManager, Guide, Text
from tiles import CHUNK_SIZE
import pygame
import threading
from random import randint
from tiles import TILE_SIZE
from entity_group import EntityGroup
from entity import *
from tiles import Chunk

# coordinates for the player starting position
global x
global y


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
        Sets the starting square for the player. Must be run after generating dungeon
        :return: the starting squares x and y coordinates
        """
        for tile_y in range(len(self.level)):
            for tile_x in range(len(self.level[tile_y])):
                if self.level[tile_y][tile_x] == 1:
                    self.level[tile_y][tile_x] = 2
                    return tile_x, tile_y

    def set_wall_top_tiles(self):
        """
        Sets the wall top tile positions
        :return: nothing
        """
        for tile_y in range(len(self.level)):
            for tile_x in range(len(self.level[tile_y])):
                if tile_y != len(self.level) - 1:
                    if self.level[tile_y][tile_x] == 0 and self.level[tile_y + 1][tile_x]:
                        self.level[tile_y][tile_x] = 4
                        self.level[tile_y + 1][tile_x] = 3


class LoadingScreen(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "loadingScreen")

        self.guiManager = GuiManager(self.sceneManager.screen)

        self.center = self.guiManager.add_guideline(
            Guide("center", None, Guide.GL_VERTICAL, 0.5, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 0))
        self.loading_text = self.center.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))

        self.completion_event = None

    def on_scene_start(self, new):
        self.completion_event = threading.Event()

        if new:
            second_thread = threading.Thread(target=generate_dungeon, args=(CHUNK_SIZE, self.completion_event, self.sceneManager))
            second_thread.start()
        else:
            self.sceneManager.set_scene("game", True)

    def update(self, dt):
        if self.completion_event.is_set():
            self.sceneManager.set_scene("game", False)

            # Set the starting positions
            self.sceneManager.scene.start_x = x
            self.sceneManager.scene.start_y = y
            self.sceneManager.scene.on_scene_start(False)

        self.loading_text.set_value(f"Loading{'.' * randint(3, 9)}")

    def render(self, screen: pygame.Surface):
        self.screen.fill((0, 0, 0))
        self.guiManager.render_guidelines()


def generate_dungeon(chunk_size, event, scene_manager):
    global x
    global y
    # Delete current world
    dir_name = "../assets/world"
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".txt"):
            os.remove(os.path.join(dir_name, item))

    width = 10
    height = 10

    dungeon = DrunkGeneration(height * CHUNK_SIZE, width * chunk_size, 600, 3)
    dungeon.generate_level()
    x, y = dungeon.set_starting_square()
    dungeon.set_wall_top_tiles()
    world = dungeon.level

    group = EntityGroup(None, None, None, TILE_SIZE)
    group.add_entity(Player).set_position(x, y)

    while True:
        r_x = randint(0, width * chunk_size - 1)
        r_y = randint(0, height * chunk_size - 1)
        if not Chunk.tile_data[world[r_y][r_x]].collider:
            group.add_entity(Staircase).set_position(r_x, r_y)
            break

    i = 0
    while i < 10:
        r_x = randint(0, width * chunk_size - 1)
        r_y = randint(0, height * chunk_size - 1)
        if not Chunk.tile_data[world[r_y][r_x]].collider:
            group.add_entity(Chest).set_position(r_x, r_y)
            i += 1

    i = 0
    while i < 60:
        r_x = randint(0, width * chunk_size - 1)
        r_y = randint(0, height * chunk_size - 1)
        if not Chunk.tile_data[world[r_y][r_x]].collider:
            group.add_entity(Enemy).set_position(r_x, r_y)
            i += 1

    group.save()

    # --------------------- REPLACE ABOVE --------------------- #

    # Save chunks to files
    for h in range(height):
        for w in range(width):
            with open(f"../assets/world/chunk_{w}_{h}.txt", "x") as f:
                for i in range(chunk_size):
                    row = world[(h * chunk_size) + i][(chunk_size * w):(chunk_size * (w + 1))]
                    for c, li in enumerate(list(map(str, row))):
                        if c != 0:
                            f.write(", ")
                        f.write(f"{li}")
                    f.write("\n")

    event.set()
    return
