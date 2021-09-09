# **2_images_&_surfaces**

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