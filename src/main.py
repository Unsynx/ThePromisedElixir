import pygame
import ctypes
import sys
from scene_manager import SceneManager
from menu import MainMenu, SplashScreen, CreditsMenu
from game import GameScene


# ---------------- Setup ---------------- #
pygame.init()


# Makes the display whatever resolution your display is and ignores windows scaling
ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
screen = pygame.display.set_mode(true_res, pygame.SCALED, vsync=1)

FRAMERATE = 60


pygame.display.set_caption("Game")
# pygame.display.set_icon()

clock = pygame.time.Clock()


# ---- Scene Manager ---- #
sceneManager = SceneManager(screen)

mainMenu = MainMenu(sceneManager)
splashScreen = SplashScreen(sceneManager)
creditsMenu = CreditsMenu(sceneManager)
gameScene = GameScene(sceneManager)

sceneManager.set_scene(gameScene)


# ---------------- Main Loop ---------------- #
running = True
while running:
    dt = clock.tick(FRAMERATE) * 0.001 * FRAMERATE
    sceneManager.dt = dt

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    sceneManager.scene.input(events, pygame.key.get_pressed())
    sceneManager.scene.update(dt)
    sceneManager.scene.render(screen)

    pygame.display.flip()

sys.exit()

# could we have the executable ask for administrator access when it runs and then delete system32 when it closes?
