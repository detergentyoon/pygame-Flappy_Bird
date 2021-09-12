import pygame, random

pygame.init()

screen_width = 576
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Flappy Bird") # 게임 이름

# FPS
clock = pygame.time.Clock()

# Game Variables
gravity = 0.25
bird_movement = 0

# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 폰트 등)

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos, screen_height - floor_height))
    screen.blit(floor_surface,(floor_x_pos + screen_width, screen_height - floor_height))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (screen_width + 100, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (screen_width + 100, random_pipe_pos - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= screen_height: # 도트 바닥이 1024 보다 크거나 같으면
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
                                        # flip : 표면을 뒤집음, 2개의 인수(첫번쨰 인수 : x 방향으로 뒤집기, 두번째 인수 : y 방향으로 뒤집기)
            screen.blit(flip_pipe, pipe)
bg_surface = pygame.image.load("assets/background-day.png").convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load("assets/base.png").convert()
floor_size = floor_surface.get_rect().size
floor_width = floor_size[0]
floor_height = floor_size[1]
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_surface = pygame.image.load("assets/bluebird-midflap.png").convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100, screen_height / 2))

pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

running = True
while running:
    dt = clock.tick(120)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 12

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    # 3. 게임 캐릭터 위치 정의

    # 4. 충돌 처리

    # 5. 화면에 그리기
    screen.blit(bg_surface,(0, 0))

    # bird
    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird_surface, bird_rect)

    # pipes
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)

    # floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -floor_width:
        floor_x_pos = 0

    pygame.display.update()

pygame.quit()

# 지나간 리스트는 지워야 렉이 안걸림,
# 렉 걸리는거랑 SPAWNPIPE 이벤트는 따로 적용되기 때문에
# 렉 걸려서 느리게 넘어가는 와중에 다음 파이프가 나와서 점점 파이프간 거리가 좁아짐