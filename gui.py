import pygame


class Align:
    W_LEFT = -1
    W_MIDDLE = 0
    W_RIGHT = 1
    H_BOTTOM = -1
    H_MIDDLE = 0
    H_TOP = 1


class GuiBase:
    def __init__(self, surface: pygame.Surface, x: int, y: int, align_w=Align.W_LEFT, align_h=Align.H_TOP):
        self.surface = surface
        self.children = []

        self.x = x
        self.y = y

        self.align_w = align_w
        self.align_h = align_h

    # This function should contain all the graphics
    def draw(self):
        pass

    def render(self):
        self.draw()

        for child in self.children:
            child.render()

            # todo: change these to adjust for the size of the surface
            if child.align_w == Align.W_LEFT:
                x = 0
            elif child.align_w == Align.W_MIDDLE:
                x = child.surface.get_width() * 0.5
            elif child.align_w == Align.W_RIGHT:
                x = child.surface.get_width()
            else:
                raise "Invalid alignment in GUI Element"

            if child.align_h == Align.H_TOP:
                y = 0
            elif child.align_w == Align.W_MIDDLE:
                y = child.surface.get_height() * 0.5
            elif child.align_w == Align.W_RIGHT:
                y = child.surface.get_height()
            else:
                raise "Invalid alignment in GUI Element"

            self.surface.blit(child.surface, (x, y))

    def __iadd__(self, other):
        self.children.append(other)

    def add_container(self, width_percentage, height_percentage, align_w, align_h):
        container_surface = pygame.Surface(self.surface.get_width() * width_percentage, self.surface.get_height() * height_percentage)
        self.children.append(GuiBase(container_surface, align_w, align_h))
        return len(self.children)

    def remove_element(self):
        pass # todo: implement


class GuiManager(GuiBase):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen, 0, 0)




