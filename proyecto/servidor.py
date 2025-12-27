from alumnos import crear_base_datos
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def buscar_por_matricula(matricula):
    conn = sqlite3.connect('alumnos.db')
    cursor = conn.cursor()
    # Buscamos la matrícula exacta
    cursor.execute("SELECT nombre FROM alumnos WHERE matricula = ?", (matricula,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/acceder', methods=['POST'])
def acceder():
    matricula_ingresada = request.form.get('matricula')
    alumno = buscar_por_matricula(matricula_ingresada)
    
    if alumno:
       
        return f"<h1>¡Bienvenido!</h1><p>Alumno: {alumno[0]}</p><p>Acceso concedido con matrícula {matricula_ingresada}</p>"
    else:
        return "<h1>Error: Matrícula no encontrada</h1><a href='/'>Intentar de nuevo</a>"

if __name__ == '__main__':
    crear_base_datos() 
    app.run(host='0.0.0.0', port=5000)