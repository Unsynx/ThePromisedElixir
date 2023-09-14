from scene_manager import Scene, SceneManager
from gui import GuiManager, Align, Square, Image
import pygame


class MainMenu(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "mainMenu")
        self.sceneManager = manager
        self.guiManager = GuiManager(self.sceneManager.screen)

        self.image = self.guiManager.add_element(Image("assets/test.jpg"))
        self.container = self.guiManager.add_container(0.5, 0.5, Align.W_MIDDLE, Align.H_MIDDLE)
        self.container += Square(100, 100, (100, 100, 100), 0, 0)

    def update(self):
        # This is runs every frame
        print("Menu")

    def render(self, screen):
        self.guiManager.render()


class SplashScreen(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "splashScreen")
        self.sceneManager = manager

    def update(self):
        print("Splash")

        self.sceneManager.set_scene("mainMenu")

    def render(self, screen: pygame.Surface):
        pass
