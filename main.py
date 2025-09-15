from flask import Flask, request, jsonify, render_template
import os
from groq import Groq
from funciones import bbdd, get_crypto_data, detectar_cripto, limpiar_respuesta, get_crypto_chart
from variables import groq_api_key

# Cliente Groq
client = Groq(api_key=groq_api_key)

app = Flask(__name__)

@app.get("/")
def serve_index():
    return render_template("index.html")

@app.get("/ping")
def ping():
    return {"ok": True, "message": "pong"}

@app.post("/qa")
def create_qa():
    data = request.get_json(silent=True) or {}
    pregunta = data.get("pregunta")

    if not pregunta:
        return jsonify({"error": "Falta el campo 'pregunta'"}), 400

    # Detectar cripto
    cripto = detectar_cripto(pregunta)

    # 🚨 Si no es una pregunta sobre criptos, respondemos directo sin llamar al LLM
    if not cripto:
        return jsonify({
            "id": None,
            "pregunta": pregunta,
            "respuesta": "⚠️ Solo hablo de criptomonedas. Pregunta sobre Bitcoin, Ethereum, u otros criptoactivos.",
            "cripto": None,
            "mercado": None,
            "grafico": {"fechas": [], "precios": []}
        }), 200

    # Llamar a Groq (prompt ajustado para Markdown)
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente experto en criptomonedas. Responde SIEMPRE en español, "
                    "excepto cuando la pregunta esté en otro idioma (entonces respondes en ese idioma).\n\n"

                    "⚠️ Solo hablas de criptomonedas. Si el usuario pregunta sobre cualquier otro tema que no sea de criptomonedas, "
                    "RESPONDE exclusivamente con el texto: '⚠️ Solo hablo de criptomonedas. Pregunta sobre Bitcoin, Ethereum, u otros criptoactivos.'\n\n"

                    "Lo que sí puedes hacer es responder a conceptos cripto (por ejemplo staking, blockchain, proof of work...).\n"
                    "Mantén un tono profesional, didáctico y claro, como si explicaras a alguien que está aprendiendo.\n"
                    "No generes respuestas de más de 400 palabras. Sé concreto.\n"
                    "Si no tienes información suficiente o no existe sobre esa criptomoneda, responde claramente: "
                    "'No dispongo de datos suficientes sobre esta criptomoneda.'\n"
                    "No inventes información. Si no conoces un detalle, indícalo en lugar de rellenar con suposiciones.\n\n"

                    "ESTILO DE RESPUESTA:\n"
                    "- Usa formato **Markdown válido**.\n"
                    "- Introducción breve en párrafo normal.\n"
                    "- Después: organiza por temas (HISTORIA, GOBERNANZA, PERSONAJES CLAVE, SEGURIDAD, DATOS RELEVANTES) "
                    "con títulos en **negrita y mayúsculas** (ej.: **HISTORIA**).\n"
                    "- Dentro de cada tema: listas con guiones (-).\n"
                    "- Palabras clave en **negrita** y términos en inglés en *cursiva*.\n"
                    "- Separa los apartados con DOBLE salto de línea.\n"
                    "- Cierra con un resumen final en lista de 4–6 bullets.\n\n"

                    "RESTRICCIONES:\n"
                    "- Nunca uses etiquetas HTML (<br>, <h1>, etc.) ni '###'.\n"
                    "- No inventes precios ni datos de mercado en tiempo real (vendrán de otra fuente).\n"
                    "- Usa comas como separador de miles (21,000,000).\n"
                )
            },
            {"role": "user", "content": pregunta}
        ],
        model="openai/gpt-oss-20b",
        stream=False
    )

    respuesta = limpiar_respuesta(completion.choices[0].message.content)

    # CoinGecko: mercado + gráfico (solo si detectamos cripto)
    mercado = None
    grafico = {"fechas": [], "precios": []}
    if cripto:
        mercado = get_crypto_data(cripto)
        grafico = get_crypto_chart(cripto, days=30)

    # Guardar en DB
    row = bbdd(pregunta, respuesta)

    # Respuesta JSON
    return jsonify({
        "id": row[0],
        "pregunta": row[1],
        "respuesta": row[2],
        "cripto": cripto,                # ej. "bitcoin"
        "mercado": mercado,              # puede traer {"error": "..."}
        "grafico": grafico               # siempre presente: {"fechas":[...], "precios":[...]}
    }), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
