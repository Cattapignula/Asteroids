import pygame

class Score:
    def __init__(self):
        self.value = 0
        self.font = pygame.font.SysFont("monospace", 35)

    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.value}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    def increment(self, points):
        self.value += points