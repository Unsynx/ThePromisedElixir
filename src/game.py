from tiles import Camera, TileManager
from scene_manager import Scene, SceneManager
from gui import GuiManager, Guide, Text, Button
import pygame
from gen import generate_dungeon
from player import Player


# This is where the main gameplay will go
class GameScene(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "game")

        self.guiManager = GuiManager(self.screen)

        # Debug Gui
        self.debug = self.guiManager.add_guideline(Guide("center", None, Guide.GL_VERTICAL, 0, Guide.ALIGN_TOP, Guide.REL_ALIGN_RIGHT, 0))
        self.fps = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))
        self.metric = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))

        # Set up camera and tile manager.
        self.camera = Camera(self.screen.get_size())
        chunk_size = 4
        self.start_x, self.start_y = generate_dungeon(chunk_size)
        self.tileManager = TileManager(self.screen, 128, chunk_size, self.camera)

        # Set up player.
        self.player = Player(self.camera, self.screen)
        self.player.x = self.start_x * self.tileManager.tile_size
        self.player.y = self.start_y * self.tileManager.tile_size

    def update(self, dt):
        pressed = pygame.key.get_pressed()
        self.camera.x += int((pressed[pygame.K_RIGHT] - pressed[pygame.K_LEFT]) * 10 * dt)
        self.camera.y += int((pressed[pygame.K_DOWN] - pressed[pygame.K_UP]) * 10 * dt)

        self.tileManager.update()

        self.fps.set_value(f"FPS: {str(round(dt*60, 1))}")
        self.metric.set_value(f"Camera: {self.camera.x}, {self.camera.y}")

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        self.tileManager.render()
        self.player.render()
        self.guiManager.render_guidelines()


