import pygame


class GuiElement:
    def __init__(self, surface: pygame.Surface):
        """
        GUI element base class

        :param surface:
        """

        self.surface = surface
        self.width, self.height = surface.get_size()
        self.hovered = False

        self.x = 0
        self.y = 0

    def get_dim(self, dim, other=False):
        if dim == GuideLine.GL_HORIZONTAL:
            if other:
                return self.height
            return self.width
        if other:
            return self.width
        return self.height

    def update(self):
        pass

    def is_hovered(self, x, y):
        self.x = x
        self.y = y

        self.hovered = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.x < mouse_x < self.x + self.width:
            if self.y < mouse_y < self.y + self.height:
                self.hovered = True


class GuideLine:
    GL_VERTICAL = 1
    GL_HORIZONTAL = 2

    ALIGN_TOP = 0
    ALIGN_LEFT = ALIGN_TOP
    ALIGN_BOTTOM = 1
    ALIGN_RIGHT = ALIGN_BOTTOM
    ALIGN_CENTER_PADDED = 2
    # ALIGN_CENTER_EQUAL = 3

    REL_ALIGN_TOP = 0
    REL_ALIGN_LEFT = REL_ALIGN_TOP
    REL_ALIGN_BOTTOM = 1
    REL_ALIGN_RIGHT = REL_ALIGN_BOTTOM
    REL_ALIGN_CENTER = 2

    def __init__(self, name: str, manager, line_type: int, percent_align: float, alignment: int, rel_alignment: int, padding: int):
        """
        Elements can be placed on the GuideLine to align them in certain ways.

        :param name: A string which you can use to reference a GuideLine object from the GuiManager class
        :param manager: The main GuiManager instance
        :param line_type: Either a vertical (GL_VERTICAL) or horizontal line (GL_HORIZONTAL)
        :param percent_align: A float between 0 to 1 which positions the line relative to the screen size
        :param alignment: Determines how the elements on the line will be aligned. ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER_PADDED, ALIGN_TOP, and ALIGN_BOTTOM
        :param rel_alignment: How the elements will be placed on the line. REL_ALIGN_TOP, REL_ALIGN_CENTER, REL_ALIGN_BOTTOM, REL_ALIGN_LEFT, and REL_ALIGN_RIGHT
        :param padding: How far apart GUI elements will be spaced
        """
        self.name = name
        self.manager = manager

        self.line_type = line_type
        self.alignment = alignment
        self.rel_alignment = rel_alignment
        self.padding = padding

        self.percent_align = max(min(percent_align, 1), 0)

        self.elements = []

    # todo: make it that you can delete elements
    def add_element(self, e: GuiElement):
        """
        Adds an element to be rendered to the GuideLine

        :rtype: object
        """
        self.elements.append(e)

    def render(self):
        elements_len = -self.padding
        for e in self.elements:
            elements_len += e.get_dim(self.line_type) + self.padding

        offset = 0
        for i, element in enumerate(self.elements):
            match self.alignment:
                case self.ALIGN_CENTER_PADDED:
                    x = int((self.manager.get_dim(self.line_type) - elements_len) * 0.5)
                    if i != 0:
                        offset += self.padding + self.elements[i-1].get_dim(self.line_type)

                case self.ALIGN_LEFT:
                    x = 0
                    if i != 0:
                        offset += self.padding + self.elements[i-1].get_dim(self.line_type)

                case self.ALIGN_RIGHT:
                    x = self.manager.get_dim(self.line_type) - element.get_dim(self.line_type)
                    if i != 0:
                        offset -= self.padding + self.elements[i-1].get_dim(self.line_type)

                case _:
                    raise "Not an option for: alignment"

            match self.rel_alignment:
                case self.REL_ALIGN_TOP:
                    y = -element.get_dim(self.line_type, True)

                case self.REL_ALIGN_BOTTOM:
                    y = 0

                case self.REL_ALIGN_CENTER:
                    y = -int(element.get_dim(self.line_type, True) * 0.5)

                case _:
                    raise "Not an option for: rel_alignment"

            if self.line_type == self.GL_HORIZONTAL:
                y += int(self.manager.get_dim(self.line_type, True) * self.percent_align)
                element.is_hovered(x + offset, y)
                element.update()
                self.manager.screen.blit(element.surface, (x + offset, y))
            else:
                y += int(self.manager.get_dim(self.line_type, True) * self.percent_align)
                element.is_hovered(y, x + offset)
                element.update()
                self.manager.screen.blit(element.surface, (y, x + offset))


class GuiManager:
    def __init__(self, screen: pygame.Surface):
        """
        The Class which renders, updates, and manages mouse interactions with GUI

        :param screen: The Surface all GUI elements will be rendered to
        """

        self.screen = screen
        self.width, self.height = screen.get_size()

        self.guideLines = {}

    def get_dim(self, dim, other=False):
        if dim == GuideLine.GL_HORIZONTAL:
            if other:
                return self.height
            return self.width
        if other:
            return self.width
        return self.height

    def add_guideline(self, guideline: GuideLine) -> GuideLine:
        """
        Adds a guideline which will be rendered

        :param guideline: A GuideLine object
        :return: A reference to the GuideLine you added to the manager
        """

        if guideline.manager is None:
            guideline.manager = self

        self.guideLines[guideline.name] = guideline
        return guideline

    def delete_guideline(self, item):
        """
        Deletes a GuideLine from the manager

        :param item: Either a GuideLine object or the name of the GuideLine
        """

        if type(input) is str:
            self.guideLines.pop(item)
        elif type(input) is GuideLine:
            self.guideLines.popitem(item)

    def __getitem__(self, item: str) -> GuideLine:
        """
        Returns a GuideLine object based on its name

        :param item: GuideLine name
        :return: GuideLine object
        """
        return self.guideLines[item]

    def render_guidelines(self):
        """
        Renders all GUI elements to the screen and runs each element's update function
        """
        for val in self.guideLines.values():
            val.render()


class ColorSquare(GuiElement):
    def __init__(self):
        super().__init__(pygame.Surface((100, 100)))
        self.surface.fill((100, 2, 234))

    def update(self):
        if self.hovered:
            self.surface.fill((142, 7, 16))
        else:
            self.surface.fill((100, 2, 234))


class ColorRect(GuiElement):
    def __init__(self):
        super().__init__(pygame.Surface((200, 100)))
        self.surface.fill((100, 100, 234))

    def update(self):
        if self.hovered:
            self.surface.fill((5, 78, 125))
        else:
            self.surface.fill((100, 100, 234))


class Button(GuiElement):
    def __init__(self, func):
        super().__init__(pygame.Surface((200, 100)))

        self.func = func

    def update(self):
        if self.hovered:
            self.surface.fill((110, 110, 110))
            if pygame.mouse.get_pressed()[0]:
                self.func()
        else:
            self.surface.fill((100, 100, 100))


class Image(GuiElement):
    def __init__(self, path: str):
        super().__init__(pygame.image.load(path))



