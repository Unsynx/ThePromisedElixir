from scene_manager import Scene, SceneManager
from gui import GuiManager, GuideLine, Button, ColorSquare
import pygame


class MainMenu(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "mainMenu")
        self.sceneManager = manager
        self.guiManager = GuiManager(self.sceneManager.screen)
        self.buttons = self.guiManager.add_guideline(GuideLine("test", None, GuideLine.GL_VERTICAL, 0.5, GuideLine.ALIGN_CENTER_PADDED, GuideLine.REL_ALIGN_CENTER, 10))
        self.buttons.add_element(Button(manager.set_scene))
        for i in range(3):
            self.buttons.add_element(ColorSquare())

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
