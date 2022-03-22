#include <ArduinoUniqueID.h>

int sensorValue = 0;
int num, i=0;

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
}

void loop() {
  UniqueID8dump(Serial);
  Serial.print(10.50);
  delay(5000);

}
