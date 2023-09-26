import sys
from tiles import Camera, TileManager
from scene_manager import Scene, SceneManager
from gui import GuiManager, Guide, Text
import pygame


# This is where the main gameplay will go
class GameScene(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "game")

        self.guiManager = GuiManager(self.screen)
        self.debug = self.guiManager.add_guideline(Guide("center", None, Guide.GL_VERTICAL, 0, Guide.ALIGN_TOP, Guide.REL_ALIGN_RIGHT, 0))
        self.fps = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 0, 0)))
        self.metric = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 0, 0)))

        self.camera = Camera(self.screen.get_size())
        self.tileManager = TileManager(self.screen, 16, 16, self.camera)

    def update(self, dt):
        pressed = pygame.key.get_pressed()
        self.camera.x += int((pressed[pygame.K_RIGHT] - pressed[pygame.K_LEFT]) * 5 * dt)
        self.camera.y += int((pressed[pygame.K_DOWN] - pressed[pygame.K_UP]) * 5 * dt)

        self.tileManager.update()

        self.fps.set_value(f"FPS: {str(round(dt*60, 1))}")
        self.metric.set_value("Yay!")

    def render(self, screen: pygame.Surface):
        screen.fill((255, 255, 255))
        self.tileManager.render()
        self.guiManager.render_guidelines()


