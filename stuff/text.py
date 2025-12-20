import pygame

font = pygame.font.Font("fonts/Pretendard-Regular.ttf", 20)
font_bold = pygame.font.Font("fonts/Pretendard-Bold.ttf", 30)

def render_text(font, text, color="#ffffff"):
    surface = font.render(text, True, color)
    return surface