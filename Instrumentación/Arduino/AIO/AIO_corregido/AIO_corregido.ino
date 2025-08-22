#include <DHT.h> // Librería para el sensor DHT

// --- Sensor de Temperatura y Humedad ---
#define DHTTYPE DHT11
#define DHTPIN 9       // Pin digital para el DHT11 en Arduino Uno
DHT dht(DHTPIN, DHTTYPE);

// --- Sensor de Nivel de Agua ---
#define alimentacionSensor 12
#define lectura A1     // Pin analógico para el sensor de nivel

int nivelLiquido = 0;
int limiteInferior = 47;
int limiteSuperior = 130;

byte ledRojo     = 11;
byte ledAmarillo = 10;
byte ledVerde    = 8;

// --- Sensor de pH ---
#define LECTURA_PH A0
int buffer_arr[10];
long avgval;
float calibration_value = 21.25; // Ajustar según tu calibración en pH7

void setup() {
  Serial.begin(9600); 
  Serial.println("Inicializando sistemas...");

  // Configuración DHT11
  dht.begin();

  // Configuración sensor de nivel
  pinMode(alimentacionSensor, OUTPUT);
  digitalWrite(alimentacionSensor, LOW);
  pinMode(ledRojo, OUTPUT);
  pinMode(ledAmarillo, OUTPUT);
  pinMode(ledVerde, OUTPUT);

  Serial.println("Bienvenido a Medidor pH");
  delay(2000);
}

void loop() {
  // --- Nivel de agua ---
  int nivel = leerSensorNivel();
  if (nivel <= limiteInferior) {
    digitalWrite(ledRojo, HIGH); 
    digitalWrite(ledAmarillo, LOW); 
    digitalWrite(ledVerde, LOW);
  } else if (nivel > limiteInferior && nivel <= limiteSuperior) {
    digitalWrite(ledRojo, LOW); 
    digitalWrite(ledAmarillo, HIGH); 
    digitalWrite(ledVerde, LOW);
  } else {
    digitalWrite(ledRojo, LOW); 
    digitalWrite(ledAmarillo, LOW); 
    digitalWrite(ledVerde, HIGH);
  }

  Serial.print("Valor Nivel: "); Serial.println(nivel);

  // --- Sensor de pH ---
  for (int i = 0; i < 10; i++) {
    buffer_arr[i] = analogRead(LECTURA_PH);
    delay(10);
  }
  avgval = 0;
  for (int i = 0; i < 10; i++) avgval += buffer_arr[i];
  avgval /= 10;

  float volt = avgval * 5.0 / 1023;
  float ph_act = 2+(-5.70 * volt + calibration_value);

  Serial.print("pH Voltaje: "); Serial.print(volt, 3);
  Serial.print(" V  |  pH: "); Serial.println(ph_act, 2);

  // --- Sensor DHT11 ---
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("ERROR EN EL SENSOR DHT11");
  } else {
    Serial.print("Humedad: "); Serial.print(humidity);
    Serial.print("%  |  Temperatura: "); Serial.print(temperature);
    Serial.println(" C");
  }

  // --- Envío a Flask ---
  Serial.print(ph_act, 2);   // pH
  Serial.print(",");
  Serial.print(nivel);       // Nivel
  Serial.print(",");
  Serial.println(temperature); // Temperatura

  delay(1000);
}

// --- Función para leer sensor de nivel ---
int leerSensorNivel() {
  digitalWrite(alimentacionSensor, HIGH);
  delay(50);
  nivelLiquido = analogRead(lectura);
  digitalWrite(alimentacionSensor, LOW);
  return nivelLiquido;
}
