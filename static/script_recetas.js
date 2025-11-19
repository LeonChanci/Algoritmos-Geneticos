let recetasCreadas = false;

async function inicializarRecetas() {
    try {
        const response = await fetch('/api/recetas_inicial', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const recetas = await response.json();
        mostrarRecetas(recetas);
        recetasCreadas = true;
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error al generar la población de recetas');
    }
}

function mostrarRecetas(recetas) {
    const tablaBody = document.getElementById('tabla-recetas-body');
    tablaBody.innerHTML = '';

    recetas.forEach((receta, i) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>Receta ${i + 1}</td>
            <td>${receta.ingredientes.join(', ')}</td>
            <td>${receta.pasos.join(', ')}</td>
            <td>${receta.fitness.toFixed(4)}</td>
            <td>${receta.nutricion.toFixed(4)}</td>
            <td>$${receta.valores_reales.costo_total.toLocaleString()}</td>
            <td>${receta.valores_reales.tiempo_total} min</td>
        `;
        tablaBody.appendChild(row);
    });

    document.getElementById('panel-recetas').style.display = 'block';
}

async function ejecutarRecetas() {
    if (!recetasCreadas) {
        alert('⚠️ Primero debe crear la población inicial de recetas usando el botón "🎲 Generar Población Inicial"');
        return;
    }

    const generaciones = document.getElementById('generaciones').value;

    try {
        const response = await fetch('/api/ejecutar_recetas', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ generaciones: parseInt(generaciones) })
        });

        console.log("Status de respuesta:", response.status); // ← DEBUG
        console.log("OK?", response.ok); // ← DEBUG

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Error en la respuesta del servidor');
        }

        const data = await response.json();
        console.log("Datos recibidos:", data); // ← DEBUG IMPORTANTE

        mostrarMejorReceta(data.mejor_receta, data.evolucion_fitness);

    } catch (error) {
        console.error('Error al ejecutar el algoritmo:', error);
        alert(error.message || 'Hubo un problema al ejecutar el algoritmo genético.');
    }
}

function mostrarMejorReceta(receta, evolucionFitness) {
    const card = document.getElementById('mejor-receta-card');
    const panel = document.getElementById('panel-mejor-receta');
    
    panel.style.display = 'block';
    panel.style.opacity = '1';

    // Mostrar valores reales de manera clara
    card.innerHTML = `
        <div class="resultado-card">
            <h3>🏆 Mejor Receta Encontrada</h3>
            <div class="receta-detalles">
                <p><strong>🍴 Ingredientes (${receta.ingredientes.length}):</strong> ${receta.ingredientes.join(', ')}</p>
                <p><strong>👨‍🍳 Pasos (${receta.pasos.length}):</strong> ${receta.pasos.join(' → ')}</p>
                
                <div class="metricas-reales">
                    <h4>📊 Valores Reales Calculados:</h4>
                    <div class="valores-grid">
                        <div class="valor-item">
                            <span class="valor-etiqueta">💪 Proteína:</span>
                            <span class="valor-numero">${receta.valores_reales.proteina}g</span>
                        </div>
                        <div class="valor-item">
                            <span class="valor-etiqueta">🍚 Carbohidratos:</span>
                            <span class="valor-numero">${receta.valores_reales.carbohidratos}g</span>
                        </div>
                        <div class="valor-item">
                            <span class="valor-etiqueta">🥑 Grasas:</span>
                            <span class="valor-numero">${receta.valores_reales.grasas}g</span>
                        </div>
                        <div class="valor-item">
                            <span class="valor-etiqueta">🔥 Calorías:</span>
                            <span class="valor-numero">${receta.valores_reales.calorias_aproximadas}</span>
                        </div>
                        <div class="valor-item">
                            <span class="valor-etiqueta">💰 Costo total:</span>
                            <span class="valor-numero">$${receta.valores_reales.costo_total.toLocaleString()}</span>
                        </div>
                        <div class="valor-item">
                            <span class="valor-etiqueta">⏱️ Tiempo total:</span>
                            <span class="valor-numero">${receta.valores_reales.tiempo_total} minutos</span>
                        </div>
                    </div>
                </div>
                
                <div class="metricas-fitness">
                    <h4>🎯 Puntajes de Fitness:</h4>
                    <span class="metrica">📊 Fitness Total: ${receta.fitness.toFixed(4)}</span>
                    <span class="metrica">💪 Nutrición: ${receta.nutricion.toFixed(4)}</span>
                    <span class="metrica">💰 Costo: ${receta.costo.toFixed(4)}</span>
                    <span class="metrica">⏱️ Tiempo: ${receta.tiempo.toFixed(4)}</span>
                </div>
            </div>
        </div>
    `;
    
    // IMPLEMENTAR GRÁFICA
    setTimeout(() => {
        const ctx = document.getElementById('grafica-recetas').getContext('2d');
        if (window.recetaChart) {
            window.recetaChart.destroy();
        }
        
        window.recetaChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: evolucionFitness.map((_, i) => `Gen ${i+1}`),
                datasets: [{
                    label: 'Evolución del Fitness',
                    data: evolucionFitness,
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    borderWidth: 2,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { 
                        beginAtZero: true, 
                        max: 1.0,
                        title: { display: true, text: 'Fitness' }
                    },
                    x: {
                        title: { display: true, text: 'Generaciones' }
                    }
                }
            }
        });
    }, 100);
}