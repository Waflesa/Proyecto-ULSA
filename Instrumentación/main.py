from flask import Flask, render_template, jsonify
import serial
import threading
import time

app = Flask(__name__)

sensor_data = {"ph": 0, "nivel": 0, "temp": 0}

# Conectar Arduino
try:
    arduino = serial.Serial('COM3', 9600, timeout=1)
    print("Arduino conectado en COM3")
except Exception as e:
    arduino = None
    print("No se pudo conectar Arduino:", e)
time.sleep(2)
# Leer datos en segundo plano
def read_arduino():
    global sensor_data
    while True:
        if arduino and arduino.in_waiting > 0:
            print("Datos recibidos de Arduino:", end=" ")
            line = arduino.readline().decode().strip()
            try:
                ph, nivel, temp = line.split(",")
                sensor_data["ph"] = float(ph)
                sensor_data["nivel"] = int(nivel)
                sensor_data["temp"] = float(temp)
            except:
                pass
        time.sleep(2)

if arduino:
    threading.Thread(target=read_arduino, daemon=True).start()

# Rutas Flask
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/contactos")
def contact():
    return render_template("contact.html")

@app.route("/data")
def data():
    return jsonify(sensor_data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
