import random
from config_recetas import *

class Receta:
    def __init__(self, ingredientes=None, pasos=None):
        # Validar y asegurar mínimo 3 ingredientes y 3 pasos
        if ingredientes is None:
            num_ingredientes = random.randint(3, 6)
            self.ingredientes = random.sample(INGREDIENTES_BASE, k=num_ingredientes)
        else:
            self.ingredientes = ingredientes
        
        if pasos is None:
            num_pasos = random.randint(3, min(5, len(PASOS_BASE)))
            self.pasos = random.sample(PASOS_BASE, k=num_pasos)
        else:
            self.pasos = pasos
        
        # Validar mínimos
        if len(self.ingredientes) < 3:
            # Agregar ingredientes aleatorios para cumplir mínimo
            disponibles = [ing for ing in INGREDIENTES_BASE if ing not in self.ingredientes]
            if disponibles:
                faltantes = 3 - len(self.ingredientes)
                self.ingredientes.extend(random.sample(disponibles, k=min(faltantes, len(disponibles))))
        
        if len(self.pasos) < 3:
            # Agregar pasos aleatorios para cumplir mínimo
            disponibles = [paso for paso in PASOS_BASE if paso not in self.pasos]
            if disponibles:
                faltantes = 3 - len(self.pasos)
                self.pasos.extend(random.sample(disponibles, k=min(faltantes, len(disponibles))))

    def calcular_valores_reales(self):
        """Calcula los valores reales de nutrición, costo y tiempo"""
        proteina = sum(INGREDIENTES_INFO[i]["proteina"] for i in self.ingredientes)
        carbo = sum(INGREDIENTES_INFO[i]["carbo"] for i in self.ingredientes)
        grasa = sum(INGREDIENTES_INFO[i]["grasa"] for i in self.ingredientes)
        precio = sum(INGREDIENTES_INFO[i]["precio"] for i in self.ingredientes)
        tiempo = sum(PASOS_TIEMPO[p] for p in self.pasos)
        
        return {
            "proteina": round(proteina, 1),
            "carbohidratos": round(carbo, 1),
            "grasas": round(grasa, 1),
            "costo_total": precio,
            "tiempo_total": tiempo,
            "calorias_aproximadas": round(proteina * 4 + carbo * 4 + grasa * 9, 1)
        }

    def calcular_fitness(self):
        valores_reales = self.calcular_valores_reales()
        proteina = valores_reales["proteina"]
        carbo = valores_reales["carbohidratos"]
        grasa = valores_reales["grasas"]
        precio = valores_reales["costo_total"]
        tiempo = valores_reales["tiempo_total"]
        
        # PENALIZACIÓN POR NO CUMPLIR MÍNIMOS
        penalizacion = 0
        if len(self.ingredientes) < 3:
            penalizacion += 0.3
        if len(self.pasos) < 3:
            penalizacion += 0.3
        
        # **FÓRMULAS MEJORADAS**
        # NUTRICIÓN: Meta de 30-50g proteína, 40-60g carbohidratos, 10-20g grasas
        nutricion_score = 0
        if 35 <= proteina <= 45 and 45 <= carbo <= 55 and 12 <= grasa <= 18:
            nutricion_score = 0.9 + min(0.1, (proteina + carbo) / 300)
        else:
            # Puntaje proporcional a qué tan cerca está del rango ideal
            proteina_dist = max(0, abs(proteina - 40) / 40)  # 40g como ideal
            carbo_dist = max(0, abs(carbo - 50) / 50)        # 50g como ideal
            grasa_dist = max(0, abs(grasa - 15) / 15)        # 15g como ideal
            nutricion_score = 0.5 / (1 + (proteina_dist + carbo_dist + grasa_dist))
        
        # COSTO: Ideal alrededor de $10,000
        if precio <= 15000:  # Hasta $15,000 es aceptable
            costo_score = 1.0 - (precio / 30000)  # $30,000 daría 0
        else:
            costo_score = max(0, 1.0 - (precio - 15000) / 30000)
        
        # TIEMPO: Ideal hasta 45 minutos
        if tiempo <= 60:  # Hasta 1 hora es aceptable
            tiempo_score = 1.0 - (tiempo / 120)  # 2 horas daría 0
        else:
            tiempo_score = max(0, 1.0 - (tiempo - 60) / 120)
        
        # VARIEDAD: Premiar recetas con más variedad de ingredientes
        variedad_score = min(1.0, len(self.ingredientes) / 8)
        
        # FITNESS FINAL (con penalización)
        total_fitness = (nutricion_score * 0.4 + 
                        costo_score * 0.3 + 
                        tiempo_score * 0.2 +
                        variedad_score * 0.1)
        
        total_fitness = max(0, total_fitness - penalizacion)
        
        return {
            "total": round(total_fitness, 4),
            "nutricion": round(nutricion_score, 4),
            "costo": round(costo_score, 4),
            "tiempo": round(tiempo_score, 4),
            "valores_reales": valores_reales  # ← NUEVO: Incluir valores reales
        }
    
    # Evalúa qué tan balanceada es la receta en proteínas, carbohidratos y grasas.
    def evaluar_nutricion(self):
        total = {"proteina": 0, "carbo": 0, "grasa": 0}
        for ing in self.ingredientes:
            info = INGREDIENTES_INFO.get(ing, {})
            for k in total:
                total[k] += info.get(k, 0)
        # Penaliza desequilibrio
        promedio = sum(total.values()) / 3
        desviacion = sum(abs(total[k] - promedio) for k in total)
        return 1 / (desviacion + 1)

    # Suma el precio de todos los ingredientes.
    def evaluar_costo(self):
        return sum(INGREDIENTES_INFO.get(ing, {}).get("precio", 1.0) for ing in self.ingredientes)

    # Suma el tiempo estimado de todos los pasos.
    def evaluar_tiempo(self):
        return sum(PASOS_TIEMPO.get(p, 10) for p in self.pasos)

    def cruzar(self, otra):
        # 1. Combinar ingredientes de ambos padres (sin repetir)
        ingredientes_combinados = list(set(self.ingredientes + otra.ingredientes))
        # Ej: Padre: [pollo, tomate, cebolla], Madre: [pollo, pasta, queso]
        # Resultado: [pollo, tomate, cebolla, pasta, queso]

        # 2. Mezclar aleatoriamente (no por proteína)
        random.shuffle(ingredientes_combinados)
        # Resultado: [queso, tomate, pollo, cebolla, pasta] (orden aleatorio)

        # 3. Seleccionar 3 a 6 ingredientes del conjunto mezclado
        num_ingredientes = random.randint(3, 6)
        hijo_ingredientes = ingredientes_combinados[:num_ingredientes]
        # Ej: Si num_ingredientes=4 → [queso, tomate, pollo, cebolla]

        # 1. Combinar todos los pasos de ambos padres (sin repetir)
        todos_los_pasos = list(set(self.pasos + otra.pasos))
        # Ej: Padre: [cortar, freír, servir], Madre: [mezclar, hornear, servir]
        # Resultado: [cortar, freír, servir, mezclar, hornear]

        # 2. Mezclar aleatoriamente
        random.shuffle(todos_los_pasos)
        # Resultado: [hornear, cortar, servir, mezclar, freír]
        
        # 3. Seleccionar 3 a 5 pasos
        num_pasos = random.randint(3, 5)
        hijo_pasos = todos_los_pasos[:num_pasos]
        # Ej: Si num_pasos=3 → [hornear, cortar, servir]

        # 4. ORDEN LÓGICO (50% de probabilidad)
        if random.random() < 0.5:  # 50% de aplicar orden lógico
            pasos_ordenados = ['cortar', 'marinar', 'mezclar', 'hervir', 'freír', 'saltear', 'grillar', 'hornear', 'batir', 'servir']

            # Filtra manteniendo el orden lógico
            hijo_pasos = [p for p in pasos_ordenados if p in hijo_pasos]
            # Ej: Si hijo_pasos tenía [hornear, cortar, servir] → se reordena a [cortar, hornear, servir]

        return Receta(hijo_ingredientes, hijo_pasos)

    # TÉCNICA 
    def mutar(self):
        # 60% de chance de mutar ingredientes
        if random.random() < 0.6:
            
            # Número entre 0 y 1
            tipo_mutacion = random.random()
            
            # Opciones disponibles (ingredientes que NO están en la receta)
            opciones = [ing for ing in INGREDIENTES_BASE if ing not in self.ingredientes]
                
            if tipo_mutacion < 0.25:  # 25% - Mutación por nutrición
                # Busca el ingrediente MÁS proteico disponible
                nuevo = max(opciones, key=lambda x: INGREDIENTES_INFO[x]["proteina"])
                # Ej: Si opciones=[pollo, lentejas, huevo] → elige pollo (25g proteína)

            elif tipo_mutacion < 0.50:  # 25% - Mutación por economía
                # Busca el ingrediente MÁS barato disponible
                nuevo = min(opciones, key=lambda x: INGREDIENTES_INFO[x]["precio"])
                # Ej: Elige ajo ($1,500) en lugar de pollo ($12,000)

            elif tipo_mutacion < 0.75:  # 25% - Mutación balanceada
                # Busca ingrediente con precio cercano a $5,000 (balanceado)
                nuevo = min(opciones, key=lambda x: abs(INGREDIENTES_INFO[x]["precio"] - 5000))
                # Ej: Elige pasta ($4,000) o tomate ($3,000)

            else:  # 25% - Mutación completamente aleatoria
                # Elige cualquier ingrediente al azar
                nuevo = random.choice(opciones)
            
            # REEMPLAZA un ingrediente aleatorio de la receta
            idx = random.randint(0, len(self.ingredientes) - 1)
            self.ingredientes[idx] = nuevo
            # Ej: Receta: [pollo, tomate, cebolla] → puede quedar [pollo, QUESO, cebolla]
    
        # 60% de chance de mutar pasos
        if random.random() < 0.4:  # 40% de mutar pasos
            opciones_pasos = [p for p in PASOS_BASE if p not in self.pasos]
            if opciones_pasos:
                # 50% agregar paso, 50% cambiar paso existente
                if random.random() < 0.5 and len(self.pasos) < 5:
                    self.pasos.append(random.choice(opciones_pasos))
                    # Ej: [cortar, freír, servir] → [cortar, freír, servir, MARINAR]
                else:  # 50% - CAMBIAR PASO EXISTENTE
                    idx_paso = random.randint(0, len(self.pasos) - 1)
                    self.pasos[idx_paso] = random.choice(opciones_pasos)
                    # Ej: [cortar, FREÍR, servir] → [cortar, HORNEAR, servir]

    def __repr__(self):
        return f"Receta({self.ingredientes}, {self.pasos})"

class AlgoritmoRecetas:
    def __init__(self):
        self.poblacion = []
        self.mejores_fitness = []
        self.promedio_fitness = []
        self.mejores_individuos = []
        self.mejor_receta = None

    def inicializar_poblacion(self):
        self.poblacion = [Receta() for _ in range(TAMANO_POBLACION)]

    def evaluar_poblacion(self):
        # Ordena la población de mayor a menor fitness.
        evaluaciones = [(r, r.calcular_fitness()) for r in self.poblacion]
        evaluaciones.sort(key=lambda x: x[1]["total"], reverse=True)
        return [r for r, f in evaluaciones]

    # TÉCNICA ELITISTA
    # TÉCNICA POR TORNEO
    def seleccionar(self, poblacion_evaluada, k=3):
        seleccionados = []

        # Mantener élite si lo deseas
        seleccionados.extend(poblacion_evaluada[:SELECCIONAR_MEJORES])

        while len(seleccionados) < TAMANO_POBLACION:
            # Elegir k competidores al azar
            competidores = random.sample(poblacion_evaluada, k)
            # Seleccionar el mejor entre ellos
            ganador = max(competidores, key=lambda x: x.calcular_fitness()["total"])
            #f = ganador.calcular_fitness()
            #print(f"Ganador del torneo: {ganador}")
            #print(f"  ↳ Nutrición: {f['nutricion']:.4f}, Costo: {f['costo']:.4f}, Tiempo: {f['tiempo']:.4f}, Total: {f['total']:.4f}")

            seleccionados.append(ganador)

        return seleccionados

    # TÉCNICA   
    def cruzar(self, seleccionados):
        nueva_poblacion = seleccionados[:SELECCIONAR_MEJORES]
        while len(nueva_poblacion) < TAMANO_POBLACION:
            padre, madre = random.sample(seleccionados, 2)
            if random.random() < PROBABILIDAD_CRUCE:
                hijo = padre.cruzar(madre)
                nueva_poblacion.append(hijo)
            else:
                nueva_poblacion.append(random.choice([padre, madre]))
        return nueva_poblacion

    # TÉCNICA 
    def mutar(self, poblacion):
        for i, receta in enumerate(poblacion):
            prob_mut = PROBABILIDAD_MUTACION * (0.3 if i < SELECCIONAR_MEJORES else 1)
            if random.random() < min(prob_mut, 0.6):
                receta.mutar()
        return poblacion

    def ejecutar(self, generaciones=100):
        self.inicializar_poblacion()
        sin_mejora = 0
        mejor_fitness_global = 0

        try:
            generaciones = int(generaciones)
        except ValueError:
            raise ValueError("El número de generaciones debe ser un entero válido")

        for generacion in range(generaciones):
            poblacion_evaluada = self.evaluar_poblacion()
            mejor_individuo = poblacion_evaluada[0]

            fitness_values = [r.calcular_fitness() for r in poblacion_evaluada]
            
            total_values = [f["total"] for f in fitness_values]
            self.mejores_fitness.append(max(total_values))
            self.promedio_fitness.append(sum(total_values) / len(total_values))
            self.mejores_individuos.append(mejor_individuo)

            # Mostrar información en consola (solo cada 10 generaciones para no saturar)
            #if (generacion + 1) % 10 == 0 or generacion == 0 or generacion == generaciones - 1:
            mejor_fitness = mejor_individuo.calcular_fitness()
            print(f"Generación {generacion + 1}:")
            print(f"Mejor Receta: {mejor_individuo}")
            print(f"  ↳ Nutrición: {mejor_fitness['nutricion']:.4f}")
            print(f"  ↳ Costo:     {mejor_fitness['costo']:.4f}")
            print(f"  ↳ Tiempo:    {mejor_fitness['tiempo']:.4f}")
            print(f"  ↳ Total:     {mejor_fitness['total']:.4f}")
            print("-" * 100)


            self.mejor_receta = mejor_individuo

            seleccionados = self.seleccionar(poblacion_evaluada)
            nueva_poblacion = self.cruzar(seleccionados)
            self.poblacion = self.mutar(nueva_poblacion)

            # Parada temprana si no hay mejora en 20 generaciones
            if self.mejores_fitness[-1] <= mejor_fitness_global + 0.001:
                sin_mejora += 1
            else:
                sin_mejora = 0
                mejor_fitness_global = self.mejores_fitness[-1]
            
            if sin_mejora >= 20:
                print(f"Parada temprana en generación {generacion + 1}")
                break

        self.mejor_receta = max(self.mejores_individuos, key=lambda x: x.calcular_fitness()["total"])

        return self.mejor_receta

    def __repr__(self):
        return f"Receta({self.ingredientes}, {self.pasos})"