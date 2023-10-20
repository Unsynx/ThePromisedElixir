from tiles import Camera, TileManager, CHUNK_SIZE, TILE_SIZE
from scene_manager import Scene, SceneManager
from gui import GuiManager, Guide, Text, Button, ProgressBar
import pygame
from entity import Player, Enemy, Dummy, Chest
from entity_group import EntityGroup


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
        self.weapon = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))

        self.debug.hide = True

        # -------------- Game Classes -------------- #
        # Set up camera and tile manager.
        self.camera = Camera(self.screen.get_size(), TILE_SIZE, None)
        self.camera.mode = Camera.CENTER_FIRST_ENTITY_SMOOTH
        self.tileManager = TileManager(self.screen, TILE_SIZE, CHUNK_SIZE, self.camera)

        # -------------- Entities and Player -------------- #
        self.group = EntityGroup(self.camera, self.screen, self.tileManager, TILE_SIZE)
        self.camera.entity_group = self.group
        self.player = None

        # -------------- Player UI -------------- #
        self.player_ui = self.guiManager.add_guideline(
            Guide("player_ui", None, Guide.GL_HORIZONTAL, 1, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_TOP, 10))
        self.health_bar = self.player_ui.add_element(
            ProgressBar(750, 20, ProgressBar.BASIC, (255, 255, 255), (0, 0, 0)))
        self.weapon_attack = self.player_ui.add_element(Text("", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))

        # Temp: Save + Load
        self.debug.add_element(Button("Save", 300, 80, self.group.save))
        self.debug.add_element(Button("Load", 300, 80, self.group.load))

        self.debug_cool = False

    def on_scene_start(self, is_loading_save):
        self.group.load()
        self.player = self.group[0]

        self.group[1].scene_manager = self.sceneManager  # Temp
        self.camera.set_position(self.player.x, self.player.y)

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
        if any(isinstance(x, Player) for x in self.group):
            self.player = self.group[0]  # Work around :(
        else:
            self.sceneManager.set_scene("lose")

        self.group.update(dt)
        self.camera.update(dt)
        self.tileManager.update()

        # Debug Menu
        self.fps.set_value(f"FPS: {str(round(dt * 60, 1))}")
        self.cam_pos.set_value(f"Camera: {round(self.camera.x, 0)}, {round(self.camera.y, 0)}")
        self.plyr_pos.set_value(f"Plyr - Position: {round(self.player.x, 0)}, {round(self.player.y, 0)}")
        self.plyr_tile_pos.set_value(f"Plyr - Tile Position: {self.player.tile_x}, {self.player.tile_y}")
        self.weapon.set_value(f"Weapon: {type(self.player.weapon).__name__}")

        # Player UI
        if self.player:
            self.health_bar.set_value(self.player.health / self.player.max_health)
            try:
                self.weapon_attack.set_value(f"{self.player.weapon.name} - {self.player.weapon.normal_attack.damage}dmg")
            except AttributeError:
                self.weapon_attack.set_value("Hands - 1dmg")

    def render(self, screen: pygame.Surface):
        screen.fill((50, 60, 57))
        self.tileManager.render()
        self.group.render()
        self.guiManager.render_guidelines()
