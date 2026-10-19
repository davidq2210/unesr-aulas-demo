# UNESR Aulas Backend - Project Context

## 1. Visión del Proyecto
Backend para el sistema de gestión y reserva de aulas de la **Universidad Nacional Experimental Simón Rodríguez (UNESR) - Núcleo Los Teques**.
- **Población:** ~3.000 estudiantes bajo el modelo andragógico (educación semipresencial, adultos trabajadores, cohortes flexibles, fines de semana y vespertino).
- **Recursos Físicos:** 12 aulas iniciales altamente demandadas y escalables.
- **Catálogo Académico:** 32 carreras (Pregrado y Postgrado), múltiples asignaturas y padrón de profesores dinámico por semestre.
- **Ventana Operativa:** Jornada continua de 07:00 a 19:00 con intervalos horarios semi-abiertos `[inicio, fin)`.

---

## 2. Arquitectura de Software: Clean Architecture
El sistema sigue los principios de Clean Architecture (Robert C. Martin) y Puertos & Adaptadores:
- **`src/domain/`**: Núcleo puro de negocio. Sin dependencias externas ni frameworks. Contiene Entidades, Value Objects, Excepciones de Dominio, Interfaces de Repositorios y Servicios de Dominio (Motor Anti-Colisión).
- **`src/application/`**: Casos de uso del sistema, DTOs de entrada/salida y puertos de salida (`IUnitOfWork`, Interfaces secundarias).
- **`src/infrastructure/`**: Implementaciones tecnológicas concretas. Persistencia con `sqlite3` estándar (WAL mode, busy_timeout=5000, transacciones atómicas `BEGIN IMMEDIATE`), seguridad (JWT, Bcrypt).
- **`src/presentation/`**: Puntos de entrada HTTP (FastAPI), routers, esquemas de transporte Pydantic y mapeo de excepciones de dominio a códigos HTTP (ej. `ColisionAulaError` -> HTTP 409).

---

## 3. Reglas de Negocio Críticas (Motor Anti-Colisión)
1. **Estado Operativo del Aula:** Solo las aulas en estado `DISPONIBLE` pueden recibir reservas. Si el estado es `EN_REMODELACION` o `INHABILITADA`, la reserva es rechazada.
2. **Anti-Colisión de Espacio (No Doble Reserva):** No puede existir más de una reserva en la misma aula y fecha cuyos rangos horarios se solapen. La condición matemática para solapamiento en intervalos semi-abiertos $[inicio, fin)$ es:
   $$\max(\text{inicio}_1, \text{inicio}_2) < \min(\text{fin}_1, \text{fin}_2)$$
   Clases contiguas (ej. 07:00-09:00 y 09:00-11:00) **no** colisionan.
3. **Disponibilidad Docente:** Un docente no puede ser asignado a dos aulas diferentes en rangos horarios solapados de la misma fecha.

---

## 4. Roles y Seguridad (RBAC)
- **`DIRECTIVO` / `COORDINADOR`:** Control total (gestión de aulas, estados, aprobaciones, catálogo y reservas).
- **`PROFESOR`:** Puede consultar disponibilidad y gestionar la reserva de sus clases asignadas.
- **`ESTUDIANTE`:** Rol de solo lectura para consulta de cartelera académica en tiempo real.

---

## 5. Estrategia de Concurrencia e Infraestructura
- **Base de datos:** SQLite monolítica local (`unesr_aulas.db`).
- **Modo WAL:** `PRAGMA journal_mode=WAL;` para lecturas concurrentes sin bloqueo de lectores por escritores.
- **Timeout:** `PRAGMA busy_timeout=5000;` para tolerar esperas de escritura sin abortar inmediatamente.
- **Transacciones Atómicas:** `BEGIN IMMEDIATE` para adquirir bloqueo exclusivo antes de leer y validar colisiones, previniendo condiciones de carrera si dos coordinadores reservan el mismo espacio en el mismo milisegundo.
- **Testing:** `unittest` nativo de Python para pruebas ultra-rápidas y reproducibles sin dependencias pesadas.
