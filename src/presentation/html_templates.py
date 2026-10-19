# Plantillas HTML mejoradas para Cartelera y Panel de la UNESR Los Teques

CARTELERA_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UNESR Los Teques - Cartelera Oficial de Aulas y Horarios</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        @media print {
            .no-print { display: none !important; }
            .print-only { display: block !important; }
            body { background: white !important; color: black !important; font-size: 11pt; }
            .print-border { border: 1px solid #1e293b !important; }
            .print-table th, .print-table td { border: 1px solid #64748b !important; padding: 4px 6px !important; }
            @page { size: landscape; margin: 1cm; }
        }
        @media screen {
            .print-only { display: none; }
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen flex flex-col font-sans">
    <!-- Membrete Oficial para Impresión Física en Pasillos -->
    <div class="print-only text-center border-b-2 border-slate-900 pb-4 mb-4">
        <h3 class="text-xs font-semibold uppercase tracking-wider text-slate-700">República Bolivariana de Venezuela • Ministerio del Poder Popular para la Educación Universitaria</h3>
        <h1 class="text-lg font-black uppercase text-slate-900 mt-1">Universidad Nacional Experimental Simón Rodríguez (UNESR)</h1>
        <h2 class="text-sm font-bold text-slate-800">Núcleo Los Teques • Subdirección Académica</h2>
        <div class="inline-block mt-2 px-4 py-1 bg-slate-100 border border-slate-400 rounded text-xs font-bold text-slate-900" id="printTituloFechas">
            CARTELERA OFICIAL DE ASIGNACIÓN DE AULAS Y HORARIOS (07:00 AM - 07:00 PM)
        </div>
    </div>

    <!-- Navbar Institucional (Se oculta al imprimir) -->
    <header class="no-print bg-blue-900 text-white shadow-md border-b-4 border-amber-500">
        <div class="max-w-7xl mx-auto px-4 py-3 flex flex-col sm:flex-row justify-between items-center gap-4">
            <div class="flex items-center space-x-3">
                <div class="w-11 h-11 bg-white text-blue-900 rounded-full flex items-center justify-center font-black text-xl shadow">
                    U
                </div>
                <div>
                    <h1 class="text-lg font-bold tracking-tight">UNESR Los Teques</h1>
                    <p class="text-xs text-amber-200">Cartelera Universitaria Digital • Pregrado y Postgrado</p>
                </div>
            </div>
            <div class="flex items-center space-x-3">
                <button onclick="window.print()" class="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold rounded-lg text-xs transition shadow flex items-center gap-2 border border-slate-700">
                    <i class="fa-solid fa-print"></i> 🖨️ Imprimir para Pasillos
                </button>
                <a href="/login" class="px-4 py-2 bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold rounded-lg text-xs transition shadow flex items-center gap-2">
                    <i class="fa-solid fa-lock"></i> Acceso Administrativo
                </a>
            </div>
        </div>
    </header>

    <!-- Contenido Principal -->
    <main class="max-w-7xl mx-auto px-4 py-6 flex-grow w-full space-y-6">
        <!-- Barra de Control y Filtros (Oculto en print) -->
        <div class="no-print bg-white rounded-xl shadow-xs border border-slate-200 p-5">
            <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
                <div>
                    <h2 class="text-xl font-black text-slate-900 flex items-center gap-2">
                        <i class="fa-solid fa-calendar-days text-blue-900"></i> Programación Académica de Aulas
                    </h2>
                    <p class="text-xs text-slate-500 mt-0.5">Jornada continua 07:00 a 19:00 • Modelo Andragógico UNESR Los Teques</p>
                </div>

                <div class="flex flex-wrap items-center gap-3">
                    <!-- Selector de Modo de Vista -->
                    <div class="bg-slate-100 p-1 rounded-lg border border-slate-300 flex items-center text-xs font-bold">
                        <button id="btnVistaDia" onclick="cambiarModoVista('dia')" class="px-3 py-1.5 rounded-md bg-blue-900 text-white shadow-xs transition">
                            <i class="fa-solid fa-calendar-day"></i> Vista del Día
                        </button>
                        <button id="btnVistaSemana" onclick="cambiarModoVista('semana')" class="px-3 py-1.5 rounded-md text-slate-600 hover:text-slate-900 transition">
                            <i class="fa-solid fa-calendar-week"></i> Matriz Semanal (Lun - Sáb)
                        </button>
                    </div>

                    <div>
                        <input type="date" id="fechaFiltro" class="border border-slate-300 rounded-lg px-3 py-1.5 text-xs focus:ring-2 focus:ring-blue-900 outline-none bg-white font-medium">
                    </div>

                    <div>
                        <select id="aulaFiltro" class="border border-slate-300 rounded-lg px-3 py-1.5 text-xs focus:ring-2 focus:ring-blue-900 outline-none bg-white font-medium">
                            <option value="">Todas las Aulas</option>
                        </select>
                    </div>

                    <button onclick="recargarCartelera()" class="px-3 py-1.5 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-semibold transition flex items-center gap-1.5">
                        <i class="fa-solid fa-rotate"></i> Actualizar
                    </button>
                </div>
            </div>
        </div>

        <!-- 1. VISTA DEL DÍA: GRID DE 12 AULAS DINÁMICAS -->
        <div id="seccionVistaDia" class="space-y-6">
            <div class="flex justify-between items-center no-print">
                <h3 class="text-base font-bold text-slate-800 flex items-center gap-2">
                    <i class="fa-solid fa-door-open text-amber-600"></i> Estado y Clases en las 12 Aulas Físicas
                </h3>
                <span class="text-xs text-slate-500 font-medium">
                    <span id="disponiblesTotal" class="font-bold text-emerald-600">8</span> Disponibles hoy
                </span>
            </div>

            <!-- Grid de Tarjetas de Aulas Dinámicas -->
            <div id="gridAulasDinamicas" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                <!-- Se puebla dinámicamente con las clases asignadas adentro de cada tarjeta -->
            </div>

            <!-- Tabla Detallada del Día -->
            <div class="bg-white rounded-xl shadow-xs border border-slate-200 overflow-hidden mt-6">
                <div class="bg-slate-100 px-5 py-3 border-b border-slate-200 flex justify-between items-center">
                    <h4 class="font-bold text-slate-800 text-sm flex items-center gap-2">
                        <i class="fa-solid fa-list-check text-blue-900"></i> Cronograma Detallado de Clases
                    </h4>
                    <span id="textoFechaDia" class="text-xs font-semibold bg-white px-2.5 py-0.5 rounded border border-slate-300 text-slate-600"></span>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs print-table">
                        <thead>
                            <tr class="bg-slate-50 border-b border-slate-200 text-slate-600 uppercase font-bold">
                                <th class="py-2.5 px-3">Horario</th>
                                <th class="py-2.5 px-3">Aula</th>
                                <th class="py-2.5 px-3">Nivel</th>
                                <th class="py-2.5 px-3">Asignatura (Código)</th>
                                <th class="py-2.5 px-3">Carrera / Programa</th>
                                <th class="py-2.5 px-3">Facilitador</th>
                            </tr>
                        </thead>
                        <tbody id="tablaDiaBody" class="divide-y divide-slate-100">
                            <!-- JS -->
                        </tbody>
                    </table>
                </div>
                <div id="diaVacioMensaje" class="hidden p-8 text-center text-slate-400">
                    <i class="fa-regular fa-calendar-xmark text-3xl mb-2"></i>
                    <p class="font-medium text-xs">No hay asignaciones programadas para los filtros seleccionados.</p>
                </div>
            </div>
        </div>

        <!-- 2. VISTA MATRIZ SEMANAL (LUNES A SÁBADO) -->
        <div id="seccionVistaSemana" class="hidden space-y-4">
            <div class="bg-blue-50 border border-blue-200 rounded-xl p-4 flex justify-between items-center">
                <div>
                    <h3 class="font-bold text-blue-950 text-sm flex items-center gap-2">
                        <i class="fa-solid fa-table text-blue-800"></i> Matriz Semanal de Distribución de Aulas (Lunes a Sábado)
                    </h3>
                    <p class="text-xs text-blue-800/80" id="rangoSemanaTexto">Semana Académica UNESR</p>
                </div>
                <span class="text-[11px] font-semibold bg-white border border-blue-200 text-blue-900 px-3 py-1 rounded-full">
                    6 Días Operativos
                </span>
            </div>

            <!-- Tabla Matriz Semanal -->
            <div class="bg-white rounded-xl shadow-xs border border-slate-200 overflow-x-auto">
                <table class="w-full text-left text-xs border-collapse print-table">
                    <thead>
                        <tr class="bg-slate-100 border-b border-slate-300 text-slate-800 font-bold uppercase" id="headersSemana">
                            <th class="py-3 px-3 border-r border-slate-200 w-32 bg-slate-200">Aula / Espacio</th>
                            <th class="py-3 px-2 border-r border-slate-200 text-center">Lunes</th>
                            <th class="py-3 px-2 border-r border-slate-200 text-center">Martes</th>
                            <th class="py-3 px-2 border-r border-slate-200 text-center">Miércoles</th>
                            <th class="py-3 px-2 border-r border-slate-200 text-center">Jueves</th>
                            <th class="py-3 px-2 border-r border-slate-200 text-center">Viernes</th>
                            <th class="py-3 px-2 text-center bg-amber-50 text-amber-900">Sábado</th>
                        </tr>
                    </thead>
                    <tbody id="cuerpoMatrizSemanal" class="divide-y divide-slate-200">
                        <!-- Generado dinámicamente: Fila por cada aula -->
                    </tbody>
                </table>
            </div>
        </div>
    </main>

    <!-- Footer Institucional -->
    <footer class="no-print bg-slate-900 text-slate-400 text-xs py-5 border-t border-slate-800 mt-auto">
        <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row justify-between items-center gap-2 text-center sm:text-left">
            <div>
                <span class="font-bold text-slate-300">Universidad Nacional Experimental Simón Rodríguez</span> • Núcleo Los Teques
            </div>
            <div class="text-slate-500">
                Modelo Andragógico • 12 Aulas Escalables • Motor Anti-Colisión WAL
            </div>
        </div>
    </footer>

    <script>
        let modoVistaActual = 'dia';
        let aulasGlobales = [];
        const hoy = new Date().toISOString().split('T')[0];
        document.getElementById('fechaFiltro').value = hoy;

        function cambiarModoVista(modo) {
            modoVistaActual = modo;
            const btnDia = document.getElementById('btnVistaDia');
            const btnSem = document.getElementById('btnVistaSemana');
            const secDia = document.getElementById('seccionVistaDia');
            const secSem = document.getElementById('seccionVistaSemana');

            if (modo === 'dia') {
                btnDia.className = "px-3 py-1.5 rounded-md bg-blue-900 text-white shadow-xs transition";
                btnSem.className = "px-3 py-1.5 rounded-md text-slate-600 hover:text-slate-900 transition";
                secDia.classList.remove('hidden');
                secSem.classList.add('hidden');
            } else {
                btnSem.className = "px-3 py-1.5 rounded-md bg-blue-900 text-white shadow-xs transition";
                btnDia.className = "px-3 py-1.5 rounded-md text-slate-600 hover:text-slate-900 transition";
                secDia.classList.add('hidden');
                secSem.classList.remove('hidden');
            }
            recargarCartelera();
        }

        async function cargarAulasCatalogo() {
            try {
                const res = await fetch('/api/v1/aulas');
                aulasGlobales = await res.json();
                const sel = document.getElementById('aulaFiltro');
                sel.innerHTML = '<option value="">Todas las Aulas</option>';
                aulasGlobales.forEach(a => {
                    sel.innerHTML += `<option value="${a.id}">${a.nombre} (${a.pabellon})</option>`;
                });
            } catch (err) {
                console.error("Error cargando aulas:", err);
            }
        }

        async function recargarCartelera() {
            const fecha = document.getElementById('fechaFiltro').value || hoy;
            const aulaId = document.getElementById('aulaFiltro').value;
            document.getElementById('textoFechaDia').textContent = "Fecha: " + fecha;
            document.getElementById('printTituloFechas').textContent = `CARTELERA OFICIAL DE ASIGNACIÓN DE AULAS - FECHA: ${fecha}`;

            if (modoVistaActual === 'dia') {
                await renderizarVistaDia(fecha, aulaId);
            } else {
                await renderizarVistaSemana(fecha, aulaId);
            }
        }

        async function renderizarVistaDia(fecha, aulaId) {
            let url = `/api/v1/cartelera?fecha=${fecha}`;
            if (aulaId) url += `&aula_id=${aulaId}`;

            try {
                const res = await fetch(url);
                const items = await res.json();

                // 1. Renderizar tarjetas de las 12 aulas dinámicas
                const grid = document.getElementById('gridAulasDinamicas');
                grid.innerHTML = '';
                let disponibles = 0;

                aulasGlobales.forEach(aula => {
                    if (aula.estado === 'DISPONIBLE') disponibles++;

                    // Filtrar clases de esta aula para hoy
                    const clasesAula = items.filter(it => it.aula_id === aula.id);

                    let badgeClass = 'bg-emerald-50 text-emerald-800 border-emerald-300';
                    let dot = 'bg-emerald-500';
                    let estadoLabel = 'Disponible';

                    if (aula.estado === 'EN_REMODELACION') {
                        badgeClass = 'bg-amber-50 text-amber-800 border-amber-300';
                        dot = 'bg-amber-500';
                        estadoLabel = 'En Remodelación';
                    } else if (aula.estado === 'INHABILITADA') {
                        badgeClass = 'bg-rose-50 text-rose-800 border-rose-300';
                        dot = 'bg-rose-500';
                        estadoLabel = 'Inhabilitada';
                    }

                    // Contenido interno con las clases programadas
                    let clasesHtml = '';
                    if (aula.estado === 'DISPONIBLE') {
                        if (clasesAula.length > 0) {
                            clasesHtml = `
                                <div class="mt-2.5 pt-2 border-t border-slate-200 space-y-1.5">
                                    <span class="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Clases asignadas hoy:</span>
                                    ${clasesAula.map(c => `
                                        <div class="p-1.5 bg-slate-50 border border-slate-200 rounded text-[11px] leading-tight">
                                            <div class="flex items-center justify-between text-blue-900 font-bold mb-0.5">
                                                <span><i class="fa-solid fa-clock text-[9px]"></i> ${c.hora_inicio} - ${c.hora_fin}</span>
                                                <span class="text-[9px] px-1 py-0.2 rounded font-semibold ${c.nivel === 'PREGRADO' ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'}">${c.nivel}</span>
                                            </div>
                                            <div class="font-bold text-slate-900 truncate" title="${c.materia_nombre}">
                                                [${c.materia_codigo}] ${c.materia_nombre}
                                            </div>
                                            <div class="text-[10px] text-slate-600 truncate mt-0.5">
                                                <i class="fa-solid fa-chalkboard-user text-[9px]"></i> ${c.docente_nombre}
                                            </div>
                                        </div>
                                    `).join('')}
                                </div>
                            `;
                        } else {
                            clasesHtml = `
                                <div class="mt-3 pt-2 border-t border-slate-100 text-center">
                                    <span class="text-[11px] text-emerald-700 font-medium bg-emerald-50 px-2 py-1 rounded inline-flex items-center gap-1">
                                        <i class="fa-solid fa-circle-check text-[10px]"></i> Totalmente Libre
                                    </span>
                                </div>
                            `;
                        }
                    } else {
                        clasesHtml = `
                            <div class="mt-3 pt-2 border-t border-slate-100 text-center">
                                <span class="text-[11px] font-medium text-slate-500 italic">No disponible para asignación</span>
                            </div>
                        `;
                    }

                    grid.innerHTML += `
                        <div class="bg-white border rounded-xl p-3.5 shadow-xs transition hover:shadow-sm ${badgeClass}">
                            <div class="flex justify-between items-start">
                                <div>
                                    <h4 class="font-black text-slate-900 text-sm">${aula.nombre}</h4>
                                    <p class="text-[11px] text-slate-500">${aula.pabellon} • ${aula.capacidad} puestos</p>
                                </div>
                                <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold ${badgeClass}">
                                    <span class="w-2 h-2 rounded-full ${dot}"></span> ${estadoLabel}
                                </span>
                            </div>
                            ${clasesHtml}
                        </div>
                    `;
                });

                document.getElementById('disponiblesTotal').textContent = disponibles;

                // 2. Renderizar tabla detallada
                const tbody = document.getElementById('tablaDiaBody');
                const emptyMsg = document.getElementById('diaVacioMensaje');
                tbody.innerHTML = '';

                if (items.length === 0) {
                    emptyMsg.classList.remove('hidden');
                } else {
                    emptyMsg.classList.add('hidden');
                    items.forEach(it => {
                        const nivelBadge = it.nivel === 'PREGRADO' 
                            ? '<span class="bg-blue-100 text-blue-800 px-2 py-0.5 rounded text-[10px] font-bold">PREGRADO</span>'
                            : '<span class="bg-purple-100 text-purple-800 px-2 py-0.5 rounded text-[10px] font-bold">POSTGRADO</span>';

                        tbody.innerHTML += `
                            <tr class="hover:bg-slate-50 transition">
                                <td class="py-2.5 px-3 font-bold text-blue-900 whitespace-nowrap">
                                    ${it.hora_inicio} - ${it.hora_fin}
                                </td>
                                <td class="py-2.5 px-3 font-bold text-slate-900">
                                    ${it.aula_nombre} <span class="text-[10px] font-normal text-slate-500">(${it.pabellon})</span>
                                </td>
                                <td class="py-2.5 px-3 whitespace-nowrap">${nivelBadge}</td>
                                <td class="py-2.5 px-3 font-semibold text-slate-900">
                                    <span class="text-blue-900 font-bold">[${it.materia_codigo}]</span> ${it.materia_nombre}
                                </td>
                                <td class="py-2.5 px-3 text-slate-600">${it.carrera_nombre}</td>
                                <td class="py-2.5 px-3 font-medium text-slate-800 whitespace-nowrap">
                                    <i class="fa-solid fa-user-tie text-slate-400"></i> ${it.docente_nombre}
                                </td>
                            </tr>
                        `;
                    });
                }
            } catch (err) {
                console.error("Error en vista día:", err);
            }
        }

        async function renderizarVistaSemana(fechaBase, aulaId) {
            let url = `/api/v1/cartelera/semanal?fecha_inicio=${fechaBase}`;
            if (aulaId) url += `&aula_id=${aulaId}`;

            try {
                const res = await fetch(url);
                const items = await res.json();

                // Calcular las 6 fechas de Lunes a Sábado
                const baseDate = new Date(fechaBase + "T00:00:00");
                const dayOfWeek = baseDate.getDay(); // 0 domingo, 1 lunes...
                const distToMon = (dayOfWeek === 0) ? -6 : 1 - dayOfWeek;
                const lunes = new Date(baseDate);
                lunes.setDate(baseDate.getDate() + distToMon);

                const diasSemana = [];
                const nombresDias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];
                for (let i = 0; i < 6; i++) {
                    const d = new Date(lunes);
                    d.setDate(lunes.getDate() + i);
                    const iso = d.toISOString().split('T')[0];
                    diasSemana.push({nombre: nombresDias[i], fechaIso: iso, diaMes: `${d.getDate()}/${d.getMonth()+1}`});
                }

                document.getElementById('rangoSemanaTexto').textContent = 
                    `Semana del ${diasSemana[0].nombre} ${diasSemana[0].diaMes} al ${diasSemana[5].nombre} ${diasSemana[5].diaMes}`;
                document.getElementById('printTituloFechas').textContent = 
                    `CARTELERA OFICIAL DE AULAS - MATRIZ SEMANAL (${diasSemana[0].diaMes} AL ${diasSemana[5].diaMes})`;

                // Render headers
                const theadTr = document.getElementById('headersSemana');
                theadTr.innerHTML = `<th class="py-2.5 px-3 border-r border-slate-300 w-36 bg-slate-200">Aula / Espacio</th>` +
                    diasSemana.map(d => `<th class="py-2 px-2 border-r border-slate-300 text-center text-xs font-bold ${d.nombre === 'Sábado' ? 'bg-amber-100 text-amber-900' : ''}">${d.nombre}<br><span class="text-[10px] font-normal text-slate-500">${d.diaMes}</span></th>`).join('');

                // Render rows por cada aula
                const tbody = document.getElementById('cuerpoMatrizSemanal');
                tbody.innerHTML = '';

                const aulasFiltradas = aulaId ? aulasGlobales.filter(a => a.id == aulaId) : aulasGlobales;

                aulasFiltradas.forEach(aula => {
                    let celdasHtml = '';

                    diasSemana.forEach(d => {
                        const clasesCelda = items.filter(it => it.aula_id === aula.id && it.fecha === d.fechaIso);
                        
                        let celdaContenido = '';
                        if (aula.estado !== 'DISPONIBLE') {
                            celdaContenido = `<div class="p-1 text-center text-[10px] font-bold text-slate-400 italic">${aula.estado.replace('_', ' ')}</div>`;
                        } else if (clasesCelda.length === 0) {
                            celdaContenido = `<div class="p-1 text-center text-[10px] text-slate-300">-</div>`;
                        } else {
                            celdaContenido = clasesCelda.map(c => `
                                <div class="p-1 mb-1 rounded bg-blue-50 border border-blue-200 text-[10px] leading-tight">
                                    <span class="font-black text-blue-900 block">${c.hora_inicio}-${c.hora_fin}</span>
                                    <span class="font-bold text-slate-800 truncate block">[${c.materia_codigo}] ${c.materia_nombre}</span>
                                    <span class="text-[9px] text-slate-600 truncate block"><i class="fa-solid fa-chalkboard-user"></i> ${c.docente_nombre}</span>
                                </div>
                            `).join('');
                        }

                        celdasHtml += `<td class="py-2 px-1.5 border-r border-slate-200 align-top ${d.nombre === 'Sábado' ? 'bg-amber-50/40' : ''}">${celdaContenido}</td>`;
                    });

                    tbody.innerHTML += `
                        <tr class="hover:bg-slate-50 transition border-b border-slate-200">
                            <td class="py-2.5 px-3 border-r border-slate-300 font-bold text-slate-900 bg-slate-50">
                                <div>${aula.nombre}</div>
                                <div class="text-[10px] font-normal text-slate-500">${aula.pabellon}</div>
                            </td>
                            ${celdasHtml}
                        </tr>
                    `;
                });

            } catch (err) {
                console.error("Error en vista semana:", err);
            }
        }

        document.getElementById('fechaFiltro').addEventListener('change', recargarCartelera);
        document.getElementById('aulaFiltro').addEventListener('change', recargarCartelera);

        cargarAulasCatalogo().then(() => recargarCartelera());
    </script>
</body>
</html>
"""

LOGIN_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UNESR Los Teques - Acceso al Sistema</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-slate-100 text-slate-800 min-h-screen flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
        <!-- Encabezado con colores UNESR -->
        <div class="bg-gradient-to-r from-blue-900 to-indigo-900 p-8 text-center text-white relative">
            <div class="w-16 h-16 bg-white text-blue-900 rounded-full flex items-center justify-center font-black text-2xl mx-auto shadow-md mb-3">
                U
            </div>
            <h2 class="text-2xl font-bold tracking-tight">Acceso Institucional</h2>
            <p class="text-amber-300 text-xs mt-1">Gestión y Reserva de Aulas • UNESR Los Teques</p>
        </div>

        <!-- Formulario -->
        <div class="p-8">
            <form id="loginForm" onsubmit="handleLogin(event)" class="space-y-5">
                <div>
                    <label class="block text-xs font-bold text-slate-700 uppercase mb-1">Usuario</label>
                    <div class="relative">
                        <i class="fa-solid fa-user absolute left-3 top-3.5 text-slate-400 text-sm"></i>
                        <input type="text" id="username" required placeholder="ej. admin o pperez" class="w-full pl-10 pr-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-900 outline-none">
                    </div>
                </div>

                <div>
                    <label class="block text-xs font-bold text-slate-700 uppercase mb-1">Contraseña</label>
                    <div class="relative">
                        <i class="fa-solid fa-lock absolute left-3 top-3.5 text-slate-400 text-sm"></i>
                        <input type="password" id="password" required placeholder="••••••••" class="w-full pl-10 pr-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-900 outline-none">
                    </div>
                </div>

                <div id="loginError" class="hidden p-3 bg-rose-50 border border-rose-200 text-rose-700 text-xs rounded-lg flex items-center gap-2">
                    <i class="fa-solid fa-circle-exclamation"></i>
                    <span id="loginErrorText">Credenciales inválidas.</span>
                </div>

                <button type="submit" class="w-full py-3 bg-blue-900 hover:bg-blue-800 text-white font-bold rounded-lg text-sm transition shadow-md flex justify-center items-center gap-2">
                    <i class="fa-solid fa-right-to-bracket"></i> Iniciar Sesión
                </button>
            </form>

            <!-- Acceso Rápido para Demostración -->
            <div class="mt-8 pt-6 border-t border-slate-100">
                <p class="text-xs font-semibold text-slate-400 uppercase text-center mb-3">Accesos Rápidos de Prueba (RBAC)</p>
                <div class="grid grid-cols-3 gap-2">
                    <button onclick="fillDemo('admin', 'unesr2026')" class="px-2 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs rounded font-medium border border-slate-200 text-center">
                        Directivo
                    </button>
                    <button onclick="fillDemo('pperez', 'docente123')" class="px-2 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs rounded font-medium border border-slate-200 text-center">
                        Profesor
                    </button>
                    <button onclick="fillDemo('estudiante', 'consulta123')" class="px-2 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs rounded font-medium border border-slate-200 text-center">
                        Estudiante
                    </button>
                </div>
            </div>

            <div class="text-center mt-6">
                <a href="/" class="text-xs text-blue-900 hover:underline font-semibold flex items-center justify-center gap-1">
                    <i class="fa-solid fa-arrow-left"></i> Volver a la Cartelera Pública
                </a>
            </div>
        </div>
    </div>

    <script>
        function fillDemo(u, p) {
            document.getElementById('username').value = u;
            document.getElementById('password').value = p;
        }

        async function handleLogin(e) {
            e.preventDefault();
            const u = document.getElementById('username').value;
            const p = document.getElementById('password').value;
            const errorDiv = document.getElementById('loginError');
            errorDiv.classList.add('hidden');

            try {
                const res = await fetch('/api/v1/auth/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username: u, password: p})
                });

                if (!res.ok) {
                    const err = await res.json();
                    throw new Error(err.detail || 'Error de autenticación');
                }

                const data = await res.json();
                localStorage.setItem('unesr_token', data.access_token);
                localStorage.setItem('unesr_user', JSON.stringify(data));

                if (data.rol === 'ESTUDIANTE') {
                    window.location.href = '/';
                } else {
                    window.location.href = '/panel';
                }
            } catch (err) {
                errorDiv.classList.remove('hidden');
                document.getElementById('loginErrorText').textContent = err.message;
            }
        }
    </script>
</body>
</html>
"""

PANEL_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UNESR Los Teques - Panel de Gestión y Asignación de Aulas</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen flex flex-col font-sans">
    <!-- Navbar del Panel -->
    <header class="bg-blue-900 text-white shadow-md border-b-4 border-amber-500">
        <div class="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <span class="w-10 h-10 bg-white text-blue-900 rounded-full flex items-center justify-center font-bold text-lg">U</span>
                <div>
                    <h1 class="text-base font-bold">Panel de Coordinación y Reserva</h1>
                    <p class="text-xs text-amber-200">UNESR Núcleo Los Teques</p>
                </div>
            </div>
            <div class="flex items-center space-x-4">
                <div class="text-right hidden sm:block">
                    <span id="userBadge" class="text-[10px] font-bold bg-amber-500 text-slate-900 px-2 py-0.5 rounded-full"></span>
                    <p id="userNameDisplay" class="text-xs text-slate-300 font-medium"></p>
                </div>
                <a href="/" class="text-xs bg-blue-950 hover:bg-slate-900 px-3 py-1.5 rounded-lg text-slate-200 transition">
                    <i class="fa-solid fa-eye"></i> Cartelera
                </a>
                <button onclick="logout()" class="text-xs bg-rose-600 hover:bg-rose-700 px-3 py-1.5 rounded-lg text-white font-semibold transition">
                    <i class="fa-solid fa-arrow-right-from-bracket"></i> Salir
                </button>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-6 flex-grow w-full space-y-6">
        <!-- Alertas de Conflicto / Éxito -->
        <div id="statusAlert" class="hidden p-4 rounded-xl text-sm font-semibold flex items-center gap-3 shadow-xs transition">
            <i id="statusIcon" class="fa-solid text-xl"></i>
            <span id="statusMessage"></span>
        </div>

        <!-- SECCIÓN 1: RECURSOS FÍSICOS (AULAS Y CAMBIO DE ESTADO) -->
        <div class="bg-white rounded-xl shadow-xs border border-slate-200 p-5">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4">
                <div>
                    <h2 class="text-lg font-bold text-slate-900 flex items-center gap-2">
                        <i class="fa-solid fa-building text-blue-900"></i> Estado de los Recursos Físicos (Aulas)
                    </h2>
                    <p class="text-xs text-slate-500">Supervisa las 12 aulas o añade nuevas salas. Modifica el estado operativo ante remodelaciones.</p>
                </div>
                <button id="btnNuevaAula" onclick="abrirModalAula()" class="hidden px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold shadow-xs transition flex items-center gap-1.5">
                    <i class="fa-solid fa-plus"></i> Añadir Aula (Escalar)
                </button>
            </div>

            <div id="panelAulasGrid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
                <!-- Se puebla con JS -->
            </div>
        </div>

        <!-- SECCIÓN 2: FORMULARIO EN CASCADA Y LISTA DE RESERVAS -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <!-- Formulario de Reserva con Menús Desplegables en Cascada -->
            <div class="bg-white rounded-xl shadow-xs border border-slate-200 p-5 lg:col-span-5">
                <div class="flex justify-between items-center mb-3">
                    <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
                        <i class="fa-solid fa-calendar-plus text-amber-600"></i> Asignar Clase a un Aula
                    </h3>
                    <span class="text-[10px] font-bold bg-blue-100 text-blue-900 px-2 py-0.5 rounded">Motor Anti-Colisión</span>
                </div>
                <p class="text-xs text-slate-500 mb-4">Selecciona en cascada el nivel, carrera, materia con código, facilitador y horario.</p>

                <form id="reservaForm" onsubmit="crearReserva(event)" class="space-y-3.5">
                    <div class="grid grid-cols-2 gap-3">
                        <div>
                            <label class="block text-[11px] font-bold text-slate-700 uppercase mb-1">Fecha</label>
                            <input type="date" id="resFecha" required class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs focus:ring-2 focus:ring-blue-900 outline-none">
                        </div>
                        <div>
                            <label class="block text-[11px] font-bold text-slate-700 uppercase mb-1">Aula Asignada</label>
                            <select id="resAula" required class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs focus:ring-2 focus:ring-blue-900 outline-none bg-white">
                                <!-- Aulas disponibles -->
                            </select>
                        </div>
                    </div>

                    <!-- 1. Filtro en Cascada: Nivel Académico -->
                    <div>
                        <label class="block text-[11px] font-bold text-slate-700 uppercase mb-1">1. Nivel Académico</label>
                        <select id="resNivel" onchange="onNivelCambiado()" class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs focus:ring-2 focus:ring-blue-900 outline-none bg-white font-semibold text-blue-900">
                            <option value="">-- Todos los Niveles --</option>
                            <option value="PREGRADO">PREGRADO (Licenciaturas y PNF)</option>
                            <option value="POSTGRADO">POSTGRADO (Maestrías y Especializaciones)</option>
                            <option value="DOCTORADO">DOCTORADO</option>
                        </select>
                    </div>

                    <!-- 2. Filtro en Cascada: Carrera o Programa -->
                    <div>
                        <label class="block text-[11px] font-bold text-slate-700 uppercase mb-1">2. Carrera / Programa</label>
                        <select id="resCarrera" onchange="onCarreraCambiada()" required class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs focus:ring-2 focus:ring-blue-900 outline-none bg-white">
                            <!-- Carreras filtradas -->
                        </select>
                    </div>

                    <!-- 3. Filtro en Cascada: Materia con Código + Botón Añadir -->
                    <div>
                        <div class="flex justify-between items-center mb-1">
                            <label class="text-[11px] font-bold text-slate-700 uppercase">3. Asignatura (con Código)</label>
                            <button type="button" onclick="abrirModalMateria()" class="text-[10px] text-blue-800 hover:underline font-bold flex items-center gap-1">
                                <i class="fa-solid fa-circle-plus"></i> + Nueva Materia
                            </button>
                        </div>
                        <select id="resMateria" required class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs focus:ring-2 focus:ring-blue-900 outline-none bg-white">
                            <!-- Materias de la carrera -->
                        </select>
                    </div>

                    <!-- 4. Facilitador / Docente + Botón Añadir -->
                    <div>
                        <div class="flex justify-between items-center mb-1">
                            <label class="text-[11px] font-bold text-slate-700 uppercase">4. Facilitador (Profesor)</label>
                            <button type="button" onclick="abrirModalDocente()" class="text-[10px] text-blue-800 hover:underline font-bold flex items-center gap-1">
                                <i class="fa-solid fa-circle-plus"></i> + Nuevo Profesor
                            </button>
                        </div>
                        <select id="resDocente" required class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs focus:ring-2 focus:ring-blue-900 outline-none bg-white">
                            <!-- Docentes -->
                        </select>
                    </div>

                    <!-- 5. Rango Horario (07:00 a 19:00) -->
                    <div class="grid grid-cols-2 gap-3">
                        <div>
                            <label class="block text-[11px] font-bold text-slate-700 uppercase mb-1">Hora Inicio</label>
                            <input type="time" id="resHoraInicio" min="07:00" max="19:00" step="1800" required value="07:00" class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs focus:ring-2 focus:ring-blue-900 outline-none">
                        </div>
                        <div>
                            <label class="block text-[11px] font-bold text-slate-700 uppercase mb-1">Hora Fin</label>
                            <input type="time" id="resHoraFin" min="07:00" max="19:00" step="1800" required value="09:00" class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs focus:ring-2 focus:ring-blue-900 outline-none">
                        </div>
                    </div>

                    <div>
                        <label class="block text-[11px] font-bold text-slate-700 uppercase mb-1">Observaciones</label>
                        <input type="text" id="resObservaciones" placeholder="Cohorte, sección o modalidad" class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs focus:ring-2 focus:ring-blue-900 outline-none">
                    </div>

                    <button type="submit" class="w-full py-2.5 bg-blue-900 hover:bg-blue-800 text-white font-bold rounded-lg text-xs transition shadow flex justify-center items-center gap-2">
                        <i class="fa-solid fa-shield-halved"></i> Validar y Confirmar Asignación
                    </button>
                </form>
            </div>

            <!-- Tabla de Reservas y Cancelación -->
            <div class="bg-white rounded-xl shadow-xs border border-slate-200 p-5 lg:col-span-7">
                <div class="flex justify-between items-center mb-4">
                    <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
                        <i class="fa-solid fa-list-check text-blue-900"></i> Asignaciones Registradas
                    </h3>
                    <input type="date" id="filtroFechaLista" class="border border-slate-300 rounded-lg px-2.5 py-1 text-xs focus:ring-2 focus:ring-blue-900 outline-none">
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs">
                        <thead>
                            <tr class="bg-slate-50 border-b border-slate-200 text-slate-600 uppercase font-bold">
                                <th class="py-2 px-2.5">Horario</th>
                                <th class="py-2 px-2.5">Aula</th>
                                <th class="py-2 px-2.5">Asignatura</th>
                                <th class="py-2 px-2.5">Facilitador</th>
                                <th class="py-2 px-2.5 text-right">Acción</th>
                            </tr>
                        </thead>
                        <tbody id="listaReservasBody" class="divide-y divide-slate-100">
                            <!-- JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </main>

    <!-- Modal 1: Agregar Nueva Aula -->
    <div id="modalAula" class="hidden fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-sm w-full p-5 shadow-2xl border border-slate-200">
            <h3 class="font-bold text-slate-900 text-base mb-3 flex items-center gap-2">
                <i class="fa-solid fa-door-open text-emerald-600"></i> Registrar Nueva Aula (Escalabilidad)
            </h3>
            <form onsubmit="guardarNuevaAula(event)" class="space-y-3">
                <div>
                    <label class="block text-[11px] font-bold text-slate-700 uppercase mb-1">Nombre</label>
                    <input type="text" id="nuevaAulaNombre" required placeholder="ej. Aula 13" class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs outline-none">
                </div>
                <div>
                    <label class="block text-[11px] font-bold text-slate-700 uppercase mb-1">Capacidad</label>
                    <input type="number" id="nuevaAulaCapacidad" required min="10" max="200" value="35" class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs outline-none">
                </div>
                <div>
                    <label class="block text-[11px] font-bold text-slate-700 uppercase mb-1">Pabellón / Edificio</label>
                    <input type="text" id="nuevaAulaPabellon" required value="Pabellón C" class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs outline-none">
                </div>
                <div class="flex justify-end gap-2 pt-2">
                    <button type="button" onclick="cerrarModalAula()" class="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 rounded-lg text-xs font-semibold">Cancelar</button>
                    <button type="submit" class="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-semibold">Guardar Aula</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Modal 2: Registrar Nuevo Profesor Rápido -->
    <div id="modalDocente" class="hidden fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-sm w-full p-5 shadow-2xl border border-slate-200">
            <h3 class="font-bold text-slate-900 text-base mb-3 flex items-center gap-2">
                <i class="fa-solid fa-user-plus text-blue-900"></i> Registrar Nuevo Facilitador
            </h3>
            <form onsubmit="guardarNuevoDocente(event)" class="space-y-3">
                <div>
                    <label class="block text-[11px] font-bold text-slate-700 uppercase mb-1">Cédula</label>
                    <input type="text" id="nuevoDocCedula" required placeholder="V-12345678" class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs outline-none">
                </div>
                <div>
                    <label class="block text-[11px] font-bold text-slate-700 uppercase mb-1">Nombres</label>
                    <input type="text" id="nuevoDocNombres" required placeholder="Nombre" class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs outline-none">
                </div>
                <div>
                    <label class="block text-[11px] font-bold text-slate-700 uppercase mb-1">Apellidos</label>
                    <input type="text" id="nuevoDocApellidos" required placeholder="Apellido" class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs outline-none">
                </div>
                <div>
                    <label class="block text-[11px] font-bold text-slate-700 uppercase mb-1">Correo Electrónico</label>
                    <input type="email" id="nuevoDocEmail" required placeholder="docente@unesr.edu.ve" class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs outline-none">
                </div>
                <div class="flex justify-end gap-2 pt-2">
                    <button type="button" onclick="cerrarModalDocente()" class="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 rounded-lg text-xs font-semibold">Cancelar</button>
                    <button type="submit" class="px-3 py-1.5 bg-blue-900 hover:bg-blue-800 text-white rounded-lg text-xs font-semibold">Registrar</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Modal 3: Registrar Nueva Materia Rápida -->
    <div id="modalMateria" class="hidden fixed inset-0 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-sm w-full p-5 shadow-2xl border border-slate-200">
            <h3 class="font-bold text-slate-900 text-base mb-3 flex items-center gap-2">
                <i class="fa-solid fa-book-medical text-amber-600"></i> Registrar Asignatura / Taller
            </h3>
            <form onsubmit="guardarNuevaMateria(event)" class="space-y-3">
                <div>
                    <label class="block text-[11px] font-bold text-slate-700 uppercase mb-1">Carrera / Programa</label>
                    <select id="modalMatCarrera" required class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs outline-none bg-white">
                        <!-- Se llena con carreras -->
                    </select>
                </div>
                <div>
                    <label class="block text-[11px] font-bold text-slate-700 uppercase mb-1">Código de Asignatura</label>
                    <input type="text" id="modalMatCodigo" required placeholder="ej. INF-301" class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs outline-none">
                </div>
                <div>
                    <label class="block text-[11px] font-bold text-slate-700 uppercase mb-1">Nombre de la Asignatura</label>
                    <input type="text" id="modalMatNombre" required placeholder="Nombre de la materia" class="w-full border border-slate-300 rounded-lg px-2.5 py-1.5 text-xs outline-none">
                </div>
                <div class="flex justify-end gap-2 pt-2">
                    <button type="button" onclick="cerrarModalMateria()" class="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 rounded-lg text-xs font-semibold">Cancelar</button>
                    <button type="submit" class="px-3 py-1.5 bg-amber-600 hover:bg-amber-700 text-white rounded-lg text-xs font-semibold">Guardar Asignatura</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        const token = localStorage.getItem('unesr_token');
        const userStr = localStorage.getItem('unesr_user');
        if (!token || !userStr) {
            window.location.href = '/login';
        }
        const currentUser = JSON.parse(userStr);

        document.getElementById('userNameDisplay').textContent = currentUser.username;
        document.getElementById('userBadge').textContent = currentUser.rol;
        if (currentUser.rol === 'DIRECTIVO' || currentUser.rol === 'COORDINADOR') {
            document.getElementById('btnNuevaAula').classList.remove('hidden');
        }

        const hoy = new Date().toISOString().split('T')[0];
        document.getElementById('resFecha').value = hoy;
        document.getElementById('filtroFechaLista').value = hoy;

        let catalogoGlobal = { carreras: [], materias: [], docentes: [] };

        function logout() {
            localStorage.clear();
            window.location.href = '/login';
        }

        function showAlert(msg, isError) {
            const alertBox = document.getElementById('statusAlert');
            const alertIcon = document.getElementById('statusIcon');
            const alertMsg = document.getElementById('statusMessage');

            alertBox.classList.remove('hidden', 'bg-emerald-50', 'text-emerald-800', 'border-emerald-200', 'bg-rose-50', 'text-rose-800', 'border-rose-200');
            alertIcon.classList.remove('fa-circle-check', 'fa-triangle-exclamation');

            if (isError) {
                alertBox.classList.add('bg-rose-50', 'text-rose-800', 'border', 'border-rose-200');
                alertIcon.classList.add('fa-triangle-exclamation');
            } else {
                alertBox.classList.add('bg-emerald-50', 'text-emerald-800', 'border', 'border-emerald-200');
                alertIcon.classList.add('fa-circle-check');
            }
            alertMsg.textContent = msg;
            alertBox.scrollIntoView({behavior: 'smooth'});
        }

        async function cargarAulasPanel() {
            const res = await fetch('/api/v1/aulas');
            const aulas = await res.json();
            const grid = document.getElementById('panelAulasGrid');
            const selectRes = document.getElementById('resAula');
            grid.innerHTML = '';
            selectRes.innerHTML = '';

            aulas.forEach(a => {
                let badgeClass = 'bg-emerald-100 text-emerald-800 border-emerald-300';
                if (a.estado === 'EN_REMODELACION') badgeClass = 'bg-amber-100 text-amber-800 border-amber-300';
                if (a.estado === 'INHABILITADA') badgeClass = 'bg-rose-100 text-rose-800 border-rose-300';

                const canEdit = (currentUser.rol === 'DIRECTIVO' || currentUser.rol === 'COORDINADOR');
                const actionHtml = canEdit ? `
                    <select onchange="cambiarEstadoAula(${a.id}, this.value)" class="text-[10px] border border-slate-300 rounded px-1.5 py-0.5 bg-white outline-none">
                        <option value="DISPONIBLE" ${a.estado === 'DISPONIBLE' ? 'selected' : ''}>Disponible</option>
                        <option value="EN_REMODELACION" ${a.estado === 'EN_REMODELACION' ? 'selected' : ''}>Remodelación</option>
                        <option value="INHABILITADA" ${a.estado === 'INHABILITADA' ? 'selected' : ''}>Inhabilitada</option>
                    </select>
                ` : `<span class="text-[10px] font-semibold">${a.estado}</span>`;

                grid.innerHTML += `
                    <div class="p-2.5 border rounded-xl bg-white shadow-xs flex flex-col justify-between ${badgeClass}">
                        <div class="flex justify-between items-start">
                            <div>
                                <h4 class="font-bold text-slate-800 text-xs">${a.nombre}</h4>
                                <span class="text-[10px] text-slate-400">${a.pabellon}</span>
                            </div>
                            <span class="text-[9px] font-bold px-1.5 py-0.2 rounded-full ${badgeClass}">
                                ${a.estado.slice(0,4)}
                            </span>
                        </div>
                        <div class="mt-2 pt-1 border-t border-slate-100">
                            ${actionHtml}
                        </div>
                    </div>
                `;

                selectRes.innerHTML += `<option value="${a.id}">${a.nombre} (${a.pabellon} - ${a.estado})</option>`;
            });
        }

        async function cambiarEstadoAula(aulaId, nuevoEstado) {
            try {
                const res = await fetch(`/api/v1/aulas/${aulaId}/estado`, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({nuevo_estado: nuevoEstado})
                });
                if (!res.ok) {
                    const err = await res.json();
                    throw new Error(err.detail || 'No se pudo cambiar el estado');
                }
                showAlert(`Estado de aula actualizado a ${nuevoEstado}`, false);
                cargarAulasPanel();
            } catch (err) {
                showAlert(err.message, true);
            }
        }

        // CARGA DE CATÁLOGO Y CASCADA
        async function cargarCatalogoCompleto() {
            try {
                const res = await fetch('/api/v1/catalogo');
                catalogoGlobal = await res.json();

                // Poblar select de carreras en modal rápida
                const modalCarr = document.getElementById('modalMatCarrera');
                modalCarr.innerHTML = '';
                catalogoGlobal.carreras.forEach(c => {
                    modalCarr.innerHTML += `<option value="${c.id}">${c.nombre} (${c.nivel})</option>`;
                });

                // Inicializar cascada nivel -> carreras -> materias
                poblarCarrerasPorNivel();
                poblarDocentes();
            } catch (err) {
                console.error("Error cargando catálogo:", err);
            }
        }

        function poblarDocentes(docenteIdSeleccionar = null) {
            const docSelect = document.getElementById('resDocente');
            docSelect.innerHTML = '';
            catalogoGlobal.docentes.forEach(d => {
                const sel = (docenteIdSeleccionar && docenteIdSeleccionar == d.id) ? 'selected' : '';
                docSelect.innerHTML += `<option value="${d.id}" ${sel}>${d.nombres} ${d.apellidos} (${d.cedula})</option>`;
            });
        }

        function onNivelCambiado() {
            poblarCarrerasPorNivel();
        }

        function poblarCarrerasPorNivel() {
            const nivelElegido = document.getElementById('resNivel').value;
            const carrSelect = document.getElementById('resCarrera');
            carrSelect.innerHTML = '';

            const filtradas = nivelElegido 
                ? catalogoGlobal.carreras.filter(c => c.nivel === nivelElegido)
                : catalogoGlobal.carreras;

            filtradas.forEach(c => {
                carrSelect.innerHTML += `<option value="${c.id}">${c.nombre} (${c.codigo})</option>`;
            });

            onCarreraCambiada();
        }

        function onCarreraCambiada() {
            const carrId = parseInt(document.getElementById('resCarrera').value);
            const matSelect = document.getElementById('resMateria');
            matSelect.innerHTML = '';

            const materiasFiltradas = catalogoGlobal.materias.filter(m => m.carrera_id === carrId);

            if (materiasFiltradas.length === 0) {
                matSelect.innerHTML = '<option value="">-- Sin materias registradas en esta carrera --</option>';
            } else {
                materiasFiltradas.forEach(m => {
                    matSelect.innerHTML += `<option value="${m.id}">[${m.codigo}] ${m.nombre}</option>`;
                });
            }
        }

        async function cargarReservasLista() {
            const fecha = document.getElementById('filtroFechaLista').value || hoy;
            try {
                const res = await fetch(`/api/v1/cartelera?fecha=${fecha}`);
                const items = await res.json();
                const tbody = document.getElementById('listaReservasBody');
                tbody.innerHTML = '';

                if (items.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="5" class="py-4 text-center text-slate-400">No hay reservas para esta fecha.</td></tr>';
                    return;
                }

                items.forEach(it => {
                    tbody.innerHTML += `
                        <tr class="hover:bg-slate-50">
                            <td class="py-2 px-2.5 font-bold whitespace-nowrap text-blue-900">${it.hora_inicio} - ${it.hora_fin}</td>
                            <td class="py-2 px-2.5 font-semibold text-slate-900">${it.aula_nombre}</td>
                            <td class="py-2 px-2.5">
                                <span class="font-bold text-blue-900">[${it.materia_codigo}]</span> ${it.materia_nombre}
                            </td>
                            <td class="py-2 px-2.5 text-slate-700 font-medium">${it.docente_nombre}</td>
                            <td class="py-2 px-2.5 text-right">
                                <button onclick="eliminarReserva(${it.reserva_id})" class="text-rose-600 hover:text-rose-800 font-bold p-1">
                                    <i class="fa-solid fa-trash-can"></i>
                                </button>
                            </td>
                        </tr>
                    `;
                });
            } catch (err) {
                console.error("Error cargando reservas:", err);
            }
        }

        async function crearReserva(e) {
            e.preventDefault();
            const matVal = document.getElementById('resMateria').value;
            if (!matVal) {
                showAlert('Por favor seleccione una materia válida.', true);
                return;
            }

            const payload = {
                aula_id: parseInt(document.getElementById('resAula').value),
                materia_id: parseInt(matVal),
                docente_id: parseInt(document.getElementById('resDocente').value),
                fecha: document.getElementById('resFecha').value,
                hora_inicio: document.getElementById('resHoraInicio').value,
                hora_fin: document.getElementById('resHoraFin').value,
                observaciones: document.getElementById('resObservaciones').value
            };

            try {
                const res = await fetch('/api/v1/reservas', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(payload)
                });

                const data = await res.json();
                if (!res.ok) {
                    throw new Error(data.detail || 'Error al procesar reserva');
                }

                showAlert('¡Reserva confirmada con éxito!', false);
                cargarReservasLista();
            } catch (err) {
                showAlert(err.message, true);
            }
        }

        async function eliminarReserva(id) {
            if (!confirm('¿Desea cancelar y liberar esta aula?')) return;
            try {
                const res = await fetch(`/api/v1/reservas/${id}`, {
                    method: 'DELETE',
                    headers: {'Authorization': `Bearer ${token}`}
                });
                if (!res.ok) throw new Error('Error al cancelar reserva');
                showAlert('Reserva liberada exitosamente', false);
                cargarReservasLista();
            } catch (err) {
                showAlert(err.message, true);
            }
        }

        // Modales
        function abrirModalAula() { document.getElementById('modalAula').classList.remove('hidden'); }
        function cerrarModalAula() { document.getElementById('modalAula').classList.add('hidden'); }
        function abrirModalDocente() { document.getElementById('modalDocente').classList.remove('hidden'); }
        function cerrarModalDocente() { document.getElementById('modalDocente').classList.add('hidden'); }
        function abrirModalMateria() { document.getElementById('modalMateria').classList.remove('hidden'); }
        function cerrarModalMateria() { document.getElementById('modalMateria').classList.add('hidden'); }

        async function guardarNuevaAula(e) {
            e.preventDefault();
            const nombre = document.getElementById('nuevaAulaNombre').value;
            const capacidad = parseInt(document.getElementById('nuevaAulaCapacidad').value);
            const pabellon = document.getElementById('nuevaAulaPabellon').value;

            try {
                const res = await fetch('/api/v1/aulas', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json', 'Authorization': `Bearer ${token}`},
                    body: JSON.stringify({nombre, capacidad, pabellon})
                });
                if (!res.ok) {
                    const err = await res.json();
                    throw new Error(err.detail || 'Error al crear aula');
                }
                cerrarModalAula();
                showAlert(`Aula '${nombre}' registrada exitosamente`, false);
                cargarAulasPanel();
            } catch (err) {
                showAlert(err.message, true);
            }
        }

        async function guardarNuevoDocente(e) {
            e.preventDefault();
            const payload = {
                cedula: document.getElementById('nuevoDocCedula').value,
                nombres: document.getElementById('nuevoDocNombres').value,
                apellidos: document.getElementById('nuevoDocApellidos').value,
                email: document.getElementById('nuevoDocEmail').value
            };

            try {
                const res = await fetch('/api/v1/catalogo/docentes', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json', 'Authorization': `Bearer ${token}`},
                    body: JSON.stringify(payload)
                });
                if (!res.ok) {
                    const err = await res.json();
                    throw new Error(err.detail || 'Error al registrar docente');
                }
                const docGuardado = await res.json();
                catalogoGlobal.docentes.push(docGuardado);
                poblarDocentes(docGuardado.id);
                cerrarModalDocente();
                showAlert(`Facilitador '${docGuardado.nombres} ${docGuardado.apellidos}' añadido al catálogo`, false);
            } catch (err) {
                showAlert(err.message, true);
            }
        }

        async function guardarNuevaMateria(e) {
            e.preventDefault();
            const payload = {
                carrera_id: parseInt(document.getElementById('modalMatCarrera').value),
                codigo: document.getElementById('modalMatCodigo').value,
                nombre: document.getElementById('modalMatNombre').value
            };

            try {
                const res = await fetch('/api/v1/catalogo/materias', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json', 'Authorization': `Bearer ${token}`},
                    body: JSON.stringify(payload)
                });
                if (!res.ok) {
                    const err = await res.json();
                    throw new Error(err.detail || 'Error al registrar materia');
                }
                const matGuardada = await res.json();
                catalogoGlobal.materias.push(matGuardada);
                // Si la carrera activa es la de la nueva materia, refrescar
                document.getElementById('resCarrera').value = matGuardada.carrera_id;
                onCarreraCambiada();
                document.getElementById('resMateria').value = matGuardada.id;
                cerrarModalMateria();
                showAlert(`Asignatura '[${matGuardada.codigo}] ${matGuardada.nombre}' agregada al catálogo`, false);
            } catch (err) {
                showAlert(err.message, true);
            }
        }

        document.getElementById('filtroFechaLista').addEventListener('change', cargarReservasLista);

        cargarAulasPanel();
        cargarCatalogoCompleto();
        cargarReservasLista();
    </script>
</body>
</html>
"""
