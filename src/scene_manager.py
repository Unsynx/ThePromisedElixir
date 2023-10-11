import pygame


class SceneManager:
    def __init__(self, screen: pygame.Surface):
        self.sceneManager = self

        self.scene = None
        self.sceneDict = {}

        self.dt = None
        self.screen = screen

    def add_scene(self, scene):
        self.sceneDict[scene.name] = scene

    def set_scene(self, scene, *args):
        if self.scene is not None:
            self.scene.on_scene_end()
          
        if type(scene) is str:
            # When scene name entered
            self.sceneDict[scene].on_scene_end()
            self.scene = self.sceneDict[scene]
        else:
            # When scene object passed
            scene.on_scene_end()
            self.scene = scene

        self.scene.on_scene_start(*args)


class Scene:
    def __init__(self, manager: SceneManager, name: str):
        self.sceneManager = manager
        self.name = name
        self.screen = manager.screen

        self.sceneManager.add_scene(self)

    def on_scene_end(self):
        pass

    def on_scene_start(self, *args):
        pass

    def input(self, events, pressed_keys):
        pass

    def update(self, dt: float):
        pass

    def render(self, screen: pygame.Surface):
        pass
