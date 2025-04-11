import sqlite3
import random

DB_PATH = 'db/preguntas.db'

def obtener_opciones(cursor, campo):
    cursor.execute(f"SELECT DISTINCT {campo} FROM preguntas")
    return [row[0] for row in cursor.fetchall()]

def seleccionar_preguntas(asignatura, tema, limite=20):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if tema:
        query = """
            SELECT id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta
            FROM preguntas
            WHERE asignatura = ? AND tema = ?
        """
        cursor.execute(query, (asignatura, tema))
    else:
        query = """
            SELECT id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta
            FROM preguntas
            WHERE asignatura = ?
        """
        cursor.execute(query, (asignatura,))

    preguntas = cursor.fetchall()
    conn.close()

    return random.sample(preguntas, min(limite, len(preguntas)))

def menu_test():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    asignaturas = obtener_opciones(cursor, 'asignatura')
    print("\nAsignaturas disponibles:")
    for i, a in enumerate(asignaturas, start=1):
        print(f"{i}. {a}")

    try:
        opcion_a = int(input("Selecciona una asignatura (número): "))
        asignatura = asignaturas[opcion_a - 1]
    except:
        print("[ERROR] Selección inválida.")
        return

    cursor.execute("SELECT DISTINCT tema FROM preguntas WHERE asignatura = ?", (asignatura,))
    temas = [row[0] for row in cursor.fetchall()]

    print(f"\nTemas disponibles para {asignatura}:")
    for i, t in enumerate(temas, start=1):
        print(f"{i}. {t}")
    print("0. Todas los temas")

    try:
        opcion_t = int(input("Selecciona un tema (número, 0 para todos): "))
        tema = temas[opcion_t - 1] if opcion_t != 0 else None
    except:
        print("[ERROR] Selección inválida.")
        return

    preguntas = seleccionar_preguntas(asignatura, tema)
    if not preguntas:
        print("No hay preguntas disponibles.")
        return

    print(f"\nComenzando test de {len(preguntas)} preguntas...\n")
    correctas = 0

    for i, (id, enunciado, a, b, c, d, correcta) in enumerate(preguntas, start=1):
        # Creamos una lista con todas las opciones posibles
        opciones = [('A', a), ('B', b), ('C', c), ('D', d)]

        # Barajamos solo los textos, pero perderemos la letra original
        textos_respuestas = [a, b, c, d]
        random.shuffle(textos_respuestas)

        # Asociamos A-D con las respuestas barajadas
        letras = ['A', 'B', 'C', 'D']
        opciones_barajadas = list(zip(letras, textos_respuestas))

        # Identificamos cuál es el texto de la respuesta correcta original
        respuesta_correcta_texto = dict(opciones)[correcta]

        # Identificamos cuál es la nueva letra que tiene esa respuesta
        nueva_respuesta_correcta = next(
            letra for letra, texto in opciones_barajadas if texto == respuesta_correcta_texto
        )

        # Mostramos la pregunta
        print(f"{i}. {enunciado}")
        for letra, texto in opciones_barajadas:
            print(f"   {letra}) {texto}")

        # Recoger respuesta del usuario
        respuesta = input("Tu respuesta (A/B/C/D): ").strip().upper()
        if respuesta == nueva_respuesta_correcta:
            print("✅ Correcto!\n")
            correctas += 1
        else:
            print(f"❌ Incorrecto. Respuesta correcta: {nueva_respuesta_correcta}\n")

    print(f"Test finalizado. Aciertos: {correctas}/{len(preguntas)}")