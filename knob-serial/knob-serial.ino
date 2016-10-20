
// Keeps track of the last pins touched
// so we know when buttons are 'released'
unsigned long last_turned = 0;

int last_pot;
int thres = 3;
int static_on = 0;

void sendOff() {
  Serial.println('#');

}


void setup() {
  while (!Serial);        // needed to keep leonardo/micro from starting too fast!

  Serial.begin(115200);
  //Serial.println("Adafruit MPR121 Capacitive Touch sensor test");

  // Default address is 0x5A, if tied to 3.3V its 0x5B
  // If tied to SDA its 0x5C and if SCL then 0x5D
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

  if ( millis() - last_turned > 500 && static_on) {
    Serial.println('#');
    static_on = 0;
  }

  // comment out this line for detailed data from the sensor!
  delay(10);
}
