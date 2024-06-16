#include "DHT.h"
#define DHTPIN 2 
#define DHTPIN2 4    
#define DHTTYPE DHT22   
DHT dht(DHTPIN, DHTTYPE);
DHT dht2(DHTPIN2, DHTTYPE);
int fan1=9;
int fan2=10;
String str;

void setup() {
  Serial.begin(9600);
  dht2.begin();
  dht.begin();
  pinMode(fan1,OUTPUT);
  pinMode(fan2,OUTPUT);
}

void loop() {
  delay(2000);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  float hif = dht.computeHeatIndex(f, h);
  float hic = dht.computeHeatIndex(t, h, false);
  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  
  float h2 = dht2.readHumidity();
  float t2 = dht2.readTemperature();
  float f2 = dht2.readTemperature(true);
  if (isnan(h2) || isnan(t2) || isnan(f2)) {
    Serial.println(F("Failed to read from DHT2 sensor!"));
    return;
  } 
  float hif2 = dht2.computeHeatIndex(f2, h2);
  float hic2 = dht2.computeHeatIndex(t2, h2, false);
  Serial.print(F("Humidity2: "));
  Serial.print(h2);
  Serial.print(F("%  Temperature2: "));
  Serial.print(t2);
  Serial.println(F("°C "));

      if (Serial.available()) {
    // 讀取傳入的字串直到"\n"結尾
    str = Serial.readStringUntil('\n');
    if (str == "Servo_ON") {           
      digitalWrite(fan1,HIGH);
      digitalWrite(fan2,HIGH);
      delay(3000);
    } else if (str == "Servo_OFF") {
        digitalWrite(fan1,LOW);
        digitalWrite(fan2,LOW);
        delay(3000);
    }
  }
}
