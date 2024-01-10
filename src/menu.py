import sys
import time

from scene_manager import Scene, SceneManager
from gui import GuiManager, Guide, BasicButton, Image, Grid, Text
import pygame
from gen import LoadingScreen
import constants as c
from save import *
from tween import Tween


class MainMenu(Scene):
    image1 = pygame.image.load("../assets/menu/MainScreenAll.png")

    def on_scene_start(self, *args):
        if args.__contains__(True):
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.load("../assets/music/forest_compressed.ogg")
            pygame.mixer.music.set_volume(c.MUSIC_VOLUME)
            pygame.mixer.music.play(-1)

    def __init__(self, manager: SceneManager):
        super().__init__(manager, "mainMenu")

        self.guiManager = GuiManager(self.sceneManager.screen)

        # ------ Buttons ------
        self.buttons = self.guiManager.add_guideline(
            Guide("buttons", None, Guide.GL_VERTICAL, 0.25, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 50))
        self.buttons.offset_y = 300

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
            Guide("logo", None, Guide.GL_VERTICAL, 0.25, Guide.ALIGN_LEFT_PADDING, Guide.REL_ALIGN_CENTER, 100))
        self.logo_g.add_element(Image("../assets/gui/images/logo_shadow.png"))

        # ------ Version Text ------
        self.text = self.guiManager.add_guideline(
            Guide("text", None, Guide.GL_HORIZONTAL, 0.97, Guide.ALIGN_RIGHT, Guide.REL_ALIGN_TOP, 25))
        self.text.add_element(Text("In Development    ", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))

    def render(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.image1, (0, 0))
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

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))

        self.guiManager.render_guidelines()


class SplashScreen(Scene):
    sound = pygame.mixer.Sound("../assets/menu/jingle.wav")

    image1 = pygame.image.load("../assets/menu/splash_1.png")
    image2 = pygame.image.load("../assets/menu/splash_2.png")

    def __init__(self, manager: SceneManager):
        super().__init__(manager, "splashScreen")

        self.start = time.time()

    def on_scene_start(self, *args):
        self.sound.play()

    def update(self, dt):
        if time.time() - self.start > 6:
            self.sceneManager.set_scene("intro")

    def render(self, screen: pygame.Surface):
        if (time.time() - self.start) % 0.5 < 0.25:
            self.screen.blit(self.image1, (0, 0))
        else:
            self.screen.blit(self.image2, (0, 0))

    def on_scene_end(self):
        self.sound.fadeout(100)
        self.sceneManager.del_scene(self)


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
    def __init__(self, manager: SceneManager, group):
        super().__init__(manager, "lose")

        self.guiManager = GuiManager(self.sceneManager.screen)
        self.group = group

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
            Guide("logo", None, Guide.GL_VERTICAL, 0.5, Guide.ALIGN_LEFT_PADDING, Guide.REL_ALIGN_CENTER, 100))
        self.logo_g.add_element(Text("You died!", Text.FONT_BASE, 128, (255, 255, 255)))

        self.text = self.guiManager.add_guideline(
            Guide("t", None, Guide.GL_VERTICAL, 0.5, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 0))

        self.anim1 = None
        self.anim2 = None
        self.anim3 = None
        self.anim4 = None
        self.anim5 = None

        self.t1 = None
        self.t2 = None
        self.t3 = None
        self.t4 = None
        self.t5 = None

    def on_scene_start(self, *args):
        self.text.add_element(Text(f"You made it to floor {args[0]}", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))

        # load highscore
        save_template = [0]
        data = read_save("save.txt", save_template)
        if args[0] > data[0]:
            save_to_file("save.txt", [args[0]])
            self.text.add_element(Text("That's a new highscore!", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))
        else:
            self.text.add_element(Text(f"Your best is floor {data[0]}", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))

        from entity import Stats
        stats = self.group.get_entity(Stats)
        self.anim1 = Tween(1000, 0, 250, Tween.quad_in_easing)
        self.anim2 = Tween(1000, 0, 350, Tween.quad_in_easing)
        self.anim3 = Tween(1000, 0, 450, Tween.quad_in_easing)
        self.anim4 = Tween(1000, 0, 550, Tween.quad_in_easing)
        self.anim5 = Tween(1000, 0, 650, Tween.quad_in_easing)

        self.t1 = self.text.add_element(Text(f"Enemies Killed: {stats.enemies_killed}", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
        self.t2 = self.text.add_element(Text(f"Potions Drank: {stats.potions_drank}", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
        self.t3 = self.text.add_element(Text(f"Books Read: {stats.books_read}", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
        self.t4 = self.text.add_element(Text(f"Traps Activated: {stats.traps_activated}", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
        self.t5 = self.text.add_element(Text(f"Chests Opened: {stats.chests_opened}", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))

    def update(self, dt: float):
        self.anim1.update()
        self.anim2.update()
        self.anim3.update()
        self.anim4.update()
        self.anim5.update()

        self.t1.visual_offset_x = self.anim1.get_current_value()
        self.t2.visual_offset_x = self.anim2.get_current_value()
        self.t3.visual_offset_x = self.anim3.get_current_value()
        self.t4.visual_offset_x = self.anim4.get_current_value()
        self.t5.visual_offset_x = self.anim5.get_current_value()

    def render(self, screen):
        self.guiManager.render_guidelines()
