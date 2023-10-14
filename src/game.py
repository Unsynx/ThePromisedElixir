from tiles import Camera, TileManager, CHUNK_SIZE, TILE_SIZE
from scene_manager import Scene, SceneManager
from gui import GuiManager, Guide, Text, Button
import pygame
from entity import Player, Enemy, Dummy
from entity_group import EntityGroup
from items import SimpleSpearWeapon


# This is where the main gameplay will go
class GameScene(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "game")

        self.guiManager = GuiManager(self.screen)

        # -------------- Debug GUI -------------- #
        self.debug = self.guiManager.add_guideline(
            Guide("center", None, Guide.GL_VERTICAL, 0, Guide.ALIGN_TOP, Guide.REL_ALIGN_RIGHT, 0))
        self.fps = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))
        self.cam_pos = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))
        self.plyr_pos = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))
        self.plyr_tile_pos = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))
        self.reload = self.debug.add_element(Button("Re-Generate", 300, 80, self.sceneManager.set_scene, "loadingScreen", True))

        self.debug.hide = True

        # -------------- Game Classes -------------- #
        # Set up camera and tile manager.
        self.camera = Camera(self.screen.get_size(), TILE_SIZE, None)
        self.camera.mode = Camera.CENTER_FIRST_ENTITY_SMOOTH

        self.start_x, self.start_y = 0, 0
        self.tileManager = TileManager(self.screen, TILE_SIZE, CHUNK_SIZE, self.camera)

        # -------------- Entities and Player -------------- #
        self.group = EntityGroup(self.camera, self.screen, self.tileManager, TILE_SIZE)
        self.camera.entity_group = self.group
        # Set up player.
        self.player = self.group.add_entity(Player)
        self.player.set_position(0, 0)
        self.player.set_weapon(SimpleSpearWeapon())

        # -------------- TEMP: Debug only -------------- #
        self.group.add_entity(Dummy).set_position(8, 8)
        self.group.add_entity(Dummy).set_position(8, 9)
        self.group.add_entity(Dummy).set_position(8, 7)
        self.group.add_entity(Dummy).set_position(7, 8)
        self.group.add_entity(Dummy).set_position(9, 8)

        # Temp: Save + Load
        self.debug.add_element(Button("Save", 300, 80, self.group.save))
        self.debug.add_element(Button("Load", 300, 80, self.group.load))

        self.debug_cool = False

    def on_scene_start(self, is_loading_save):
        if is_loading_save:
            self.group.load()
        else:
            # Calls when world is newly generated
            self.player.set_position(self.start_x, self.start_y)

        self.player = self.group.entities[0]

        # Resets loaded tiles when reloading world
        for _ in range(len(self.tileManager.chunks)):
            self.tileManager.del_chunk(0)

    def input(self, events, pressed):
        # Toggle Debug Menu
        if pressed[pygame.K_e] and self.debug_cool:
            if self.debug.hide:
                self.debug.hide = False
            else:
                self.debug.hide = True
            self.debug_cool = False
        elif not pressed[pygame.K_e]:
            self.debug_cool = True

        self.camera.input()
        self.group.input(pressed)

    def update(self, dt):
        self.group.update(dt)
        self.camera.update(dt)
        self.tileManager.update()

        # Debug Menu
        self.fps.set_value(f"FPS: {str(round(dt * 60, 1))}")
        self.cam_pos.set_value(f"Camera: {round(self.camera.x, 0)}, {round(self.camera.y, 0)}")
        self.plyr_pos.set_value(f"Plyr - Position: {round(self.player.x, 0)}, {round(self.player.y, 0)}")
        self.plyr_tile_pos.set_value(f"Plyr - Tile Position: {self.player.tile_x}, {self.player.tile_y}")

    def render(self, screen: pygame.Surface):
        screen.fill((50, 60, 57))
        self.tileManager.render()
        self.group.render()
        self.guiManager.render_guidelines()
