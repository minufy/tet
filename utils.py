import pygame

SCREEN_W = 1280
SCREEN_H = 720

UNIT = 24

DAS = 117
ARR = 0
SDF = 0

ATTACK_TABLE = {
    0: 0,
    1: 0,
    2: 1,
    3: 2,
    4: 4
}

DEPTH = 1
BEST_COUNT = 5

DANGER_ZONE = 8

font = pygame.font.Font("Pretendard-Regular.ttf", 20)
font_bold = pygame.font.Font("Pretendard-Bold.ttf", 30)

def render_text(font, text, color="#ffffff"):
    surface = font.render(text, True, color)
    return surface

WEIGHTS = []