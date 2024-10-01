#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "manpookungZ";
const char* password = "lefq2341";
const char* mqtt_server = "192.168.6.34";
const int mqttPort = 1883;               

const int ledPin = 2;

WiFiClient espClient;
PubSubClient client(espClient);

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
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  Serial.println(message);
  
  
  if (message == "on") {
    digitalWrite(ledPin, HIGH); 
    Serial.println("LED is ON");
  } else if (message == "off") {
    digitalWrite(ledPin, LOW); 
    Serial.println("LED is OFF");
  } else {
    int value = message.toInt();
    if (value >= 3 && value <= 99) { 
      int pwmValue = map(value, 3, 99, 1, 255); 
      analogWrite(ledPin, pwmValue); 
      Serial.print("Setting LED brightness to: ");
      Serial.println(pwmValue);
    } else {
      Serial.println("Received an unknown command or out of range.");
    }
  }

}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
      client.subscribe("light");  //topic
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(9600);
  Serial.println("Setup starting...");
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW); 

  setup_wifi();
  client.setServer(mqtt_server, mqttPort);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect(); 
  }
  client.loop(); 
}
