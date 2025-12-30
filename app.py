from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

def obtener_datos(legajo_id):
    try:
        # Cargamos el CSV con los ajustes que ya probamos
        df = pd.read_csv('base_datos_empleados_trenes.csv', sep=';', encoding='latin-1')
        # Convertimos a int por las dudas y buscamos
        empleado = df[df['Legajo'] == int(legajo_id)]
        if not empleado.empty:
            return empleado.iloc[0].to_dict()
    except Exception as e:
        print(f"Error al leer datos: {e}")
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consultar', methods=['POST'])
def consultar():
    data = request.json
    legajo = data.get('legajo')
    datos = obtener_datos(legajo)
    
    if datos:
        respuesta = (f"¡Hola {datos['Nombre']}! 👋<br><br>"
                   f"Consulté tu legajo y este es tu saldo:<br>"
                   f"• <b>Días por antigüedad:</b> {datos['Días Totales (2024)']} días.<br>"
                   f"• <b>Días ya gozados:</b> {datos['Días Gozados']} días.<br>"
                   f"• <b>Saldo disponible: {datos['Saldo Pendiente']} días corridos.</b>")
        return jsonify({"status": "ok", "respuesta": respuesta})
    
    return jsonify({"status": "error", "respuesta": "No encontré ese número de legajo. ¿Lo podrás revisar? 🤔"})

if __name__ == '__main__':
    app.run(debug=True)