import pygame
import sys

clock = pygame.time.Clock()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
scroll = [0, 0]

def load_map(path):
    f = open(path, "r")
    data = f.read()
    f.close()
    data = data.split("\n")
    game_map = []
    for line in data:
        game_map.append(list(line))
    return game_map

game_map = load_map("test_map.txt")
dirt_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
dirt_img.fill((100, 100, 100))

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = TILE_SIZE // 2
        self.h = TILE_SIZE // 2
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill((175, 100, 175))
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.movement = [0, 0]
        self.moving_left = False
        self.moving_right = False
        self.y_momentum = 0
        self.air_timer = 0
    
    def move(self, tiles):
        collision_types = {"top": False, "bottom": False, "left": False, "right": False}
        self.rect.x += self.movement[0]
        hit_list = collision_test(self.rect, tiles)
        for tile in hit_list:
            if self.movement[0] < 0:
                self.rect.left = tile.right
                collision_types["left"] = True
            elif self.movement[0] > 0:
                self.rect.right = tile.left
                collision_types["right"] = True
        self.rect.y += self.movement[1]
        hit_list = collision_test(self.rect, tiles)
        for tile in hit_list:
            if self.movement[1] < 0:
                self.rect.top = tile.bottom
                collision_types["top"] = True
            elif self.movement[1] > 0:
                self.rect.bottom = tile.top
                collision_types["bottom"] = True
        return collision_types
    
    def update(self, tiles):
        self.movement = [0, 0]
        if self.moving_left:
            self.movement[0] -= 5
        elif self.moving_right:
            self.movement[0] += 5
        self.movement[1] += self.y_momentum
        self.y_momentum += 1.5
        if self.y_momentum > 8:
            self.y_momentum = 8
        
        collisions = self.move(tiles)
        if collisions["bottom"]:
            self.y_momentum = 1
            self.air_timer = 0
        else:
            self.air_timer += 1
        if collisions["top"]:
            self.y_momentum = 0
    
    def draw(self, screen, scroll):
        screen.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
    
    def set_pos(self, x, y):
        self.x = x
        self.y = y
    
    def get_pos(self):
        return [self.x, self.y]

player = Player(100, 800)

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