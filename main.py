# Punto de entrada. Menú inicial y control general.

# main.py
import pygame
from graphics import init_display, draw_text
from game import start_local_game, start_ai_game

def main():
    screen = init_display()
    draw_text(screen, "Seleccione modo:", 48, 300, 200)
    draw_text(screen, "1 - Jugador vs Jugador", 36, 300, 300)
    draw_text(screen, "2 - Jugador vs IA", 36, 300, 360)
    pygame.display.update()

    modo = None
    while modo not in [1, 2]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    modo = 1
                elif event.key == pygame.K_2:
                    modo = 2

    # Preguntar "el mejor de cuántos gana"
    partidas = ""
    esperando_confirmacion = True

    while esperando_confirmacion:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    partidas += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    partidas = partidas[:-1]
                elif event.key == pygame.K_RETURN and partidas.isdigit():
                    esperando_confirmacion = False

        screen.fill((255, 255, 255))
        draw_text(screen, "¿El mejor de cuántos gana?", 40, 300, 280)
        draw_text(screen, partidas, 50, 300, 340)
        draw_text(screen, "Presiona ENTER para continuar", 24, 300, 400)
        pygame.display.update()

    partidas = int(partidas)
    if modo == 1:
        start_local_game(screen, partidas)
    else:
        start_ai_game(screen, partidas)

if __name__ == "__main__":
    main()
