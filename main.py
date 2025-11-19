from flask import Flask, render_template, request, jsonify
from app import AlgoritmoGenetico
from recetas import AlgoritmoRecetas
import json

app = Flask(__name__)

# Instancias globales para las rutas tradicionales (POST de formularios)
ag_global = AlgoritmoGenetico()  # Algoritmo de Paracaidistas
ar_global = AlgoritmoRecetas()   # Algoritmo de Recetas

ag_estado_actual = None
poblacion_actual = None

ar_estado_actual = None
recetas_actual = None


###########################################################################################
################################### ALGORITMO PARACAIDISTA ################################
###########################################################################################
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'inicializar' in request.form:
            ag_global.inicializar_poblacion()
            poblacion_data = [
                {
                    'numero': i+1,
                    'masa': round(p.masa, 2),
                    'velocidad': round(p.velocidad, 2),
                    'fuerza': round(p.fuerza, 2),
                    'tiempo': round(p.tiempo, 2),
                    'fitness': round(p.calcular_fitness(), 4)
                }
                for i, p in enumerate(ag_global.poblacion)
            ]
            return render_template('index.html', poblacion=poblacion_data)
        
        elif 'ejecutar' in request.form:
            generaciones = int(request.form.get('generaciones', 10))
            ag_global.ejecutar(generaciones)  # ← Usar instancia global
            return render_template('index.html', 
                                 mejor_paracaidista=ag_global.mejor_paracaidista,
                                 fitness_evolucion=ag_global.mejores_fitness)
    
    return render_template('index.html')

@app.route('/api/poblacion_inicial', methods=['POST'])
def api_poblacion_inicial():
    global ag_estado_actual, poblacion_actual
    
    # Crear nueva instancia y guardar el estado
    ag_estado_actual = AlgoritmoGenetico()
    ag_estado_actual.inicializar_poblacion()
    
    poblacion_actual = [
        {
            'numero': i+1,
            'masa': round(p.masa, 2),
            'velocidad': round(p.velocidad, 2),
            'fuerza': round(p.fuerza, 2),
            'tiempo': round(p.tiempo, 2),
            'fitness': round(p.calcular_fitness(), 4)
        }
        for i, p in enumerate(ag_estado_actual.poblacion)
    ]
    return jsonify(poblacion_actual)

@app.route('/api/ejecutar_algoritmo', methods=['POST'])
def api_ejecutar_algoritmo():
    global ag_estado_actual, poblacion_actual

    if ag_estado_actual is None or poblacion_actual is None:
        return jsonify({'error': 'Primero debe crear la población inicial'}), 400
    
    data = request.json
    generaciones_solicitadas = data.get('generaciones', 15)
    fitness_aterrizaje = data.get('fitnessAterrizaje', 0.8)
    print(generaciones_solicitadas)
    print(fitness_aterrizaje)
    ag_api = ag_estado_actual
    
    # NUEVO: Lista para guardar mejores por generación
    mejores_por_generacion = []
    
    buen_aterrizaje_encontrado = False
    generacion_buen_aterrizaje = 0
    generaciones_ejecutadas = 0
    
    for generacion in range(generaciones_solicitadas):
        poblacion_evaluada = ag_api.evaluar_poblacion()
        mejor_individuo = poblacion_evaluada[0]
        fitness_actual = mejor_individuo.calcular_fitness()
        
        # GUARDAR MEJOR DE ESTA GENERACIÓN
        mejores_por_generacion.append({
            'masa': round(mejor_individuo.masa, 2),
            'velocidad': round(mejor_individuo.velocidad, 2),
            'fuerza': round(mejor_individuo.fuerza, 2),
            'tiempo': round(mejor_individuo.tiempo, 2),
            'fitness': round(fitness_actual, 4)
        })
        
        ag_api.mejores_fitness.append(fitness_actual)
        ag_api.mejores_individuos.append(mejor_individuo)
        ag_api.mejor_paracaidista = mejor_individuo
        
        generaciones_ejecutadas = generacion + 1
        
        if fitness_actual <= fitness_aterrizaje:
            buen_aterrizaje_encontrado = True
            generacion_buen_aterrizaje = generacion + 1
            break
        
        seleccionados = ag_api.seleccionar(poblacion_evaluada)
        nueva_poblacion = ag_api.cruzar(seleccionados)
        ag_api.poblacion = ag_api.mutar(nueva_poblacion)
    
    if ag_api.mejores_individuos:
        mejor_global = min(ag_api.mejores_individuos, key=lambda x: x.calcular_fitness())
        mejor_ultima_generacion = ag_api.mejores_individuos[-1]
    else:
        mejor_global = ag_api.poblacion[0] if ag_api.poblacion else None
        mejor_ultima_generacion = mejor_global
    
    resultado = {
        'mejor_paracaidista': {
            'masa': round(mejor_global.masa, 2),
            'velocidad': round(mejor_global.velocidad, 2),
            'fuerza': round(mejor_global.fuerza, 2),
            'tiempo': round(mejor_global.tiempo, 2),
            'fitness': round(mejor_global.calcular_fitness(), 4)
        },
        'mejor_ultima_generacion': {
            'masa': round(mejor_ultima_generacion.masa, 2),
            'velocidad': round(mejor_ultima_generacion.velocidad, 2),
            'fuerza': round(mejor_ultima_generacion.fuerza, 2),
            'tiempo': round(mejor_ultima_generacion.tiempo, 2),
            'fitness': round(mejor_ultima_generacion.calcular_fitness(), 4)
        },
        # NUEVO: Agregar esta línea
        'mejores_por_generacion': mejores_por_generacion,
        
        'total_generaciones_solicitadas': generaciones_solicitadas,
        'total_generaciones_ejecutadas': generaciones_ejecutadas,
        'buen_aterrizaje_encontrado': buen_aterrizaje_encontrado,
        'generacion_buen_aterrizaje': generacion_buen_aterrizaje if buen_aterrizaje_encontrado else 0,
        'evolucion_fitness': ag_api.mejores_fitness
    }
    
    return jsonify(resultado)














###########################################################################################
################################### ALGORITMO RECETAS #####################################
###########################################################################################

@app.route('/recetas', methods=['GET', 'POST'])
def recetas():
    # Agregar soporte para formularios tradicionales (como en index)
    if request.method == 'POST':
        if 'inicializar' in request.form:
            ar_global.inicializar_poblacion()
            recetas_data = []
            for i, r in enumerate(ar_global.poblacion):
                fitness = r.calcular_fitness()
                recetas_data.append({
                    'numero': i + 1,
                    'ingredientes': r.ingredientes,
                    'pasos': r.pasos,
                    'fitness': round(fitness["total"], 4)
                })
            return render_template('recetas.html', recetas=recetas_data)
        
        elif 'ejecutar' in request.form:
            generaciones = int(request.form.get('generaciones', 100))
            ar_global.ejecutar(generaciones)
            return render_template('recetas.html', 
                                 mejor_receta=ar_global.mejor_receta,
                                 evolucion_fitness=ar_global.mejores_fitness)
    
    return render_template('recetas.html')

@app.route('/api/recetas_inicial', methods=['POST'])
def api_recetas_inicial():
    global ar_estado_actual, recetas_actual
    
    ar_estado_actual = AlgoritmoRecetas()
    ar_estado_actual.inicializar_poblacion()
    
    recetas_actual = []
    for i, r in enumerate(ar_estado_actual.poblacion):
        fitness = r.calcular_fitness()
        valores_reales = r.calcular_valores_reales()  # ← NUEVO
        
        recetas_actual.append({
            'numero': i + 1,
            'ingredientes': r.ingredientes,
            'pasos': r.pasos,
            'fitness': round(fitness["total"], 4),
            'nutricion': round(fitness["nutricion"], 4),
            'costo': round(fitness["costo"], 4),
            'tiempo': round(fitness["tiempo"], 4),
            'valores_reales': valores_reales  # ← NUEVO: Incluir valores reales
        })
    return jsonify(recetas_actual)

@app.route('/api/ejecutar_recetas', methods=['POST'])
def api_ejecutar_recetas():
    global ar_estado_actual, recetas_actual
    
    if ar_estado_actual is None or recetas_actual is None:
        return jsonify({'error': 'Primero debe crear la población inicial de recetas'}), 400
    
    data = request.json
    generaciones_solicitadas = data.get('generaciones', 100)
    
    ar_api = ar_estado_actual
    mejor_receta = ar_api.ejecutar(generaciones_solicitadas)
    fitness = mejor_receta.calcular_fitness()
    
    resultado = {
        'mejor_receta': {
            'ingredientes': mejor_receta.ingredientes,
            'pasos': mejor_receta.pasos,
            'fitness': round(fitness["total"], 4),
            'nutricion': round(fitness["nutricion"], 4),
            'costo': round(fitness["costo"], 4),
            'tiempo': round(fitness["tiempo"], 4),
            'valores_reales': fitness["valores_reales"]  # ← NUEVO
        },
        'evolucion_fitness': ar_api.mejores_fitness
    }
    
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True, port=5000)