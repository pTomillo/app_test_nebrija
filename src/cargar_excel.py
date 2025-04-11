import pandas as pd
import sqlite3
import os

def importar_preguntas():
    excel_path = 'data/preguntas.xlsx'
    db_path =  'db/preguntas.db'

    if not os.path.exists(excel_path):
        print(f"[ERROR] No se ha encontrado el archivo excel en: {excel_path}")
        return

    print(f"[INFO] Cargando preguntas desde el Excel...")

    df = pd.read_excel(excel_path)

    columnas_necesarias = {'Asignatura', 'Tema', 'Pregunta', 'Opción A', 'Opción B', 'Opción C', 'Opción D', 'Respuesta Correcta'}
    if not columnas_necesarias.issubset(df.columns):
        print("[ERROR] El archivo Excel no tiene las columnas necesarias")
        return

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS preguntas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asignatura TEXT,
                tema TEXT,
                pregunta TEXT,
                opcion_a TEXT,
                opcion_b TEXT,
                opcion_c TEXT,
                opcion_d TEXT,
                respuesta_correcta TEXT
            )
        ''')

    cursor.execute("DELETE FROM preguntas")

    for _, row in df.iterrows():
        cursor.execute('''
                    INSERT INTO preguntas (
                        asignatura, tema, pregunta,
                        opcion_a, opcion_b, opcion_c, opcion_d,
                        respuesta_correcta
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
            row['Asignatura'], row['Tema'], row['Pregunta'],
            row['Opción A'], row['Opción B'], row['Opción C'], row['Opción D'],
            str(row['Respuesta Correcta']).strip().upper()
        ))
    conn.commit()
    conn.close()
    print("[INFO] Preguntas cargadas correctamente.")