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
        self.surface.fill((25, 100, 7))
        # pass

    def render(self):
        self.draw()

        for child in self.children:
            child.render()

            if child.align_w == Align.W_LEFT:
                x = 0
            elif child.align_w == Align.W_MIDDLE:
                x = int((self.surface.get_width() - child.surface.get_width()) * 0.5)
            elif child.align_w == Align.W_RIGHT:
                x = int(self.surface.get_width() - child.surface.get_width())
            else:
                raise "Invalid alignment in GUI Element"

            if child.align_h == Align.H_TOP:
                y = 0
            elif child.align_h == Align.H_MIDDLE:
                y = int((self.surface.get_height() - child.surface.get_height()) * 0.5)
            elif child.align_h == Align.H_BOTTOM:
                y = int(self.surface.get_height() - child.surface.get_height())
            else:
                raise "Invalid alignment in GUI Element"

            self.surface.blit(child.surface, (x, y))

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __setitem__(self, key, value):
        pass

    def __getitem__(self, item):
        return self.children[item]

    def add_container(self, width_percentage, height_percentage, align_w, align_h):
        container_surface = pygame.Surface((self.surface.get_width() * width_percentage, self.surface.get_height() * height_percentage))
        self.children.append(GuiBase(container_surface, 0, 0, align_w, align_h))
        return len(self.children) - 1

    def remove_element(self):
        pass # todo: implement


class GuiManager(GuiBase):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen, 0, 0)

    def draw(self):
        pass


class Square(GuiBase):
    def __init__(self, width, height, color, x, y):
        super().__init__(pygame.Surface((width, height)), x, y)
        self.color = color
        self.width = width
        self.height = height

    def render(self):
        pygame.draw.rect(self.surface, self.color, (0, 0, self.width, self.height))
