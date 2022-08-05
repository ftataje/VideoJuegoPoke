import random
import pygame
import math

from pygame import mixer

pygame.init()

pantalla = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Invasión Mankey")
icono = pygame.image.load("pokebola.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("fondo001.jpg")

mixer.music.load("sonido_fondo002.mp3")
mixer.music.play(-1)

img_jugador = pygame.image.load("pikachu.png")
jugador_x = 368
jugador_y = 536
jugador_x_cambio = 0

img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("mankey.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(20, 200))
    enemigo_x_cambio.append(0.3)
    enemigo_y_cambio.append(50)

img_bala = pygame.image.load("relampago.png")
bala_x = 0
bala_y = 536
bala_x_cambio = 0
bala_y_cambio = 1
bala_visible = False

puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

fuente_final = pygame.font.Font("freesansbold.ttf", 40)

def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1,2))
    if distancia < 27:
        return True
    else:
        return False

def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (0,0,0))
    pantalla.blit(texto, (x, y))

def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (0, 0, 0))
    pantalla.blit(mi_fuente_final, (60, 200))

se_ejecuta = True
while se_ejecuta:

    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.5
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.5
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound("trueno_sonido000.mp3")
                sonido_bala.play()
                if bala_visible == False:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    jugador_x += jugador_x_cambio
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    for e in range(cantidad_enemigos):
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break
        enemigo_x[e] += enemigo_x_cambio[e]
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.3
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.3
            enemigo_y[e] += enemigo_y_cambio[e]
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound("golpe_sonido.mp3")
            sonido_colision.play()
            bala_y = 536
            bala_visible = False
            puntaje += 1
            print(puntaje)
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(20, 200)
        enemigo(enemigo_x[e], enemigo_y[e], e)

    if bala_y <= -64:
        bala_y = 536
        bala_visible = False
    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    jugador(jugador_x, jugador_y)

    mostrar_puntaje(texto_x, texto_y)

    pygame.display.update()
