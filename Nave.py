import numpy as np
import random
import pygame
import time

# Parámetros del problema
GRAVEDAD = 9.81  # m/s^2
MAX_VELOCIDAD_SEGURA = 5  # Velocidad de aterrizaje segura
NUM_GENERACIONES = 50
TAMANO_POBLACION = 50
PROB_MUTACION = 0.1
UMBRAL_FITNESS = 0.80  # Condición de parada

# Configuración de Pygame
pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
nave_img = pygame.image.load("nave.png")
nave_img = pygame.transform.scale(nave_img, (50, 50))
fondo_img = pygame.image.load("fondo.png")
fondo_img = pygame.transform.scale(fondo_img, (WIDTH, HEIGHT))
explosion_img = pygame.image.load("explosion.png")
explosion_img = pygame.transform.scale(explosion_img, (80, 80))
atterizaje_img = pygame.image.load("atterizaje.png")
atterizaje_img = pygame.transform.scale(atterizaje_img, (80, 80))

# Definir la estructura de un individuo
def crear_individuo():
    return {
        'V': random.uniform(0, 20),  # Velocidad inicial (m/s)
        'S': random.uniform(100, 500),  # Altura inicial (comienza en la parte superior)
        'B': random.uniform(50, 100),  # Combustible disponible (unidades)
        'F': random.uniform(0, 20)  # Fuerza aplicada por los motores (m/s^2)
    }

# Crear la población inicial
def inicializar_poblacion():
    return [crear_individuo() for _ in range(TAMANO_POBLACION)]

# Función de fitness
def calcular_fitness(individuo):
    velocidad_final = individuo['V'] + individuo['F'] - GRAVEDAD
    penalizacion_combustible = (100 - individuo['B']) / 100  # Más combustible usado, menor fitness
    fitness = max(0, 1 - abs(velocidad_final / MAX_VELOCIDAD_SEGURA) - penalizacion_combustible)
    return fitness

# Selección de los mejores individuos
def seleccion(poblacion):
    poblacion_ordenada = sorted(poblacion, key=calcular_fitness, reverse=True)
    return poblacion_ordenada[:TAMANO_POBLACION // 2]  # Selección de los mejores

# Cruce entre individuos
def cruce(padre1, padre2):
    hijo = {
        'V': (padre1['V'] + padre2['V']) / 2,
        'S': (padre1['B'] + padre2['B']) / 2,
        'B': (padre1['B'] + padre2['B']) / 2,
        'F': (padre1['F'] + padre2['F']) / 2,
    }
    return hijo

# Mutación
def mutar(individuo):
    if random.random() < PROB_MUTACION:
        individuo['V'] += random.uniform(0, 2)
        individuo['B'] += random.uniform(0, 5)
        individuo['F'] += random.uniform(0, 2)
    return individuo

# Dibujar la simulación
def dibujar_nave(altura, velocidad, combustible, fuerza, optimo):
    screen.blit(fondo_img, (0, 0))
    nave=600
    for i in range(2):  # Movimiento en 5 segundos
        y_pos = HEIGHT - int(nave * (1 - i / 2))
        screen.blit(fondo_img, (0, 0))
        screen.blit(nave_img, (WIDTH//2 - 25, y_pos))
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(f"Vel: {velocidad:.2f} m/s Alt: {altura:.2f} m B: {combustible:.2f} F: {fuerza:.2f}", True, (255, 255, 255))
        screen.blit(texto, (20, 20))
        pygame.display.flip()
        time.sleep(1)
    
    if optimo:
        mensaje = fuente.render("¡Aterrizaste!", True, (0, 0, 0))  # Letras negras
        screen.blit(mensaje, (WIDTH//2 - 50, HEIGHT//2))
        screen.blit(atterizaje_img, (WIDTH//2 - 40, y_pos))
        pygame.display.flip()
        time.sleep(5)
    else:
        screen.blit(explosion_img, (WIDTH//2 - 40, y_pos))  # Explosión
        pygame.display.flip()
        time.sleep(5)

# Algoritmo genético principal
def algoritmo_genetico():
    poblacion = inicializar_poblacion()
    
    for generacion in range(NUM_GENERACIONES):
        poblacion = seleccion(poblacion)
        nueva_generacion = []
        
        while len(nueva_generacion) < TAMANO_POBLACION:
            padre1, padre2 = random.sample(poblacion, 2)
            hijo = cruce(padre1, padre2)
            hijo = mutar(hijo)
            nueva_generacion.append(hijo)
        
        poblacion = nueva_generacion
        
        # Mejor individuo de la generación actual
        mejor = max(poblacion, key=calcular_fitness)
        velocidad_final = mejor['V'] + mejor['F'] - GRAVEDAD
        print(f"Generación {generacion}: Mejor velocidad final: {velocidad_final:.2f} m/s, Combustible restante: {mejor['B']:.2f}")
        
        optimo = calcular_fitness(mejor) >= UMBRAL_FITNESS
        dibujar_nave(mejor['S'], velocidad_final, mejor['B'], mejor['F'], optimo)
        
        # Condición de parada
        if optimo:
            print("Se ha alcanzado la mejor solución antes del número máximo de generaciones.")
            return mejor
    
    return max(poblacion, key=calcular_fitness)

# Ejecutar el algoritmo
mejor_solucion = algoritmo_genetico()
print("Mejor solución encontrada:", mejor_solucion)

pygame.quit()
