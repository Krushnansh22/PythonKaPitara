import pygame 
import os
import random
pygame.init()
pygame.font.init()

# Constants
FOOD_WIDTH, FOOD_HEIGHT = 25, 25
SNAKE_WIDTH, SNAKE_HEIGHT = 50, 50
WIDTH, HEIGHT = 900, 500
SPEED = 4
FPS = 60

# Initial directions
DIRECTION1 = 'up'
DIRECTION2 = 'down'

# Fonts
WELCOME_FONT = pygame.font.SysFont('ganesh', 200)
SMALL_WELCOME_FONT = pygame.font.SysFont('comisans', 25)
SCORE_FONT = pygame.font.SysFont('comicsans', 30)

# Game window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Load images
BODY_IMAGE1 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', "body.png")), (SNAKE_WIDTH, SNAKE_HEIGHT))
HEAD_IMAGE1 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', "Head_up.png")), (SNAKE_WIDTH, SNAKE_HEIGHT))

BODY_IMAGE2 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', "body2.png")), (SNAKE_WIDTH, SNAKE_HEIGHT))
HEAD_IMAGE2 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', "Head2_up.png")), (SNAKE_WIDTH, SNAKE_HEIGHT))

FOOD_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', "powerup.png")), (FOOD_WIDTH, FOOD_HEIGHT))

GAMEOVER = pygame.USEREVENT + 1

def home_screen():
    while True:
        WIN.fill(pygame.Color('lightgreen')) 
        WIN.blit(WELCOME_FONT.render(';fk',1,(0,0,0)),(320,100))
        WIN.blit(SMALL_WELCOME_FONT.render('...hai sab sale. 2',1,(0,0,0)),(460,250))
        WIN.blit(SCORE_FONT.render("[P]lay",1,(255,0,0)),(420,300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            key = pygame.key.get_pressed()
            if key[pygame.K_p]:
                main()
        pygame.display.update()

def draw_game(Head1, Head2, Food, score1, score2, BodyList1, BodyList2):
    HEAD_IMAGE1 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', f"Head_{DIRECTION1}.png")), (SNAKE_WIDTH, SNAKE_HEIGHT))
    HEAD_IMAGE2 = pygame.transform.scale(pygame.image.load(os.path.join('Assets', f"Head2_{DIRECTION2}.png")), (SNAKE_WIDTH, SNAKE_HEIGHT))
    
    score_text1 = SCORE_FONT.render(f'SCORE 1: {score1}', 1, (0, 0, 0), (255, 255, 255))
    score_text2 = SCORE_FONT.render(f'SCORE 2: {score2}', 1, (0, 0, 0), (255, 255, 255))
    
    WIN.fill(pygame.Color('lightgreen'))
    WIN.blit(score_text1, (10, 30))
    WIN.blit(score_text2, (WIDTH - 200, 30))
    WIN.blit(FOOD_IMAGE, (Food.x, Food.y))
    
    for xny in BodyList1:
        WIN.blit(BODY_IMAGE1, (xny[0], xny[1]))
    for xny in BodyList2:
        WIN.blit(BODY_IMAGE2, (xny[0], xny[1]))
    
    WIN.blit(HEAD_IMAGE1, (Head1.x, Head1.y))
    WIN.blit(HEAD_IMAGE2, (Head2.x, Head2.y))
    
    pygame.display.update()

def move(Head, direction):
    if Head.y < 0 or Head.y + SNAKE_HEIGHT > HEIGHT or Head.x < 0 or Head.x + SNAKE_WIDTH > WIDTH:
        pygame.event.post(pygame.event.Event(GAMEOVER))
    if direction == "up":
        Head.y -= SPEED
    if direction == "down":
        Head.y += SPEED
    if direction == "left":
        Head.x -= SPEED
    if direction == "right":
        Head.x += SPEED

def reset_screen(score1, score2):
    WIN.fill(pygame.Color('lightgreen'))
    score_text = SCORE_FONT.render(f'GAME OVER! PLAYER 1: {score1} PLAYER 2: {score2}', 1, (0, 0, 0), (255, 255, 255))
    WIN.blit(score_text, (250, 250))
    WIN.blit(SCORE_FONT.render('[SPACE] to Restart', 1, (0, 0, 0), (255, 255, 255)), (250, 300))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

def main():
    global DIRECTION1, DIRECTION2
    start1 = start2 = False
    clock = pygame.time.Clock()
    WIN.fill(pygame.Color('lightgreen'))
    Head1 = pygame.Rect(200, 200, SNAKE_WIDTH, SNAKE_HEIGHT)
    Head2 = pygame.Rect(600, 200, SNAKE_WIDTH, SNAKE_HEIGHT)
    food_exists = False
    loop = True
    score1 = score2 = 0
    body_len1 = body_len2 = 0
    BodyList1 = []
    BodyList2 = []
    
    while loop:
        clock.tick(FPS)
        if score1 != 0:
            body_len1 = score1 
        if score2 != 0:
            body_len2 = score2 
        if not food_exists:
            Food_position_x = random.randrange(0, WIDTH - FOOD_WIDTH)
            Food_position_y = random.randrange(0, HEIGHT - FOOD_HEIGHT)
            Food = pygame.Rect(Food_position_x, Food_position_y, FOOD_WIDTH, FOOD_HEIGHT)
            food_exists = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == GAMEOVER:
                loop = False
                reset_screen(score1, score2)
        
        key = pygame.key.get_pressed()  
        
        if key[pygame.K_w] and DIRECTION1 != 'down':
            DIRECTION1 = "up"
            start1 = True
        if key[pygame.K_s] and DIRECTION1 != 'up':
            DIRECTION1 = "down"
        if key[pygame.K_a] and DIRECTION1 != 'right':
            DIRECTION1 = "left"
        if key[pygame.K_d] and DIRECTION1 != 'left':
            DIRECTION1 = "right"
        
        if key[pygame.K_UP] and DIRECTION2 != 'down':
            DIRECTION2 = "up"
            start2 = True
        if key[pygame.K_DOWN] and DIRECTION2 != 'up':
            DIRECTION2 = "down"
        if key[pygame.K_LEFT] and DIRECTION2 != 'right':
            DIRECTION2 = "left"
        if key[pygame.K_RIGHT] and DIRECTION2 != 'left':
            DIRECTION2 = "right"
        
        HeadList1 = [Head1.x, Head1.y]
        HeadList2 = [Head2.x, Head2.y]
        
        if HeadList1 in BodyList1 or HeadList2 in BodyList2 or HeadList1 in BodyList2 or HeadList2 in BodyList1:
            reset_screen(score1, score2)
        
        BodyList1.append(HeadList1)
        BodyList2.append(HeadList2)
        
        if start1:
            move(Head1, DIRECTION1)
        if start2:
            move(Head2, DIRECTION2)
        
        if Head1.colliderect(Food):
            score1 += 1
            food_exists = False
        if Head2.colliderect(Food):
            score2 += 1
            food_exists = False
        
        if len(BodyList1) >= body_len1:
            del BodyList1[0]
        if len(BodyList2) >= body_len2:
            del BodyList2[0]
        
        draw_game(Head1, Head2, Food, score1, score2, BodyList1, BodyList2)
        pygame.display.update()

if __name__ == "__main__":
    home_screen()
