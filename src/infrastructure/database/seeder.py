from datetime import date
from src.infrastructure.database.connection import get_db_connection
from src.infrastructure.database.schema import init_db_schema
from src.infrastructure.security.password_hasher import hash_password


def seed_database(db_path: str = "unesr_aulas.db", force_update: bool = False) -> None:
    """
    Inicializa de manera idempotente la base de datos con los datos institucionales
    completos de la UNESR Núcleo Los Teques (12 aulas, catálogo de pregrado y postgrado,
    docentes, usuarios y reservas de ejemplo).
    Si force_update es True, inserta los nuevos programas y materias sin borrar datos existentes.
    """
    conn = get_db_connection(db_path)
    init_db_schema(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM aulas;")
    count_aulas = cursor.fetchone()[0]

    # Iniciar transacción atómica
    conn.execute("BEGIN IMMEDIATE;")
    try:
        # 1. 12 Aulas iniciales si no existen
        if count_aulas == 0:
            for i in range(1, 9):
                pabellon = "Pabellón A" if i <= 4 else "Pabellón B"
                cursor.execute(
                    "INSERT INTO aulas (nombre, capacidad, pabellon, estado) VALUES (?, ?, ?, ?);",
                    (f"Aula {i:02d}", 35 if i % 2 == 1 else 40, pabellon, "DISPONIBLE")
                )

            cursor.execute("INSERT INTO aulas (nombre, capacidad, pabellon, estado) VALUES (?, ?, ?, ?);", ("Aula 09", 30, "Pabellón C", "EN_REMODELACION"))
            cursor.execute("INSERT INTO aulas (nombre, capacidad, pabellon, estado) VALUES (?, ?, ?, ?);", ("Aula 10", 30, "Pabellón C", "EN_REMODELACION"))
            cursor.execute("INSERT INTO aulas (nombre, capacidad, pabellon, estado) VALUES (?, ?, ?, ?);", ("Aula 11", 25, "Pabellón C", "INHABILITADA"))
            cursor.execute("INSERT INTO aulas (nombre, capacidad, pabellon, estado) VALUES (?, ?, ?, ?);", ("Aula 12", 25, "Pabellón C", "INHABILITADA"))

        # 2. Catálogo Académico Real UNESR Los Teques
        carreras_data = [
            # PREGRADO
            ("INF-01", "Lic. en Administración mención Informática", "PREGRADO"),
            ("RRHH-01", "Lic. en Administración mención Recursos Humanos", "PREGRADO"),
            ("MER-01", "Lic. en Administración mención Mercadeo", "PREGRADO"),
            ("OYS-01", "Lic. en Administración mención Organización y Sistemas", "PREGRADO"),
            ("RMF-01", "Lic. en Administración mención Recursos Materiales y Financieros", "PREGRADO"),
            ("AGRO-01", "Lic. en Administración de Empresas Agropecuarias", "PREGRADO"),
            ("AGROE-01", "Lic. en Agroecología", "PREGRADO"),
            ("MEDV-01", "PNF en Medicina Veterinaria", "PREGRADO"),
            ("EDU-01", "Lic. en Educación Integral", "PREGRADO"),
            ("EDUA-01", "Lic. en Educación mención Agropecuaria", "PREGRADO"),
            ("EDUP-01", "Lic. en Educación Preescolar", "PREGRADO"),

            # POSTGRADO / DOCTORADO / TALLERES
            ("MCE-01", "Maestría en Ciencias de la Educación", "POSTGRADO"),
            ("MCA-01", "Maestría en Ciencias Administrativas (Gerencia Estratégica)", "POSTGRADO"),
            ("MGP-01", "Maestría en Gerencia Pública", "POSTGRADO"),
            ("DCE-01", "Doctorado en Ciencias de la Educación", "DOCTORADO"),
            ("DCA-01", "Doctorado en Ciencias Administrativas", "DOCTORADO"),
        ]

        for cod, nom, niv in carreras_data:
            cursor.execute(
                """
                INSERT INTO carreras (codigo, nombre, nivel)
                VALUES (?, ?, ?)
                ON CONFLICT(codigo) DO UPDATE SET nombre = excluded.nombre, nivel = excluded.nivel;
                """,
                (cod, nom, niv)
            )

        # Mapa de código de carrera a ID
        cursor.execute("SELECT id, codigo FROM carreras;")
        carr_map = {row["codigo"]: row["id"] for row in cursor.fetchall()}

        # 3. Materias con código y nombre formal
        materias_data = [
            # Informática
            (carr_map["INF-01"], "INF-101", "Algoritmos y Programación"),
            (carr_map["INF-01"], "INF-102", "Bases de Datos"),
            (carr_map["INF-01"], "INF-103", "Sistemas de Información"),
            (carr_map["INF-01"], "INF-201", "Redes de Computadoras"),
            # Recursos Humanos
            (carr_map["RRHH-01"], "RRHH-101", "Gestión del Talento Humano"),
            (carr_map["RRHH-01"], "RRHH-102", "Legislación Laboral Venezolana"),
            # Mercadeo
            (carr_map["MER-01"], "MER-101", "Investigación de Mercados"),
            (carr_map["MER-01"], "MER-102", "Estrategias de Comercialización"),
            # Organización y Sistemas
            (carr_map["OYS-01"], "OYS-101", "Análisis y Diseño de Procesos"),
            (carr_map["OYS-01"], "OYS-102", "Manuales Administrativos"),
            # Recursos Materiales y Financieros
            (carr_map["RMF-01"], "RMF-201", "Presupuesto y Finanzas"),
            (carr_map["RMF-01"], "RMF-202", "Contabilidad de Costos"),
            # Empresas Agropecuarias & Agroecología
            (carr_map["AGRO-01"], "AGR-101", "Administración de Fincas y Unidades de Producción"),
            (carr_map["AGROE-01"], "AGC-101", "Sistemas Agroecológicos Sostenibles"),
            # Medicina Veterinaria
            (carr_map["MEDV-01"], "VET-101", "Anatomía y Fisiología Animal"),
            (carr_map["MEDV-01"], "VET-102", "Salud Pública y Epidemiología Veterinaria"),
            # Educación Integral, Agropecuaria y Preescolar
            (carr_map["EDU-01"], "EDU-301", "Andragogía y Métodos de Aprendizaje"),
            (carr_map["EDU-01"], "EDU-302", "Didáctica de la Lectoescritura"),
            (carr_map["EDUA-01"], "EDA-201", "Pedagogía de la Producción Agrícola"),
            (carr_map["EDUP-01"], "EDP-201", "Desarrollo Psicomotor Infantil"),

            # Postgrado
            (carr_map["MCE-01"], "MCE-501", "Epistemología de la Educación Andragógica"),
            (carr_map["MCE-01"], "MCE-502", "Diseño Curricular Universitario"),
            (carr_map["MCA-01"], "MCA-601", "Planificación y Gerencia Estratégica"),
            (carr_map["MCA-01"], "MCA-602", "Toma de Decisiones Financieras"),
            (carr_map["MGP-01"], "MGP-501", "Políticas Públicas y Estado"),

            # Doctorado
            (carr_map["DCE-01"], "DCE-701", "Seminario de Investigación Doctoral I"),
            (carr_map["DCA-01"], "DCA-701", "Teoría Organizacional y Paradigmas Administrativos"),
        ]

        for c_id, cod, nom in materias_data:
            cursor.execute(
                """
                INSERT INTO materias (carrera_id, codigo, nombre)
                VALUES (?, ?, ?)
                ON CONFLICT(codigo) DO UPDATE SET carrera_id = excluded.carrera_id, nombre = excluded.nombre;
                """,
                (c_id, cod, nom)
            )

        # 4. Padrón Docente
        docentes_data = [
            ("V-15234567", "Pedro", "Pérez", "pperez@unesr.edu.ve"),
            ("V-16890123", "María", "Rodríguez", "mrodriguez@unesr.edu.ve"),
            ("V-14567890", "Carlos", "Gómez", "cgomez@unesr.edu.ve"),
            ("V-12987654", "Ana", "Mendoza", "amendoza@unesr.edu.ve"),
            ("V-18765432", "Franklin", "Quintero", "fquintero@unesr.edu.ve"),
        ]

        for ced, nom, ape, eml in docentes_data:
            cursor.execute(
                """
                INSERT INTO docentes (cedula, nombres, apellidos, email, activo)
                VALUES (?, ?, ?, ?, 1)
                ON CONFLICT(cedula) DO UPDATE SET nombres = excluded.nombres, apellidos = excluded.apellidos, email = excluded.email;
                """,
                (ced, nom, ape, eml)
            )

        cursor.execute("SELECT id, cedula FROM docentes;")
        doc_map = {row["cedula"]: row["id"] for row in cursor.fetchall()}

        # 5. Usuarios Iniciales RBAC
        cursor.execute(
            """
            INSERT INTO usuarios (username, email, password_hash, rol, activo)
            VALUES (?, ?, ?, ?, 1)
            ON CONFLICT(username) DO NOTHING;
            """,
            ("admin", "admin@unesr.edu.ve", hash_password("unesr2026"), "DIRECTIVO")
        )
        cursor.execute(
            """
            INSERT INTO usuarios (username, email, password_hash, rol, docente_id, activo)
            VALUES (?, ?, ?, ?, ?, 1)
            ON CONFLICT(username) DO NOTHING;
            """,
            ("pperez", "pperez@unesr.edu.ve", hash_password("docente123"), "PROFESOR", doc_map["V-15234567"])
        )
        cursor.execute(
            """
            INSERT INTO usuarios (username, email, password_hash, rol, activo)
            VALUES (?, ?, ?, ?, 1)
            ON CONFLICT(username) DO NOTHING;
            """,
            ("estudiante", "estudiante@unesr.edu.ve", hash_password("consulta123"), "ESTUDIANTE")
        )

        # 6. Reserva de Ejemplo inicial (si no hay reservas aún)
        cursor.execute("SELECT COUNT(*) FROM reservas;")
        if cursor.fetchone()[0] == 0:
            cursor.execute("SELECT id FROM usuarios WHERE username = 'admin';")
            admin_uid = cursor.fetchone()[0]

            cursor.execute("SELECT id FROM materias WHERE codigo = 'INF-101';")
            mat_id = cursor.fetchone()[0]

            hoy = date.today().isoformat()
            cursor.execute(
                """
                INSERT INTO reservas (aula_id, docente_id, materia_id, fecha, hora_inicio, hora_fin, creado_por_usuario_id, observaciones)
                VALUES (1, ?, ?, ?, '07:00', '09:00', ?, 'Clase inaugural de Algoritmos y Programación');
                """,
                (doc_map["V-15234567"], mat_id, hoy, admin_uid)
            )

        conn.execute("COMMIT;")
    except Exception:
        conn.execute("ROLLBACK;")
        raise
    finally:
        cursor.close()
        conn.close()
