import time

from scene_manager import SceneManager, Scene
from gui import *
from entity import Entity, Player, Stats
import pygame.surface
from particles import ChestClose, ParticleManager
import constants as c
from items import Weapon, NoWeapon
from random import randint, choice


class ChestScreen(Scene):
    sound = pygame.mixer.Sound("../assets/sfx/box_break.wav")
    sound.set_volume(c.SFX_VOLUME)

    def __init__(self, manager: SceneManager, particle_manager: ParticleManager, pos, group):
        super().__init__(manager, "chest")

        self.guiManager = GuiManager(self.sceneManager.screen)
        self.particle_manager = particle_manager
        self.x, self.y = pos

        self.back = self.guiManager.add_guideline(
            Guide("img", None, Guide.GL_VERTICAL, 0, Guide.ALIGN_LEFT, Guide.REL_ALIGN_BOTTOM, 0))
        self.back.add_element(Image("../assets/gui/images/backdrop1.png"))

        # ------ Buttons ------
        self.buttons = self.guiManager.add_guideline(
            Guide("buttons", None, Guide.GL_HORIZONTAL, 0.9, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 50))

        self.buttons.add_element(BasicButton("Equip", 300, 75, self.set_weapon))
        self.buttons.add_element(BasicButton("Don't Equip", 300, 75, manager.set_scene, "game", False))

        self.logo_g = self.guiManager.add_guideline(
            Guide("logo", None, Guide.GL_VERTICAL, 0.5, Guide.ALIGN_LEFT_PADDING, Guide.REL_ALIGN_CENTER, 100))
        self.weapon_g = self.guiManager.add_guideline(
            Guide("wep", None, Guide.GL_VERTICAL, 0.5, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 10))
        self.old_weapon_g = self.guiManager.add_guideline(
            Guide("wep2", None, Guide.GL_VERTICAL, 0.2, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 10))

        self.chest_g = self.guiManager.add_guideline(
            Guide("chest", None, Guide.GL_VERTICAL, 0.5, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 0))
        self.chest = self.chest_g.add_element(Image("../assets/player/chest.png").scale_by(2))

        self.weapon = None
        self.player = None

        self.group = group
        self.start = 0

    def on_scene_end(self):
        self.group.change_queue_lifetime_by(time.time() - self.start)
        self.sceneManager.del_scene(self)

    def set_weapon(self):
        self.player.set_weapon(self.weapon)
        self.sceneManager.set_scene("game", False)

    def on_scene_start(self, weapon, player):
        self.start = time.time()

        self.weapon = weapon

        self.logo_g.add_element(Text(f"{weapon.pretty_name} - Tier {weapon.tier}", Text.FONT_BASE, 128, (255, 255, 255)))
        self.weapon_g.add_element(Image(weapon.icon_path).scale_by(2))
        self.weapon_g.add_element(WeaponPatternImage(self.weapon.pattern))
        self.weapon_g.add_element(Text(f"{weapon.damage}dmg", Text.FONT_BASE, Text.SIZE_HEADER, (255, 255, 255)))

        old = player.weapon
        self.old_weapon_g.add_element(Text(f"Current Weapon:", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
        self.old_weapon_g.add_element(Text(f"{old.pretty_name}", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
        self.old_weapon_g.add_element(Text(f"Tier {old.tier}", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))
        try:
            self.old_weapon_g.add_element(Image(old.icon_path))
        except TypeError:
            pass
        self.old_weapon_g.add_element(WeaponPatternImage(old.pattern))
        self.old_weapon_g.add_element(Text(f"{old.damage}dmg", Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))

        self.logo_g.hide = True
        self.buttons.hide = True
        self.weapon_g.hide = True
        self.old_weapon_g.hide = True
        self.player = player

        def set_visibility():
            self.logo_g.hide = False
            self.buttons.hide = False
            self.weapon_g.hide = False
            self.old_weapon_g.hide = False
            self.chest_g.hide = True
            x = self.screen.get_width() / 2 + self.particle_manager.camera.rel_x
            y = self.screen.get_height() / 2 + self.particle_manager.camera.rel_y
            self.sound.play()
            self.particle_manager.add_system(ChestClose(x, y))

        self.sceneManager.add_to_queue(set_visibility, 0.5)

    def update(self, dt: float):
        self.particle_manager.update(dt)

    def render(self, screen):
        screen.fill((0, 0, 0))
        self.guiManager.render_guidelines()
        self.particle_manager.render()


class Loot:
    DIFFICULTY_SCALE = 15
    FLOOR_SCALE = 15

    def __init__(self):
        self.tier0_weapons = []
        self.tier1_weapons = []
        self.tier2_weapons = []
        self.tier3_weapons = []
        self.tier4_weapons = []

        for w in Weapon.__subclasses__():
            match w().tier:
                case c.TIER_0:
                    self.tier0_weapons.append(w)
                case c.TIER_1:
                    self.tier1_weapons.append(w)
                case c.TIER_2:
                    self.tier2_weapons.append(w)
                case c.TIER_3:
                    self.tier3_weapons.append(w)
                case c.TIER_4:
                    self.tier4_weapons.append(w)
                case _:
                    pass

    def get_weapon(self, floor, offset=0):
        floor -= offset
        num = randint(min(-100 + floor * self.FLOOR_SCALE, 0), min(100, floor * self.FLOOR_SCALE))
        num += floor * self.DIFFICULTY_SCALE

        if floor < 1:
            return NoWeapon()

        tier = None
        if num < 50:
            tier = self.tier0_weapons
        elif num < 100:
            tier = self.tier1_weapons
        elif num < 200:
            tier = self.tier2_weapons
        elif num < 300:
            tier = self.tier3_weapons
        else:
            tier = self.tier4_weapons

        try:
            return choice(tier)()
        except IndexError:
            print("No weapon in tier. returning no weapon")
            return NoWeapon()


class Chest(Entity):
    loot = Loot()

    def __init__(self):
        super().__init__()
        self.surface = pygame.image.load("../assets/player/chest.png")
        self.intractable = True
        self.floor = None

        self.serialize("floor", lambda: self.floor)

    def set_floor(self, floor):
        self.floor = floor
        return self

    def on_interact(self, entity: Entity):
        if not type(entity) is Player:
            return

        self.group.get_entity(Stats).chests_opened += 1
        self.scene_manager.set_scene(ChestScreen(self.scene_manager, self.particle_manager, (self.x, self.y), self.group), self.loot.get_weapon(self.floor), entity)
        self.group.remove(self)
