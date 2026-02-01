import time
from flask import Flask
from src.idempotency import idempotent_hardcore

app = Flask(__name__)

@app.route('/process-payment', methods=['POST'])
@idempotent_hardcore
def process_payment():
    """
    Simula um processamento pesado.
    """
    # 💤 Simula delay de 2 segundos (Processando cartão...)
    # Isso abre uma janela enorme para Race Condition
    time.sleep(2)
    
    return {"status": "authorized", "receipt": "12345-ABC"}, 200

if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True)
