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
BEST_COUNT = 2

DANGER_ZONE = 8

font = pygame.font.Font("Pretendard-Regular.ttf", 30)

def render_text(text, color):
    surface = font.render(text, True, color)
    return surface

WEIGHTS = [
    ({'line': -0.035, 'change_rate': -0.25, 'holes': -1.3, 'avg_height': 0, 'well_depth': 0.007}, {'line': 0.699, 'change_rate': -0.25, 'holes': -1.3, 'avg_height': -0.804, 'well_depth': -0.031}),
    ({'line': -0.072, 'change_rate': -1.037, 'holes': -0.629, 'avg_height': 0, 'well_depth': 0.031}, {'line': 0.264, 'change_rate': -1.037, 'holes': -0.629, 'avg_height': -0.351, 'well_depth': -0.009}),
    ({'line': -0.417, 'change_rate': -0.364, 'holes': -0.452, 'avg_height': 0, 'well_depth': 0.028}, {'line': 0.723, 'change_rate': -0.364, 'holes': -0.452, 'avg_height': -0.591, 'well_depth': -0.033}),
    ({'line': -0.114, 'change_rate': -0.248, 'holes': -1.312, 'avg_height': 0, 'well_depth': 0.012}, {'line': 0.417, 'change_rate': -0.248, 'holes': -1.312, 'avg_height': -0.3, 'well_depth': 0.0}),
]