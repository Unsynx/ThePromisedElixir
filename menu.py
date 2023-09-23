import random
import sys

from scene_manager import Scene, SceneManager
from gui import GuiManager, GuideLine, Button, Image, Grid, Text, ProgressBar
import pygame


class MainMenu(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "mainMenu")

        self.guiManager = GuiManager(self.sceneManager.screen)

        # ------ Backdrop ------
        self.back = self.guiManager.add_guideline(GuideLine("img", None, GuideLine.GL_VERTICAL, 0, GuideLine.ALIGN_LEFT, GuideLine.REL_ALIGN_BOTTOM, 0))

        self.back.add_element(Image("assets/test.jpg"))

        # ------ Buttons ------
        self.buttons = self.guiManager.add_guideline(GuideLine("buttons", None, GuideLine.GL_HORIZONTAL, 0.95, GuideLine.ALIGN_CENTER_PADDED, GuideLine.REL_ALIGN_CENTER, 50))

        self.buttons.add_element(Button("Start", 300, 75, manager.set_scene, "game"))
        self.buttons.add_element(Button("Credits", 300, 75, manager.set_scene, "creditsMenu"))
        self.buttons.add_element(Button("Quit", 300, 75, sys.exit))

        # ------ Testing ------
        self.test = self.guiManager.add_guideline(GuideLine("test", None, GuideLine.GL_VERTICAL, 0.5, GuideLine.ALIGN_CENTER_PADDED, GuideLine.REL_ALIGN_CENTER, 50))

        self.progress_bar = self.test.add_element(ProgressBar(1000, 50, ProgressBar.BASIC, (230, 85, 65), ProgressBar.DEFAULT_BACK_COLOR))
        self.fps = self.test.add_element(Text("test", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))

    def update(self, dt):
        # This is runs every frame
        # self.progress_bar.set_value(random.uniform(0, 1))
        self.fps.set_value(str(round(dt*60, 1)))

    def render(self, screen):
        self.guiManager.render_guidelines()


class CreditsMenu(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "creditsMenu")

        self.guiManager = GuiManager(self.sceneManager.screen)

        self.center = self.guiManager.add_guideline(GuideLine("center", self.guiManager, GuideLine.GL_VERTICAL, 0.5, GuideLine.ALIGN_CENTER_PADDED, GuideLine.REL_ALIGN_CENTER, 75))

        # ------ Grid ------
        self.grid = Grid(1000, 750, 10)
        self.grid[2].padding = 250

        self.grid.add_element(1, Text("Credits", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))
        self.grid.add_element(2, Text("Niklas Chaney", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
        self.grid.add_element(2, Text("Alec Benton", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))

        self.center.add_element(self.grid)

        # ------ Button ------
        self.center.add_element(Button("Main Menu", 300, 75, manager.set_scene, "mainMenu"))

    def update(self, dt):
        self.screen.fill((0, 0, 0))

        self.guiManager.render_guidelines()


class SplashScreen(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "splashScreen")

    def update(self, dt):
        print("Splash")

        self.sceneManager.set_scene("mainMenu")

    def render(self, screen: pygame.Surface):
        pass
