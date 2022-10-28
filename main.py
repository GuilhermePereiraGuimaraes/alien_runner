from tabnanny import check
from tkinter import CENTER
import pygame
from sys import exit
from random import randint

def display_score():
    current_time = (pygame.time.get_ticks()//1000) - start_time
    score_surface = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 7
        
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    
    else:
        return []
    
def colisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Alien Runner')
clock = pygame.time.Clock()
font_type = 'font/OriginTech.ttf'
test_font = pygame.font.Font(font_type, 40)
font_title = pygame.font.Font(font_type, 60)
instruction_font = pygame.font.Font(font_type, 20)
game_active = False
start_time = 0
death_count = 0
score = 0

sky_surface = pygame.image.load('graphics/Sky.png').convert()
sky_surface_2 = pygame.image.load('graphics/Sky.png').convert()

ground_surface = pygame.image.load("graphics/ground.png").convert()
ground_surface_2 = pygame.image.load("graphics/ground.png").convert()
ground_sky_x_pos = 0

#Obstacles
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
fly_surface = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha() 


obstacle_rect_list = []

#Player 
player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0 

# Intro Screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand_scaled = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand_scaled.get_rect(center = (400,200))

#Texts for intro screen
text_title = font_title.render("Alien Runner", False, (0,120,100))
text_title_rect = text_title.get_rect(center = (400, 50))
text_instructions = instruction_font.render("Press Space Bar or Mouse button to start", False, (0,120,100))
text_instructions_rect = text_instructions.get_rect(midbottom = (400, 330))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

checar = True
contar = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if player_rect.bottom ==300:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player_gravity = -20
                if event.type == pygame.MOUSEBUTTONDOWN:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # snail_rect.left = 800 
                start_time = pygame.time.get_ticks() // 1000
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                game_active = True
                # snail_rect.left = 800
                start_time = pygame.time.get_ticks() // 1000
        
        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900, 1100),300)))
            else:
                obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(900, 1100),210)))


    contar += 1

    if game_active: 
        #Cenário
        screen.blit(sky_surface, (ground_sky_x_pos, 0))
        screen.blit(sky_surface_2, (ground_sky_x_pos+800, 0))
        screen.blit(ground_surface, (ground_sky_x_pos, 300))
        screen.blit(ground_surface_2, (ground_sky_x_pos+800, 300))
        
        #Score
        score = display_score()

        #Caracol
        # screen.blit(snail_surface, snail_rect)
        
        #Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surface, player_rect)

        #Obstacle Moviment
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #Collision
        game_active = colisions(player_rect, obstacle_rect_list)
        if game_active == False:
            death_count += 1

    else:
        obstacle_rect_list.clear()
        if death_count > 0:
            text_title = font_title.render("Game Over", False, (0,120,100))
            text_title_rect = text_title.get_rect(center = (400, 50))
            player_stand_scaled = pygame.transform.rotozoom(player_stand,90,2)
            text_instructions = instruction_font.render("Press Space Bar or Mouse button to restart", False, (0,120,100))
            text_deaths = instruction_font.render(f"Deaths: {death_count}", False, (0,120,100))
            text_deaths_rect = text_deaths.get_rect(midbottom = (400, 360))
            text_score = instruction_font.render(f"Score: {score}", False, (0,120,100))
            text_score_rect = text_score.get_rect(midbottom = (400, 390))
        screen.fill((94,129,162))
        screen.blit(player_stand_scaled, player_stand_rect)
        screen.blit(text_title, text_title_rect)
        screen.blit(text_instructions, text_instructions_rect)
        if death_count>0:
            screen.blit(text_deaths, text_deaths_rect)
            screen.blit(text_score, text_score_rect)
        

       
            
    if contar % 10 == 0:
        if checar == True:
            player_surface = pygame.image.load(
                'graphics/Player/player_walk_2.png').convert_alpha()
            checar = False
        else:
            player_surface = pygame.image.load(
                'graphics/Player/player_walk_1.png').convert_alpha()
            checar = True

    ground_sky_x_pos -= 5
    # snail_rect.x -= 10
    # if snail_rect.x <= -100:
    #     snail_rect.x = 800
    if ground_sky_x_pos <= -800:
        ground_sky_x_pos = 0

    pygame.display.update()
    clock.tick(60)
