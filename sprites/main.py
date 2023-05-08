from turtle import pos
import pygame
import sys
import os
import random
from pygame.locals import *


# ================================================================
#                       Despliega matriz
# ================================================================

def crea_cuadrado(x: int, y: int, color: tuple, ALTO_CUADRADO: int, ANCHO_CUADRADO: int):

    pygame.draw.rect(ventana, color, [x, y, ANCHO_CUADRADO, ALTO_CUADRADO])


def despliega_matriz(ALTO_CUADRADO: int, ANCHO_CUADRADO: int, matrix: list):

    y = 0
    for row in matrix:
        x = 0
        for item in row:

            # piso
            if item == 0:
                # crea_cuadrado(x, y, (255, 255, 255),
                #               ALTO_CUADRADO, ANCHO_CUADRADO)  # blanco
                ventana.blit(piso, (x, y))
            # pared
            elif item == 1:
                # crea_cuadrado(x, y, (200, 100, 60), ALTO_CUADRADO,
                #               ANCHO_CUADRADO)  # naranjo
                ventana.blit(pared, (x, y))
            # # pasillo o ex-moneda
            elif item == 2:
                crea_cuadrado(x, y, (100, 200, 50), ALTO_CUADRADO,
                              ANCHO_CUADRADO)  #verde
                # ventana.blit(obstaculo, (x, y))
            # pared rompible
            elif item == -1:
                # crea_cuadrado(x, y, (200, 50, 100), ALTO_CUADRADO,
                #               ANCHO_CUADRADO)  # rosado oscuro
                ventana.blit(pared_rompible, (x, y))

            # bomba
            elif item == -2:
                # crea_cuadrado(x, y, (200, 200, 20), ALTO_CUADRADO,
                #               ANCHO_CUADRADO)  # verde amarillo
                ventana.blit(piso, (x, y))
                ventana.blit(bomba, (x, y))

            #llave
            elif item == -3:
                # crea_cuadrado(x, y, (100, 200, 10), ALTO_CUADRADO,
                #               ANCHO_CUADRADO)  # verde claro
                ventana.blit(piso, (x, y))
                ventana.blit(llave, (x, y))

            #puerta
            elif item == -4:
                # crea_cuadrado(x, y, (100, 150, 2), ALTO_CUADRADO,
                #               ANCHO_CUADRADO)  # verde oscuro
                ventana.blit(piso, (x, y))
                ventana.blit(puerta, (x, y))
                
            #powerups
            elif item == -5:
                # crea_cuadrado(x, y, (100, 10, 235), ALTO_CUADRADO,
                #               ANCHO_CUADRADO)  # verde oscuro
                ventana.blit(piso, (x, y))
                ventana.blit(bomba_grande, (x, y))

            x += ANCHO_CUADRADO  # for ever item/number in that row we move one "step" to the right
        y += ALTO_CUADRADO   # for every new row we move one "step" downwards
    # pygame.display.update()

# ================================================================
#                       Generacion random
# ================================================================


def agrega_paredes(mat: list, n: int):

    for i in range(n):

        x = random.randrange(0, len(mat))
        y = random.randrange(0, len(mat[0]))

        while ((x,y) in [(1,1),(1,2),(2,1)] or mat[y][x] != 0):
            x = random.randrange(0, len(mat))
            y = random.randrange(0, len(mat[0]))

        mat[y][x] = -1

    return mat


def agrega_elementos(mat: list):

    x = random.randrange(0, len(mat))
    y = random.randrange(0, len(mat[0]))

    while (mat[y][x] != -1):
        x = random.randrange(0, len(mat))
        y = random.randrange(0, len(mat[0]))

        # mat[y][x] = valor

    return [x,y]


def posicion_amigos(mat: list, pos: list):

    x = random.randrange(0, len(mat))
    y = random.randrange(0, len(mat[0]))

    while (mat[y][x] != -1 or [y, x] in pos):
        x = random.randrange(0, len(mat))
        y = random.randrange(0, len(mat[0]))

    return [x, y]


def explota_bomba_normal(x_bomba:int, y_bomba:int, matrix: list):

    if (matrix[x_bomba+1][y_bomba] == -1):
        matrix[x_bomba+1][y_bomba] = 0

    if (matrix[x_bomba][y_bomba+1] == -1):
        matrix[x_bomba][y_bomba+1] = 0

    if (matrix[x_bomba-1][y_bomba] == -1):
        matrix[x_bomba-1][y_bomba] = 0

    if (matrix[x_bomba][y_bomba-1] == -1):
        matrix[x_bomba][y_bomba-1] = 0

    return matrix

def explota_bomba_grande(x_bomba:int, y_bomba:int, matrix: list):

    if (matrix[x_bomba+1][y_bomba] == -1):
        matrix[x_bomba+1][y_bomba] = 0

    if (matrix[x_bomba][y_bomba+1] == -1):
        matrix[x_bomba][y_bomba+1] = 0

    if (matrix[x_bomba-1][y_bomba] == -1):
        matrix[x_bomba-1][y_bomba] = 0

    if (matrix[x_bomba][y_bomba-1] == -1):
        matrix[x_bomba][y_bomba-1] = 0

    if (matrix[x_bomba+1][y_bomba+1] == -1):
        matrix[x_bomba+1][y_bomba+1] = 0

    if (matrix[x_bomba-1][y_bomba+1] == -1):
        matrix[x_bomba-1][y_bomba+1] = 0

    if (matrix[x_bomba-1][y_bomba-1] == -1):
        matrix[x_bomba-1][y_bomba-1] = 0

    if (matrix[x_bomba+1][y_bomba-1] == -1):
        matrix[x_bomba+1][y_bomba-1] = 0

    return matrix

def movimiento_cpu(matrix: list, posiciones: list, n: int):

        movio = False

        while (not movio):

            direccion = random.randint(0, 7)

            #arriba
            if direccion == 0:
                #print([posiciones[0][0]][posiciones[0][1]-1], matrix[posiciones[0][0]][posiciones[0][1]-1])
                if posiciones[n][1] - 1 >= 0 and matrix[posiciones[n][1]-1][posiciones[n][0]] == 0:
                    posiciones[n][1] -= 1
                    movio = True

            elif direccion == 1:
                #print(matrix[posiciones[n][0]-1][posiciones[n][1]])
                if posiciones[n][0] - 1 >= 0 and matrix[posiciones[n][1]][posiciones[n][0]-1] == 0:
                    posiciones[n][0] -= 1
                    movio = True

            elif direccion == 2:
                #print(matrix[posiciones[n][0]][posiciones[n][1]+1])
                if posiciones[n][1] + 1 < 20 and matrix[posiciones[n][1]+1][posiciones[n][0]] == 0:
                    posiciones[n][1] += 1
                    movio = True

            elif direccion == 3:

                if posiciones[n][0] + 1 < 20 and matrix[posiciones[n][1]][posiciones[n][0]+1] == 0:
                    posiciones[n][0] += 1
                    movio = True
            #quieto
            if (direccion >= 4): movio = True

        return posiciones

# ================================================================
#                       Funciones pantallas
# ================================================================

ANCHO_VENTANA = 1000
ALTO_VENTANA = 700
ANCHO_CUADRADO = 35
ALTO_CUADRADO = 35

LADOS_CUADRADO = (ANCHO_CUADRADO, ALTO_CUADRADO)

pygame.init()

ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Tutorial")
ventana.fill((195, 247, 126))  # color de fondo
pygame.key.set_repeat(500, 50) #Para permitir la repeticion de teclas, primer parametro es cuanto se demora en milisegundos la primera, y el segundo el resto

pantalla_inicio = pygame.image.load('./assets/inicio.png')
pantalla_derrota = pygame.image.load('./assets/game_over.png')
pantalla_victoria = pygame.image.load('./assets/victoria.png')
menu_instrucciones = pygame.image.load('./assets/instrucciones.png')

astronauta = pygame.image.load('./assets/astronaut.png')
astronauta = pygame.transform.scale(astronauta, LADOS_CUADRADO)

bomba = pygame.image.load('./assets/bomb.png')
bomba = pygame.transform.scale(bomba, LADOS_CUADRADO)

bomba_grande = pygame.image.load('./assets/bomb_big.png')
bomba_grande = pygame.transform.scale(bomba_grande, LADOS_CUADRADO)

puerta = pygame.image.load('./assets/door.png')
puerta = pygame.transform.scale(puerta, LADOS_CUADRADO)

llave = pygame.image.load('./assets/key.png')
llave = pygame.transform.scale(llave, LADOS_CUADRADO)

pared = pygame.image.load('./assets/pared.png')
pared = pygame.transform.scale(pared, LADOS_CUADRADO)

piso = pygame.image.load('./assets/piso.png')
piso = pygame.transform.scale(piso, LADOS_CUADRADO)

pared_rompible = pygame.image.load('./assets/pared_rompible.png')
pared_rompible = pygame.transform.scale(pared_rompible, LADOS_CUADRADO)

gusano = pygame.image.load('./assets/worm.png')
gusano = pygame.transform.scale(gusano, LADOS_CUADRADO)


def main_nivel():
    
    # -------------------------------------------------

    matrix =  [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,0,0,0,1,0,1,0,0,1,0,1,0,0,0,1,0,1],
        [1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1],
        [1,0,1,0,0,0,1,1,1,0,0,1,1,1,0,0,0,1,0,1],
        [1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1],
        [1,0,1,0,0,0,1,0,1,0,0,1,0,1,0,0,0,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,0,1],
        [1,0,1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,0,0,0,1,0,1,0,0,1,0,1,0,0,0,1,0,1],
        [1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1],
        [1,0,1,0,0,0,1,1,1,0,0,1,1,1,0,0,0,1,0,1],
        [1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1],
        [1,0,1,0,0,0,1,0,1,0,0,1,0,1,0,0,0,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]

    cantidad_obstaculos = 100
    n_personajes = 3  # minimo 1 para que haya un player
    posiciones = []
    muertos = []
    rip = False
    detonando = 0

    bombas_grandes = 0
    cantidad_powerups = 3
    pos_powerups = []
    tiempo_inicial = pygame.time.get_ticks()
    tiempo_total = 0
    tiempo_maximo = 300000 # 300000milisegundos 300 segundos, 5 minutos

    fuente = pygame.font.SysFont('unispacebold', 32)
    #Personas encontradas
    encontrado = []

    llave = False
    puerta = False
    for i in range(n_personajes):
        encontrado.append(0)

    matrix_nueva = agrega_paredes(matrix, cantidad_obstaculos)

    #Se agregan power-ups
    for i in range(cantidad_powerups):
        pos_powerups.append(agrega_elementos(matrix_nueva)) #-5

    #Se agrega llave
    pos_llave = agrega_elementos(matrix_nueva) #-3

    #Se agrega puerta
    pos_puerta = agrega_elementos(matrix_nueva) #-4

    for i in range(n_personajes):
        posiciones.append(posicion_amigos(matrix_nueva, posiciones))
        # rol_infiltrado.append(0)
        muertos.append(0)

    #Posición del usuario siempre en [1,1]
    posiciones[0] = [1,1]

    # -------------------------------------------------

    pygame.display.flip()

    reloj = pygame.time.Clock()
    despliega_matriz(ALTO_CUADRADO, ANCHO_CUADRADO, matrix_nueva)
    corriendo = True
    while corriendo:

        ventana.fill((31, 52, 87))
        tiempo_total = pygame.time.get_ticks()

           #Se agregan power-ups
        for i in range(len(pos_powerups)):
            if (matrix[pos_powerups[i][1]][pos_powerups[i][0]] == 0):
                matrix[pos_powerups[i][1]][pos_powerups[i][0]] = -5

        if (not llave and matrix[pos_llave[1]][pos_llave[0]] == 0):
            matrix[pos_llave[1]][pos_llave[0]] = -3

        if (matrix[pos_puerta[1]][pos_puerta[0]] == 0):
            matrix[pos_puerta[1]][pos_puerta[0]] = -4

        despliega_matriz(ALTO_CUADRADO, ANCHO_CUADRADO, matrix_nueva)

        # Coloca cpus en el mapa en negro
        for i in range(n_personajes):

            if (muertos[i] < 3):

                x = 0
                x = posiciones[i][0] * ANCHO_CUADRADO
                y = posiciones[i][1] * ALTO_CUADRADO

                # Sólo se muestran si no están en pared
                if (matrix[posiciones[i][1]][posiciones[i][0]] != -1):
                    if (i == 0):
                        ventana.blit(astronauta, (x, y))
                    else:
                        # crea_cuadrado(x, y, (0, 0, 0), ALTO_CUADRADO,
                        #                 ANCHO_CUADRADO)  # negro
                        ventana.blit(gusano, (x, y))

        reloj.tick(15)  # Fuerza a correr a 60 FPS

        #detona bombas
        tiempo_actualizado = pygame.time.get_ticks()
        if (detonando == 1 and tiempo_actualizado - tiempo_pasado >= 1000):
            
            detonando = 0
            matrix[y_bomba][x_bomba] = 0

            if (bombas_grandes <= 0):

                matrix = explota_bomba_normal(y_bomba, x_bomba, matrix)
                if (posiciones[0] in [[x_bomba,y_bomba], [x_bomba,y_bomba+1], [x_bomba,y_bomba+1], [x_bomba-1,y_bomba],[x_bomba,y_bomba-1]]):
                    muertos[0] += 1
                print('boom')

            else:

                matrix = explota_bomba_grande(y_bomba, x_bomba, matrix)
                if (posiciones[0] in [[x_bomba,y_bomba], [x_bomba,y_bomba+1], [x_bomba,y_bomba+1], [x_bomba-1,y_bomba],[x_bomba,y_bomba-1],[x_bomba+1,y_bomba+1], [x_bomba-1,y_bomba+1], [x_bomba-1,y_bomba-1],[x_bomba+1,y_bomba-1]]):
                    muertos[0] += 1
                bombas_grandes -= 1
                print('kaboom')

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                corriendo = False

            #Movimiento player
            elif (event.type == pygame.KEYDOWN):

                if event.key == K_w:
                    if posiciones[0][1] - 1 >= 0 and matrix[posiciones[0][1]-1][posiciones[0][0]] not in [-1,1,-2]:#not in [0, -1]:
                        posiciones[0][1] -= 1

                elif event.key == K_a:
                    if posiciones[0][0] - 1 >= 0 and matrix[posiciones[0][1]][posiciones[0][0]-1] not in [-1,1,-2]:#not in [0, -1]:
                        posiciones[0][0] -= 1

                elif event.key == K_s:
                    if posiciones[0][1] + 1 < 20 and matrix[posiciones[0][1]+1][posiciones[0][0]] not in [-1,1,-2]:#not in [0, -1]:
                        posiciones[0][1] += 1

                elif event.key == K_d:
                    if posiciones[0][0] + 1 < 20 and matrix[posiciones[0][1]][posiciones[0][0]+1] not in [-1,1,-2]:#not in [0, -1]:
                        posiciones[0][0] += 1

                elif event.key == K_SPACE:
                    if (muertos[0] < 3 and detonando == 0 and matrix[posiciones[0][1]][posiciones[0][0]+1] != -4):
                        detonando = 1
                        tiempo_pasado = pygame.time.get_ticks()
                        x_bomba = posiciones[0][0]
                        y_bomba = posiciones[0][1]
                        matrix[y_bomba][x_bomba] = -2

                elif event.key == K_r:
                    if (rip):
                        return False, False

                    else:
                        return True, False

        #matar
        if (muertos[0] < 3 and (posiciones.count(posiciones[0]) > 1)):
            muertos[0] += 1

        #movimiento cpu
        for i in range(n_personajes-1):

            if (encontrado[i+1] and not muertos[i+1]):
                posiciones = movimiento_cpu(matrix, posiciones, i+1)

            if (not encontrado[i+1] and matrix[posiciones[i+1][1]][posiciones[i+1][0]] == 0):
                encontrado[i+1] = 1

        #chequear llave
        for pos in posiciones:

            #Chequea llave
            if (matrix[pos[1]][pos[0]] == -3):
                llave = True
                matrix[pos[1]][pos[0]] = 0

            #Chequea powerup
            if (matrix[pos[1]][pos[0]] == -5):
                bombas_grandes += 1
                matrix[pos[1]][pos[0]] = 0
                pos_powerups.remove(pos)

            #Chequea puerta
            if (llave and matrix[pos[1]][pos[0]] == -4):
                puerta = True
                matrix[pos[1]][pos[0]] = 0


        segundos = (tiempo_maximo - (tiempo_total - tiempo_inicial))//1000
        tiempo_txt = fuente.render(
            f"Quedan {segundos} segundos", True, (255, 255, 255))
        ventana.blit(tiempo_txt, (710, 100))

        vidas_txt = fuente.render(
            f"{3-muertos[0]} vidas", True, (255, 255, 255))
        ventana.blit(vidas_txt, (710, 150))

        powerups_txt = fuente.render(
            f"{bombas_grandes} bombas grandes", True, (255, 255, 255))
        ventana.blit(powerups_txt, (710, 200))

        if(puerta and llave):
            return False, True

        if (muertos[0] >= 3 or tiempo_total - tiempo_inicial >= tiempo_maximo):
            return False, False


        pygame.display.flip()
        pygame.display.update()

    sys.exit()

# --------------------------------------------------------------------------------------------------------------------


def pantallaInstrucciones():

    ventana.fill((100, 150, 80))  # color de fondo

    fuente = pygame.font.SysFont('unispacebold', 32)

    vidasTxt = fuente.render(
        "Aqui van las instrucciones, presione espacio para volver al menu", True, (255, 255, 255))
    ventana.blit(vidasTxt, (100, 100))

    ventana.blit(menu_instrucciones,(0,0))

    pygame.display.flip()

    corriendo = True
    while corriendo:
        for event in pygame.event.get():

            if (event.type == pygame.QUIT):
                corriendo = False

            elif (event.type == pygame.KEYDOWN):

                if event.key == K_SPACE:
                    main_menu()

                elif event.key == K_ESCAPE:
                    corriendo = False

    sys.exit()

# --------------------------------------------------------------------------------------------------------------------

def final(ganador):

    fuente = pygame.font.SysFont('unispacebold', 32)

    if ganador:
    #Imprime pantalla victoria
        ventana.fill((100, 150, 80))  # color de fondo
        texto = fuente.render(
        "ganaste, presione espacio para volver al menu", True, (255, 255, 255))

        ventana.blit(texto, (100,100))
        ventana.blit(pantalla_victoria,(0,0))

    else:
    #imprime pantalla derrota
        ventana.fill((200, 100, 80))  # color de fondo
        texto = fuente.render(
        "perdiste, presione espacio para volver al menu", True, (255, 255, 255))

        ventana.blit(texto, (100,100))
        ventana.blit(pantalla_derrota,(0,0))

    pygame.display.flip()
    corriendo = True

    while corriendo:
        for event in pygame.event.get():

                if (event.type == pygame.QUIT):
                    corriendo = False

                #Controlar jugador1
                elif (event.type == pygame.KEYDOWN):

                    if event.key == K_r or event.key == K_SPACE:
                        main_menu()


                    elif event.key == K_ESCAPE:
                        corriendo = False
    sys.exit(0)

# --------------------------------------------------------------------------------------------------------------------

def main_menu():

    ventana.fill((195, 150, 200))  # color de fondo

    fuente = pygame.font.SysFont('unispacebold', 32)

    vidasTxt = fuente.render(
        "menu principal, presione espacio para empezar, i para instrucciones", True, (255, 255, 255))
    ventana.blit(vidasTxt, (100, 100))

    ventana.blit((pantalla_inicio),(0,0))

    pygame.display.flip()

    corriendo = True
    while corriendo:
        for event in pygame.event.get():

            if (event.type == pygame.QUIT):
                corriendo = False

            # Controlar jugador1
            elif (event.type == pygame.KEYDOWN):

                if event.key == K_SPACE:
                    reiniciar = True
                    while reiniciar:
                        reiniciar, ganador = main_nivel()
                    final(ganador)

                elif event.key == K_ESCAPE:
                    corriendo = False

                elif event.key == K_i:
                    pantallaInstrucciones()

    sys.exit()


main_menu()