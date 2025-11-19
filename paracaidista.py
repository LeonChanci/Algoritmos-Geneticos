import random
from config import *

class Paracaidista:
    def __init__(self, masa=None, velocidad=None, fuerza=None, tiempo=None):
        # random.uniform: Genera un número decimal aleatorio entre a y b (incluyendo ambos)
        self.masa = masa if masa is not None else random.uniform(MASA_MIN, MASA_MAX)
        self.velocidad = velocidad if velocidad is not None else random.uniform(VELOCIDAD_MIN, VELOCIDAD_MAX)
        self.fuerza = fuerza if fuerza is not None else random.uniform(FUERZA_MIN, FUERZA_MAX)
        self.tiempo = tiempo if tiempo is not None else random.uniform(TIEMPO_MIN, TIEMPO_MAX)
        
    def calcular_fitness(self):
        # Se evalua que tan cerca se está de los valores ideales
        # Si esta cerca la penalización es baja, si el valor esta lejos la penalización es alta
        penalizacion_velocidad = abs(self.velocidad - VELOCIDAD_IDEAL) ** 1.5
        penalizacion_tiempo = abs(self.tiempo - TIEMPO_IDEAL) ** 0.8
        penalizacion_masa = abs(self.masa - MASA_IDEAL) / (MASA_MAX - MASA_MIN)
        penalizacion_fuerza = abs(self.fuerza - FUERZA_IDEAL) / (FUERZA_MAX - FUERZA_MIN)

        fitness = (PESO_VELOCIDAD * penalizacion_velocidad +
                   PESO_TIEMPO * penalizacion_tiempo +
                   PESO_MASA * penalizacion_masa +
                   PESO_FUERZA * penalizacion_fuerza)

        return fitness
        
    # TÉCNICA DE CRUCE UNIFORME
    def cruzar(self, otro_paracaidista):
        # Cruce uniforme: se cruzan dos paracaidistas específicos
        # Define la MECÁNICA del cruce genético
        # Retorna UN NUEVO hijo combinando genes de dos padres
        return Paracaidista(
            masa=self.masa if random.random() < 0.5 else otro_paracaidista.masa,
            velocidad=self.velocidad if random.random() < 0.5 else otro_paracaidista.velocidad,
            fuerza=self.fuerza if random.random() < 0.5 else otro_paracaidista.fuerza,
            tiempo=self.tiempo if random.random() < 0.5 else otro_paracaidista.tiempo
        )
    
    # 1, TÉCNICA DE MUTACIÓN FUERTE (10% de probabilidad)
    # 2. TÉCNICA DE MUTACIÓN SUAVE (90% de probabilidad)
    def mutar(self):
        # Como MUTA el paracaidista específico
        # Define la MECÁNICA de la mutación individual
        # Modifica los genes de el paracaidista en particular
        if random.random() < PORCENTAJE_MUTACION_FUERTE:
            # Mutación fuerte: cambiar todos los atributos 
            # Cambio completo de todos los genes
            self.masa = random.uniform(MASA_MIN, MASA_MAX)
            self.velocidad = random.uniform(VELOCIDAD_MIN, VELOCIDAD_MAX)
            self.fuerza = random.uniform(FUERZA_MIN, FUERZA_MAX)
            self.tiempo = random.uniform(TIEMPO_MIN, TIEMPO_MAX)

        # Mutación normal: cambiar solo un atributo
        # Pequeña variación en un solo gen
        else:
            # Se elige aleatoriamente el atributo a mutar 0 - 34
            atributo_a_mutar = random.randint(0, 3)
            # Se elige aleatoriamente cuanto va a cambiar el atributo
            variacion = random.gauss(0, 0.3)  # Pequeña variación gaussiana
            
            if atributo_a_mutar == 0:
                self.masa = max(MASA_MIN, min(MASA_MAX, self.masa * (1 + variacion)))
            elif atributo_a_mutar == 1:
                self.velocidad = max(VELOCIDAD_MIN, min(VELOCIDAD_MAX, self.velocidad * (1 + variacion)))
            elif atributo_a_mutar == 2:
                self.fuerza = max(FUERZA_MIN, min(FUERZA_MAX, self.fuerza * (1 + variacion)))
            else:
                self.tiempo = max(TIEMPO_MIN, min(TIEMPO_MAX, self.tiempo * (1 + variacion)))
    
    def __str__(self):
        return f"Masa: {self.masa:.2f} kg, Vel: {self.velocidad:.2f} m/s, Fuerza: {self.fuerza:.2f} N, Tiempo: {self.tiempo:.2f} s, Fitness: {self.calcular_fitness():.2f}"