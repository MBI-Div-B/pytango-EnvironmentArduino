#include <Wire.h>
#include <Adafruit_AM2315.h>

/***************************************************
 * Driver to read out the AM2315 using the Adafruit_AM2315 lib and
 * send data to a RasPi via serial interface
 * the program is waiting for a character from the RasPi, 
 * getting a 't' causes sending back the temperature in a String
 * getting a 'h' causes sending back the humidity in a String
 * 
 * Program bases on the example program "am2315test" (view text below)
 * 
  This is an example for the AM2315 Humidity + Temp sensor

  Designed specifically to work with the Adafruit BMP085 Breakout 
  ----> https://www.adafruit.com/products/1293

  These displays use I2C to communicate, 2 pins are required to  
  interface
  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/

// Connect RED of the AM2315 sensor to 5.0V
// Connect BLACK to Ground
// Connect WHITE to i2c clock - on '168/'328 Arduino Uno/Duemilanove/etc thats Analog 5
// Connect YELLOW to i2c data - on '168/'328 Arduino Uno/Duemilanove/etc thats Analog 4

Adafruit_AM2315 am2315;
//float t,  //temperature variable to send
//      h;  //humidity variable to send

#define NUM_AM2315          1
#define PERIOD_DEFAULT_ms  5000

char c;
float temp_sums[NUM_AM2315];
float humid_sums[NUM_AM2315];

float temp_mean[NUM_AM2315];
float humid_mean[NUM_AM2315];
long count, rate;
long nextUpdate;
long period = PERIOD_DEFAULT_ms;

void setup() {
  Serial.begin(115200);
  //Serial.println("new AM2315 module"); //new sensor module AM2315 connected; 

  if (! am2315.begin()) {
     Serial.println("Sensor not found, check wiring!");
     while (1);
  }

  for (int i = 0; i < NUM_AM2315; i++) {
    temp_sums[i] = 0;    // by default, do not monitor
    humid_sums[i] = 0;
    temp_mean[i] = 0;
    humid_mean[i] = 0;
  }
  count = 0;
  rate = 0;
  nextUpdate = millis() + period;
  
}

void loop() {
  signalGathering();
  //wait for a serial msg
  if (Serial.available() > 0) {    
    
   c = Serial.read(); //get incoming charakter
      //check the charakter
      switch (c) {
          case 't':                                     //in case of a 't'
            Serial.println(temp_mean[0],3);   //send back the temperature
            
            break;
          case 'h':                                     //in case of a 'h'
            Serial.println(humid_mean[0],3);   //send back the humidity
            
            break;
           case 'r':                                     //in case of a 'h'
            Serial.println(rate);   //send back the humidity
            
            break;
            
          default:
          
          break;
        }
  }
  

}

void signalGathering() {
  // periodically, average the watched ADC channels
  if (millis() >= nextUpdate) {
    // Serial.print("count"); Serial.print("  "); Serial.println(count);
    for (int i = 0; i < NUM_AM2315; i++) {
      if (count > 0) {    // if monitoring
        // Serial.print(i); Serial.print("  "); Serial.println(float(ai_sums[i]));
        temp_mean[i] = float(temp_sums[i]) / count;
        humid_mean[i] = float(humid_sums[i]) / count;
        temp_sums[i] = 0;
        humid_sums[i] = 0;
      }
    }
    nextUpdate = millis() + period;
    rate = 1000 * count / period;    // loops per second
    count = 0;
  }
  // this is where the ADC channels are read
  for (int i = 0; i < NUM_AM2315; i++) {
    
      temp_sums[i] += am2315.readTemperature();
      delay(50);
      humid_sums[i] += am2315.readHumidity();
      delay(50);
  }
  count++;
}





