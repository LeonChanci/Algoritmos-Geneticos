# 🧠 Algoritmos Genéticos: Paracaidista + Recetas Culinarias

## 📄 Ficha Técnica Académica

| Campo | Información |
|-------|-------------|
| **Universidad** | Politénico Colombiano Jaime Isaza Cadavid 🏫 |
| **Facultad** | Facultad de Ingeniería 📚 |
| **Programa Académico** | Ingeniería Informática 🎓 |
| **Asignatura** | Inteligencia Artificial 🤖 |
| **Docente** | Jorge Eliecer Giraldo Plaza 🧑 |
| **Estudiante** | León Ángel Chancí Guzmán 👨‍🎓 |
| **Año** | 2025 |

## 🚀 Descripción
Sistema web dual que implementa algoritmos genéticos para dos problemas diferentes:
- ** 🪂 Algoritmo Genético:** Paracaidista Óptimo: Optimiza parámetros de aterrizaje para encontrar la combinación perfecta
- ** 🍳 Algoritmo Genético:** Recetas Culinarias: Genera recetas balanceadas considerando nutrición, costo y tiempo

## 📦 Instalación

**1. Clonar el repositorio:**
```bash
git clone https://github.com/LeonChanci/Algoritmos-Geneticos
cd Algoritmos-Geneticos

**2. Crear entorno virtual:**
```bash
python -m venv venv
```

**3. Activar entorno virtual:**
```bash
Windows: .\venv\Scripts\activate
Linux/Mac: source venv/bin/activate

**4. Instalar dependencias:**
```bash
pip install -r requirements.txt
```

**5. Ejecutar la aplicación:**
```bash
python app.py
```

**6. Abrir en el navegador:**

**http://localhost:5000**


## 🪂 Algoritmo Genético: Paracaidista Óptimo
**🎯 Funcionalidades**

- Optimización de parámetros de aterrizaje seguro
- Generación de población inicial aleatoria
- Evolución generacional con técnicas élitistas
- Animación visual del proceso de aterrizaje
- Cálculo de fitness basado en distancia a valores ideales

**📊 Parámetros del Sistema**
**Variables de Entrada:**
- ⚖️ Masa del paracaidista (60-100 kg)
- ⚡ Velocidad de aterrizaje (3-8 m/s)
- 💪 Fuerza de apertura (800-1800 N)
- ⏱️ Tiempo de descenso (120-240 s)

**Valores Ideales:**
- Masa ideal: 80 kg
- Velocidad ideal: 5 m/s
- Fuerza ideal: 1000 N
- Tiempo ideal: 160 s

**🧠 Técnicas Genéticas Implementadas**

- **Selección:** Élitista (2 mejores) + Ruleta proporcional
- **Cruce:** Uniforme (50% probabilidad por gen)
- **Mutación:** Combinación fuerte (10%) + suave (90%)
- **Fitness:** Distancia ponderada a valores ideales


## 🍳 Algoritmo Genético: Recetas Culinarias
**🎯 Funcionalidades**

- Generación de recetas con mínimo 3 ingredientes y 3 pasos
- Optimización multi-objetivo: nutrición, costo y tiempo
- Cálculo automático de valores nutricionales reales
- Evaluación de balance proteínas/carbohidratos/grasas
- Sistema de mutación inteligente por dominio

**📊 Parámetros Nutricionales**

**Ingredientes Disponibles (15):**
- 🍗 Proteínas: pollo, huevo, lentejas, queso
- 🍚 Carbohidratos: pasta, arroz, papa, pan
- 🥦 Verduras: tomate, cebolla, pimiento, zanahoria
- 🌿 Condimentos: ajo, albahaca, espinaca, champiñones

**Técnicas Culinarias (10):**
- 🔪 Preparación: cortar, batir, marinar
- 🔥 Cocción: hervir, freír, hornear, saltear, grillar
- 🍽️ Finalización: mezclar, servir

**Valores Ideales:**
- Proteínas: 35-45g
- Carbohidratos: 45-55g
- Grasas: 12-18g
- Costo: ≤ $15,000 COP
- Tiempo: ≤ 60 minutos

**🧠 Técnicas Genéticas Implementadas**

- **Selección:** Torneo (k=3) + Élitismo (2 mejores)
- **Cruce:** Combinación inteligente con orden lógico
- **Mutación:** Nutricional, económica, balanceada y aleatoria
- **Fitness:** Multi-objetivo con penalizaciones por mínimos

## 🛠️ Tecnologías

**Backend**
- **Flask** - Framework web
- **Python** 🐍 - Lenguaje principal
- **NumPy** - Cálculos numéricos

**Frontend**
- **HTML5** - Estructura web
- **CSS3** - Estilos y diseño responsive
- **JavaScript** - Interactividad
- **Chart.js** - Gráficas interactivas

**Algoritmos**
- Algoritmos Genéticos - Optimización evolutiva
- Selección por Torneo - Mantener diversidad
- Cruce Uniforme - Combinación balanceada
- Mutación Adaptativa - Exploración inteligente

## 📁 Estructura del Proyecto

```
Algoritmos-Geneticos/
├── main.py                 # Aplicación principal Flask
├── app.py                  # Algoritmo genético paracaidistas
├── recetas.py              # Algoritmo genético recetas
├── paracaidista.py         # Clase Paracaidista
├── config.py               # Configuración parámetros paracaidista
├── config_recetas.py       # Configuración ingredientes y nutrición
├── requirements.txt        # Dependencias
├── static/
│   ├── styles.css          # Estilos generales
│   ├── styles_paracaidista.css
│   ├── styles_recetas.css
│   └── images/
│       ├── paracaidista_cayendo.png
│       ├── paracaidista_buen_aterrizaje.png
│       └── paracaidista_mal_aterrizaje.png
├── templates/
│   ├── index.html          # Interfaz paracaidistas
│   └── recetas.html        # Interfaz recetas
└── README.md               # Este archivo
```

## 🚀 Uso del Sistema
**1. Algoritmo Paracaidista** 🪂
- Configurar número de generaciones y umbral de fitness
- Generar población inicial de 10 paracaidistas
- Ejecutar evolución con animación en tiempo real
- Analizar resultados y gráficas de convergencia

**2. Algoritmo Recetas** 🍳
- Configurar número de generaciones (25-500)
- Generar población inicial de 20 recetas
- Ejecutar algoritmo de optimización multi-objetivo
- Evaluar receta óptima con valores nutricionales reales

## 👨‍💻 Autor
León Ángel Chancí Guzmán
Estudiante de Ingeniería Informática
Politécnico Colombiano Jaime Isaza Cadavid