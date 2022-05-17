import pygame

def load_map(path):
    f = open(path, "r")
    data = f.read()
    f.close()
    data = data.split("\n")
    game_map = []
    for line in data:
        game_map.append(list(line))
    return game_map

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

# def nearby_tiles(x,y,tiles):
#     x_loc = int(round(x/32,0))
#     y_loc = int(round(y/32,0))
#     tile_list = []
#     for y in range(3):
#         for x in range(3):
#             loc = str(x_loc+x-1) + ';' + str(y_loc+y-1)
#             if loc in tiles:
#                 for tile in tiles[loc][0]:
#                     if tile[:-4] in collision_types:
#                         tile_list.append([tiles[loc][1]*32,tiles[loc][2]*32,32,32])
#                         break
#     return tile_list

def move(rect, movement, tiles, mode, screen, scroll):
    collision_types = {"top": False, "bottom": False, "left": False, "right": False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] < 0:
            rect.left = tile.right
            collision_types["left"] = True
            if mode == "debug":
                pygame.draw.rect(screen, (255, 0, 0), (tile.x - scroll[0], tile.y - scroll[1], tile.w, tile.h))
        elif movement[0] > 0:
            rect.right = tile.left
            collision_types["right"] = True
            if mode == "debug":
                pygame.draw.rect(screen, (255, 0, 0), (tile.x - scroll[0], tile.y - scroll[1], tile.w, tile.h))
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] < 0:
            rect.top = tile.bottom
            collision_types["top"] = True
            if mode == "debug":
                pygame.draw.rect(screen, (255, 0, 0), (tile.x - scroll[0], tile.y - scroll[1], tile.w, tile.h))
        elif movement[1] > 0:
            rect.bottom = tile.top
            collision_types["bottom"] = True
            if mode == "debug":
                pygame.draw.rect(screen, (255, 0, 0), (tile.x - scroll[0], tile.y - scroll[1], tile.w, tile.h))
    return collision_types

class Player():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill((116, 1, 113))
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.movement = [0, 0]
        self.speed = 5
        self.moving_left = False
        self.moving_right = False
        self.jumping = False
        self.y_momentum = 0
        self.air_timer = 0
    
    
    def update(self, tiles, mode, screen, scroll):
        self.movement = [0, 0]
        if self.moving_left:
            self.movement[0] -= self.speed
        elif self.moving_right:
            self.movement[0] += self.speed
        self.movement[1] += self.y_momentum
        self.y_momentum += 1.5
        if self.y_momentum > 8:
            self.y_momentum = 8
        
        collisions = move(self.rect, self.movement, tiles, mode, screen, scroll)
        if collisions["bottom"]:
            self.jumping = False
            self.y_momentum = 1
            self.air_timer = 0
        else:
            self.air_timer += 1
        if collisions["top"]:
            self.y_momentum = 0

    def draw(self, screen, scroll):
        screen.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))