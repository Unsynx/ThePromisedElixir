import sys
import time

from scene_manager import Scene, SceneManager
from gui import GuiManager, Guide, BasicButton, Image, Grid, Text
import pygame
from gen import LoadingScreen
import constants as c


class MainMenu(Scene):
    background = pygame.image.load("../assets/MainScreenBack.png")
    cliff = pygame.image.load("../assets/MainScreenCliff.png")
    player = pygame.image.load("../assets/MainScreenFrog.png")
    glow = pygame.image.load("../assets/Glow.png")
    glow = pygame.transform.scale_by(glow, 0.25)

    def on_scene_start(self, *args):
        if args.__contains__(True):
            pygame.mixer.music.fadeout(1000)
            pygame.mixer.music.load("../assets/music/forest_compressed.ogg")
            pygame.mixer.music.set_volume(c.MUSIC_VOLUME)
            pygame.mixer.music.play(-1)

    def __init__(self, manager: SceneManager):
        super().__init__(manager, "mainMenu")

        self.guiManager = GuiManager(self.sceneManager.screen)

        # ------ Buttons ------
        self.buttons = self.guiManager.add_guideline(
            Guide("buttons", None, Guide.GL_HORIZONTAL, 0.95, Guide.ALIGN_LEFT_PADDING, Guide.REL_ALIGN_TOP, 30))

        self.sceneManager.del_scene("loadingScreen")

        # So that we don't have a bunch of unused loading screens
        def get_scene():
            return LoadingScreen(self.sceneManager)

        self.buttons.add_element(BasicButton("New Game", 300, 75, lambda x: manager.set_scene(get_scene(), x), True))
        # self.buttons.add_element(Button("Load Game", 300, 75, lambda x: manager.set_scene(get_scene(), x), False))
        self.buttons.add_element(BasicButton("Credits", 300, 75, manager.set_scene, "creditsMenu"))
        self.buttons.add_element(BasicButton("Quit", 300, 75, sys.exit))

        # ------ Logo ------
        self.logo_g = self.guiManager.add_guideline(
            Guide("logo", None, Guide.GL_VERTICAL, 0.25, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 0))
        self.logo_g.add_element(Image("../assets/gui/images/logo_shadow.png"))

        # ------ Version Text ------
        self.text = self.guiManager.add_guideline(
            Guide("text", None, Guide.GL_HORIZONTAL, 0.97, Guide.ALIGN_RIGHT, Guide.REL_ALIGN_TOP, 25))
        self.text.add_element(Text("In Development    ", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))

    def update(self, dt):
        pass

    def render(self, screen):
        x, y = pygame.mouse.get_pos()
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.cliff, (x * 0.03, 0))
        rot_img = pygame.transform.rotate(self.glow, int(time.time() * -8) % 360)
        offset_x = (rot_img.get_width() - self.glow.get_width()) // 2
        offset_y = (rot_img.get_height() - self.glow.get_height()) // 2
        self.screen.blit(rot_img, (x * 0.03 + 700 - offset_x, 125 - offset_y))
        self.screen.blit(self.player, (x * 0.03, 0))
        self.guiManager.render_guidelines()


class CreditsMenu(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "creditsMenu")

        self.guiManager = GuiManager(self.sceneManager.screen)

        self.center = self.guiManager.add_guideline(Guide(
            "center", self.guiManager, Guide.GL_VERTICAL, 0.5, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 75))

        # ------ Grid ------
        self.grid = Grid(1000, 850, 10)
        self.grid[0].padding = 250
        self.grid[0].offset_y = 20
        self.grid[4].offset_y = 20

        self.grid.add_element(0, Text("Credits:", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))
        self.grid.add_element(1, Text("Programming and Art - Niklas Chaney", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
        self.grid.add_element(2, Text("Programming - Alec Benton", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
        self.grid.add_element(3, Text('Testing - M.SKH,  T.H,  N.A,  K.S,  O.A,  E.M', Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
        self.grid.add_element(4, Text("Sounds:", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))
        self.grid.add_element(5, Text("Ambience_Cave_00 - LittleRobotSoundFactory", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
        self.grid.add_element(6, Text("https://creativecommons.org/licenses/by/4.0/", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
        self.grid.add_element(7, Text("Creepy Forest - Augmentality (Brandon Morris)", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
        self.grid.add_element(8, Text("https://creativecommons.org/publicdomain/zero/1.0/", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
        self.grid.add_element(9, Text("Additional credits in assets/sfx/credits.txt", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))

        self.center.add_element(self.grid)

        # ------ Button ------
        self.center.add_element(BasicButton("Main Menu", 300, 75, manager.set_scene, "mainMenu"))

    def update(self, dt):
        self.screen.fill((0, 0, 0))

        self.guiManager.render_guidelines()


class SplashScreen(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "splashScreen")

    def update(self, dt):
        print("Splash")

        self.sceneManager.set_scene("mainMenu", True)

    def render(self, screen: pygame.Surface):
        pass


class TempWinScreen(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "win")

        self.guiManager = GuiManager(self.sceneManager.screen)

        # ------ Backdrop ------
        self.back = self.guiManager.add_guideline(
            Guide("img", None, Guide.GL_VERTICAL, 0, Guide.ALIGN_LEFT, Guide.REL_ALIGN_BOTTOM, 0))
        self.back.add_element(Image("../assets/gui/images/backdrop1.png"))

        # ------ Buttons ------
        self.buttons = self.guiManager.add_guideline(
            Guide("buttons", None, Guide.GL_HORIZONTAL, 0.9, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 50))

        self.buttons.add_element(BasicButton("Home", 300, 75, manager.set_scene, "mainMenu"))
        self.buttons.add_element(BasicButton("Quit", 300, 75, sys.exit))

        self.logo_g = self.guiManager.add_guideline(
            Guide("logo", None, Guide.GL_VERTICAL, 0.5, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 0))
        self.logo_g.add_element(Text("You Win!", Text.FONT_BASE, 128, (255, 255, 255)))

    def render(self, screen):
        self.guiManager.render_guidelines()


class TempLoseScreen(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "lose")

        self.guiManager = GuiManager(self.sceneManager.screen)

        # ------ Backdrop ------
        self.back = self.guiManager.add_guideline(
            Guide("img", None, Guide.GL_VERTICAL, 0, Guide.ALIGN_LEFT, Guide.REL_ALIGN_BOTTOM, 0))
        self.back.add_element(Image("../assets/gui/images/backdrop1.png"))

        # ------ Buttons ------
        self.buttons = self.guiManager.add_guideline(
            Guide("buttons", None, Guide.GL_HORIZONTAL, 0.9, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 50))

        self.buttons.add_element(BasicButton("Home", 300, 75, manager.set_scene, "mainMenu", True))
        self.buttons.add_element(BasicButton("Retry", 300, 75, manager.set_scene, "loadingScreen", True, True))
        self.buttons.add_element(BasicButton("Quit", 300, 75, sys.exit))

        self.logo_g = self.guiManager.add_guideline(
            Guide("logo", None, Guide.GL_VERTICAL, 0.5, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 0))
        self.logo_g.add_element(Text("You Lose!", Text.FONT_BASE, 128, (255, 255, 255)))

    def on_scene_start(self, *args):
        self.logo_g.add_element(Text(f"You made it to floor {args[0]}", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))

    def render(self, screen):
        self.guiManager.render_guidelines()
