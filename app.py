# Final app.py 
from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
import os
import logging

# Konfigurasi logging ke console
logging.basicConfig(level=logging.ERROR)

# logging.basicConfig(level=logging.ERROR, filename='error.log', format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Memuat variabel dari file .env
load_dotenv()

# Mendapatkan kunci API dari variabel lingkungan
SECRET_KEY = os.getenv("OPENAI_API_KEY")
logging.debug(f"Nilai OPENAI_API_KEY: {SECRET_KEY}")
if not SECRET_KEY:
    raise EnvironmentError("API_KEY tidak ditemukan. Pastikan variabel lingkungan diatur dengan benar.")

openai.api_key = SECRET_KEY

# Fungsi untuk mendapatkan respons dari OpenAI
def get_completion(prompt, model="gpt-4o-mini"):
    try:
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message["content"]
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
    app.run()  # Ganti debug=False di produksi
