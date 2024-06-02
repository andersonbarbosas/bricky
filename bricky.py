import pygame
from pygame import mixer
from pygame.locals import *
import random

mixer.init()
pygame.init()

# Variables
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bricky')
icon = pygame.image.load("img/1f410.png").convert_alpha()
pygame.display.set_icon(icon)
info_button = pygame.image.load('img/empty.png').convert_alpha()

# Sound
lose = pygame.mixer.Sound('sound/8-bit-cannon-fire-96505.mp3')
pygame.mixer.music.set_volume(0.1)
ping = pygame.mixer.Sound('sound/shooting-sound-fx-159024.mp3')
pygame.mixer.music.set_volume(0.1)
crash = pygame.mixer.Sound('sound/slimejump-6913.mp3')
pygame.mixer.music.set_volume(0.1)

# Fonts
game_font = pygame.font.Font("font/gomarice.ttf", 60)
score_font = pygame.font.Font("font/gomarice.ttf", 20)
info_font = pygame.font.Font("font/gomarice.ttf", 20)

# BG Settings
bg = (210, 210, 210)
 
# Bricks Colors
block_red = (240, 128, 128)
block_green = (72, 201, 176)
block_blue = (93, 173, 226)
block_hard = (230, 150, 220)

# Paddle Colors
paddle_col = (178, 186, 187)
paddle_outline = (107, 106, 107)

# Game Variables
cols = 7
rows = 9
clock = pygame.time.Clock()
FPS = 80
live_ball = False
game_over = 0

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Brick Wall Class <----------------------------------------------------------------------------------- WALL
class wall(): 
    def __init__(self):
        self.width = SCREEN_WIDTH // cols
        self.height = 25
    
    def create_wall(self):
        self.blocks = []
        # Define an empty list for ab individual block
        block_individual = []
        for row in range(rows):
            # Reset the block row list
            block_row = []
            # Iterate through each column in that row
            for col in range(cols):
                # Generate x and y positions for each block and create a rectangle from that
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                # Assign block strength based on row
                if row < 3:
                    strength = 3
                elif row < 6:
                    strength = 2
                elif row < 8:
                    strength = 1
                # Create a list at this point to store the rect and colour data
                block_individual = [rect, strength]
                # Append that individual block to the block row
                block_row.append(block_individual)
            # Append the row to the full list of blocks
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                # Assign a colour based on block strength
                if block[1] == 3:
                    block_col = block_blue
                elif block[1] == 2:
                    block_col = block_green
                elif block[1] == 1:
                    block_col = block_red
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, bg, (block[0]), 2, 7)
                pygame.draw.rect(screen, bg, (block[0]), 2, 1)

# Paddle Class <---------------------------------------------------------------------------------------- PADDLE
class paddle():
    def __init__(self):
       self.reset()

    def move(self):
        # Reset Movement Direction
        self.direction = 1
        key = pygame.key.get_pressed()
        if (key[pygame.K_LEFT] or key[pygame.K_d]) and self.rect.left > (0 + 2):
            self.rect.x -= self.speed
            self.direction = -1
        if (key[pygame.K_RIGHT] or key[pygame.K_a]) and self.rect.right < (SCREEN_WIDTH - 3):
            self.rect.x += self.speed
            self.direction = 1

    def draw(self): 
        pygame.draw.rect(screen, paddle_col, self.rect, 0, 20)
        pygame.draw.rect(screen, paddle_outline, self.rect, 2, 20)

    def reset(self):
        z = 10 # Usar essa variable para dificultar o game!!
        # Define paddle variables
        self.height = 20
        self.width = int(SCREEN_WIDTH / cols)
        self.x = int((SCREEN_WIDTH / 2) - (self.width / 2))
        self.y = SCREEN_HEIGHT - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x - (z//2), self.y, self.width + z, self.height) 
        self.direction = 0

# Ball Class <------------------------------------------------------------------------------------------ BALL
class game_ball():
    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):
        self.score = 0
        # Collision Threshold
        collision_thresh = 10

        # Start of with the assumption that the wall has been destroyed completely
        wall_destroyed = 1
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                # Check collision
                if self.rect.colliderect(item[0]):
                    # Check if collision was from above
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                        
                    # Check if collision was from below
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1 
                                               
                    # Check if collision was from left
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_y > 0:
                        self.speed_x *= -1
                        
                    # Check if collision was from right
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_y < 0:
                        self.speed_x *= -1
                        
                    # Reduce the block's strength by doing damage to it
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)
                        crash.play()
                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                    self.score += 1
                    
                # Increase item counter
                item_count += 1
                
            # Increase row counter
            row_count += 1

            score = (self.score - 63)
        draw_text(f"Score: {score * -1}", score_font, (50, 50, 50), (SCREEN_WIDTH - 80), 680)
        #draw_text("Info", info_font, (50, 50, 50), 15, 680)

        # After iterating through all blocks, check if the wall is destroyed
        if wall_destroyed == 1:
            self.game_over = 1

        # Check for collision with walls
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1   # Se o valor for negativo, fica positivo, se for positivo fica negativo

        # Check for a collision with top and bottom of the screen
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > SCREEN_HEIGHT + 50:
            self.game_over = -1
            lose.play()

        # Look for collision with paddle
        if self.rect.colliderect(player_paddle):
            # Change ball color on paddle collision
            self.h = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            # Check if colliding from the top paddle
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:   # abs == Absolut
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                   self.speed_x = - self.speed_max
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

    def draw(self):
        pygame.draw.circle(screen, self.h, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        
        if self.rect.bottom > SCREEN_HEIGHT + 50:
            self.game_over = -1
            
    def reset(self, x, y):
        self.ball_rad = 10  # Height Ball
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 5
        self.speed_y = -5
        self.speed_max = 6
        self.game_over = 0
        self.h = (190, 0, 0) # Begin Color Ball

# Button Class <---------------------------------------------------------------------------------------- BUTTON
class Button(): 
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def draw(self):
        global game_paused
        # Get Mouse Position
        pos = pygame.mouse.get_pos()

        # Check mouseover and Clicked Conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.pause_game()

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        # Draw Button on Screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # Code for Pause Game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.pause_game()

    def pause_game(self):
        global run
        is_paused = True
        # Create a Pause Loop
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    run = False
                    pygame.quit()

 # Create Button Instances
info = Button(5, 675, info_button, 1)

score = 0
game_ball.score = score
# Create a wall
wall = wall()
wall.create_wall()

# Create Paddle
player_paddle = paddle()

# Create Ball
ball = game_ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

run = True
while run:

    clock.tick(FPS)
    screen.fill(bg)

    # Draw Wall
    wall.draw_wall()
    player_paddle.draw()
    ball.draw()
    info.draw()

    if live_ball == False:
        draw_text("Click to Start", game_font, (50, 50, 50), (SCREEN_WIDTH // 5 ), 213)
        draw_text("Press Q for quit /", info_font, (50, 50, 50), (SCREEN_WIDTH // 5 )+2, 300)
        draw_text("/ Press SPACE for pause", info_font, (50, 50, 50), (SCREEN_WIDTH // 2.2 ), 300)

    if live_ball:
        # Draw Paddle
        player_paddle.move()
        # Draw Ball
        game_over = ball.move()
        if game_over != 0:
            live_ball = False
        if game_over == -1:
            draw_text("loser", game_font, (0, 0, 0), 60, 60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if  event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
            player_paddle.reset()
            wall.create_wall()
        key = pygame.key.get_pressed()
        if key[pygame.K_q]:
            run = False
    pygame.display.update()

pygame.quit()