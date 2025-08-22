from flask import Flask, render_template, jsonify
import serial
import threading
import time

app = Flask(__name__)

sensor_data = {"ph": 0, "nivel": 0, "temp": 0}

# Conectar Arduino
try:
    arduino = serial.Serial('COM6', 9600, timeout=1)
    print("Arduino conectado en COM6")
    time.sleep(2)
except Exception as e:
    arduino = None
    print("No se pudo conectar Arduino:", e)

# Leer datos en segundo plano
def read_arduino():
    global sensor_data
    while True:
        if arduino and arduino.in_waiting > 0:
            try:
                line = arduino.readline().decode("utf-8").strip()
                if line:
                    print("Línea recibida:", line)
                    values = line.split(",")
                    if len(values) == 3:
                        ph, nivel, temp = values
                        sensor_data["ph"] = float(ph)
                        sensor_data["nivel"] = int(nivel)
                        sensor_data["temp"] = float(temp)
                        print("Datos actualizados:", sensor_data)
            except Exception as e:
                print("Error procesando línea:", e)

        time.sleep(0.1)

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
    app.run(debug=True, port=5000, use_reloader=False)