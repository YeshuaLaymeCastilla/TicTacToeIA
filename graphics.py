# Todo lo visual: dibujo del tablero, piezas, líneas, textos.

import pygame
from config import *

def init_display():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic Tac Toe")
    screen.fill(WHITE)
    return screen

def draw_grid(screen):
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), LINE_WIDTH)

def draw_mark(screen, row, col, player):
    center_x = col * CELL_SIZE + CELL_SIZE // 2
    center_y = row * CELL_SIZE + CELL_SIZE // 2
    radius = CELL_SIZE // 4
    if player == 'X':
        color = BLUE
        offset = radius // 1.5
        pygame.draw.line(screen, color, (center_x - offset, center_y - offset),
                         (center_x + offset, center_y + offset), LINE_WIDTH)
        pygame.draw.line(screen, color, (center_x + offset, center_y - offset),
                         (center_x - offset, center_y + offset), LINE_WIDTH)
    else:
        color = RED
        pygame.draw.circle(screen, color, (center_x, center_y), radius, LINE_WIDTH)

def draw_winner_line(screen, start_pos, end_pos):
    pygame.draw.line(screen, PURPLE, start_pos, end_pos, LINE_WIDTH)

def draw_text(screen, text, size, x, y):
    font = pygame.font.SysFont(None, size)
    img = font.render(text, True, TEXT_COLOR)
    rect = img.get_rect(center=(x, y))
    screen.blit(img, rect)
