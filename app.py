from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from markupsafe import escape
from datetime import datetime

app = Flask(__name__)

# Inisialisasi chatbot
chatbot = ChatBot("AsistenPertamina")

# Latih dengan percakapan Bahasa Indonesia
trainer = ListTrainer(chatbot)
percakapan_indonesia = [
    "Halo", "Hai!",
    "Apa kabar?", "Saya baik, terima kasih.",
    "Apa itu BBM?", "BBM adalah Bahan Bakar Minyak, seperti Pertalite dan Pertamax.",
    "Apa itu LPG?", "LPG adalah gas untuk memasak, seperti Bright Gas atau gas 3kg.",
    "Siapa kamu?", "Saya asisten virtual Pertamina.",
    "Apa itu Pertalite?", "Pertalite adalah jenis BBM dengan RON 90 dari Pertamina.",
    "Bagaimana menghubungi Pertamina?", "Silakan hubungi 135 atau email cs@pertamina.co.id.",
    "Apa layanan Pertamina?", "Kami menyediakan BBM, LPG, pelumas, dan energi untuk industri."
]

trainer.train(percakapan_indonesia)

# Tambahkan percakapan Bahasa Inggris
percakapan_english = [
    "Hello", "Hi there!",
    "How are you?", "I'm good, thank you.",
    "What is BBM?", "BBM means fuel like Pertalite or Pertamax.",
    "What is LPG?", "LPG is cooking gas, such as Bright Gas or 3kg gas.",
    "Who are you?", "I'm Pertamina's virtual assistant.",
    "How to contact Pertamina?", "You can call 135 or email cs@pertamina.co.id.",
    "What services do you provide?", "We provide fuel, LPG, lubricants, and industrial energy."
]

trainer.train(percakapan_english)

# Halaman-halaman web
@app.route('/index')
def index():
    return render_template('index.html', title='Beranda')

@app.route('/about')
def about():
    return render_template('about.html', title='Tentang Kami')

@app.route('/services')
def services():
    return render_template('services.html', title='Layanan')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Kontak')

@app.route('/chatbot')
def chatbot_page():
    current_time = datetime.now().strftime("%H:%M")
    return render_template('chatbot.html', title='Chatbot', current_time=current_time)

# Endpoint untuk respon chatbot
@app.route('/get')
def dapatkan_respon():
    pesan_user = request.args.get('msg', '')
    lang = request.args.get('lang', 'id')  # Default bahasa Indonesia
    user_msg = escape(pesan_user).lower()

    if lang == 'en':
        # Bahasa Inggris
        if "hello" in user_msg or "hi" in user_msg:
            reply = "Hello! How can I assist you today?"
        elif "fuel" in user_msg or "pertalite" in user_msg or "pertamax" in user_msg:
            reply = "We provide various fuels such as Pertalite, Pertamax, and Dexlite."
        elif "gas" in user_msg or "lpg" in user_msg:
            reply = "We provide LPG in 3kg, 5.5kg, and 12kg packages."
        elif "contact" in user_msg:
            reply = "Please contact us at 135 or email cs@pertamina.co.id."
        elif "pertamina" in user_msg:
            reply = "Pertamina is Indonesia's state-owned energy company."
        else:
            reply = "Sorry, I didn’t understand that. Please ask something else."
    else:
        # Bahasa Indonesia
        if "halo" in user_msg or "hai" in user_msg:
            reply = "Hai!"
        elif "apa kabar" in user_msg or "bagaimana kabarmu" in user_msg:
            reply = "Saya baik, terima kasih sudah bertanya!"
        elif "bbm" in user_msg or "pertalite" in user_msg or "pertamax" in user_msg:
            reply = "Kami menyediakan berbagai jenis BBM seperti Pertalite, Pertamax, dan Dexlite."
        elif "lpg" in user_msg or "gas" in user_msg:
            reply = "Kami menyediakan LPG 3kg, Bright Gas 5.5kg & 12kg."
        elif "tentang" in user_msg or "pertamina" in user_msg:
            reply = "Pertamina adalah BUMN energi yang melayani kebutuhan energi nasional sejak 1957."
        elif "kontak" in user_msg or "hubungi" in user_msg:
            reply = "Silakan hubungi kami di 135 atau email cs@pertamina.co.id."
        else:
            # Pesan default jika tidak dikenali
            reply = "Maaf, saya belum memahami pertanyaan Anda. Silakan coba ajukan dengan kata lain ya."

    return jsonify({"reply": reply})


if __name__ == '__main__':
    app.run(debug=True)
