import pygame
import os
pygame.font.init()
pygame.mixer.init()
pygame.init()
# Declarations
WIDTH, HEIGHT = 900, 500
CHARACTER_WIDTH, CHARACTER_HEIGHT = 50, 65 
FPS = 60
VELOCITY = 3
PROJECTILE_VELOCITY = 10
MAX_ATTACKS = 3

NARUTO_HIT = pygame.USEREVENT + 1
SASUKE_HIT = pygame.USEREVENT + 2
GAME_OVER = pygame.USEREVENT + 3

Health_font = pygame.font.SysFont('comicsans',40)
Winner_font = pygame.font.SysFont('comicsans',60)
Title_font = pygame.font.SysFont('vinerhanditc',70)
FONT_2 = pygame.font.SysFont('comicsans',20)
# Assests Handeling
NARUTO_IMAGE_RAW = pygame.image.load(os.path.join('Assets','Naruto.png'))
SASUKE_IMAGE_RAW = pygame.image.load(os.path.join('Assets','Sasuke.png'))
NARUTO_IMAGE = pygame.transform.scale(NARUTO_IMAGE_RAW, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
SASUKE_IMAGE = pygame.transform.flip((pygame.transform.scale(SASUKE_IMAGE_RAW, (CHARACTER_WIDTH, CHARACTER_HEIGHT))),1,0)
BG = pygame.image.load(os.path.join("Assets","Home_page.png"))
BACKGROUND = pygame.transform.scale(BG, (WIDTH, HEIGHT))


Naruto_fire_sound = pygame.mixer.Sound(os.path.join("Assets","Rasengen.mp3"))
Sasuke_fire_sound = pygame.mixer.Sound(os.path.join("Assets","katon.mp3"))

######
import random

# Constants for stamina
MAX_STAMINA = 100
STAMINA_COST = 10
POWERUP_SPAWN_INTERVAL = 5000  # 5 seconds
POWERUP_DURATION = 10000  # 10 seconds

# Load powerup image
POWERUP_IMAGE = pygame.image.load(os.path.join('Assets', 'powerup.png'))
POWERUP_IMAGE = pygame.transform.scale(POWERUP_IMAGE, (30, 30))

# Event for spawning powerup
SPAWN_POWERUP = pygame.USEREVENT + 4

# Setting up the event to trigger every 5 seconds
pygame.time.set_timer(SPAWN_POWERUP, POWERUP_SPAWN_INTERVAL)

# Implementation
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gavacha Sarpanch - Hokage")

def draw_welcome_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_0]:
            main()
        WIN.blit(BACKGROUND,(0,0)) #Change for Background
        Title_text = Title_font.render("Konoha Clash",1,(128,70,27))
        Title_text_2 = FONT_2.render("[0]Start",1,(0,0,0))
        WIN.blit(Title_text,(237,375))
        WIN.blit(Title_text_2,(420,450)) 
        pygame.display.update()

def draw_game(Naruto, Sasuke, Naruto_chakra, Sasuke_chakra, Naruto_health, Sasuke_health, Naruto_stamina, Sasuke_stamina, powerup, winner):
    WIN.fill(pygame.Color("lightskyblue"))
    naruto_health_text = Health_font.render("Naruto:" + str(Naruto_health), 1, (255, 0, 255))
    sasuke_health_text = Health_font.render("Sasuke:" + str(Sasuke_health), 1, (255, 255, 0))
    naruto_stamina_text = Health_font.render("Stamina:" + str(Naruto_stamina), 1, (255, 0, 255))
    sasuke_stamina_text = Health_font.render("Stamina:" + str(Sasuke_stamina), 1, (255, 255, 0))
    
    WIN.blit(naruto_health_text, (50, 10))
    WIN.blit(sasuke_health_text, (620, 10))
    WIN.blit(naruto_stamina_text, (50, 50))
    WIN.blit(sasuke_stamina_text, (620, 50))
    WIN.blit(NARUTO_IMAGE, (Naruto.x, Naruto.y))
    WIN.blit(SASUKE_IMAGE, (Sasuke.x, Sasuke.y))
    
    for projectile in Naruto_chakra:
        pygame.draw.rect(WIN, (255, 0, 255), projectile)
    for projectile in Sasuke_chakra:
        pygame.draw.rect(WIN, (255, 255, 0), projectile)
    
    if powerup:
        WIN.blit(POWERUP_IMAGE, (powerup.x, powerup.y))
    
    pygame.display.update()


def draw_winner(winner):
    pygame.display.update()
    WIN.blit(Winner_font.render(f"{winner}",1,(255,255,255)),(300,150))
    pygame.display.update()
    pygame.time.delay(5000)

def Naruto_movements(keys_pressed, Naruto):
    # Naruto Moves
    if keys_pressed[pygame.K_w] and Naruto.y - VELOCITY > 0 : # UP
        Naruto.y -= VELOCITY
    if keys_pressed[pygame.K_s] and Naruto.y + CHARACTER_HEIGHT + VELOCITY < HEIGHT : # DOWN
        Naruto.y += VELOCITY
    if keys_pressed[pygame.K_a] and Naruto.x - VELOCITY > 0 : # LEFT
        Naruto.x -= VELOCITY
    if keys_pressed[pygame.K_d] and Naruto.x + CHARACTER_WIDTH + VELOCITY < WIDTH : # RIGHT
        Naruto.x += VELOCITY


def Sasuke_movements(keys_pressed, Sasuke):
    # Sasuke Moves
    if keys_pressed[pygame.K_UP] and Sasuke.y - VELOCITY > 0: # UP
        Sasuke.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and Sasuke.y + CHARACTER_HEIGHT + VELOCITY < HEIGHT: # DOWN
        Sasuke.y += VELOCITY
    if keys_pressed[pygame.K_LEFT] and Sasuke.x - VELOCITY > 0 : # LEFT
        Sasuke.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and Sasuke.x + CHARACTER_WIDTH + VELOCITY < WIDTH: # RIGHT
        Sasuke.x += VELOCITY


def handle_attacks(Naruto_chakra, Sasuke_chakra, Naruto, Sasuke):
    for projectile in Naruto_chakra:
        projectile.x += PROJECTILE_VELOCITY
        if Sasuke.colliderect(projectile):
            pygame.event.post(pygame.event.Event(SASUKE_HIT))
            Naruto_chakra.remove(projectile)
        elif projectile.x > WIDTH:
            Naruto_chakra.remove(projectile)
            
    for projectile in Sasuke_chakra:
        projectile.x -= PROJECTILE_VELOCITY
        if Naruto.colliderect(projectile):
            pygame.event.post(pygame.event.Event(NARUTO_HIT))
            Sasuke_chakra.remove(projectile)
        elif projectile.x < 0:
            Sasuke_chakra.remove(projectile)


def main():
    Naruto = pygame.Rect(100, 200, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    Sasuke = pygame.Rect(700, 200, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    
    Naruto_chakra = []
    Sasuke_chakra = []
    
    Sasuke_health = 10
    Naruto_health = 10
    Sasuke_stamina = MAX_STAMINA
    Naruto_stamina = MAX_STAMINA
    
    powerup = None
    powerup_timer = 0
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()   
                
            if event.type == pygame.KEYDOWN:
                # Naruto Attacks
                if event.key == pygame.K_LSHIFT and len(Naruto_chakra) < MAX_ATTACKS and Naruto_stamina >= STAMINA_COST:
                    projectile = pygame.Rect(Naruto.x + CHARACTER_WIDTH, Naruto.y + CHARACTER_HEIGHT//3, 10, 5)
                    Naruto_chakra.append(projectile)
                    Naruto_stamina -= STAMINA_COST
                    Naruto_fire_sound.play()

                # Sasuke Attacks
                if event.key == pygame.K_KP0 and len(Sasuke_chakra) < MAX_ATTACKS and Sasuke_stamina >= STAMINA_COST:
                    projectile = pygame.Rect(Sasuke.x , Sasuke.y + CHARACTER_HEIGHT//3, 10, 5)
                    Sasuke_chakra.append(projectile)
                    Sasuke_stamina -= STAMINA_COST
                    Sasuke_fire_sound.play()

            if event.type == NARUTO_HIT:
                Naruto_health -= 1
            if event.type == SASUKE_HIT:
                Sasuke_health -= 1
            if event.type == SPAWN_POWERUP:
                if not powerup:
                    powerup_x = random.randint(50, WIDTH - 50)
                    powerup_y = random.randint(50, HEIGHT - 50)
                    powerup = pygame.Rect(powerup_x, powerup_y, 30, 30)
                    powerup_timer = pygame.time.get_ticks()

        winner = ""
        if Naruto_health <= 0:
            winner = "Sasuke Wins!!"
        if Sasuke_health <= 0:
            winner = "Naruto Wins!!"
        if winner != "":
            draw_winner(winner)
        
        if powerup and pygame.time.get_ticks() - powerup_timer > POWERUP_DURATION:
            powerup = None

        keys_pressed = pygame.key.get_pressed()
        Naruto_movements(keys_pressed, Naruto)
        Sasuke_movements(keys_pressed, Sasuke)
        handle_attacks(Naruto_chakra, Sasuke_chakra, Naruto, Sasuke)
        
        if powerup:
            if Naruto.colliderect(powerup):
                Naruto_stamina = MAX_STAMINA
                powerup = None
            elif Sasuke.colliderect(powerup):
                Sasuke_stamina = MAX_STAMINA
                powerup = None

        draw_game(Naruto, Sasuke, Naruto_chakra, Sasuke_chakra, Naruto_health, Sasuke_health, Naruto_stamina, Sasuke_stamina, powerup, winner)
        pygame.display.update()
    main()



if __name__ == "__main__":
    draw_welcome_screen()