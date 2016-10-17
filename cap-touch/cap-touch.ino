/*********************************************************
  This is a library for the MPR121 12-channel Capacitive touch sensor

  Designed specifically to work with the MPR121 Breakout in the Adafruit shop
  ----> https://www.adafruit.com/products/

  These sensors use I2C communicate, at least 2 pins are required
  to interface

  Adafruit invests time and resources providing this open source code,
  please support Adafruit and open-source hardware by purchasing
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.
  BSD license, all text above must be included in any redistribution
**********************************************************/

#include <Wire.h>
#include "Adafruit_MPR121.h"

// You can have up to 4 on one i2c bus but one is enough for testing!
Adafruit_MPR121 cap = Adafruit_MPR121();

// Keeps track of the last pins touched
// so we know when buttons are 'released'
uint16_t lasttouched = 0;
uint16_t currtouched = 0;
unsigned long last_turned = 0;

int last_pot;
int thres = 3;
int static_on = 0;

void sendOff() {
  for (uint8_t i = 0; i < 12; i++) {
    Serial.println(char(i + 97));
  }
  Serial.println('#');

}


void setup() {
  while (!Serial);        // needed to keep leonardo/micro from starting too fast!

  Serial.begin(115200);
  //Serial.println("Adafruit MPR121 Capacitive Touch sensor test");

  // Default address is 0x5A, if tied to 3.3V its 0x5B
  // If tied to SDA its 0x5C and if SCL then 0x5D
  if (!cap.begin(0x5A)) {
    Serial.println("MPR121 not found, check wiring?");
    while (1);
  }
  sendOff();
  last_pot = analogRead(A0);

  //Serial.println("MPR121 found!");
}


void loop() {

  //read pot
  int pot_val = analogRead(A0);
  if (abs(pot_val - last_pot) > thres) {
    last_pot = pot_val;
    Serial.print("@");
    int val = map(pot_val, 0, 1023, 0, 100);
    Serial.println(val);
    last_turned = millis();
    // Send static on
    if (!static_on) {
      static_on = 1;
      Serial.println('*');

    }
  }

  if ( millis() - last_turned > 1000 && static_on) {
    Serial.println('#');
    static_on = 0;
  }

  // Get the currently touched pads
  currtouched = cap.touched();

  for (uint8_t i = 0; i < 12; i++) {
    // it if *is* touched and *wasnt* touched before, alert!
    if ((currtouched & _BV(i)) && !(lasttouched & _BV(i)) ) {
      Serial.println(char(i + 65));
    }
    // if it *was* touched and now *isnt*, alert!
    if (!(currtouched & _BV(i)) && (lasttouched & _BV(i)) ) {
      Serial.println(char(i + 97));
    }
  }

  // reset our state
  lasttouched = currtouched;

  // comment out this line for detailed data from the sensor!
  delay(10);
}
