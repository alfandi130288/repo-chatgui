from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
import logging
from dotenv import load_dotenv

# Load environment variables dari file .env
load_dotenv()

# Konfigurasi logging ke console
logging.basicConfig(level=logging.ERROR)

app = Flask(__name__)
# Mengatur kunci API OpenAI
  # Menggunakan nilai dari variabel lingkungan
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)

if not client.api_key:
    raise EnvironmentError("API_KEY tidak ditemukan. Pastikan variabel lingkungan diatur dengan benar.")

# Fungsi untuk mendapatkan respons dari OpenAI
def get_completion(prompt, model="gpt-4o-mini"):
    try:
        messages = [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(model=model,
        messages=messages,
        temperature=0)
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Terjadi kesalahan saat memanggil API OpenAI: {e}")
        return "Maaf, terjadi kesalahan pada server. Silakan coba lagi nanti."

# Halaman utama
@app.route("/")
def home():    
    return render_template("index.html")

# Endpoint untuk mendapatkan respons dari chatbot
@app.route("/get", methods=["POST"])
def get_bot_response():
    userText = request.form.get('message', '').strip()
    if not userText:
        return jsonify({'response': 'Input tidak valid. Silakan masukkan pesan yang jelas.'})
    response = get_completion(userText)
    return jsonify({'response': response})

# Menjalankan aplikasi Flask
if __name__ == "__main__":
    app.run(debug=False)  # Ganti debug=False di produksi