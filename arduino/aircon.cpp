#include <IRremoteESP8266.h>
#include <IRsend.h>
#include <ir_Daikin.h>
#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "manpookungZ";
const char* password = "lefq2341";
const char* mqtt_server = "192.168.6.34";
const int mqttPort = 1883;


WiFiClient espClient;
PubSubClient client(espClient);

void callback(char* topic, byte* payload, unsigned int length);
void reconnect();
void setup_wifi();

int ready = 0;
int temp;
String dataString;
const uint16_t irLEDPin = 2; 
IRDaikinESP ac(irLEDPin);    

void setup() {
  ac.begin();
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqttPort);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  if (ready == 1) {
    if (dataString.equals("on")) {
      ac.on();
      ac.setFan(2);
      ac.setMode(kDaikinCool);

      ac.setSwingVertical(true);
      ac.setSwingHorizontal(true);
      ac.disableOffTimer();

      Serial.println(ac.toString());
      ac.send();
    } else if (dataString.equals("off")) {
      ac.off();
    } else {
      temp = dataString.toInt();
      ac.setTemp(temp);
    }
    ac.send();
    Serial.print("Command : ");
    Serial.print(dataString);
    Serial.print(", Temperature : ");
    Serial.println(temp);
    dataString = "";
    ready = 0;
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  // off on up down
  char payloadChar[120];
  int i = 0;
  for (i = 0; i < length; i++) {
    payloadChar[i] = (char)payload[i];
  }
  payloadChar[i] = '\0';
  Serial.println(payloadChar);
  dataString = String(payloadChar);
  ready = 1;
}

void setup_wifi() {

  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  WiFi.setAutoReconnect(true);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}


void reconnect() {
  while (!client.connected()) {
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("mqtt connected");
      client.subscribe("condi");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}