import os
from scene_manager import Scene, SceneManager
from gui import GuiManager, Guide, Text
from tiles import CHUNK_SIZE
import pygame
import threading

from random import randint


class LoadingScreen(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "loadingScreen")

        self.guiManager = GuiManager(self.sceneManager.screen)

        self.center = self.guiManager.add_guideline(Guide("center", None, Guide.GL_VERTICAL, 0.5, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 0))
        self.loading_text = self.center.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))

        self.completion_event = threading.Event()

    def on_scene_start(self):
        second_thread = threading.Thread(target=generate_dungeon, args=(CHUNK_SIZE, self.completion_event))
        second_thread.start()

    def update(self, dt):
        if self.completion_event.is_set():
            self.sceneManager.set_scene("game")

            # Set the starting positions
            self.sceneManager.scene.start_x = 10
            self.sceneManager.scene.start_y = 10
            self.sceneManager.scene.on_scene_start()

        self.loading_text.set_value(f"Loading{'.'*randint(3, 9)}")

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

    # Create world
    # --------------------- REPLACE BELOW --------------------- #
    width = 100
    height = 100

    world = []
    for y in range(height * chunk_size):
        row = []
        for x in range(width * chunk_size):
            row.append(randint(0, 1))
        world.append(row)

    # World gen
    start_x = randint(0, height*chunk_size-1)
    start_y = randint(0, height*chunk_size-1)
    world[start_y][start_x] = 2

    # --------------------- REPLACE ABOVE --------------------- #

    # Save chunks to files
    for h in range(height):
        for w in range(width):
            with open(f"../assets/world/chunk_{w}_{h}.txt", "x") as f:
                for i in range(chunk_size):
                    row = world[(h * chunk_size) + i][(chunk_size * w):(chunk_size * (w+1))]
                    for c, li in enumerate(list(map(str, row))):
                        if c != 0:
                            f.write(", ")
                        f.write(f"{li}")
                    f.write("\n")

    event.set()
