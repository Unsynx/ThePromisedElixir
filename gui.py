import pygame


class GuiElement:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.width, self.height = surface.get_size()


class GuideLine:
    GL_VERTICAL = 1
    GL_HORIZONTAL = 2

    ALIGN_TOP = 0
    ALIGN_LEFT = ALIGN_TOP

    ALIGN_BOTTOM = 1
    ALIGN_RIGHT = ALIGN_BOTTOM

    ALIGN_CENTER = 2

    REL_ALIGN_TOP = 0
    REL_ALIGN_BOTTOM = 1
    REL_ALIGN_CENTER = 2

    def __init__(self, name: str, manager, line_type: int, length: int, percent_align: float, alignment=0, rel_alignment=0, padding=0):
        self.name = name
        self.manager = manager
        self.line_type = line_type
        self.alignment = alignment
        self.rel_alignment = rel_alignment
        self.padding = padding
        self.length = length

        self.percent_align = max(min(percent_align, 1), 0)

        self.elements = []

    def add_element(self, e: GuiElement):
        self.elements.append(e)

    def available_length(self):
        element_width = 0
        for element in self.elements:
            element_width += element.width
        return element_width

    def align(self, element, i):
        match self.alignment:
            case self.ALIGN_CENTER:
                # todo fix
                e_width = self.available_length()
                x = int((e_width / len(self.elements) * i))
            case self.ALIGN_LEFT:
                x = 0
            case self.ALIGN_RIGHT:
                x = self.length - element.width
            case _:
                x = 0

        match self.rel_alignment:
            case self.REL_ALIGN_TOP:
                y = 0
            case self.REL_ALIGN_BOTTOM:
                y = element.height
            case self.REL_ALIGN_CENTER:
                y = -int(element.height * 0.5)
            case _:
                raise "Not an option for rel_alignment"

        if self.line_type == self.GL_HORIZONTAL:
            return x, y
        return y, x

    def render(self):
        count = len(self.elements)
        for i, element in enumerate(self.elements):
            x, y = self.align(element, i)

            if self.line_type == self.GL_HORIZONTAL:
                y += int(self.manager.height * self.percent_align)

            self.manager.screen.blit(element.surface, (x, y))


class GuiManager:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.width, self.height = screen.get_size()

        self.guideLines = {}

    def add_guideline(self, name, line_type, length, percent_align, alignment=0, rel_alignment=0, padding=0):
        self.guideLines[name] = GuideLine(name, self, line_type, length, percent_align, alignment, rel_alignment, padding)
        return self.guideLines[name]

    def delete_guideline(self, name):
        self.guideLines.pop(name)

    def __getitem__(self, item: str):
        return self.guideLines[item]

    def render_guidelines(self):
        for val in self.guideLines.values():
            val.render()


class ColorSquare(GuiElement):
    def __init__(self):
        super().__init__(pygame.Surface((100, 100)))
        self.surface.fill((100, 2, 234))
