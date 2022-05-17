#============================================================================================

import pygame, random
pygame.init()

#============================================================================================

# Variables #

# Display Surface
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake")

# Set Clock
FPS = 20
clock = pygame.time.Clock() # Similar to fixed time

# In Game
SNAKE_SIZE = 20
head_x = WINDOW_WIDTH / 2
head_y = WINDOW_HEIGHT / 2 + 100
snake_dx = 0
snake_dy = 0
score = 0

# Colors
GREEN = (0, 255, 0)
DARKGREEN = (0, 50, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARKRED = (150, 0, 0)
WHITE = (255, 255, 255) 

# Texts
font = pygame.font.SysFont("gabriola", 48)

score_text = font.render("Score: " + str(score), True, BLUE)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

game_over_text = font.render("GAMEOVER", True, RED)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

continue_text = font.render("Press any key to play again", True, RED)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 64)

#Set sound and music
pickup_sound = pygame.mixer.Sound("assets/pickup.wav")

#Set images
apple_coord = (500, 500, SNAKE_SIZE, SNAKE_SIZE)
apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)

head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)

body_cords = []

#============================================================================================

# Game Loop
running = True
while running:
    # Check if its quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if snake_dx != 1 * SNAKE_SIZE:
                    snake_dx = -1 * SNAKE_SIZE
                    snake_dy = 0
            if event.key == pygame.K_RIGHT:
                if snake_dx != -1 * SNAKE_SIZE:
                    snake_dx = 1 * SNAKE_SIZE
                    snake_dy = 0
            if event.key == pygame.K_UP:
                if snake_dy != 1 * SNAKE_SIZE:
                    snake_dx = 0
                    snake_dy = -1 * SNAKE_SIZE
            if event.key == pygame.K_DOWN:
                if snake_dy != -1 * SNAKE_SIZE:
                    snake_dx = 0
                    snake_dy = 1 * SNAKE_SIZE

    # Add head to body list
    body_cords.insert(0, head_coord)
    body_cords.pop()

    # Move snake
    head_x += snake_dx
    head_y += snake_dy
    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

    # Check game over
    if head_rect.left < 0 or head_rect.right > WINDOW_WIDTH or head_rect.top < 0 or head_rect.bottom > WINDOW_HEIGHT or head_coord in body_cords:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()
        
        #Pause until input
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                
                if event.type == pygame.KEYDOWN:
                    score = 0
                    head_x = WINDOW_WIDTH / 2
                    head_y = WINDOW_HEIGHT / 2 + 100
                    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
                    body_cords = []
                    snake_dx = 0
                    snake_dy = 0
                    is_paused = False
                
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    # Check collsion
    if head_rect.colliderect(apple_rect):
        score += 1
        pickup_sound.play()
        apple_x = random.randint(0, WINDOW_WIDTH - SNAKE_SIZE)
        apple_y = random.randint(0, WINDOW_HEIGHT - SNAKE_SIZE)
        apple_coord = (apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE)
        body_cords.append(head_coord)

    # Update HUD
    score_text = font.render("Score: " + str(score), True, BLUE)

    # Fill surface
    display_surface.fill(WHITE)

    # Blit HUD
    display_surface.blit(score_text, score_rect)

    # Blit assets
    for body in body_cords:
        pygame.draw.rect(display_surface, DARKGREEN, body)
        
    head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)
    apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)

    # Update
    pygame.display.update()
    clock.tick(FPS)

# End game
pygame.quit()