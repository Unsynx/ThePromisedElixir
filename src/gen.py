import os
from scene_manager import Scene, SceneManager
from gui import GuiManager, Guide, Text
from tiles import CHUNK_SIZE
import pygame
import threading
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
        return ['0'] * self.width

    def generate_level(self):
        while self.wall_countdown >= 0:
            if self.level[self.y][self.x] == '1':
                self.level[self.y][self.x] = '0'
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


class LoadingScreen(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "loadingScreen")

        self.guiManager = GuiManager(self.sceneManager.screen)

        self.center = self.guiManager.add_guideline(
            Guide("center", None, Guide.GL_VERTICAL, 0.5, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 0))
        self.loading_text = self.center.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))

        self.completion_event = threading.Event()

    def on_scene_start(self):
        second_thread = threading.Thread(target=generate_dungeon, args=(CHUNK_SIZE, self.completion_event))
        second_thread.start()

    def update(self, dt):
        if self.completion_event.is_set():
            # set starting positions
            self.sceneManager.sceneDict["game"].start_x = 10
            self.sceneManager.sceneDict["game"].start_y = 10

            self.sceneManager.set_scene("game")

        self.loading_text.set_value(f"Loading{'.' * randint(3, 9)}")

    def render(self, screen: pygame.Surface):
        self.screen.fill((0, 0, 0))
        self.guiManager.render_guidelines()


def generate_dungeon(chunk_size, event):
    # Delete current world
    dir_name = "../assets/world"
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".txt"):
            os.remove(os.path.join(dir_name, item))

    # --------------------- REPLACE BELOW --------------------- #
    width = 10
    height = 10
    dungeon = DrunkGeneration(height * CHUNK_SIZE, width * chunk_size, 600, 3)
    dungeon.generate_level()

    # Create world

    world = dungeon.level

    # World gen
    start_x = randint(0, width * CHUNK_SIZE - 1)
    start_y = randint(0, height * CHUNK_SIZE - 1)
    world[start_y][start_x] = 2

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
