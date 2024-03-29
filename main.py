import pygame
import pygame.freetype
import random

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True
game_over = False


font = pygame.freetype.SysFont(pygame.font.get_default_font(), 32)

tile_gap = 15

starting_pos = (random.randint(0, screen.get_width()//tile_gap) * tile_gap, random.randint(0, screen.get_height()//tile_gap) * tile_gap)
movement = [1, 0]
snake_len = 4

apple_is_eaten = True

snake_arr = [pygame.Rect(starting_pos[0], starting_pos[1], tile_gap, tile_gap)]
for i in range(3):
    snake_arr.append(pygame.Rect(snake_arr[-1].x - tile_gap, snake_arr[-1].y, tile_gap, tile_gap))

def apple_gen():
    return (random.randint(1, screen.get_width()//tile_gap - 1) * tile_gap, random.randint(1, screen.get_height()//tile_gap - 1) * tile_gap)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and game_over:
        snake_len = 4
        game_over = False
    if keys[pygame.K_UP] and movement[1] != 1:
        movement = [0, -1]
    if keys[pygame.K_DOWN] and movement[1] != -1:
        movement = [0, 1]
    if keys[pygame.K_RIGHT] and movement[0] != -1:
        movement = [1, 0]
    if keys[pygame.K_LEFT] and movement[0] != 1:
        movement = [-1, 0]

    screen.fill(pygame.Color(0, 0, 0))

    for i in range(1, screen.get_width()//tile_gap):
        pygame.draw.line(screen, pygame.Color(255, 255, 255), (i*tile_gap, 0), (i*tile_gap, screen.get_height()))
    
    for i in range(1, screen.get_height()//tile_gap):
        pygame.draw.line(screen, pygame.Color(255, 255, 255), (0, i*tile_gap), (screen.get_width(), i*tile_gap))

    if apple_is_eaten:
        apple_pos = apple_gen()
        apple = pygame.Rect(apple_pos[0], apple_pos[1], tile_gap, tile_gap)
        apple_is_eaten = False
    
    pygame.draw.rect(screen, pygame.Color(255,0,0), apple, width=0)
    new_snake_part = pygame.Rect(snake_arr[0].x + movement[0] * tile_gap, snake_arr[0].y + movement[1] * tile_gap, tile_gap, tile_gap)
    snake_arr.insert(0, new_snake_part)
    while len(snake_arr) > snake_len:
        snake_arr.pop()
    for snake_part in snake_arr:
        pygame.draw.rect(screen, pygame.Color(0, 255, 0), snake_part, width=0)
    
    if game_over:
        continue

    if apple.colliderect(snake_arr[0]):
        snake_len += 1
        apple_is_eaten = True
    
    if snake_arr[0].x < 0:
        snake_arr[0].x = screen.get_width()
    if snake_arr[0].x > screen.get_width():
        snake_arr[0].x = 0
    if snake_arr[0].y < 0:
        snake_arr[0].y = screen.get_height()
    if snake_arr[0].y > screen.get_height():
        snake_arr[0].y = 0
    
    for i in range(1, len(snake_arr)):
        if snake_arr[0].colliderect(snake_arr[i]):
            game_over = True
    
    text_surface_score, rect_score = font.render("Score: " + str(snake_len - 4), (255, 255, 0))
    if game_over:
        text_surface_gameover, rect_gameover = font.render("GAME OVER", (255, 0, 0), size= 64)
        text_surface_tip, rect_tip = font.render("Press space to play again", (255, 255, 0), size= 32)
        screen.blit(text_surface_gameover, text_surface_gameover.get_rect(center = screen.get_rect().center))
        screen.blit(text_surface_tip, (text_surface_tip.get_rect(center = screen.get_rect().center).x, text_surface_tip.get_rect(center = screen.get_rect().center).y + tile_gap * 4))
    screen.blit(text_surface_score, (15, 15))

    pygame.display.update()
    clock.tick(15)


pygame.quit()