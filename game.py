import sys
from scene_manager import Scene, SceneManager
from gui import GuiManager, Guide, Text
import pygame


# This is where the main gameplay will go
class GameScene(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "game")

        self.guiManager = GuiManager(self.screen)
        self.center = self.guiManager.add_guideline(Guide("center", None, Guide.GL_VERTICAL, 0.5, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 0))
        self.center.add_element(Text("Killer Gameplay", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))

    def update(self, dt):
        pass

    def render(self, screen: pygame.Surface):
        self.guiManager.render_guidelines()
