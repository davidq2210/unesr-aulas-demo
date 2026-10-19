# TDD Evidence Report: Sistema Completo de Gestión y Reserva de Aulas (UNESR Los Teques)

## 1. Resumen Ejecutivo
- **Institución:** Universidad Nacional Experimental Simón Rodríguez (UNESR) - Núcleo Los Teques.
- **Población:** ~3.000 estudiantes (educación andragógica y semipresencial).
- **Recursos Físicos:** 12 aulas iniciales escalables (estados: `DISPONIBLE`, `EN_REMODELACION`, `INHABILITADA`).
- **Arquitectura:** Clean Architecture (Domain $\rightarrow$ Application $\rightarrow$ Infrastructure $\rightarrow$ Presentation).
- **Stack Técnico:** Python 3.12, FastAPI, SQLite nativo (`PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000; BEGIN IMMEDIATE`), TailwindCSS.
- **Framework de Testing:** `unittest` estándar de Python.
- **Batería de Pruebas:** **53 tests ejecutados, 53 aprobados, 0 fallos (100% PASS en 0.993s)**.

---

## 2. Nuevas Capacidades y Mejoras Incorporadas

1. **Catálogo Académico UNESR Enriquecido:**
   - 11 programas de **PREGRADO** (Lic. en Administración menciones: Informática, Recursos Humanos, Mercadeo, Organización y Sistemas, Recursos Materiales y Financieros; Lic. en Administración de Empresas Agropecuarias, Lic. en Agroecología, PNF en Medicina Veterinaria, Lic. en Educación Integral, Educación mención Agropecuaria, Educación Preescolar).
   - 5 programas de **POSTGRADO y DOCTORADO** (Maestría en Ciencias de la Educación, Maestría en Ciencias Administrativas mención Gerencia Estratégica, Maestría en Gerencia Pública, Doctorado en Ciencias de la Educación, Doctorado en Ciencias Administrativas).
   - Códigos oficiales por materia (ej. `[INF-101] Algoritmos y Programación`, `[RMF-201] Presupuesto y Finanzas`, `[MCE-501] Epistemología de la Educación Andragógica`).
   - Endpoints para extender dinámicamente el catálogo: `POST /api/v1/catalogo/docentes` y `POST /api/v1/catalogo/materias`.

2. **Tarjetas de Aula Dinámicas en Cartelera:**
   - Si un aula está `DISPONIBLE` y tiene clases asignadas en la fecha seleccionada, la tarjeta muestra internamente los bloques de horario, asignatura con código, badge de Pregrado/Postgrado y nombre del facilitador. Si está libre, indica *"Totalmente Libre"*.

3. **Matriz Semanal Completa (Lunes a Sábado):**
   - Selector interactivo *"Vista del Día"* vs *"Matriz Semanal (Lun - Sáb)"*.
   - Endpoint `GET /api/v1/cartelera/semanal?fecha_inicio=YYYY-MM-DD` que consulta el rango continuo de 6-7 días.
   - Tabla matriz con filas por aula y columnas por día (Lunes a Sábado), detallando los bloques horarios y facilitadores.

4. **Modo Impresión Oficial para Pasillos:**
   - Botón visible `🖨️ Imprimir para Pasillos`.
   - Reglas `@media print` que ocultan menús y botones, muestran membrete institucional oficial de la UNESR y formatean las tablas con bordes nítidos para impresión física o PDF.

5. **Menús en Cascada y Modales Rápidos en `/panel`:**
   - Formulario en cascada: Nivel Académico $\rightarrow$ Carrera/Programa $\rightarrow$ Asignatura con Código $\rightarrow$ Facilitador $\rightarrow$ Horario (07:00 a 19:00).
   - Modales rápidos para añadir nuevos facilitadores y materias sin salir del panel.

---

## 3. Matriz Completa de Evidencias de Pruebas (53 Tests)

| # | Comportamiento Garantizado | Archivo de Prueba | Tipo | Resultado |
|---|----------------------------|-------------------|------|-----------|
| 1 | Rechazo de rangos con hora_inicio >= hora_fin | `test_value_objects.py` | Unit | PASS |
| 2 | Rechazo de horarios fuera de jornada (07:00 a 19:00) | `test_value_objects.py` | Unit | PASS |
| 3 | Inmutabilidad de `RangoHorario` | `test_value_objects.py` | Unit | PASS |
| 4 | Detección de solapamiento en rangos idénticos | `test_value_objects.py` | Unit | PASS |
| 5 | Detección de solapamiento parcial cruzado | `test_value_objects.py` | Unit | PASS |
| 6 | Detección de solapamiento por inclusión | `test_value_objects.py` | Unit | PASS |
| 7 | Clases contiguas `[07:00, 09:00)` y `[09:00, 11:00)` NO colisionan | `test_value_objects.py` | Unit | PASS |
| 8 | Rangos horarios disjuntos no colisionan | `test_value_objects.py` | Unit | PASS |
| 9 | Aula disponible valida operatividad sin excepción | `test_entities.py` | Unit | PASS |
| 10 | Aula en remodelación lanza `AulaNoDisponibleError` | `test_entities.py` | Unit | PASS |
| 11 | Aula inhabilitada lanza `AulaNoDisponibleError` | `test_entities.py` | Unit | PASS |
| 12 | Mutación controlada de estado de aula | `test_entities.py` | Unit | PASS |
| 13 | Integridad de entidades académicas (Carrera, Materia, Docente) | `test_entities.py` | Unit | PASS |
| 14 | Verificación de privilegios de usuario por rol | `test_entities.py` | Unit | PASS |
| 15 | Estructura de datos e inmutabilidad de `Reserva` | `test_entities.py` | Unit | PASS |
| 16 | Motor Anti-Colisión rechaza reservas en aulas no disponibles | `test_motor_anti_colision.py` | Unit | PASS |
| 17 | Motor Anti-Colisión lanza `ColisionAulaError` ante choque de espacio | `test_motor_anti_colision.py` | Unit | PASS |
| 18 | Motor Anti-Colisión aprueba clases contiguas en misma aula | `test_motor_anti_colision.py` | Unit | PASS |
| 19 | Motor Anti-Colisión permite misma hora en fechas distintas | `test_motor_anti_colision.py` | Unit | PASS |
| 20 | Motor Anti-Colisión lanza `ColisionDocenteError` si profesor choca | `test_motor_anti_colision.py` | Unit | PASS |
| 21 | Motor Anti-Colisión excluye la propia reserva al editar | `test_motor_anti_colision.py` | Unit | PASS |
| 22 | `CrearReservaUseCase` persiste con `Unit of Work` transaccional | `test_crear_reserva_use_case.py` | Unit | PASS |
| 23 | `CrearReservaUseCase` falla si el aula física no existe | `test_crear_reserva_use_case.py` | Unit | PASS |
| 24 | `CrearReservaUseCase` propaga `AulaNoDisponibleError` | `test_crear_reserva_use_case.py` | Unit | PASS |
| 25 | `CrearReservaUseCase` propaga `ColisionAulaError` | `test_crear_reserva_use_case.py` | Unit | PASS |
| 26 | `CrearReservaUseCase` propaga `ColisionDocenteError` | `test_crear_reserva_use_case.py` | Unit | PASS |
| 27 | Directivo cambia estado de aula a `EN_REMODELACION` | `test_cambiar_estado_aula_use_case.py` | Unit | PASS |
| 28 | Coordinador inhabilita aula | `test_cambiar_estado_aula_use_case.py` | Unit | PASS |
| 29 | Profesor y Estudiante son rechazados con `PermisoDenegadoError` | `test_cambiar_estado_aula_use_case.py` | Unit | PASS |
| 30 | Error al intentar actualizar estado de aula inexistente | `test_cambiar_estado_aula_use_case.py` | Unit | PASS |
| 31 | Cartelera expone código de materia y nivel académico | `test_consultar_cartelera_use_case.py` | Unit | PASS |
| 32 | Cartelera semanal consulta rango completo Lunes a Sábado | `test_consultar_cartelera_use_case.py` | Unit | PASS |
| 33 | Cartelera semanal filtra por aula específica | `test_consultar_cartelera_use_case.py` | Unit | PASS |
| 34 | Hashing seguro PBKDF2 y verificación con `secrets.compare_digest` | `test_security.py` | Unit | PASS |
| 35 | Emisión y validación de tokens JWT estándar (HMAC-SHA256) | `test_security.py` | Unit | PASS |
| 36 | Rechazo de tokens JWT expirados o con firma adulterada | `test_security.py` | Unit | PASS |
| 37 | Validación de pragmas SQLite: `WAL`, `busy_timeout=5000`, `foreign_keys=ON` | `test_sqlite_repositories.py` | Integration | PASS |
| 38 | CRUD y persistencia de `Aula` en SQLite nativo | `test_sqlite_repositories.py` | Integration | PASS |
| 39 | Persistencia atómica de `Reserva`, adapter cartelera con código/nivel y consulta semanal | `test_sqlite_repositories.py` | Integration | PASS |
| 40 | Registro dinámico de docentes y asignaturas en catálogo | `test_sqlite_repositories.py` | Integration | PASS |
| 41 | Seeder institucional idempotente: puebla 12 aulas y catálogo completo | `test_seeder.py` | Integration | PASS |
| 42 | **Condición de Carrera Multihilo:** 5 hilos simultáneos: exactamente 1 éxito y 4 colisiones controladas | `test_concurrencia_sqlite.py` | Integration | PASS |
| 43 | `POST /api/v1/auth/login` emite JWT válido para Directivo | `test_api_endpoints.py` | E2E | PASS |
| 44 | `POST /api/v1/auth/login` rechaza credenciales inválidas (401) | `test_api_endpoints.py` | E2E | PASS |
| 45 | `GET /api/v1/cartelera` retorna cartelera pública con código y nivel (200) | `test_api_endpoints.py` | E2E | PASS |
| 46 | `GET /api/v1/cartelera/semanal` retorna matriz semanal (200) | `test_api_endpoints.py` | E2E | PASS |
| 47 | `GET /api/v1/aulas` lista las 12 aulas físicas con sus estados (200) | `test_api_endpoints.py` | E2E | PASS |
| 48 | `PATCH /api/v1/aulas/{id}/estado` actualiza estado operativo con RBAC (200) | `test_api_endpoints.py` | E2E | PASS |
| 49 | **Motor Anti-Colisión:** `POST /api/v1/reservas` retorna **HTTP 409 Conflict** | `test_api_endpoints.py` | E2E | PASS |
| 50 | **Validación Operativa:** Intento de reserva en aula en remodelación retorna **HTTP 409 Conflict** | `test_api_endpoints.py` | E2E | PASS |
| 51 | Creación exitosa (201) y liberación/cancelación (DELETE 200) de reserva | `test_api_endpoints.py` | E2E | PASS |
| 52 | Registro dinámico de nuevo docente y nueva materia vía API (201) | `test_api_endpoints.py` | E2E | PASS |
| 53 | Disponibilidad de vistas web interactivas: `/` (Cartelera), `/login`, `/panel` | `test_api_endpoints.py` | E2E | PASS |
