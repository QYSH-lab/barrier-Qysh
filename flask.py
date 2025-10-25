from flask import Flask, request, jsonify
import pandas as pd
import requests

app = Flask(_name_)

# === Настройки ===
EXCEL_FILE = r"C:\Users\105 LAB\Desktop\ \New Лист Microsoft Excel (1).xlsx"
CLIENT_ARDUINO_URL = "http://172.20.10.2:5001/command"  # ПК2
PORT = 5000

# === Загрузка номеров из Excel ===
def load_numbers():
    df = pd.read_excel(EXCEL_FILE)
    return set(df.iloc[:, 0].astype(str).str.strip().str.upper())

valid_numbers = load_numbers()

@app.route('/', methods=['GET'])
def index():
    return "<h1>✅ Сервер работает на ПК1</h1>", 200

# 📩 ПК3 шлёт сюда распознанный номер
@app.route('/plate', methods=['POST'])
def receive_plate():
    data = request.get_json()
    plate = data.get('plate', '').strip().upper()
    print(f"[SERVER] Получен номер: {plate}")
    

    if plate in valid_numbers:
        print(f"[SERVER] ✅ Номер {plate} найден, отправляю ПК2 → OPEN")
        try:
            requests.post(CLIENT_ARDUINO_URL, json={'access': True})
        except Exception as e:
            print(f"[SERVER] ❌ Ошибка отправки на ПК2: {e}")
        return jsonify({'status': 'allowed'})
    else:
        print(f"[SERVER] ❌ Номер {plate} не найден")
        try:
            requests.post(CLIENT_ARDUINO_URL, json={'access': False})
        except Exception as e:
            print(f"[SERVER] ❌ Ошибка отправки на ПК2: {e}")
        return jsonify({'status': 'denied'})

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=PORT)