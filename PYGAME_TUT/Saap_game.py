import pygame 
import os
import random
pygame.init()
pygame.font.init()
FOOD_WIDTH, FOOD_HEIGHT = 25,25
SNAKE_WIDTH, SNAKE_HEIGHT = 50,50
WIDTH, HEIGHT = 900, 500
SPEED = 4
FPS = 60
DIRECTION = 'up'

WELCOME_FONT = pygame.font.SysFont('ganesh',200)
SMALL_WELCOME_FONT = pygame.font.SysFont('comisans',25)
SCORE_FONT = pygame.font.SysFont('comicsans',30)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))


BODY_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets',"body.png")),(SNAKE_WIDTH, SNAKE_HEIGHT))

FOOD_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets',"powerup.png")),(FOOD_WIDTH, FOOD_HEIGHT))


GAMEOVER = pygame.USEREVENT + 1

def home_screen():
    while True:
        WIN.fill(pygame.Color('lightgreen'))
        WIN.blit(WELCOME_FONT.render(';fk',1,(0,0,0)),(320,100))
        WIN.blit(SMALL_WELCOME_FONT.render('...hai sab sale.',1,(0,0,0)),(460,250))
        WIN.blit(SCORE_FONT.render("[P]lay",1,(255,0,0)),(420,300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            key = pygame.key.get_pressed()
            if key[pygame.K_p]:
                main()
        pygame.display.update()


def draw_game(Head, Food, score, BodyList):
    HEAD_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets',f"Head_{DIRECTION}.png")),(SNAKE_WIDTH,SNAKE_HEIGHT))
    
    score_text = SCORE_FONT.render(f'SCORE: {score}',1,(0,0,0),(255,255,255))
    WIN.fill(pygame.Color('lightgreen'))
    WIN.blit(score_text,(700,30))
    WIN.blit(FOOD_IMAGE,(Food.x ,Food.y))
    for xny in BodyList:
        WIN.blit(BODY_IMAGE,(xny[0],xny[1]))
    WIN.blit(HEAD_IMAGE,(Head.x, Head.y))
    pygame.display.update()

def move(Head):
    global DIRECTION
    if Head.y < 0 or Head.y + SNAKE_HEIGHT > HEIGHT or Head.x < 0 or Head.x + SNAKE_WIDTH > WIDTH:
        pygame.event.post(pygame.event.Event(GAMEOVER))
    if DIRECTION == "up"  :
        Head.y -= SPEED
    if DIRECTION == "down" :
        Head.y += SPEED
    if DIRECTION == "left" :
        Head.x -= SPEED
    if DIRECTION == "right" :
        Head.x += SPEED

def reset_screen(score):
    WIN.fill(pygame.Color('lightgreen'))
    score_text = SCORE_FONT.render(f'GAME OVER! YOUR SCORE: {score}',1,(0,0,0),(255,255,255))
    WIN.blit(score_text,(250,250))
    WIN.blit(SCORE_FONT.render('[SPACE] to Restart',1,(0,0,0),(255,255,255)),(250,300))
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
    global DIRECTION 
    start = False 
    clock = pygame.time.Clock()
    WIN.fill(pygame.Color('lightgreen'))
    Head = pygame.Rect(400,200,SNAKE_WIDTH,SNAKE_HEIGHT)
    food_exists = False
    loop = True
    score = 0
    body_len = 0
    BodyList = []
    while loop:
        clock.tick(FPS)
        if score != 0:
            body_len = score + 3
        if not food_exists:
            Food_position_x = random.randrange(0,WIDTH - FOOD_WIDTH)
            Food_position_y = random.randrange(0,HEIGHT - FOOD_HEIGHT)
            Food = pygame.Rect(Food_position_x, Food_position_y, FOOD_WIDTH, FOOD_HEIGHT)
            food_exists = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == GAMEOVER:
                loop = False
                reset_screen(score)
            current_dir = DIRECTION
            key = pygame.key.get_pressed()  
            if key[pygame.K_w] and DIRECTION != 'down':
                DIRECTION = "up"
                start = True
            if key[pygame.K_s] and DIRECTION != 'up':
                DIRECTION = "down"
            if key[pygame.K_a] and DIRECTION != 'right':
                DIRECTION = "left"
            if key[pygame.K_d] and DIRECTION != 'left':
                DIRECTION = "right"
        HeadList = []
        HeadList.append(Head.x)
        HeadList.append(Head.y)
        if HeadList in BodyList:
            reset_screen()
        BodyList.append(HeadList)
        if start:
            move(Head)
        if Head.colliderect(Food):
            score += 1
            food_exists = False
        if len(BodyList) >= body_len:
            del BodyList[0]
        draw_game(Head, Food, score, BodyList)
        pygame.display.update()

if __name__ == "__main__":
    home_screen()