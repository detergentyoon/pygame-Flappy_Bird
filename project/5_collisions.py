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
game_active = True

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

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe): # ture 를 반환하므로 if 를 사용할 수 있음
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False

    return True # 2개의 트리거 중 어느 것도 트리거하지 않으면 true를 반환 

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
            if event.key == pygame.K_SPACE and game_active == True:
                bird_movement = 0
                bird_movement -= 12
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, screen_height / 2)
                bird_movement = 0 # 재시작 시 이 값을 할당하지 않으면 `bird_movement += gravity` 값이 계속해서 쌓이며 새가 제어할 수 없을 정도의 속도로 하강해버리는 버그가 발생

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            # append 를 extend(확장) 로 바꾼 이유 :
            # create_pipe() 의 반환값은 쉼표로 구분된 변수로 돌아가기 때문에 튜플을 반환하므로
            # 이 튜플의 압축을 풀거나 최소한 다른 작업을 수행해야 하므로 다른 목록에 추가할 수 없음.
            # 이 코드에서는 이 목록을 가져오는 확장을 사용하고 두 요소가 있는 튜플인 this가 반환하는 모든 항목으로 확장하는 것.
            # 이 튜플은 여전히 작동해야

    # 3. 게임 캐릭터 위치 정의

    # 4. 충돌 처리

    # 5. 화면에 그리기
    screen.blit(bg_surface,(0, 0))

    if game_active:
        # bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface, bird_rect)
        game_active = check_collision(pipe_list)

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