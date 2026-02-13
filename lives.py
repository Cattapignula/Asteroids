import pygame

class Lives:
    def __init__(self):
        self.value = 3
        self.font = pygame.font.SysFont("monospace", 25)

    def draw(self, screen):
        lives_text = self.font.render(f"Lives: {self.value}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 90))

    def decrease(self):
        self.value -= 1