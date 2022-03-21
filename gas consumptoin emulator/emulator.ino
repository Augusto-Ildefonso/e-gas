#include <ArduinoUniqueID.h>

int sensorValue = 0;
int num;

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  UniqueID8dump(Serial);
}

void loop() {
  Serial.print("/");
  Serial.print(55555);
  delay(2000);
}
