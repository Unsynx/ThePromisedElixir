import pygame
import sys
from scene_manager import SceneManager
from screeninfo import get_monitors
from menu import *
from dialogue import DialogueScene1

# ---------------- Setup ---------------- #
pygame.init()
pygame.mixer.init()

# Makes the display whatever resolution your display is and ignores windows scaling
primary_monitor = get_monitors()[0]
screen = pygame.display.set_mode((primary_monitor.width, primary_monitor.height), pygame.SCALED, vsync=1)
# screen = pygame.display.set_mode((1920, 1080), pygame.SCALED, vsync=1)
FRAMERATE = 60

# Nice comment

pygame.display.set_caption("Game")
# pygame.display.set_icon()

clock = pygame.time.Clock()




# ---- Scene Manager ---- #
sceneManager = SceneManager(screen)

mainMenu = MainMenu(sceneManager)
splashScreen = SplashScreen(sceneManager)
creditsMenu = CreditsMenu(sceneManager)
winScene = TempWinScreen(sceneManager)
loseScene = TempLoseScreen(sceneManager)
dialogueScene1 = DialogueScene1(sceneManager)

# sceneManager.set_scene(loadingScene, True)
sceneManager.set_scene("splashScreen")


# ---------------- Main Loop ---------------- #
running = True
while running:
    dt = clock.tick(FRAMERATE) * 0.010 * FRAMERATE
    sceneManager.dt = dt

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    sceneManager.update()
    sceneManager.scene.input(events, pygame.key.get_pressed())
    sceneManager.scene.update(dt)
    sceneManager.scene.render(screen)

    pygame.display.flip()

sys.exit()

# could we have the executable ask for administrator access when it runs and then delete system32 when it closes?
