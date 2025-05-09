from flask import Flask, request, jsonify
from pysentimiento import create_analyzer

app = Flask(__name__)

analizador = create_analyzer(task="sentiment", lang="es")

@app.route("/analizar", methods=["POST"])
def analizar_sentimiento():
    datos = request.get_json()


    if not datos or "id" not in datos or "texto" not in datos:
        return jsonify({"error": "Se requiere 'id' y 'texto'"}), 400

    id_feedback = datos["id"]
    texto = datos["texto"]

    resultado = analizador.predict(texto)

    respuesta = {
        "id": id_feedback,
        "resultado": resultado.output,       # positivo / negativo / neutro
        "probabilidades": resultado.probas   # {'POS': 0.75, 'NEG': 0.10, 'NEU': 0.15}
    }

    return jsonify(respuesta), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
