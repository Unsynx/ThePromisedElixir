from tiles import Camera, TileManager, CHUNK_SIZE, TILE_SIZE
from scene_manager import Scene, SceneManager
from gui import GuiManager, Guide, Text, BasicButton, ProgressBar, LevelIntro
import pygame
from entity import Player
from entity_group import EntityGroup
from particles import ParticleManager


# This is where the main gameplay will go
class GameScene(Scene):
    def __init__(self, manager: SceneManager, level):
        super().__init__(manager, "game")
        self.level = level

        self.guiManager = GuiManager(self.screen)
        self.player_alive = True

        # -------------- Debug GUI -------------- #
        self.debug = self.guiManager.add_guideline(
            Guide("center", None, Guide.GL_VERTICAL, 0, Guide.ALIGN_TOP, Guide.REL_ALIGN_RIGHT, 0))
        self.fps = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))
        self.cam_pos = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))
        self.plyr_pos = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))
        self.plyr_tile_pos = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))
        self.weapon = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))
        self.lvl = self.debug.add_element(Text("", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))

        self.debug.hide = True

        # -------------- Game Classes -------------- #
        # Set up camera and tile manager.
        self.camera = Camera(self.screen.get_size(), TILE_SIZE, None)
        self.tileManager = TileManager(self.screen, TILE_SIZE, CHUNK_SIZE, self.camera)
        self.particleManager = ParticleManager(self.screen, self.camera)

        # -------------- Entities and Player -------------- #
        self.group = EntityGroup(self.camera, self.screen, self.tileManager, self.sceneManager, self.particleManager, TILE_SIZE)
        self.camera.group = self.group
        self.player = None

        # -------------- Player UI -------------- #
        self.player_ui = self.guiManager.add_guideline(
            Guide("player_ui", None, Guide.GL_VERTICAL, 0.5, Guide.ALIGN_BOTTOM, Guide.REL_ALIGN_CENTER, 10))
        self.weapon_attack = self.player_ui.add_element(Text("", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
        self.health_bar = self.player_ui.add_element(
            ProgressBar(750, 25, ProgressBar.SMOOTH, (155, 43, 45), (0, 0, 0)))

        # Temp: Save + Load
        self.debug.add_element(BasicButton("Save", 300, 80, self.group.save))
        self.debug.add_element(BasicButton("Load", 300, 80, self.group.load))

        # -------------- Tutorial UI -------------- #
        if level == 1:
            self.tut = self.guiManager.add_guideline(
                Guide("tut", None, Guide.GL_VERTICAL, 0.005, Guide.ALIGN_TOP, Guide.REL_ALIGN_RIGHT, 10))
            self.tut.add_element(Text("Instructions:", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))
            self.tut.add_element(Text("Movement - Arrows", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
            self.tut.add_element(Text("Attack by moving into enemies", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
            self.tut.add_element(Text("Collect weapons from chests", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
            self.tut.add_element(Text("Find the stairs!", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))

        self.intro = self.guiManager.add_guideline(
                Guide("intro", None, Guide.GL_VERTICAL, 0.5, Guide.REL_ALIGN_CENTER, Guide.REL_ALIGN_CENTER, 5))
        self.card = self.intro.add_element(LevelIntro(f"Level {self.level}"))
        self.group.add_to_queue(self.card.start, 1.25)

        self.debug_cool = False

    def on_scene_start(self, is_loading_save):
        if is_loading_save:
            self.group.load()
        self.player = self.group[0]

        self.group[1].scene_manager = self.sceneManager  # Temp
        self.camera.set_position(self.player.x + int(self.player.surface.get_width() * 0.5),
                                 self.player.y + int(self.player.surface.get_height() * 0.5))

        # Resets loaded tiles when reloading world
        for _ in range(len(self.tileManager.chunks)):
            self.tileManager.del_chunk(0)

        self.group.on_scene_start(self.sceneManager.scene.name)

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
            if self.player_alive:
                self.player_alive = False
                from menu import TempLoseScreen
                self.group.add_to_queue(self.sceneManager.set_scene, 1.5, TempLoseScreen(self.sceneManager, self.group), self.level)

        self.group.update(dt)
        self.camera.update(dt)
        self.tileManager.update()
        self.particleManager.update(dt)

        # Debug Menu
        self.fps.set_value(f"FPS: {str(round(dt * 60, 1))}")
        self.cam_pos.set_value(f"Camera: {round(self.camera.x, 0)}, {round(self.camera.y, 0)}")
        self.plyr_pos.set_value(f"Plyr - Position: {round(self.player.x, 0)}, {round(self.player.y, 0)}")
        self.plyr_tile_pos.set_value(f"Plyr - Tile Position: {self.player.tile_x}, {self.player.tile_y}")
        self.weapon.set_value(f"Weapon: {self.player.weapon.name}")
        self.lvl.set_value(f"Floor: {self.level}")

        # Player UI
        if self.player:
            self.health_bar.set_value(self.player.health / self.player.max_health)
            self.weapon_attack.set_value(f"{self.player.health}/{self.player.max_health}hp       {self.player.weapon.pretty_name} - {self.player.weapon.damage}dmg")

    def render(self, screen: pygame.Surface):
        screen.fill((50, 60, 57))
        self.tileManager.render()
        self.group.render()
        self.guiManager.render_guidelines()
        self.particleManager.render()
