import pygame


class Button:
    def __init__(self, rect, text, callback, mode=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = pygame.font.SysFont("Arial", 20)
        self.base_color = (200, 200, 200)
        self.hover_color = (150, 150, 150)
        self.selected_color = (100, 100, 100)  # Darker color when selected.
        self.selected = False
        self.mode = mode  # Used for solver mode buttons.

    def draw(self, surface):
        # Use the selected color if selected; otherwise, use hover color if applicable.
        if self.selected:
            color = self.selected_color
        elif self.rect.collidepoint(pygame.mouse.get_pos()):
            color = self.hover_color
        else:
            color = self.base_color
        pygame.draw.rect(surface, color, self.rect)
        # Draw the text centered on the button.
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()
