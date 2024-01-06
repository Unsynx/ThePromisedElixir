from scene_manager import SceneManager, Scene
from gui import *
from entity import Entity, Player
import pygame.surface
from tiles import Camera, TileManager

dialogue_1_text = "The dialogue system works"


class DialogueScene1(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "dialogue1")

        self.guiManager = GuiManager(self.sceneManager.screen)

        self.back = self.guiManager.add_guideline(
            Guide("img", None, Guide.GL_VERTICAL, 0, Guide.ALIGN_LEFT, Guide.REL_ALIGN_BOTTOM, 0))
        self.back.add_element(Image("../assets/gui/images/backdrop1.png"))

        self.buttons = self.guiManager.add_guideline(
            Guide("buttons", None, Guide.GL_HORIZONTAL, 0.9, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 50))
        self.buttons.add_element(BasicButton("Continue", 300, 75, manager.set_scene, "game", False))

        self.logo_g = self.guiManager.add_guideline(
            Guide("logo", None, Guide.GL_VERTICAL, 0.5, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 0))
        self.text = self.logo_g.add_element(Text(f"{dialogue_1_text}", Text.FONT_BASE, 64, (255, 255, 255)))

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

        self.scene_manager.set_scene(f"dialogue{self.dialogue_number}")
