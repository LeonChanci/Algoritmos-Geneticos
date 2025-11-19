import numpy as np
import random
from config import *
from paracaidista import Paracaidista


class AlgoritmoGenetico:
    def __init__(self):
        self.poblacion = []
        self.mejores_fitness = []
        self.promedio_fitness = []
        self.mejores_individuos = []
        self.mejor_paracaidista = None
        
    def inicializar_poblacion(self):
        # Llenar el vector población con el tamaño de la población -> 10 paracaidistas
        self.poblacion = [Paracaidista() for _ in range(TAMANO_POBLACION)]
        self.mejores_fitness = []
        self.promedio_fitness = []
        self.mejores_individuos = []
        self.mejor_paracaidista = None
        
    def evaluar_poblacion(self):
        # Evaluar la población y ordenarla
        return sorted(self.poblacion, key=lambda x: x.calcular_fitness())
        # Resultado: [mejor, segundo_mejor, tercero, ..., peor]
    
    # TÉCNICA ÉLISTICA PARA LOS 2 MEJORES
    # TÉCNICA DE SELECCION PROPORCIONAL PARA LOS DEMAS
    def seleccionar(self, poblacion_evaluada):
        # Élite: los mejores directamente
        seleccionados = poblacion_evaluada[:SELECCIONAR_MEJORES] # Selecciona los 2 mejores
        
        # Ruleta: para el resto, pero asegurando diversidad - convergencia media
        # Ruleta: donde cada paracaidista tiene un espacio proporcional a su calidad (entre mejor fitness mas probable)
        fitness_values = [ind.calcular_fitness() for ind in poblacion_evaluada]
        max_fitness = max(fitness_values)
        
        # pesos = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1] ← p1=mejor, p10=peor
        pesos = [max_fitness - fit + 0.1 for fit in fitness_values]  # +0.1 para evitar 0
        # Esto CREA una probabilidad de selección dinámica:
        # - Mejores individuos: Alta probabilidad
        # - Peores individuos: Baja probabilidad

        # Guardar las pociciones de los mejores individuos
        indices_seleccionados = set(range(SELECCIONAR_MEJORES))
        
        # Se gira la ruleta 8 veces
        while len(seleccionados) < TAMANO_POBLACION: # Hasta completar 10
            # Los mejores tienen pesos más altos → más probabilidad
            idx = random.choices(range(len(poblacion_evaluada)), weights=pesos, k=1)[0]
            # Resultado posible: [p1, p1, p2, p4, p1, p2, p4, p3]
            if idx not in indices_seleccionados:
                seleccionados.append(poblacion_evaluada[idx])
                indices_seleccionados.add(idx)
        
        return seleccionados
    
    # TÉCNICA DE CRUCE UNIFORME
    def cruzar(self, seleccionados):
        # "CUÁNDO y QUÉ paracaidistas se cruzan"
        # Define la ESTRATEGIA de reproducción de la población
        # Gestiona todo el proceso de creación de nueva generación
        nueva_poblacion = seleccionados[:SELECCIONAR_MEJORES]  # Mantener élite
        
        # Crear 8 nuevos hijos por cruce
        while len(nueva_poblacion) < TAMANO_POBLACION: # Hasta completar 10
            # random.sample: Devuelve una lista de 2 elementos únicos seleccionados aleatoriamente de la lista
            # Sacamos un padre y una madre aleatoriamente de los 10 paracaidistas seleccionados
            padre, madre = random.sample(seleccionados, 2)  # Dos padres diferentes

            # random.random(): Genera un número decimal aleatorio entre 0.0 y 1.0 (incluyendo 0.0, excluyendo 1.0)
            if random.random() < PROBABILIDAD_CRUCE:
                hijo = padre.cruzar(madre)
                nueva_poblacion.append(hijo)
            else:
                # Si no hay cruce, agregar uno de los padres aleatoriamente}
                # random.choice(): Selecciona un elemento aleatorio de una lista (puede repetir elementos)
                nueva_poblacion.append(random.choice([padre, madre]))
                    
        return nueva_poblacion
        
    # 1. TÉCNICA DE MUTACIÓN FUERTE (10% de probabilidad)
    # 2. TÉCNICA DE MUTACIÓN SUAVE (90% de probabilidad)
    def mutar(self, poblacion):
        # "CUÁNDO y QUÉ paracaidistas mutan"
        # Define la ESTRATEGIA de mutación de la población
        # Decide qué individuos deben mutar y con qué probabilidad
        for i, individuo in enumerate(poblacion):
            # Mutar todos los individuos, pero con diferente probabilidad
            if i < SELECCIONAR_MEJORES:
                # Mutación suave para la élite en 0.3
                prob_mut = PROBABILIDAD_MUTACION * 0.3  # Menos mutación -> Conservar buenos genes 
                # 0.3 reduce la probabilidad base a casi un tercio
            else:
                # Mutación normal para el resto
                prob_mut = PROBABILIDAD_MUTACION * (1 + individuo.calcular_fitness() / 50) # Más mutación -> Peores individuos
                # Ejem: 20.00 (Muy malo) -> 0.5 * (1 + 20/50) = 70%	Necesita mucha más mutación
                # Ejem: 0.02 (Excelente) -> 0.5 * (1 + 0.02/50) = 50.2%	Mutación normal
            
            if random.random() < min(prob_mut, 0.6):
                individuo.mutar()
        return poblacion
    
    def ejecutar(self, generaciones=10):
        self.inicializar_poblacion()
        
        print(f"# Generaciones: {generaciones}")

        # MOSTRAR POBLACIÓN INICIAL
        print("=" * 100)
        print("POBLACIÓN INICIAL (10 PARACAIDISTAS ALEATORIOS):")
        print("=" * 100)
        for i, paracaidista in enumerate(self.poblacion, 1):
            print(f"Paracaidista {i}: {paracaidista}")
        print("=" * 100)
        print("\nINICIANDO EVOLUCIÓN...\n")

        for generacion in range(generaciones):
            # Evaluar la ppoblación y ordenarla
            poblacion_evaluada = self.evaluar_poblacion()

            # Se selecciona el mejor individuo
            mejor_individuo = poblacion_evaluada[0]
            
            # Registrar estadísticas
            fitness_values = [ind.calcular_fitness() for ind in poblacion_evaluada]
            self.mejores_fitness.append(min(fitness_values))
            self.promedio_fitness.append(sum(fitness_values) / len(fitness_values))
            self.mejores_individuos.append(mejor_individuo)
            
            # Mostrar información en consola (solo cada 10 generaciones para no saturar)
            if (generacion + 1) % 10 == 0 or generacion == 0 or generacion == generaciones - 1:
                print(f"Generación {generacion + 1}:")
                # Mejor fitness: El valor más bajo de fitness en la generación (el individuo más apto)
                print(f"Mejor fitness: {self.mejores_fitness[-1]:.4f}")
                # Promedio fitness: La suma de todos los fitness dividida por el número de individuos
                print(f"Promedio fitness: {self.promedio_fitness[-1]:.4f}")

                print(f"Mejor paracaidista: {mejor_individuo}")
                print("-" * 100)

            # Guardar el mejor de cada generación    
            self.mejor_paracaidista = mejor_individuo

            # Seleccionar, cruzar y mutar
            seleccionados = self.seleccionar(poblacion_evaluada)
            nueva_poblacion = self.cruzar(seleccionados)
            self.poblacion = self.mutar(nueva_poblacion)
  
        # Mostrar el mejor resultado final
        mejor = min(self.poblacion, key=lambda x: x.calcular_fitness())
        print("\n" + "="*100)
        print("MEJOR PARACAIDISTA ENCONTRADO:")
        print(mejor)
        print("="*100)

        # Encontrar el mejor absoluto de todas las generaciones
        self.mejor_paracaidista = min(self.mejores_individuos, key=lambda x: x.calcular_fitness())
        
        return self.mejor_paracaidista