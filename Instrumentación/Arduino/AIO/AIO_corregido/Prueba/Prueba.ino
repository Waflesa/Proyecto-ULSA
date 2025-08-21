// Pines de los sensores
#define PIN_PH A0
#define PIN_NIVEL A1
#define PIN_TEMP A2

void setup() {
  Serial.begin(9600); // Inicializa el puerto serial
}

void loop() {
  // Leer valores de sensores (simulados para prueba)
  float ph = analogRead(PIN_PH) * (15.0 / 1023.0);        // Escala pH 0-14
  int nivel = analogRead(PIN_NIVEL);                      // Nivel 0-1023
  float temp = analogRead(PIN_TEMP) * (70.0 / 1023.0);    // Temperatura 0-50°C

  // Enviar datos por Serial en formato CSV: ph,nivel,temp
  Serial.print(ph, 2);
  Serial.print(",");
  Serial.print(nivel);
  Serial.print(",");
  Serial.println(temp, 1);

  delay(1000); // Esperar 1 segundo antes de la siguiente lectura
}
