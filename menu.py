from scene_manager import Scene, SceneManager
import pygame


class MainMenu(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "mainMenu")
        self.sceneManager = manager

    def update(self):
        # This is runs every frame
        print("Menu")

    def render(self, screen):
        pygame.draw.rect(screen, (0, 100, 0), (0, 0, 100, 100))


class SplashScreen(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager, "splashScreen")
        self.sceneManager = manager

    def update(self):
        print("Splash")

        self.sceneManager.set_scene("mainMenu")

    def render(self, screen: pygame.Surface):
        screen.fill(())
