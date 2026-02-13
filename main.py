import pygame
import sys
from constants import *
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from score import Score
from lives import Lives
from particles import Particle

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    particles = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Particle.containers = (particles, updatable, drawable)

    asteroid_field = AsteroidField()
    score = Score()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    clock = pygame.time.Clock()
    dt = 0
    lives = Lives()
    is_game_over = False
    
    cred_font = pygame.font.SysFont("monospace", 10)
    cred_msg = cred_font.render("Made by Matteo the Awsome", True, "green")
    cred_msg_rect = cred_msg.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 30))

    go_font = pygame.font.SysFont("monospace", 50)
    go_msg = go_font.render("GAME OVER - Press R to Restart", True, "red")
    go_msg_rect = go_msg.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))


    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return     

        screen.fill("black")
        screen.blit(cred_msg, cred_msg_rect)
        
        updatable.update(dt)

        if not is_game_over:
            for obj in drawable:
                obj.draw(screen)
        else:
            screen.blit(go_msg, go_msg_rect)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                is_game_over = False
                lives.value = 3
                score.value = 0
                for asteroid in asteroids:
                    asteroid.kill()
                for shot in shots:
                    shot.kill()
                player.respawn()

        if not is_game_over:
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    for _ in range(15):
                        Particle(player.position.x, player.position.y, 2)
                    if player.invulnerable_timer <= 0:
                        lives.decrease()
                        if lives.value <= 0:
                            lives.value = 0
                            is_game_over = True
                            score.save_high_score()
                            print("Game over!")
                        else:
                            player.respawn()  
                   
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    for _ in range(15):
                        Particle(asteroid.position.x, asteroid.position.y, 2)
                    asteroid.split()
                    shot.kill()
                    if asteroid.radius > ASTEROID_MIN_RADIUS:
                        score.increment(100)
                    else:
                        score.increment(200)

        lives.draw(screen)
        score.draw(screen)
        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()


