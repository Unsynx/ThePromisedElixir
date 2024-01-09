from scene_manager import SceneManager, Scene
from gui import *
from entity import Entity, Player
import pygame.surface
import constants as c


class DialogueScene(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "dialogue")

        self.guiManager = GuiManager(self.sceneManager.screen)

        self.back = self.guiManager.add_guideline(
            Guide("img", None, Guide.GL_VERTICAL, 0, Guide.ALIGN_LEFT, Guide.REL_ALIGN_BOTTOM, 0))
        self.back.add_element(Image("../assets/gui/images/backdrop1.png"))

        self.anim = None

        self.bg = self.guiManager.add_guideline(
            Guide("book", None, Guide.GL_VERTICAL, 0, Guide.ALIGN_LEFT, Guide.REL_ALIGN_BOTTOM, 0))
        self.book = self.bg.add_element(Image("../assets/Book.png"))

        self.buttons = self.guiManager.add_guideline(
            Guide("buttons", None, Guide.GL_HORIZONTAL, 0.9, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 50))
        self.buttons.add_element(BasicButton("Continue", 300, 75, manager.set_scene, "game", False))

        self.logo_g = self.guiManager.add_guideline(
            Guide("logo", None, Guide.GL_VERTICAL, 0.15, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_RIGHT, 0))
        self.text = None

    def on_scene_start(self, *args):
        num = args[0]
        for line in c.DIALOGUE[num]:
            self.logo_g.add_element(Text(line, Text.FONT_BASE, 64, (0, 0, 0)))

        self.anim = Tween(1000, 0, 250, Tween.quad_in_easing)

    def update(self, dt: float):
        if self.anim:
            self.anim.update()
            y = self.anim.get_current_value()
            self.book.visual_offset_y = y
            self.logo_g.offset_y = y
            if y == 0:
                self.anim = None

    def render(self, screen):
        self.guiManager.render_guidelines()


class Dialogue(Entity):
    def __init__(self):
        super().__init__()
        self.dialogue_number = 0
        self.surface = pygame.image.load("../assets/player/book.png")
        self.intractable = True

        self.serialize("dialogue_number", lambda: self.dialogue_number)

    def set_dialogue_number(self, num: int):
        self.dialogue_number = num
        return self

    def on_interact(self, entity: Entity):
        if not type(entity) is Player:
            return

        self.scene_manager.del_scene("dialogue")
        self.scene_manager.add_scene(DialogueScene(self.scene_manager))
        self.scene_manager.set_scene("dialogue", self.dialogue_number)

        self.group.remove(self)


class FinalDialogue(Dialogue):
    def __init__(self):
        super().__init__()
        self.surface = pygame.image.load("../assets/player/BookDead.png")
