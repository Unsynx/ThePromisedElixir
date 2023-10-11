import sys
from scene_manager import Scene, SceneManager
from gui import GuiManager, Guide, Button, Image, Grid, Text, ProgressBar
import pygame


class MainMenu(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "mainMenu")

        self.guiManager = GuiManager(self.sceneManager.screen)

        # ------ Backdrop ------
        self.back = self.guiManager.add_guideline(Guide("img", None, Guide.GL_VERTICAL, 0, Guide.ALIGN_LEFT, Guide.REL_ALIGN_BOTTOM, 0))

        self.back.add_element(Image("../assets/gui/images/backdrop1.png"))

        # ------ Buttons ------
        self.buttons = self.guiManager.add_guideline(Guide("buttons", None, Guide.GL_VERTICAL, 0.2, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 50))

        self.buttons.add_element(Button("New Game", 300, 75, manager.set_scene, "loadingScreen", True))
        self.buttons.add_element(Button("Load Game", 300, 75, manager.set_scene, "loadingScreen", False))
        self.buttons.add_element(Button("Credits", 300, 75, manager.set_scene, "creditsMenu"))
        self.buttons.add_element(Button("Quit", 300, 75, sys.exit))

        # ------ Logo ------
        self.logo_g = self.guiManager.add_guideline(Guide("logo", None, Guide.GL_VERTICAL, 0.75, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 0))
        self.logo_g.add_element(Image("../assets/gui/images/logo_shadow.png"))

        # ------ Version Text ------
        self.text = self.guiManager.add_guideline(Guide("text", None, Guide.GL_VERTICAL, 0, Guide.ALIGN_BOTTOM, Guide.REL_ALIGN_RIGHT, 25))
        self.text.add_element(Text("  In Development", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))

    def update(self, dt):
        pass

    def render(self, screen):
        self.guiManager.render_guidelines()


class CreditsMenu(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "creditsMenu")

        self.guiManager = GuiManager(self.sceneManager.screen)

        self.center = self.guiManager.add_guideline(Guide("center", self.guiManager, Guide.GL_VERTICAL, 0.5, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 75))

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
