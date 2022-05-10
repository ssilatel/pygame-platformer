import pygame
import sys
import engine as e

clock = pygame.time.Clock()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
scroll = [0, 0]


game_map = e.load_map("test_map.txt")
dirt_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
dirt_img.fill((100, 100, 100))
player = e.Player(300, 800, TILE_SIZE // 2, TILE_SIZE // 2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.moving_left = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.moving_right = True
            if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
                if player.air_timer < 6:
                    player.y_momentum = -20
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.moving_left = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.moving_right = False

    screen.fill((0, 0, 0))

    scroll[0] += (player.rect.x - scroll[0] - ((SCREEN_WIDTH // 2) - (TILE_SIZE // 4))) // 10
    scroll[1] += (player.rect.y - scroll[1] - ((SCREEN_HEIGHT // 2) - (TILE_SIZE // 4))) // 10

    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == "1":
                screen.blit(dirt_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile != "0":
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1
    
    player.update(tile_rects)
    player.draw(screen, scroll)
    
    pygame.display.update()
    clock.tick(60)