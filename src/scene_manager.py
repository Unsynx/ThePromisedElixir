import pygame
import time


class SceneManager:
    def __init__(self, screen: pygame.Surface):
        self.sceneManager = self

        self.scene = None
        self.sceneDict = {}

        self.dt = None
        self.screen = screen

        self.queue = []
        self.queue_timer = []
        self.queue_args = []

    def add_to_queue(self, func, delay, *args):
        self.queue.append(func)
        self.queue_timer.append(time.time() + delay)
        self.queue_args.append(args)

    def remove_from_queue(self, i):
        self.queue.pop(i)
        self.queue_timer.pop(i)
        self.queue_args.pop(i)

    def add_scene(self, scene):
        self.sceneDict[scene.name] = scene

    def update(self):
        delete = []
        for i, timer in enumerate(self.queue_timer):
            if time.time() > timer:
                self.queue[i](*self.queue_args[i])
                delete.append(i)
        delete.reverse()
        for i in delete:
            self.remove_from_queue(i)

    def del_scene(self, scene):
        try:
            self.sceneDict.pop(scene)
        except KeyError:
            print(f"No scene of key {scene}")

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
