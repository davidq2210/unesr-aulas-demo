import sqlite3


def init_db_schema(conn: sqlite3.Connection) -> None:
    """
    Crea las tablas e índices relacionales del sistema si no existen.
    """
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS aulas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        capacidad INTEGER NOT NULL,
        pabellon TEXT NOT NULL,
        estado TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS carreras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL UNIQUE,
        nombre TEXT NOT NULL,
        nivel TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        carrera_id INTEGER NOT NULL,
        codigo TEXT NOT NULL UNIQUE,
        nombre TEXT NOT NULL,
        FOREIGN KEY (carrera_id) REFERENCES carreras(id) ON DELETE RESTRICT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS docentes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cedula TEXT NOT NULL UNIQUE,
        nombres TEXT NOT NULL,
        apellidos TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        activo INTEGER NOT NULL DEFAULT 1
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        rol TEXT NOT NULL,
        docente_id INTEGER,
        activo INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (docente_id) REFERENCES docentes(id) ON DELETE SET NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aula_id INTEGER NOT NULL,
        docente_id INTEGER NOT NULL,
        materia_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        hora_inicio TEXT NOT NULL,
        hora_fin TEXT NOT NULL,
        creado_por_usuario_id INTEGER NOT NULL,
        observaciones TEXT DEFAULT '',
        FOREIGN KEY (aula_id) REFERENCES aulas(id) ON DELETE RESTRICT,
        FOREIGN KEY (docente_id) REFERENCES docentes(id) ON DELETE RESTRICT,
        FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE RESTRICT,
        FOREIGN KEY (creado_por_usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT
    );
    """)

    # Índices para acelerar el Motor Anti-Colisión y las consultas de cartelera
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_reservas_aula_fecha ON reservas(aula_id, fecha);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_reservas_docente_fecha ON reservas(docente_id, fecha);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_reservas_fecha ON reservas(fecha);")

    cursor.close()
