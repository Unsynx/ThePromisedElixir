from scene_manager import Scene, SceneManager
from gui import GuiManager, Guide, BasicButton, Image, Text
import pygame
from tween import Tween
import time


class Scene3(Scene):
    image1 = pygame.image.load("../assets/intro/Scene3.png")
    image2 = pygame.image.load("../assets/intro/Scene3_2.png")
    image3 = pygame.image.load("../assets/intro/Scene3_3.png")
    image4 = pygame.image.load("../assets/intro/Scene3_4.png")

    sound = pygame.mixer.Sound("../assets/intro/scene3_narration.wav")
    sound2 = pygame.mixer.Sound("../assets/intro/final_narration.wav")

    def on_scene_start(self, *args):
        self.sound.play()
        self.start = time.time()

    def __init__(self, manager: SceneManager):
        super().__init__(manager, "intro3")

        self.guiManager = GuiManager(self.sceneManager.screen)
        self.g = self.guiManager.add_guideline(Guide("", None, Guide.GL_HORIZONTAL, 0.9, Guide.ALIGN_LEFT_PADDING, Guide.REL_ALIGN_BOTTOM, 30))
        self.g.add_element(BasicButton("Skip", 300, 75, manager.set_scene, "mainMenu", True))

        self.start = 0

        self.started = False

    def render(self, screen):
        t = time.time() - self.start
        self.screen.blit(self.image1, (0, 0))

        if t < 3:
            self.screen.blit(self.image1, (0, 0))
        elif t < 4:
            self.screen.blit(self.image2, (0, 0))
        elif t < 5:
            self.screen.blit(self.image3, (0, 0))
        else:
            self.screen.blit(self.image4, (0, 0))

        if t > 8:
            self.sceneManager.set_scene("mainMenu", True)

        self.guiManager.render_guidelines()

    def on_scene_end(self):
        if self.started:
            self.sceneManager.del_scene(self)
            self.sound.fadeout(100)
            self.sound2.play()
        self.started = True


class Scene2(Scene):
    image1 = pygame.image.load("../assets/intro/Scene2_table.png")
    image2 = pygame.image.load("../assets/intro/Scene2_paper.png")

    sound = pygame.mixer.Sound("../assets/intro/scene2_narration.wav")

    def on_scene_start(self, *args):
        self.sound.play()
        self.start = time.time()

    def __init__(self, manager: SceneManager):
        super().__init__(manager, "intro2")

        self.guiManager = GuiManager(self.sceneManager.screen)
        self.g = self.guiManager.add_guideline(Guide("", None, Guide.GL_HORIZONTAL, 0.9, Guide.ALIGN_LEFT_PADDING, Guide.REL_ALIGN_BOTTOM, 30))
        self.g.add_element(BasicButton("Skip", 300, 75, manager.set_scene, "mainMenu", True))

        self.anim = Tween(1000, 0, 2000, Tween.quad_out_easing)

        self.start = 0

    def render(self, screen):
        t = time.time() - self.start
        self.screen.blit(self.image1, (0, 0))
        self.anim.update()
        self.screen.blit(self.image2, (0, self.anim.get_current_value()))

        if t > 9.3:
            self.sceneManager.set_scene(Scene3(self.sceneManager))

        self.guiManager.render_guidelines()

    def on_scene_end(self):
        self.sceneManager.del_scene(self)
        self.sound.fadeout(100)


class Scene1(Scene):
    image1 = pygame.image.load("../assets/intro/Scene1_empty.png")
    image2 = pygame.image.load("../assets/intro/Scene1_flash.png")
    image3 = pygame.image.load("../assets/intro/Scene1_tower.png")

    sound = pygame.mixer.Sound("../assets/intro/scene1_narration.wav")

    def on_scene_start(self, *args):
        self.sound.play()
        self.start = time.time()

    def __init__(self, manager: SceneManager):
        super().__init__(manager, "intro")

        self.guiManager = GuiManager(self.sceneManager.screen)
        self.g = self.guiManager.add_guideline(Guide("", None, Guide.GL_HORIZONTAL, 0.9, Guide.ALIGN_LEFT_PADDING, Guide.REL_ALIGN_BOTTOM, 30))
        self.g.add_element(BasicButton("Skip", 300, 75, manager.set_scene, "mainMenu", True))

        self.start = 0

    def render(self, screen):
        t = time.time() - self.start
        if t < 13.1:
            self.screen.blit(self.image1, (0, 0))
        elif t < 13.5:
            self.screen.blit(self.image2, (0, 0))
        else:
            self.screen.blit(self.image3, (0, 0))

        if t > 22:
            self.sceneManager.set_scene(Scene2(self.sceneManager))

        self.guiManager.render_guidelines()

    def on_scene_end(self):
        self.sceneManager.del_scene(self)
        self.sound.fadeout(100)

