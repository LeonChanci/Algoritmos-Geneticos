let poblacionCreada = false;

async function inicializarPoblacion() {
    try {
        // Resetear valores
        valoresGeneracionInicial = {
            masa: null,
            velocidad: null,
            fuerza: null,
            tiempo: null,
            fitness: null
        };

        const response = await fetch('/api/poblacion_inicial', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const poblacion = await response.json();
        mostrarPoblacion(poblacion);
        poblacionCreada = true;
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error al crear la población inicial');
    }
}

function mostrarPoblacion(poblacion) {
    const tablaBody = document.getElementById('tabla-poblacion-body');
    tablaBody.innerHTML = '';
    
    poblacion.forEach(paracaidista => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${paracaidista.numero}</td>
            <td>${paracaidista.masa}</td>
            <td>${paracaidista.velocidad}</td>
            <td>${paracaidista.fuerza}</td>
            <td>${paracaidista.tiempo}</td>
            <td>${paracaidista.fitness}</td>
        `;
        tablaBody.appendChild(row);
    });
    
    document.getElementById('panel-poblacion').style.display = 'block';
}

function mostrarResultados(resultados) {
    const mejorGlobal = resultados.mejor_paracaidista;
    const mejorUltimaGeneracion = resultados.mejor_ultima_generacion;
    
    let mensajeResultado = '';
    
    if (resultados.buen_aterrizaje_encontrado) {
        mensajeResultado = `
            <div class="resultado-exito">
                <h3>🎉 ¡BUEN ATERRIZAJE ENCONTRADO!</h3>
                <p>Se encontró una solución óptima en la <strong>generación ${resultados.generacion_buen_aterrizaje}</strong></p>
                <p>Generaciones ejecutadas: ${resultados.total_generaciones_ejecutadas} de ${resultados.total_generaciones_solicitadas} solicitadas</p>
            </div>
        `;
    } else {
        mensajeResultado = `
            <div class="resultado-info">
                <h3>⚠️ LÍMITE DE GENERACIONES ALCANZADO</h3>
                <p>No se encontró un buen aterrizaje en <strong>${resultados.total_generaciones_solicitadas} generaciones</strong></p>
                <p>Generaciones ejecutadas: ${resultados.total_generaciones_ejecutadas}</p>
                <p>💡 <em>Sugerencia: Intenta con más generaciones</em></p>
            </div>
        `;
    }
    
    // VERIFICAR SI SON EL MISMO PARACAIDISTA
    const sonIguales = 
        mejorGlobal.masa === mejorUltimaGeneracion.masa &&
        mejorGlobal.velocidad === mejorUltimaGeneracion.velocidad &&
        mejorGlobal.fuerza === mejorUltimaGeneracion.fuerza &&
        mejorGlobal.tiempo === mejorUltimaGeneracion.tiempo &&
        mejorGlobal.fitness === mejorUltimaGeneracion.fitness;
    
    let contenidoParacaidistas = '';
    
    if (sonIguales) {
        // MOSTRAR SOLO UNO (evitar duplicación)
        contenidoParacaidistas = `
            <div class="mejor-info">
                <h3>🏆 Paracaidista Óptimo Encontrado</h3>
                <p>⚖️ Masa: ${mejorGlobal.masa} kg</p>
                <p>⚡ Velocidad: ${mejorGlobal.velocidad} m/s</p>
                <p>💪 Fuerza: ${mejorGlobal.fuerza} N</p>
                <p>⏱️ Tiempo: ${mejorGlobal.tiempo} s</p>
                <p>🎯 Fitness: ${mejorGlobal.fitness}</p>
                <p style="color: #666; font-style: italic; margin-top: 10px;">
                    💡 El mejor paracaidista global coincide con el de la última generación
                </p>
            </div>
        `;
    } else {
        // MOSTRAR AMBOS (son diferentes)
        contenidoParacaidistas = `
            <div class="mejor-info">
                <h3>🏆 Mejor Paracaidista Global</h3>
                <p>⚖️ Masa: ${mejorGlobal.masa} kg</p>
                <p>⚡ Velocidad: ${mejorGlobal.velocidad} m/s</p>
                <p>💪 Fuerza: ${mejorGlobal.fuerza} N</p>
                <p>⏱️ Tiempo: ${mejorGlobal.tiempo} s</p>
                <p>🎯 Fitness: ${mejorGlobal.fitness}</p>
            </div>
            
            <div class="mejor-info">
                <h3>🔄 Mejor de la Última Generación</h3>
                <p>⚖️ Masa: ${mejorUltimaGeneracion.masa} kg</p>
                <p>⚡ Velocidad: ${mejorUltimaGeneracion.velocidad} m/s</p>
                <p>💪 Fuerza: ${mejorUltimaGeneracion.fuerza} N</p>
                <p>⏱️ Tiempo: ${mejorUltimaGeneracion.tiempo} s</p>
                <p>🎯 Fitness: ${mejorUltimaGeneracion.fitness}</p>
            </div>
        `;
    }
    
    document.getElementById('mejor-paracaidista').innerHTML = `
        ${mensajeResultado}
        ${contenidoParacaidistas}
    `;
    
    document.getElementById('panel-resultados').style.display = 'block';
}

async function ejecutarAlgoritmoConAnimacion() {
    // Validar que exista población inicial
    if (!poblacionCreada) {
        alert('⚠️ Primero debe crear la población inicial usando el botón "🎲 Crear Población Inicial"');
        return;
    }

    const generacionesSolicitadas = parseInt(document.getElementById('generaciones').value);
    const fitnessAterrizaje = parseFloat(document.getElementById('fitnessAterrizaje').value);

    console.log("Enviando:", { generaciones: generacionesSolicitadas, fitnessAterrizaje: fitnessAterrizaje });

    const animacionContenedor = document.getElementById('animacion-contenedor');
    const paracaidistaImg = document.getElementById('paracaidista-img');
    const resultadoImg = document.getElementById('resultado-img');
    const generacionInfo = document.getElementById('generacion-actual');
    const fitnessInfo = document.getElementById('fitness-actual');
    
    // Mostrar contenedor de animación
    animacionContenedor.style.display = 'block';
    
    try {
        const response = await fetch('/api/ejecutar_algoritmo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ generaciones: generacionesSolicitadas,
                fitnessAterrizaje: fitnessAterrizaje
             })
        });

        const resultados = await response.json();
        
        // Ejecutar animación solo para las generaciones que realmente se ejecutaron
        for (let gen = 0; gen < resultados.total_generaciones_ejecutadas; gen++) {
            const mejorDeGeneracion = await obtenerMejorDeGeneracion(gen, resultados);
            
            await animarGeneracion(gen, resultados.evolucion_fitness[gen], mejorDeGeneracion, 
                                 paracaidistaImg, resultadoImg, generacionInfo, fitnessInfo);
            
            // Pausa entre generaciones (1 segundo) solo si no hemos terminado
            if (gen < resultados.total_generaciones_ejecutadas - 1) {
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
        }
        
        // Mostrar resultado final
        mostrarResultados(resultados);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error al ejecutar el algoritmo');
    }
}

// Función auxiliar para obtener información del mejor individuo por generación
async function obtenerMejorDeGeneracion(generacion, resultados) {
    // Usar la información detallada por generación si está disponible
    if (resultados.mejores_por_generacion && resultados.mejores_por_generacion[generacion]) {
        return resultados.mejores_por_generacion[generacion];
    } else {
        // Fallback: usar el mejor global (esto solo para compatibilidad)
        console.warn('No hay datos por generación, usando mejor global');
        return {
            masa: resultados.mejor_paracaidista.masa,
            velocidad: resultados.mejor_paracaidista.velocidad,
            fuerza: resultados.mejor_paracaidista.fuerza,
            tiempo: resultados.mejor_paracaidista.tiempo,
            fitness: resultados.evolucion_fitness[generacion]
        };
    }
}

// Cambiar la variable global para guardar la GENERACIÓN INICIAL
let valoresGeneracionInicial = {
    masa: null,
    velocidad: null,
    fuerza: null,
    tiempo: null,
    fitness: null
};

let generacionActual = 0;

async function animarGeneracion(generacion, fitness, mejorIndividuo, paracaidistaImg, resultadoImg, generacionInfo, fitnessInfo) {
    const FITNESS_BUEN_ATERRIZAJE = parseFloat(document.getElementById('fitnessAterrizaje').value);

    return new Promise((resolve) => {
        // VELOCIDAD CONSTANTE según fitness
        let velocidadCaida;
        if (fitness <= FITNESS_BUEN_ATERRIZAJE) velocidadCaida = 4.0;
        else if (fitness <= 1.0) velocidadCaida = 6.0;
        else if (fitness <= 2.0) velocidadCaida = 9.0;
        else if (fitness <= 5.0) velocidadCaida = 12.0;
        else velocidadCaida = 16.0;
        
        // GUARDAR VALORES DE LA PRIMERA GENERACIÓN
        if (generacion === 0) {
            valoresGeneracionInicial = {
                masa: mejorIndividuo.masa,
                velocidad: mejorIndividuo.velocidad,
                fuerza: mejorIndividuo.fuerza,
                tiempo: mejorIndividuo.tiempo,
                fitness: fitness
            };
        }
        
        // FUNCIÓN PARA RESALTAR CAMBIOS vs GENERACIÓN INICIAL
        function resaltarCambio(valorActual, valorInicial, unidad = '') {
            if (generacion === 0) {
                return `<span>${valorActual}${unidad}</span>`; // Primera generación
            }
            
            const diferencia = valorActual - valorInicial;
            const cambioPorcentual = ((diferencia / valorInicial) * 100).toFixed(1);
            
            if (Math.abs(diferencia) < 0.01) { // Cambio muy pequeño
                return `<span style="color: gray">${valorActual}${unidad} (=)</span>`;
            } else if (diferencia < 0) {
                return `<span style="color: green">${valorActual}${unidad} (${cambioPorcentual}%) ↓</span>`;
            } else {
                return `<span style="color: red">${valorActual}${unidad} (+${cambioPorcentual}%) ↑</span>`;
            }
        }
        
        // Actualizar información
        generacionInfo.innerHTML = `
            <p><strong>Generación:</strong> ${generacion + 1}</p>
            <p><strong>Masa:</strong> ${resaltarCambio(mejorIndividuo.masa, valoresGeneracionInicial.masa, ' kg')}</p>
            <p><strong>Velocidad:</strong> ${resaltarCambio(mejorIndividuo.velocidad, valoresGeneracionInicial.velocidad, ' m/s')}</p>
            <p><strong>Fuerza:</strong> ${resaltarCambio(mejorIndividuo.fuerza, valoresGeneracionInicial.fuerza, ' N')}</p>
            <p><strong>Tiempo:</strong> ${resaltarCambio(mejorIndividuo.tiempo, valoresGeneracionInicial.tiempo, ' s')}</p>
        `;
        
        fitnessInfo.innerHTML = `
            <p><strong>Fitness:</strong> ${resaltarCambio(fitness, valoresGeneracionInicial.fitness, '')}</p>
            <p><strong>Vel. constante:</strong> ${velocidadCaida} px/frame</p>
        `;
        
        // Resto del código de animación IGUAL...
        paracaidistaImg.style.display = 'block';
        resultadoImg.style.display = 'none';
        paracaidistaImg.style.top = '10px';
        
        let posicion = 10;
        const caidaInterval = setInterval(() => {
            posicion += velocidadCaida;
            paracaidistaImg.style.top = posicion + 'px';
            
            if (posicion >= 285) {
                clearInterval(caidaInterval);
                paracaidistaImg.style.display = 'none';
                resultadoImg.style.display = 'block';
                
                if (fitness <= FITNESS_BUEN_ATERRIZAJE) {
                    resultadoImg.src = IMAGEN_BUEN_ATERRIZAJE;
                    resultadoImg.style.width = "25px";
                    resultadoImg.style.height = "auto";
                    resultadoImg.style.objectFit = "contain";
                    resultadoImg.alt = "Buen aterrizaje";
                } else {
                    resultadoImg.src = IMAGEN_MAL_ATERRIZAJE;
                    resultadoImg.alt = "Mal aterrizaje";
                }
                
                resolve();
            }
        }, 50);
    });
}