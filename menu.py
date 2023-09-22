from scene_manager import Scene, SceneManager
from gui import GuiManager, GuideLine, Button, ColorSquare, Image
import pygame


class MainMenu(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "mainMenu")

        self.guiManager = GuiManager(self.sceneManager.screen)
        self.back = self.guiManager.add_guideline(GuideLine("img", None, GuideLine.GL_VERTICAL, 0, GuideLine.ALIGN_LEFT, GuideLine.REL_ALIGN_BOTTOM, 0))
        self.back.add_element(Image("assets/test.jpg"))
        self.buttons = self.guiManager.add_guideline(GuideLine("buttons", None, GuideLine.GL_VERTICAL, 0.5, GuideLine.ALIGN_LEFT, GuideLine.REL_ALIGN_CENTER, 10))
        self.buttons.add_element(Button(manager.set_scene, "creditsMenu"))
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

    def update(self):
        print("Splash")

        self.sceneManager.set_scene("mainMenu")

    def render(self, screen: pygame.Surface):
        pass


class CreditsMenu(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "creditsMenu")

    def update(self):
        self.screen.fill((255, 255, 255))
