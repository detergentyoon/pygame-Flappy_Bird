import pygame

pygame.init()

screen_width = 576
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Flappy Bird") # 게임 이름

# FPS
clock = pygame.time.Clock()

# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 폰트 등)

running = True
while running:
    dt = clock.tick(60)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 3. 게임 캐릭터 위치 정의

    # 4. 충돌 처리

    # 5. 화면에 그리기

    pygame.display.update()

pygame.quit()