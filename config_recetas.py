# === GENÉTICO GENERAL ===
TAMANO_POBLACION = 20
SELECCIONAR_MEJORES = 2
PROBABILIDAD_CRUCE = 0.8
PROBABILIDAD_MUTACION = 0.7

# === INFORMACIÓN NUTRICIONAL Y ECONÓMICA ===
INGREDIENTES_INFO = {
    "pollo": {"proteina": 25, "carbo": 0, "grasa": 3, "precio": 12000},         # $12,000/kg (pechuga)
    "tomate": {"proteina": 1, "carbo": 4, "grasa": 0, "precio": 3000},          # $3,000/kg
    "ajo": {"proteina": 1, "carbo": 2, "grasa": 0, "precio": 1500},             # $1,500/100g
    "pasta": {"proteina": 7, "carbo": 30, "grasa": 1, "precio": 4000},          # $4,000/500g
    "queso": {"proteina": 8, "carbo": 1, "grasa": 9, "precio": 8000},           # $8,000/250g (mozzarella)
    "cebolla": {"proteina": 1, "carbo": 9, "grasa": 0, "precio": 2500},         # $2,500/kg
    "arroz": {"proteina": 2.5, "carbo": 28, "grasa": 0.3, "precio": 3000},      # $3,000/libra
    "pimiento": {"proteina": 1, "carbo": 6, "grasa": 0.2, "precio": 3500},      # $3,500/kg
    "zanahoria": {"proteina": 1, "carbo": 10, "grasa": 0.2, "precio": 2000},    # $2,000/kg
    "albahaca": {"proteina": 3, "carbo": 2, "grasa": 0.6, "precio": 2000},      # $2,000/ramo
    "papa": {"proteina": 2, "carbo": 17, "grasa": 0.1, "precio": 2000},         # $2,000/kg
    "lentejas": {"proteina": 9, "carbo": 20, "grasa": 0.4, "precio": 3500},     # $3,500/500g
    "espinaca": {"proteina": 2.9, "carbo": 3.6, "grasa": 0.4, "precio": 3000},  # $3,000/atado
    "huevo": {"proteina": 13, "carbo": 1, "grasa": 11, "precio": 12000},        # $12,000/30 unidades
    "champiñones": {"proteina": 3, "carbo": 3, "grasa": 0.3, "precio": 6000}    # $6,000/200g
}

PASOS_TIEMPO = {
    "hervir": 10,
    "freír": 15,
    "hornear": 30,
    "saltear": 10,
    "mezclar": 5,
    "marinar": 20,
    "cortar": 5,
    "servir": 2,
    "batir": 5,
    "grillar": 20
}


# === BASE CULINARIA ===
# Representa el universo de ingredientes posibles que pueden aparecer en una receta.
INGREDIENTES_BASE = list(INGREDIENTES_INFO.keys())

# Representa el conjunto de técnicas o acciones culinarias que pueden aplicarse.
PASOS_BASE = list(PASOS_TIEMPO.keys())

