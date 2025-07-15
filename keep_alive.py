from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "✅ Bot is alive!"

def keep_alive():
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
