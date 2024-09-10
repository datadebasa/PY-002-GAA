from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Menambahkan CORS untuk seluruh aplikasi
# Token API yang diharapkan
EXPECTED_TOKEN = "27981"

# Inisialisasi model
model = genai.GenerativeModel("gemini-1.5-flash")


# Rute untuk API generate content
@app.route("/generate", methods=["POST"])
def generate_content():
    data = request.get_json()
    prompt = data.get("prompt", "")
    token = data.get("token", "")
    token_gemini = data.get("token_gemini", "")

    # Memeriksa jika prompt kosong
    if not prompt:
        return jsonify({"error": "Prompt tidak boleh kosong"}), 400

    # Memeriksa jika token tidak sesuai
    if token != EXPECTED_TOKEN:
        return jsonify({"error": "Token tidak valid atau tidak sesuai"}), 403

    # Konfigurasi API Key dari Google Generative AI
    genai.configure(api_key=token_gemini)

    # Menghasilkan narasi dari prompt
    response = model.generate_content(prompt)
    narasi = response.text

    return jsonify({"narasi": narasi})


# # Rute untuk mendapatkan token
# @app.route("/get-token", methods=["GET"])
# def get_token():
#     # Mengambil token dari environment variable atau bisa juga dari sumber lain
#     token = EXPECTED_TOKEN  # Token hardcode yang digunakan
#     return jsonify({"token": token})


if __name__ == "__main__":
    app.run(debug=True)
