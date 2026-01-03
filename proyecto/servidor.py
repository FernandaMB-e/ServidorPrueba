from alumnos import crear_base_datos
from flask import Flask, render_template, request, jsonify
import sqlite3
import socket  # Nueva librería para detectar la IP

app = Flask(__name__)

# Función para obtener la IP real de la laptop en la red local
def obtener_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No necesita conexión real, solo para detectar la interfaz activa
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def buscar_por_matricula(matricula):
    conn = sqlite3.connect('alumnos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, matricula, sede, grupo, especialidad FROM alumnos WHERE matricula = ?", (matricula,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

@app.route('/sw.js')
def serve_sw():
    return app.send_static_file('sw.js')

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/acceder', methods=['POST'])
def acceder():
    matricula_ingresada = request.form.get('matricula')
    alumno = buscar_por_matricula(matricula_ingresada)
    if alumno:
        return jsonify({
            "success": True,
            "nombre": alumno[0],
            "matricula": alumno[1],
            "sede": alumno[2],
            "grupo": alumno[3],
            "especialidad": alumno[4]
        })
    return jsonify({"success": False})

if __name__ == '__main__':
    crear_base_datos()
    mi_ip = obtener_ip_local()
    
    # MENSAJE PARA EL PROFESOR
    print("\n" + "="*50)
    print("   SISTEMA ESCOLAR CARGADO EXITOSAMENTE")
    print("="*50)
    print(f"\n PROFESOR, ESCRIBA ESTO EN EL PIZARRÓN:")
    print(f"\n >>> http://{mi_ip}:5000 <<<")
    print("\n" + "="*50)
    print(" MANTENGA ESTA VENTANA ABIERTA DURANTE LA CLASE\n")

    app.run(host='0.0.0.0', port=5000, debug=False) # debug=False para que sea más estable