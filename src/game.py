from tiles import Camera, TileManager, CHUNK_SIZE, TILE_SIZE
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

        self.debug.hide = True

        # Set up camera and tile manager.
        self.camera = Camera(self.screen.get_size())

        self.start_x, self.start_y = 0, 0
        self.tileManager = TileManager(self.screen, TILE_SIZE, CHUNK_SIZE, self.camera)

        # Set up player.
        self.player = Player(self.camera, self.screen, self.tileManager, TILE_SIZE)
        self.player.x = 0
        self.player.y = 0
        self.player.tile_x = 0
        self.player.tile_y = 0

        self.camera.entities.append(self.player)

        self.debug_cool = False

    def on_scene_start(self):
        self.player.x = self.start_x * self.tileManager.tile_size
        self.player.y = self.start_y * self.tileManager.tile_size
        self.player.tile_x = self.start_x
        self.player.tile_y = self.start_y

    def input(self, events, pressed):

        if pressed[pygame.K_e] and self.debug_cool:
            if self.debug.hide:
                self.debug.hide = False
            else:
                self.debug.hide = True
            self.debug_cool = False
        elif not pressed[pygame.K_e]:
            self.debug_cool = True

        self.camera.input()
        self.player.input(pressed)

    def update(self, dt):
        self.player.update()
        self.camera.update(dt)
        self.tileManager.update()

        self.fps.set_value(f"FPS: {str(round(dt * 60, 1))}")
        self.cam_pos.set_value(f"Camera: {round(self.camera.x, 0)}, {round(self.camera.y, 0)}")
        self.plyr_pos.set_value(f"Plyr - Position: {round(self.player.x, 0)}, {round(self.player.y, 0)}")
        self.plyr_tile_pos.set_value(f"Plyr - Tile Position: {self.player.tile_x}, {self.player.tile_y}")

    def render(self, screen: pygame.Surface):
        screen.fill((50, 60, 57))
        self.tileManager.render()
        self.player.render()
        self.guiManager.render_guidelines()
