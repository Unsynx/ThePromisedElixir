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

        self.hide = False

    def get_dim(self, dim, other=False):
        if dim == Guide.GL_HORIZONTAL:
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

    def set_value(self, value):
        pass


class Guide:
    GL_VERTICAL = 1
    GL_HORIZONTAL = 2

    ALIGN_TOP = 0
    ALIGN_LEFT = ALIGN_TOP
    ALIGN_BOTTOM = 1
    ALIGN_RIGHT = ALIGN_BOTTOM
    ALIGN_CENTER_PADDED = 2

    ALIGN_LEFT_PADDING = 4
    # ALIGN_CENTER_EQUAL = 3

    REL_ALIGN_TOP = 0
    REL_ALIGN_LEFT = REL_ALIGN_TOP
    REL_ALIGN_BOTTOM = 1
    REL_ALIGN_RIGHT = REL_ALIGN_BOTTOM
    REL_ALIGN_CENTER = 2

    def __init__(self, name: str, manager, line_type: int, percent_align: float, alignment: int, rel_alignment: int,
                 padding: int):
        """
        Elements can be placed on the Guide to align them in certain ways.

        :param name: A string which you can use to reference a Guide object from the GuiManager class
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

        self.offset_x = 0
        self.offset_y = 0

        self.elements = []

        self.hide = False

    # todo: make it that you can delete elements
    def add_element(self, e: GuiElement) -> GuiElement:
        """
        Adds an element to be rendered to the Guide

        :rtype: object
        :return: A reference to the Element
        """
        self.elements.append(e)
        return e

    def render(self):
        if self.hide:
            return

        elements_len = -self.padding
        for e in self.elements:
            elements_len += e.get_dim(self.line_type) + self.padding

        offset = 0
        for i, element in enumerate(self.elements):
            match self.alignment:
                case self.ALIGN_CENTER_PADDED:
                    x = int((self.manager.get_dim(self.line_type) - elements_len) * 0.5)

                case self.ALIGN_LEFT:
                    x = 0

                case self.ALIGN_RIGHT:
                    x = self.manager.get_dim(self.line_type) - elements_len

                case self.ALIGN_LEFT_PADDING:
                    x = self.padding
                case _:
                    raise "Not an option for: alignment"
            if i != 0:
                offset += self.padding + self.elements[i - 1].get_dim(self.line_type)

            match self.rel_alignment:
                case self.REL_ALIGN_TOP:
                    y = -element.get_dim(self.line_type, True)

                case self.REL_ALIGN_BOTTOM:
                    y = 0

                case self.REL_ALIGN_CENTER:
                    y = -int(element.get_dim(self.line_type, True) * 0.5)

                case _:
                    raise "Not an option for: rel_alignment"

            y += int(self.manager.get_dim(self.line_type, True) * self.percent_align)
            if self.line_type == self.GL_HORIZONTAL:
                final_x = x + offset + self.offset_x
                final_y = y + self.offset_y

            else:
                final_x = y + self.offset_x
                final_y = x + offset + self.offset_y

            element.is_hovered(final_x, final_y)
            element.update()
            if not element.hide:
                self.manager.screen.blit(element.surface, (final_x, final_y))


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
        if dim == Guide.GL_HORIZONTAL:
            if other:
                return self.height
            return self.width
        if other:
            return self.width
        return self.height

    def add_guideline(self, guideline: Guide) -> Guide:
        """
        Adds a guideline which will be rendered

        :param guideline: A Guide object
        :return: A reference to the Guide you added to the manager
        """

        if guideline.manager is None:
            guideline.manager = self

        self.guideLines[guideline.name] = guideline
        return guideline

    def delete_guideline(self, item):
        """
        Deletes a Guide from the manager

        :param item: Either a Guide object or the name of the Guide
        """

        if type(input) is str:
            self.guideLines.pop(item)
        elif type(input) is Guide:
            self.guideLines.popitem(item)

    def __getitem__(self, item: str) -> Guide:
        """
        Returns a Guide object based on its name

        :param item: Guide name
        :return: Guide object
        """
        return self.guideLines[item]

    def render_guidelines(self):
        """
        Renders all GUI elements to the screen and runs each element's update function
        """
        for val in self.guideLines.values():
            val.render()


class CornerSquare(GuiElement):
    STYLE_ORNATE = "../assets/gui/corners/StyleOrnateCorner.png"
    STYLE_SIMPLE = "../assets/gui/corners/StyleSimpleCorner.png"
    STYLE_SIMPLE_HOVERED = "../assets/gui/corners/StyleSimpleCornerHovered.png"

    def __init__(self, width: int, height: int, style: str):
        super().__init__(pygame.Surface((width, height)))
        self.corner_size = 0

        self.width = width
        self.height = height

        self.style = style

        self.draw()

    def draw(self):
        corner = pygame.image.load(self.style)
        self.corner_size = corner.get_width()

        # Draw corners
        # todo make better
        if self.style == self.STYLE_SIMPLE_HOVERED:
            self.surface.fill((62, 58, 95))
        else:
            self.surface.fill((34, 32, 53))

        pygame.draw.rect(self.surface, (255, 255, 255), self.surface.get_rect(), 4)
        self.surface.blit(corner, (0, 0))
        corner = pygame.transform.rotate(corner, 90)
        self.surface.blit(corner, (0, self.height - self.corner_size))
        corner = pygame.transform.rotate(corner, 90)
        self.surface.blit(corner, (self.width - self.corner_size, self.height - self.corner_size))
        corner = pygame.transform.rotate(corner, 90)
        self.surface.blit(corner, (self.width - self.corner_size, 0))

        # Make transparent
        self.surface.set_colorkey((255, 0, 255))


class Text(GuiElement):
    FONT_BASE = "../assets/gui/fonts/Pixellari.ttf"

    SIZE_MAIN = 36
    SIZE_HEADER = 48

    def __init__(self, text: str, font: str, font_size: int, color):
        self.text = text
        self.font = pygame.font.Font(font, font_size)
        self.color = color

        super().__init__(self.draw())

    def draw(self):
        return self.font.render(self.text, False, self.color)

    def set_value(self, value):
        self.text = value
        self.surface = self.draw()


class Button(GuiElement):
    def __init__(self, text, width, height, func, *args):
        super().__init__(pygame.Surface((width, height)))

        self.dummy_manager = GuiManager(self.surface)
        self.line = self.dummy_manager.add_guideline(
            Guide("dummy", None, Guide.GL_HORIZONTAL, 0.5, Guide.ALIGN_CENTER_PADDED, Guide.REL_ALIGN_CENTER, 0))

        self.back = CornerSquare(width, height, CornerSquare.STYLE_SIMPLE)
        self.back_hovered = CornerSquare(width, height, CornerSquare.STYLE_SIMPLE_HOVERED)
        self.line.add_element(Text(text, Text.FONT_BASE, Text.SIZE_MAIN, (255, 255, 255)))

        self.draw()

        self.func = func
        self.args = args

    def draw(self):
        self.surface.fill((255, 0, 255))
        self.surface.blit(self.back_hovered.surface if self.hovered else self.back.surface, (0, 0))
        self.dummy_manager.render_guidelines()
        self.surface.set_colorkey((255, 0, 255))

    def update(self):
        self.draw()
        if self.hovered:
            if pygame.mouse.get_pressed()[0]:
                self.func(*self.args)


class Image(GuiElement):
    def __init__(self, path: str):
        super().__init__(pygame.image.load(path))


class Grid(GuiElement):
    def __init__(self, width: int, height: int, rows: int):
        super().__init__(pygame.Surface((width, height)))

        self.back = CornerSquare(width, height, CornerSquare.STYLE_ORNATE)

        self.dummy_manager = GuiManager(self.surface)

        for i in range(rows):
            self.dummy_manager.add_guideline(
                Guide(f"row{i}", self.dummy_manager, Guide.GL_HORIZONTAL, 1.0 / rows * i, Guide.ALIGN_CENTER_PADDED,
                      Guide.REL_ALIGN_BOTTOM, 0))

        self.draw()

    def add_element(self, row: int, e: GuiElement):
        self.dummy_manager[f"row{row}"].add_element(e)
        self.draw()

    def __getitem__(self, row):
        return self.dummy_manager[f"row{row}"]

    def draw(self):
        self.surface.fill((255, 0, 255))
        self.surface.blit(self.back.surface, (0, 0))
        self.dummy_manager.render_guidelines()
        self.surface.set_colorkey((255, 0, 255))


class ProgressBar(GuiElement):
    BASIC = "../assets/gui/corners/SimpleFIllCorner.png"

    DEFAULT_BACK_COLOR = (34, 32, 53)

    def __init__(self, width: int, height: int, style: str, fill_color, back_color):
        super().__init__(pygame.Surface((width, height)))
        self.color = fill_color
        self.back_color = back_color

        self.corner = pygame.image.load(style)
        self.corner_size = self.corner.get_width()

        self.progress = 0.5
        self.render()

    def set_value(self, percent: float):
        self.progress = max(min(percent, 1), 0)
        self.render()

    def render(self):
        self.surface.fill(self.back_color)
        pygame.draw.rect(self.surface, self.color, pygame.Rect(0, 0, int(self.width * self.progress), self.height))
        pygame.draw.rect(self.surface, (255, 255, 255), self.surface.get_rect(), 4)

        corner = self.corner
        corner.set_colorkey((0, 255, 255))
        self.surface.blit(corner, (0, 0))
        corner = pygame.transform.rotate(self.corner, 90)
        corner.set_colorkey((0, 255, 255))
        self.surface.blit(corner, (0, self.height - self.corner_size))
        corner = pygame.transform.rotate(corner, 90)
        corner.set_colorkey((0, 255, 255))
        self.surface.blit(corner, (self.width - self.corner_size, self.height - self.corner_size))
        corner = pygame.transform.rotate(corner, 90)
        corner.set_colorkey((0, 255, 255))
        self.surface.blit(corner, (self.width - self.corner_size, 0))

        self.surface.set_colorkey((255, 0, 255))
