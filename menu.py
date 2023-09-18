from scene_manager import Scene, SceneManager
from gui import GuiManager, GuideLine, ColorSquare
import pygame


class MainMenu(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "mainMenu")
        self.sceneManager = manager
        self.guiManager = GuiManager(self.sceneManager.screen)
        self.test = self.guiManager.add_guideline("test", GuideLine.GL_HORIZONTAL, 1.0, 0.5, alignment=GuideLine.ALIGN_RIGHT, rel_alignment=GuideLine.REL_ALIGN_CENTER)

    def update(self):
        # This is runs every frame
        pass

    def render(self, screen):
        self.guiManager.render_guidelines()


class SplashScreen(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "splashScreen")
        self.sceneManager = manager

    def update(self):
        print("Splash")

        self.sceneManager.set_scene("mainMenu")

    def render(self, screen: pygame.Surface):
        pass
