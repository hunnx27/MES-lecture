// Arduino 센서 시뮬레이터
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// WiFi 설정
const char* ssid = "your_wifi_ssid";
const char* password = "your_wifi_password";

// MQTT 설정
const char* mqtt_server = "192.168.1.100";  // MES 서버 IP
const int mqtt_port = 1883;
const char* mqtt_topic = "factory/sensor/data";

WiFiClient espClient;
PubSubClient client(espClient);

// 센서 핀 설정
#define TEMP_SENSOR A0      // 온도 센서
#define PRESSURE_SENSOR A1  // 압력 센서
#define VIBRATION_SENSOR A2 // 진동 센서
#define SPEED_SENSOR 2      // 속도 센서 (디지털)

void setup() {
  Serial.begin(115200);
  
  // WiFi 연결
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi 연결됨");
  
  // MQTT 연결
  client.setServer(mqtt_server, mqtt_port);
  reconnect();
  
  // 센서 핀 설정
  pinMode(TEMP_SENSOR, INPUT);
  pinMode(PRESSURE_SENSOR, INPUT);
  pinMode(VIBRATION_SENSOR, INPUT);
  pinMode(SPEED_SENSOR, INPUT);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  // 센서 데이터 읽기
  float temperature = readTemperature();
  float pressure = readPressure();
  float vibration = readVibration();
  int speed = readSpeed();
  
  // JSON 생성
  StaticJsonDocument<200> doc;
  doc["equipment_id"] = "EQ-001";
  doc["timestamp"] = millis();
  doc["temperature"] = temperature;
  doc["pressure"] = pressure;
  doc["vibration"] = vibration;
  doc["speed"] = speed;
  
  char jsonBuffer[200];
  serializeJson(doc, jsonBuffer);
  
  // MQTT 전송
  if (client.publish(mqtt_topic, jsonBuffer)) {
    Serial.println("📊 데이터 전송: " + String(jsonBuffer));
  } else {
    Serial.println("❌ 전송 실패");
  }
  
  delay(1000);  // 1초마다 전송
}

// 온도 센서 읽기 (예: LM35)
float readTemperature() {
  int rawValue = analogRead(TEMP_SENSOR);
  float voltage = rawValue * (5.0 / 1023.0);
  float temperature = voltage * 100.0;  // LM35: 10mV/°C
  return temperature;
}

// 압력 센서 읽기
float readPressure() {
  int rawValue = analogRead(PRESSURE_SENSOR);
  // 센서 사양에 맞게 변환 (예: 0-1023 → 0-100 kPa)
  float pressure = map(rawValue, 0, 1023, 95, 105);
  return pressure;
}

// 진동 센서 읽기
float readVibration() {
  int rawValue = analogRead(VIBRATION_SENSOR);
  float vibration = rawValue * (3.0 / 1023.0);  // 0-3V
  return vibration;
}

// 속도 센서 읽기 (홀센서/엔코더)
int readSpeed() {
  // 실제로는 인터럽트로 RPM 계산
  // 여기서는 시뮬레이션
  return random(950, 1000);
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("MQTT 연결 중...");
    if (client.connect("ArduinoClient")) {
      Serial.println("✅ 연결됨");
    } else {
      Serial.print("❌ 실패, rc=");
      Serial.println(client.state());
      delay(5000);
    }
  }
}