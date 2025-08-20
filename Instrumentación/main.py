from flask import Flask, render_template, jsonify
import serial
import serial.tools.list_ports
import time
import threading

app = Flask(__name__)

# ------------------------------
# Detectar Arduino automáticamente
# ------------------------------
def encontrar_arduino():
    puertos = serial.tools.list_ports.comports()
    for puerto in puertos:
        if "Arduino" in puerto.description or "CH340" in puerto.description:
            return puerto.device
    return None

arduino_port = encontrar_arduino()
arduino = None

if arduino_port:
    try:
        arduino = serial.Serial(arduino_port, 9600, timeout=1)
        time.sleep(2)  # Esperar reinicio del Arduino
        print(f"Arduino conectado en {arduino_port}")
    except serial.SerialException as e:
        print(f"Error abriendo el puerto: {e}")
else:
    print("No se encontró Arduino conectado.")

# ------------------------------
# Variables de sensores
# ------------------------------
sensor_data = {
    "ph": None,
    "nivel": None,
    "temp": None
}

# ------------------------------
# Función para leer Arduino
# ------------------------------
def leer_arduino():
    global sensor_data
    while True:
        if arduino and arduino.is_open:
            try:
                linea = arduino.readline().decode('utf-8').strip()
                # Suponiendo que Arduino envía datos como: PH,Nivel,Temp
                # Ejemplo: 7.12,65,24.5
                if linea:
                    partes = linea.split(',')
                    if len(partes) == 3:
                        sensor_data['ph'] = float(partes[0])
                        sensor_data['nivel'] = float(partes[1])
                        sensor_data['temp'] = float(partes[2])
            except Exception as e:
                print(f"Error leyendo Arduino: {e}")
        time.sleep(1)  # Leer cada segundo

# Solo iniciar el thread si Arduino está disponible
if arduino:
    hilo = threading.Thread(target=leer_arduino, daemon=True)
    hilo.start()

# ------------------------------
# Rutas de Flask
# ------------------------------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/contactos")
def contact():
    return render_template("contact.html")

@app.route("/data")
def data():
    # Si no hay Arduino, usar datos simulados
    if sensor_data['ph'] is None:
        import random
        sensor_data['ph'] = round(6 + random.random() * 2, 2)
        sensor_data['nivel'] = round(50 + random.random() * 50)
        sensor_data['temp'] = round(20 + random.random() * 10, 1)
    return jsonify(sensor_data)

# ------------------------------
# Ejecutar Flask
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
