# Lógica del tablero, turnos y condiciones de victoria.

import pygame
import random
from graphics import draw_grid, draw_mark, draw_text, draw_winner_line
from config import *
from ai import get_ai_move

def check_winner(board):
    # Revisa filas
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != '':
            return board[row][0], ((0, row), (2, row))
    # Revisa columnas
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return board[0][col], ((col, 0), (col, 2))
    # Revisa diagonal principal
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0], ((0, 0), (2, 2))
    # Revisa diagonal secundaria
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2], ((2, 0), (0, 2))
    return None, None

def is_full(board):
    return all(cell != '' for row in board for cell in row)

def draw_win_line(screen, win_coords):
    start = (win_coords[0][0] * CELL_SIZE + CELL_SIZE // 2,
             win_coords[0][1] * CELL_SIZE + CELL_SIZE // 2)
    end = (win_coords[1][0] * CELL_SIZE + CELL_SIZE // 2,
           win_coords[1][1] * CELL_SIZE + CELL_SIZE // 2)
    draw_winner_line(screen, start, end)

def reset_board():
    return [['' for _ in range(3)] for _ in range(3)]

def draw_score(screen, score1, score2, best_of, modo, turno_actual=None, inicio=False):
    pygame.draw.rect(screen, WHITE, pygame.Rect(0, 600, 600, 100))
    if modo == 1:
        draw_text(screen, f"X: {score1}", 28, 100, 620)
        draw_text(screen, f"O: {score2}", 28, 500, 620)
    else:
        draw_text(screen, f"Tú: {score1}", 28, 100, 620)
        draw_text(screen, f"IA: {score2}", 28, 500, 620)

    draw_text(screen, f"Al mejor de {best_of}", 24, WIDTH // 2, 650)

    if inicio:
        draw_text(screen, turno_actual, 28, WIDTH // 2, 610)
    elif turno_actual:
        draw_text(screen, f"{turno_actual}", 28, WIDTH // 2, 610)

    pygame.display.update()

def announce_winner(screen, winner_text):
    screen.fill(WHITE)
    draw_text(screen, winner_text, 50, WIDTH // 2, HEIGHT // 2)
    pygame.display.update()
    pygame.time.wait(3000)

def start_local_game(screen, best_of):
    board = reset_board()
    turn = 'X'
    score_x, score_o = 0, 0
    running = True

    while running:
        screen.fill(WHITE)
        draw_grid(screen)
        draw_score(screen, score_x, score_o, best_of, modo=1, turno_actual=f"Empieza {turn}", inicio=True)
        pygame.time.wait(1500)
        board = reset_board()
        winner = None

        while not winner and not is_full(board):
            draw_score(screen, score_x, score_o, best_of, modo=1, turno_actual=f"Turno: {turn}")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row = y // CELL_SIZE
                    col = x // CELL_SIZE
                    if row < 3 and board[row][col] == '':
                        board[row][col] = turn
                        draw_mark(screen, row, col, turn)
                        pygame.display.update()
                        winner, coords = check_winner(board)
                        if winner:
                            draw_win_line(screen, coords)
                            pygame.display.update()
                            pygame.time.wait(1000)
                            if winner == 'X':
                                score_x += 1
                            else:
                                score_o += 1
                        turn = 'O' if turn == 'X' else 'X'

        if is_full(board) and not winner:
            pygame.time.wait(1000)

        if score_x == best_of:
            announce_winner(screen, "¡Gana X!")
            running = False
        elif score_o == best_of:
            announce_winner(screen, "¡Gana O!")
            running = False

def start_ai_game(screen, best_of):
    board = reset_board()
    human = 'X' if random.choice([True, False]) else 'O'
    ai = 'O' if human == 'X' else 'X'
    turn = 'X'
    score_human, score_ai = 0, 0
    running = True

    while running:
        screen.fill(WHITE)
        quien_empieza = "Tú empiezas primero" if turn == human else "La IA empieza primero"
        draw_grid(screen)
        draw_score(screen, score_human, score_ai, best_of, modo=2, turno_actual=quien_empieza, inicio=True)
        pygame.time.wait(1500)
        board = reset_board()
        winner = None

        while not winner and not is_full(board):
            if turn == human:
                draw_score(screen, score_human, score_ai, best_of, modo=2, turno_actual="Tu turno")
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        row = y // CELL_SIZE
                        col = x // CELL_SIZE
                        if row < 3 and board[row][col] == '':
                            board[row][col] = human
                            draw_mark(screen, row, col, human)
                            pygame.display.update()
                            winner, coords = check_winner(board)
                            if winner:
                                draw_win_line(screen, coords)
                                pygame.display.update()
                                pygame.time.wait(1000)
                                if winner == human:
                                    score_human += 1
                                else:
                                    score_ai += 1
                            turn = ai
            else:
                draw_score(screen, score_human, score_ai, best_of, modo=2, turno_actual="Turno de la IA")
                pygame.time.wait(500)
                row, col = get_ai_move(board, ai, human)
                board[row][col] = ai
                draw_mark(screen, row, col, ai)
                pygame.display.update()
                winner, coords = check_winner(board)
                if winner:
                    draw_win_line(screen, coords)
                    pygame.display.update()
                    pygame.time.wait(1000)
                    if winner == ai:
                        score_ai += 1
                    else:
                        score_human += 1
                turn = human

        if is_full(board) and not winner:
            pygame.time.wait(1000)

        if score_human == best_of:
            announce_winner(screen, "¡Ganaste!")
            running = False
        elif score_ai == best_of:
            announce_winner(screen, "¡La IA gana!")
            running = False
