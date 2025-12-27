import sqlite3

def crear_base_datos():
    conn = sqlite3.connect('alumnos.db')
    cursor = conn.cursor()
    # Creamos la tabla con la columna matricula
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            matricula TEXT UNIQUE NOT NULL,
            sede TEXT NOT NULL,
            grupo TEXT NOT NULL,
            especialidad TEXT NOT NULL
        )
    ''')
    
    # Insertamos unos alumnos de prueba
    alumnos_ejemplo = [
        ('Juan Perez', '20230001','Gnr.Felipe Angeles','1A','Tecnico agropecuario'),
        ('Maria Lopez', '20230002','Gnr.Felipe Angeles','1B','Tecnico en soporte y mantenimiento de equipo de computo'),
        ('Carlos Ruiz', '20230003','Gnr.Felipe Angeles','1A','Tecnico agropecuario')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO alumnos (nombre, matricula, sede, grupo, especialidad) 
        VALUES (?, ?, ?, ?, ?)
    ''', alumnos_ejemplo)
    
    conn.commit()

    # 3. Mostrar los valores en una tabla limpia
    print(f"{'ID':<3} | {'MATRÍCULA':<10} | {'NOMBRE':<15} | {'SEDE':<10} | {'GPO':<5} | {'ESPECIALIDAD'}")
    print("-" * 75)
    
    cursor.execute("SELECT * FROM alumnos")
    for fila in cursor.fetchall():
        # fila[0]=id, [1]=nombre, [2]=matricula, [3]=sede, [4]=grupo, [5]=especialidad
        print(f"{fila[0]:<3} | {fila[2]:<10} | {fila[1]:<15} | {fila[3]:<10} | {fila[4]:<5} | {fila[5]}")

    conn.close()

