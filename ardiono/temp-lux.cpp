#include <Wire.h>
#include <Adafruit_AHTX0.h> 
#include <BH1750.h>
#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "manpookungZ";
const char* password = "lefq2341";
const char* mqtt_server = "192.168.6.34";

WiFiClient espClient;
PubSubClient client(espClient);
Adafruit_AHTX0 aht;
BH1750 lightMeter;

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("Starting setup...");
  Wire.begin();

  if (!aht.begin()) {
    Serial.println("Failed to find AHT20 sensor!");
    while (1); 
  }
  Serial.println("AHT20 sensor initialized.");

  if (!lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE)) {
    Serial.println("Error initializing GY-302 sensor (BH1750)");
    while (1);  
  }
  Serial.println("GY-302 sensor initialized.");
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);  
  Serial.print(temp.temperature);
  float lux = lightMeter.readLightLevel();
  Serial.print(lux);
  char msg[100];
  snprintf(msg, sizeof(msg), "{%.2f}", temp.temperature);
  client.publish("ShowTemp", msg);
  snprintf(msg, sizeof(msg), "{%.2f}", lux);
  client.publish("Lux", msg);
  delay(30000);
}
