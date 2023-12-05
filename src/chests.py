from scene_manager import SceneManager, Scene
from gui import *
from entity import Entity, Player
import pygame.surface
from tiles import Camera, TileManager
from items import SimpleSpearWeapon, IceWand, FireKnife
from random import choice


class ChestScreen(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "chest")

        self.guiManager = GuiManager(self.sceneManager.screen)

        self.back = self.guiManager.add_guideline(
            Guide("img", None, Guide.GL_VERTICAL, 0, Guide.ALIGN_LEFT, Guide.REL_ALIGN_BOTTOM, 0))
        self.back.add_element(Image("../assets/gui/images/backdrop1.png"))

        # ------ Buttons ------
        self.buttons = self.guiManager.add_guideline(
            Guide("buttons", None, Guide.GL_HORIZONTAL, 0.9, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 50))

        self.buttons.add_element(Button("Equip", 300, 75, self.set_weapon))
        self.buttons.add_element(Button("Don't Equip", 300, 75, manager.set_scene, "game", False))

        self.logo_g = self.guiManager.add_guideline(
            Guide("logo", None, Guide.GL_VERTICAL, 0.5, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 0))
        self.text = self.logo_g.add_element(Text("You Lose!", Text.FONT_BASE, 128, (255, 255, 255)))

        self.weapon = None
        self.player = None

    def set_weapon(self):
        self.player.set_weapon(self.weapon)
        self.sceneManager.set_scene("game", False)

    def on_scene_start(self, weapon, player):
        self.weapon = weapon
        self.text.set_value(weapon.name)
        self.player = player

    def render(self, screen):
        self.guiManager.render_guidelines()


class Chest(Entity):
    def __init__(self):
        super().__init__()
        self.surface = pygame.image.load("../assets/player/chest.png")
        self.intractable = True

    def on_interact(self, entity: Entity):
        if not type(entity) is Player:
            return

        weapons = (
            SimpleSpearWeapon,
            IceWand,
            FireKnife
        )

        self.scene_manager.set_scene("chest", choice(weapons)(), entity)
        self.group.remove(self)
