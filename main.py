import pygame
import sys
import engine as e
import math

clock = pygame.time.Clock()
pygame.font.init()
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 360
TILE_SIZE = 32
display_surf = pygame.display.set_mode((SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2), 0, 32)
screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
scroll = [0, 0]
game_map = e.load_map("test_map.txt")
MAP_SIZE = int(len(game_map))
dirt_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
dirt_img.fill((100, 100, 100))
player = e.Player(2 * TILE_SIZE, 11 * TILE_SIZE, TILE_SIZE // 2, TILE_SIZE // 2)

class Watcher:
    def __init__(self, pos):
        self.pos = pos
        self.angle = math.pi * 2
        self.fov = math.pi / 2
        self.half_fov = self.fov / 2
        self.casted_rays = 42
        self.max_depth = int(MAP_SIZE * TILE_SIZE)
        self.step_angle = self.fov / self.casted_rays
    
    def draw(self):
        pygame.draw.circle(screen, (255, 255, 255), (self.pos[0] - scroll[0], self.pos[1] - scroll[1]), 10, 0, False, False, True, True)
    
    def watch(self, mode):
        if mode == "debug":
            pygame.draw.line(screen, (255, 0, 0), (self.pos[0] - scroll[0], self.pos[1] - scroll[1]), ((self.pos[0] - math.sin(self.angle) * 500) - scroll[0], (self.pos[1] + math.cos(self.angle) * 500) - scroll[1]))
            pygame.draw.line(screen, (255, 0, 0), (self.pos[0] - scroll[0], self.pos[1] - scroll[1]), ((self.pos[0] - math.sin(self.angle - self.half_fov) * 500) - scroll[0], (self.pos[1] + math.cos(self.angle - self.half_fov) * 500) - scroll[1]))
            pygame.draw.line(screen, (255, 0, 0), (self.pos[0] - scroll[0], self.pos[1] - scroll[1]), ((self.pos[0] - math.sin(self.angle + self.half_fov) * 500) - scroll[0], (self.pos[1] + math.cos(self.angle + self.half_fov) * 500) - scroll[1]))

        targets = []
        starting_angle = (self.angle - self.half_fov) + (self.step_angle / 2)
        for ray in range(self.casted_rays):
            for depth in range(self.max_depth):
                target_x = self.pos[0] - math.sin(starting_angle) * depth
                target_y = self.pos[1] + math.cos(starting_angle) * depth

                col = int(target_x / TILE_SIZE)
                row = int(target_y / TILE_SIZE)

                if game_map[row][col] == "1":
                    if mode == "debug":
                        pygame.draw.line(screen, (255, 0, 0), (self.pos[0] - scroll[0], self.pos[1] - scroll[1]), (target_x - scroll[0], target_y - scroll[1]))
                    targets.append([target_x - scroll[0], target_y - scroll[1]])
                    break
            starting_angle += self.step_angle
        pygame.draw.polygon(screen, (255, 255, 167), [[self.pos[0] - scroll[0], self.pos[1] - scroll[1]], *targets])

w1 = Watcher([12 * TILE_SIZE, 9 * TILE_SIZE])
w2 = Watcher([53 * TILE_SIZE, 7 * TILE_SIZE])
w3 = Watcher([23 * TILE_SIZE, 2 * TILE_SIZE])
w4 = Watcher([7 * TILE_SIZE, 3 * TILE_SIZE])
watchers = [w1, w2, w3, w4]

def restart():
    player.rect.x = 2 * TILE_SIZE
    player.rect.y = 11 * TILE_SIZE
    player.movement = [0, 0]

def game_loop():
    mode = "prod"
    running = True
    while running:
        screen.fill((0, 0, 0))

        scroll[0] += (player.rect.x - scroll[0] - ((SCREEN_WIDTH // 2) - (TILE_SIZE // 4))) // 10
        scroll[1] += (player.rect.y - scroll[1] - ((SCREEN_HEIGHT // 2) - (TILE_SIZE // 4))) // 10

        for w in watchers:
            w.draw()
            w.watch(mode)

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
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.moving_left = False
                    player.moving_right = True
                if (event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE):
                    if player.air_timer < 6 and not player.jumping:
                        player.y_momentum -= player.jump_height
                        player.jumping = True
                if event.key == pygame.K_r:
                    restart()
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
        
        surf = pygame.transform.scale(screen, (screen.get_width() * 2, screen.get_height() * 2))
        display_surf.blit(surf, (0, 0, surf.get_width(), surf.get_height()))

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
    options = [["PLAY", 40], ["OPTIONS", 30], ["QUIT", 30]]
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
        
        surf = pygame.transform.scale(screen, (screen.get_width() * 2, screen.get_height() * 2))
        display_surf.blit(surf, (0, 0, surf.get_width(), surf.get_height()))

        pygame.display.update()
        clock.tick(60)

def pause_menu():
    options = [["RESUME", 40], ["OPTIONS", 30], ["QUIT", 30]]
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
        
        surf = pygame.transform.scale(screen, (screen.get_width() * 2, screen.get_height() * 2))
        display_surf.blit(surf, (0, 0, surf.get_width(), surf.get_height()))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
