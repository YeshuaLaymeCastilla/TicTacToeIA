# Implementación del algoritmo MiniMax.

# ai.py

import copy
import random

def get_ai_move(board, ai, human):
    best_score = float('-inf')
    best_move = None

    for row in range(3):
        for col in range(3):
            if board[row][col] == '':
                board_copy = copy.deepcopy(board)
                board_copy[row][col] = ai
                score = minimax(board_copy, False, ai, human)
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    # Si no se encontró (no debería pasar), elige al azar
    if best_move is None:
        empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == '']
        return random.choice(empty_cells)

    return best_move

def minimax(board, is_maximizing, ai, human):
    winner = evaluate(board)
    if winner == ai:
        return 1
    elif winner == human:
        return -1
    elif is_draw(board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == '':
                    board[row][col] = ai
                    score = minimax(board, False, ai, human)
                    board[row][col] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == '':
                    board[row][col] = human
                    score = minimax(board, True, ai, human)
                    board[row][col] = ''
                    best_score = min(score, best_score)
        return best_score

def evaluate(board):
    # Horizontal
    for row in board:
        if row[0] == row[1] == row[2] != '':
            return row[0]
    # Vertical
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '':
            return board[0][col]
    # Diagonales
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    return None

def is_draw(board):
    return all(cell != '' for row in board for cell in row) and evaluate(board) is None
