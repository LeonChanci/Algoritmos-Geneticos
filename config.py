# Parámetros del algoritmo genético
TAMANO_POBLACION = 10
SELECCIONAR_MEJORES = 2
PROBABILIDAD_CRUCE = 0.8
PROBABILIDAD_MUTACION = 0.6
PORCENTAJE_MUTACION_FUERTE = 0.10  # 10% de mutaciones más agresivas


# Parámetros del paracaidista (límites para valores aleatorios)
MASA_MIN = 60  # kg Peso Min del paracaidista
MASA_MAX = 100  # kg Peso Max del paracaidista

VELOCIDAD_MIN = 3  # m/s Velocidad Min de aterrizaje del paracaidista
VELOCIDAD_MAX = 8 # m/s Velocidad Max de aterrizaje del paracaidista

FUERZA_MIN = 800  # N Fuerza Min del aterizaje del paracaidista
FUERZA_MAX = 1800  # N Fuerza Max del aterizaje del paracaidista

TIEMPO_MIN = 120  # s Tiempo Min de aterrizaje del paracaidista
TIEMPO_MAX = 240  # s Tiempo Max de aterrizaje del paracaidista


# Parámetros Ideales para la función de evaluación
MASA_IDEAL = 80         # kg (peso ideal del paracaidista con equipo)
VELOCIDAD_IDEAL = 5     # m/s (velocidad de aterrizaje segura)
FUERZA_IDEAL = 1000     # N (fuerza ideal de apertura del paracaídas)
TIEMPO_IDEAL = 160      # s (tiempo ideal de caída)


# Parámetros con Peso para la función de evaluación
PESO_MASA = 0.2         # Peso de la masa en la función de evaluación
PESO_VELOCIDAD = 0.5    # Peso de la velocidad en la función de evaluación
PESO_FUERZA = 0.1       # Peso de la fuerza en la función de evaluación
PESO_TIEMPO = 0.2       # Peso del tiempo en la función de evaluación