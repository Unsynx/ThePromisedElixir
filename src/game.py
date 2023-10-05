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
        self.debug = self.guiManager.add_guideline(
            Guide("center", None, Guide.GL_VERTICAL, 0, Guide.ALIGN_TOP, Guide.REL_ALIGN_RIGHT, 0))
        self.fps = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))
        self.cam_pos = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))
        self.plyr_pos = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))
        self.plyr_tile_pos = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))

        # Set up camera and tile manager.
        self.camera = Camera(self.screen.get_size())
        chunk_size = 4
        tile_size = 128
        self.start_x, self.start_y = generate_dungeon(chunk_size)
        self.tileManager = TileManager(self.screen, tile_size, chunk_size, self.camera)

        # Set up player.
        self.player = Player(self.camera, self.screen, self.tileManager, tile_size)
        self.player.x = self.start_x * self.tileManager.tile_size
        self.player.y = self.start_y * self.tileManager.tile_size
        self.player.tile_x = self.start_x
        self.player.tile_y = self.start_y

        self.camera.entities.append(self.player)

    def input(self, events, pressed_keys):
        self.camera.input()
        self.player.input(pressed_keys)

    def update(self, dt):
        self.player.update()
        self.camera.update(dt)
        self.tileManager.update()

        self.fps.set_value(f"FPS: {str(round(dt * 60, 1))}")
        self.cam_pos.set_value(f"Camera: {round(self.camera.x, 0)}, {round(self.camera.y, 0)}")
        self.plyr_pos.set_value(f"Plyr - Position: {round(self.player.x, 0)}, {round(self.player.y, 0)}")
        self.plyr_tile_pos.set_value(f"Plyr - Tile Position: {self.player.tile_x}, {self.player.tile_y}")

    def render(self, screen: pygame.Surface):
        screen.fill((0, 0, 0))
        self.tileManager.render()
        self.player.render()
        self.guiManager.render_guidelines()
