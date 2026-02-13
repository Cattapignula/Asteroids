import pygame
import os

class Score:
    def __init__(self):
        self.value = 0
        self.file_path = "highscore.txt"
        self.high_score = self.load_high_score()
        self.font = pygame.font.SysFont("monospace", 35)

    def load_high_score(self):
        if not os.path.exists(self.file_path):
            return 0
        try:
            with open(self.file_path, "r") as f:
                return int(f.read())
        except (ValueError, IOError):
            return 0

    def save_high_score(self):
        if self.value > self.high_score:
            self.high_score = self.value
            with open(self.file_path, "w") as f:
                f.write(str(self.value))

    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.value}", True, "white")
        high_text = self.font.render(f"High: {self.high_score}", True, "gold")
        screen.blit(score_text, (10, 10))
        screen.blit(high_text, (10, 50))

    def increment(self, points):
        self.value += points