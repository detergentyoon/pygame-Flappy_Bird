# **2_images_&_surfaces**
## **image convert**
```python
background = pygame.image.load("image/background-day.png").convert()
background = pygame.transform.scale2x(background)
```
`transform.scale2x(background)` : `background` 표면을 가져와 크기를 두배로 늘리고 이 변수를 스케일된 표면으로 덮어씁니다.

두 문장 코드를 `background = pygame.transform.scale2x(pygame.image.load("image/background-day.png"))` 의 형태로 한 줄로 작성할 수도 있지만 두 줄로 작성한 코드의 경우가 더 깨끗해보이기 때문에 두 줄로 작성하였습니다.

<br>

라인의 끝에 붙여진 `convert()` 는 꼭 필요한 작업은 아니지만 이미지를 변환하는 작업을 pygame용으로 작업하기 더 쉬운 파일 유형으로 변환해줍니다.

기본적으로 pygame에서 게임을 더 쉽게 실행할 수 있꼬 더 빠른 속도로 게임을 실행할 수 있게 해주지만, 코드를 실행했을 때 `convert()` 에 대한 표현이 가시적으로 나타나진 않습니다.

하지만 게임이 더 복잡해지고 바빠지면 `convert()` 를 통해 더 일관된 속도로 게임을 실행하는 데 도움이 될 수 있습니다.

<br>

## **floor process**
```python
def draw_floor():
    screen.blit(floor_surface,(floor_x_pos, screen_height - floor_height))
    screen.blit(floor_surface,(floor_x_pos + screen_width, screen_height - floor_height))
```
첫번째 `floor_surface` 가 끝나는 지점에 또 하나의 `floor_surface` 를 추가하여 아래 코드의 `floor_x_pos -= 1` 과 호환성을 이룹니다.
```python
floor_x_pos -= 1
```
`floor_x_pos -= 1` 은 `while`문 내에 있기 때문에 매 `tick(n)` 마다 floor 가 왼쪽으로 이동하는 애니메이션 효과를 냅니다. fps 가 높을 수록 더 자연스럽습니다.
```python
if floor_x_pos <= -floor_width:
        floor_x_pos = 0
```
`floor_x_pos` 이 `-floor_width(-576)` 이면 다시 `floor_x_pos` 을 x 좌표 0 으로 이동시켜 `floor` 가 이동하는 애니메이션 효과가 끊기지 않도록 합니다.

이 동작은 너무 빠르기 때문에 우리는 실제로 전환을 볼 수 없으며 매우 자연스러운 애니메이션 효과를 냅니다.

<br>

# **3_bird process**
## **get_rect()**
```python
bird_rect = bird_surface.get_rect(center = (100, screen_height / 2))
```
`get_rect()` 는 불러온 표면(surface) 주위에 직사각형을 배치하고 전달하는 인수에 따른 결과를 출력하는 것입니다.

이 코드에서는 사각형에서 한 점을 잡는데, 그 점은 중심(center)이며, x 와 y 위치 할당된 튜플(왼쪽에서 100px, 화면중앙에 놓을 것이므로 screen_height / 2 )을 통해 표면의 너비와 높이를 갖는 직사각형을 갖고, 이 직사각형의 중심은 이 튜플 안의 좌표 점에 있습니다.

<br>

## **Bird Jump process**
```python
if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 12
```
`bird_movement -= 12` 를 통해 키 입력 시 새가 12px 만큼 점프하게 만듭니다. pygame 에서는 y 값이 위에서 아래로 향할 수록 양수가 되기 때문에 음수값을 연산해서 점프하는 것 처럼 보이게 할 수 있습니다.

점프력 픽셀값인 `-12` 를 더하기 전에 `bird_movement = 0` 을 먼저 정의하는 것은 새의 점프가 중력값에 영향을 받지 않도록 하기 위함입니다.

![gravity_jump](info/gravity_jump.png)

만약 계속해서 0.25씩 증가하는 중력값에 -12 를 연산하면 n초 간 쌓인 중력값 만큼에서 -12 를 연산하기 때문에 정확히 -12px 만큼 점프할 수 없습니다.

새의 점프가 중력에 영향을 받지 않는 이질적인 움직임을 작동하기 위해서 `bird_movement = 0` 으로 거듭해서 더해진 중력값을 초기화를 한 후 -12px 를 움직이게 하면 쌓인 중력값이 얼마였던간에 새가 정확히 -12px 을 점프할 수 있게됩니다. 