from alumnos import crear_base_datos
from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Función actualizada para traer todos los campos de tu tabla
def buscar_por_matricula(matricula):
    conn = sqlite3.connect('alumnos.db')
    cursor = conn.cursor()
    # Buscamos nombre, matricula, sede, grupo y especialidad
    cursor.execute("SELECT nombre, matricula, sede, grupo, especialidad FROM alumnos WHERE matricula = ?", (matricula,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

@app.route('/sw.js')
def serve_sw():
    # Esto permite que la PWA se instale y funcione offline
    return app.send_static_file('sw.js')

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/acceder', methods=['POST'])
def acceder():
    matricula_ingresada = request.form.get('matricula')
    alumno = buscar_por_matricula(matricula_ingresada)
    
    if alumno:
        # Enviamos el JSON completo con los 5 datos clave
        return jsonify({
            "success": True,
            "nombre": alumno[0],
            "matricula": alumno[1],
            "sede": alumno[2],
            "grupo": alumno[3],
            "especialidad": alumno[4]
        })
    else:
        # Si la matrícula no existe
        return jsonify({"success": False})

if __name__ == '__main__':
    crear_base_datos() 
    # El host '0.0.0.0' es lo que permite que los alumnos se conecten a tu IP
    app.run(host='0.0.0.0', port=5000, debug=True)