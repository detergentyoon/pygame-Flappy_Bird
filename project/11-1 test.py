import pygame, random

# Functions
def draw_floor():
    screen.blit(floor_surface,(floor_x_pos, screen_height - floor_height))
    screen.blit(floor_surface,(floor_x_pos + screen_width, screen_height - floor_height))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_green_surface.get_rect(midtop = (screen_width + 100, random_pipe_pos))
    top_pipe = pipe_green_surface.get_rect(midbottom = (screen_width + 100, random_pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= screen_height:
            screen.blit(pipe_green_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_green_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    global can_score

    for pipe in pipes:
        if bluebird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False
        elif yellowbird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False
        elif redbird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False

    if bluebird_rect.top <= -100 or bluebird_rect.bottom >= 900 or yellowbird_rect.top <= -100 or yellowbird_rect.bottom >= 900 or redbird_rect.top <= -100 or redbird_rect.bottom >= 900:
        death_sound.play()
        can_score = True
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, - bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bluebird_frames[bird_index] or yellowbird_frames[bird_index] or redbird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bluebird_rect.centery or yellowbird_rect.centery or redbird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (screen_width / 2, 100))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255,255,255))
        score_rect = score_surface.get_rect(center = (screen_width / 2, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High score: {int(high_score)}", True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (screen_width / 2, 850))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score == True:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True

pygame.init()

screen_width = 576
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Flappy Bird")

# FPS
clock = pygame.time.Clock()

game_font = pygame.font.Font("04B_19.ttf", 40)

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True
change_surface = 0

# User game init
bg_surface = pygame.image.load("assets/background-day.png").convert()
bg_surface = pygame.transform.scale2x(bg_surface)
bg_night_surface = pygame.image.load("assets/background-night.png").convert()
bg_night_surface = pygame.transform.scale2x(bg_night_surface)

floor_surface = pygame.image.load("assets/base.png").convert()
floor_size = floor_surface.get_rect().size
floor_width = floor_size[0]
floor_height = floor_size[1]
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_index = 0
bluebird_downflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-downflap.png").convert_alpha())
bluebird_midflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-midflap.png").convert_alpha())
bluebird_upflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-upflap.png").convert_alpha())
bluebird_frames = [bluebird_downflap, bluebird_midflap, bluebird_upflap]
bluebird_surface = bluebird_frames[bird_index]
bluebird_rect = bluebird_surface.get_rect(center = (100, screen_height / 2))

yellowbird_downflap = pygame.transform.scale2x(pygame.image.load("assets/yellowbird-downflap.png").convert_alpha())
yellowbird_midflap = pygame.transform.scale2x(pygame.image.load("assets/yellowbird-midflap.png").convert_alpha())
yellowbird_upflap = pygame.transform.scale2x(pygame.image.load("assets/yellowbird-upflap.png").convert_alpha())
yellowbird_frames = [yellowbird_downflap, yellowbird_midflap, yellowbird_upflap]
yellowbird_surface = yellowbird_frames[bird_index]
yellowbird_rect = yellowbird_surface.get_rect(center = (100, screen_height / 2))

redbird_downflap = pygame.transform.scale2x(pygame.image.load("assets/redbird-downflap.png").convert_alpha())
redbird_midflap = pygame.transform.scale2x(pygame.image.load("assets/redbird-midflap.png").convert_alpha())
redbird_upflap = pygame.transform.scale2x(pygame.image.load("assets/redbird-upflap.png").convert_alpha())
redbird_frames = [redbird_downflap, redbird_midflap, redbird_upflap]
redbird_surface = redbird_frames[bird_index]
redbird_rect = redbird_surface.get_rect(center = (100, screen_height / 2))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_green_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_green_surface = pygame.transform.scale2x(pipe_green_surface)
pipe_red_surface = pygame.image.load("assets/pipe-red.png").convert()
pipe_red_surface = pygame.transform.scale2x(pipe_red_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

game_over_surface = pygame.transform.scale2x(pygame.image.load("assets/gameover.png").convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (screen_width / 2, screen_height / 2 ))

# sounds
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_die.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

running = True
while running:
    dt = clock.tick(120)

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                bird_movement = 0
                bird_movement -= 10
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False: # regame
                game_active = True
                pipe_list.clear()
                bluebird_rect.center = (100, screen_height / 2)
                bird_movement = 0
                score = 0
                change_surface += 1

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
                
            bluebird_surface, bluebird_rect = bird_animation()

    # Background
    screen.blit(bg_surface,(0, 0))
    if change_surface >= 5:
        screen.blit(bg_night_surface, (0, 0))
        if change_surface == 10:
            change_surface = 0

    if game_active:
        # Bird
        if score <= 2:
            bird_movement += gravity
            rotated_bird = rotate_bird(bluebird_surface)
            bluebird_rect.centery += bird_movement
            screen.blit(rotated_bird, bluebird_rect)
            game_active = check_collision(pipe_list)
        elif 3 <= score <= 5:
            bird_movement += gravity
            rotated_bird = rotate_bird(yellowbird_surface)
            yellowbird_rect.centery += bird_movement
            screen.blit(rotated_bird, yellowbird_rect)
            game_active = check_collision(pipe_list)
        elif 6 <= score:
            bird_movement += gravity
            rotated_bird = rotate_bird(redbird_surface)
            redbird_rect.centery += bird_movement
            screen.blit(rotated_bird, redbird_rect)
            game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score
        pipe_score_check()
        score_display("main_game")
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -floor_width:
        floor_x_pos = 0

    pygame.display.update()

pygame.quit()