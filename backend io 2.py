from flask import Flask, request, jsonify
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS

def esquina_noroeste(oferta_original, demanda_original):
    oferta = oferta_original.copy()
    demanda = demanda_original.copy()
    filas, columnas = len(oferta), len(demanda)
    resultado = np.zeros((filas, columnas))

    i, j = 0, 0
    while i < filas and j < columnas:
        asignacion = min(oferta[i], demanda[j])
        resultado[i][j] = asignacion
        oferta[i] -= asignacion
        demanda[j] -= asignacion

        if oferta[i] == 0:
            i += 1
        if demanda[j] == 0:
            j += 1

    return {"asignaciones": resultado.tolist()}

def costo_minimo(costos, oferta_original, demanda_original):
    oferta = oferta_original.copy()
    demanda = demanda_original.copy()
    filas, columnas = len(oferta), len(demanda)
    resultado = np.zeros((filas, columnas))
    costos_copy = np.array(costos, dtype=float)

    while np.sum(oferta) > 0 and np.sum(demanda) > 0:
        i, j = np.unravel_index(np.argmin(costos_copy), costos_copy.shape)
        
        asignacion = min(oferta[i], demanda[j])
        resultado[i][j] = asignacion
        oferta[i] -= asignacion
        demanda[j] -= asignacion

        if oferta[i] == 0:
            costos_copy[i, :] = np.inf  

        if demanda[j] == 0:
            costos_copy[:, j] = np.inf  

    return {"asignaciones": resultado.tolist()}

@app.route('/')
def home():
    return jsonify({"message": "API de transporte funcionando"})

@app.route('/costo-minimo', methods=['POST'])
def calcular_costo_minimo():
    datos = request.json
    resultado = costo_minimo(datos["costos"], datos["oferta"], datos["demanda"])
    return jsonify(resultado)

@app.route('/esquina-noroeste', methods=['POST'])
def calcular_esquina_noroeste():
    datos = request.json
    resultado = esquina_noroeste(datos["oferta"], datos["demanda"])
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
