from flask import Flask, request, jsonify
import time
import serial

# === Настройки Arduino ===
# Укажи свой COM-порт (проверь в Arduino IDE → Инструменты → Порт)
COM_PORT = 'COM4'
BAUD_RATE = 9600

# === Подключение к Arduino ===
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"[ARDUINO SERVER] ✅ Подключено к Arduino на {COM_PORT}")
except Exception as e:
    ser = None
    print(f"[ARDUINO SERVER] ⚠️ Не удалось подключиться к Arduino: {e}")

# === Flask сервер ===
app = Flask(_name_)

@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    access = data.get('access', False)
    print(f"[ARDUINO SERVER] Получена команда от ПК1: {access}")

    if ser:
        if access:
            print("[ARDUINO SERVER] ✅ Открываю шлагбаум (SG-5010)")
            ser.write(b'OPEN\n')   # Arduino поймает команду OPEN
        else:
            print("[ARDUINO SERVER] ⛔ Доступ запрещён")
            ser.write(b'DENY\n')   # Можно игнорировать или оставить для логики
    else:
        print("[ARDUINO SERVER] ⚠️ Arduino не подключена — команда не отправлена")

    return jsonify({'status': 'ok'})

if _name_ == '_main_':
    print("[ARDUINO SERVER] 🌐 Запуск Flask на ПК2, порт 5001")
    app.run(host='0.0.0.0', port=5001)