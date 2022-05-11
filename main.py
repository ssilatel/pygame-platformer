import pygame
import sys
import engine as e
import math

clock = pygame.time.Clock()
pygame.font.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
scroll = [0, 0]

game_map = e.load_map("test_map.txt")
dirt_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
dirt_img.fill((100, 100, 100))
player = e.Player(100, 900, TILE_SIZE // 2, TILE_SIZE // 2)

def game_loop():
    mode = "prod"
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    player.moving_left = False
                    player.moving_right = False
                    pause_menu()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.moving_right = False
                    player.moving_left = True
                    player.facing_right = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.moving_left = False
                    player.moving_right = True
                    player.facing_right = True
                if (event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE):
                    if player.on_wall and player.jumping:
                        player.on_wall = False
                        player.y_momentum -= 20
                        player.jumping_timer = 0
                        if player.facing_right:
                            pass
                        else:
                            pass
                    if player.air_timer < 6 and not player.jumping:
                        player.y_momentum -= 20
                        player.jumping = True
                if event.key == pygame.K_r:
                    player.rect.x = 100
                    player.rect.y = 900
                    player.movement = [0, 0]
                if event.key == pygame.K_TAB:
                    if mode == "prod":
                        mode = "debug"
                    elif mode == "debug":
                        mode = "prod"
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
        
        player.update(tile_rects, mode, screen, scroll)
        player.draw(screen, scroll)
        
        pygame.display.update()
        clock.tick(60)

def draw_menu_font(x, y, size, text, color, selected):
    font = pygame.font.SysFont(None, size)
    font_img = font.render(text, True, color)
    size = font_img.get_size()
    screen.blit(font_img, (x - size[0] // 2, y - size[1] // 2))
    if selected:
        pygame.draw.rect(screen, (255, 255, 255), ((x - size[0] // 2) - 50 // 2, y - 5, 8, 8))

def main_menu():
    options = [["PLAY", 50], ["OPTIONS", 40], ["QUIT", 40]]
    selected_choice = 0
    choices = []
    for o in options:
        choices.append([o[0], False])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if choices[selected_choice][0] == "PLAY":
                        game_loop()
                    elif choices[selected_choice][0] == "QUIT":
                        pygame.quit()
                        sys.exit()
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected_choice -= 1
                    if (selected_choice) < 0:
                        selected_choice = len(choices) - 1
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected_choice += 1
                    if selected_choice > len(choices) - 1:
                        selected_choice = 0
        
        for c in choices:
            c[1] = False
        choices[selected_choice][1] = True
        
        screen.fill((80, 30, 80))

        for i, option in enumerate(options):
            draw_menu_font(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + (50 * i), option[1], option[0], (255, 255, 255), choices[i][1])

        pygame.display.update()
        clock.tick(60)

def pause_menu():
    options = [["RESUME", 50], ["OPTIONS", 40], ["QUIT", 40]]
    selected_choice = 0
    choices = []
    for o in options:
        choices.append([o[0], False])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_loop()
                if event.key == pygame.K_SPACE:
                    if choices[selected_choice][0] == "RESUME":
                        game_loop()
                    elif choices[selected_choice][0] == "QUIT":
                        pygame.quit()
                        sys.exit()
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected_choice -= 1
                    if (selected_choice) < 0:
                        selected_choice = len(choices) - 1
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected_choice += 1
                    if selected_choice > len(choices) - 1:
                        selected_choice = 0
        
        for c in choices:
            c[1] = False
        choices[selected_choice][1] = True
        
        screen.fill((60, 3, 95))

        for i, option in enumerate(options):
            draw_menu_font(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + (50 * i), option[1], option[0], (255, 255, 255), choices[i][1])

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()