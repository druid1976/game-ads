import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 500
HEIGHT = 500
CELL_SIZE = 50
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

# Constants for health bar and item bag
BAR_HEIGHT = 20  # Height of the health bar
BAG_HEIGHT = 20  # Height of the item bag
HEALTH_BAR_COLOR = (0, 255, 0)  # Color of the health bar
BAG_COLOR = (255, 255, 0)  # Color of the item bag
MAX_HEALTH = 100
player_health = MAX_HEALTH
player_items = ["Item 1", "Item 2", "Item 3"]  # Example items


# Create the game window with extended height   
SCREEN_HEIGHT = HEIGHT + BAR_HEIGHT + BAG_HEIGHT
screen = pygame.display.set_mode((WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Game")

# Function to draw health bar
def draw_health_bar():
    health_bar_width = player_health / MAX_HEALTH * WIDTH
    pygame.draw.rect(screen, HEALTH_BAR_COLOR, (0, HEIGHT, health_bar_width, BAR_HEIGHT))

# Function to draw item bag
def draw_item_bag():
    item_str = ", ".join(player_items)
    font = pygame.font.Font(None, 24)
    text = font.render("Items: " + item_str, True, BAG_COLOR)
    text_rect = text.get_rect()
    text_rect.bottomright = (WIDTH, HEIGHT + BAR_HEIGHT + BAG_HEIGHT)
    screen.blit(text, text_rect)





# Load images
player_img = pygame.image.load("images/Hero.png")
player_img = pygame.transform.scale(player_img, (CELL_SIZE, CELL_SIZE))

mob_img = pygame.image.load("images/egg/skeleton-animation_18.png")
mob_img = pygame.transform.scale(mob_img, (CELL_SIZE, CELL_SIZE))

wall_img = pygame.image.load("images/Wall.png")
wall_img = pygame.transform.scale(wall_img, (CELL_SIZE, CELL_SIZE))

floor_image = pygame.image.load("images/Floor.png")

sword_img = pygame.image.load("images/Sword.png")
key_img = pygame.image.load("images/Key.png")
door_img = pygame.image.load("images/DoorClosed.png")

# Load map data from file
def load_map(file_name):
    with open(file_name, "r") as file:
        map_data = [line.strip() for line in file]
    return map_data

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Game")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def move(self, dx, dy):
        new_rect = self.rect.move(dx, dy)
        if not any(wall.rect.colliderect(new_rect) for wall in walls):
            self.rect = new_rect

# Mob class
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = mob_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.move_timer = 0

    def move_towards_player(self, player):
        if pygame.time.get_ticks() - self.move_timer > 200:  # Adjust speed here (200 milliseconds = 0.2 seconds)
            dx = player.rect.x - self.rect.x
            dy = player.rect.y - self.rect.y
            dist = math.hypot(dx, dy)
            if dist > CELL_SIZE:  # Only move if distance is greater than one cell size
                dx = dx / dist
                dy = dy / dist
                new_rect = self.rect.move(dx * CELL_SIZE, dy * CELL_SIZE)
                if not any(wall.rect.colliderect(new_rect) for wall in walls):
                    self.rect = new_rect
            self.move_timer = pygame.time.get_ticks()


# Item class
class Item(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Door class
class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = door_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Wall class
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = wall_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Function to create the map based on map data
def create_map(map_data):
    walls = pygame.sprite.Group()
    items = pygame.sprite.Group()
    doors = pygame.sprite.Group()
    player = None
    mob = None
    for y, line in enumerate(map_data):
        for x, char in enumerate(line):
            if char == "#":
                wall = Wall(x * CELL_SIZE, y * CELL_SIZE)
                walls.add(wall)
            elif char == "P":
                player = Player(x * CELL_SIZE, y * CELL_SIZE)
            elif char == "M":
                mob = Mob(x * CELL_SIZE, y * CELL_SIZE)
            elif char == "S":
                sword = Item(sword_img, x * CELL_SIZE, y * CELL_SIZE)
                items.add(sword)
            elif char == "K":
                key = Item(key_img, x * CELL_SIZE, y * CELL_SIZE)
                items.add(key)
            elif char == "D":
                door = Door(x * CELL_SIZE, y * CELL_SIZE)
                doors.add(door)
    return walls, items, doors, player, mob

# Load map data from file
map_data = load_map("maps/map0.txt")

# Create the map
walls, items, doors, player, mob = create_map(map_data)

# Initialize the sprite group
all_sprites = pygame.sprite.Group()

# Add player and mob to the sprite group if they are not None
if player:
    all_sprites.add(player)
if mob:
    all_sprites.add(mob)

# Game loop
clock = pygame.time.Clock()
running = True
player_moved = False  # Flag to track if the player has moved

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move(-CELL_SIZE, 0)
                player_moved = True
            elif event.key == pygame.K_RIGHT:
                player.move(CELL_SIZE, 0)
                player_moved = True
            elif event.key == pygame.K_UP:
                player.move(0, -CELL_SIZE)
                player_moved = True
            elif event.key == pygame.K_DOWN:
                player.move(0, CELL_SIZE)
                player_moved = True

    # Move mob towards player if player moved
    if player_moved:
        if mob:
            mob.move_towards_player(player)
        player_moved = False  # Reset player moved flag after mob has moved

    # Draw everything
    screen.fill(WHITE)
    screen.blit(floor_image, (0, 0))
    # Draw walls
    for wall in walls:
        screen.blit(wall.image, wall.rect)
    # Draw items
    for item in items:
        screen.blit(item.image, item.rect)
    # Draw doors
    for door in doors:
        screen.blit(door.image, door.rect)
    # Draw player and mob
    # Draw player and mob
    all_sprites.draw(screen)
    # Draw health bar
    draw_health_bar()
    # Draw item bag
    draw_item_bag()
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(10)

# Quit Pygame
pygame.quit()
sys.exit()
