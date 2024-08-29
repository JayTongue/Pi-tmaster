#include <WiFi.h>
#include <GyverOLED.h>
#include <math.h>
#include "max6675.h"

const char* ssid = "CHANGE_SSID";
const char* password = "CHANGE_PW";

// Define pins for thermocouples
int thermoSO_1 = 15;
int thermoCS_1 = 14;
int thermoSCK_1 = 13;
int thermoSO_2 = 16;
int thermoCS_2 = 17;
int thermoSCK_2 = 18;

IPAddress local_IP(192, 168, 1, 1);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

// Initialize MAX6675 instances
MAX6675 thermocouple_1(thermoSCK_1, thermoCS_1, thermoSO_1);
MAX6675 thermocouple_2(thermoSCK_2, thermoCS_2, thermoSO_2);

// Initialize OLED
GyverOLED<SSH1106_128x64> oled;

// Web server on port 80
WiFiServer server(80); 


void setup() {
  delay(500);

  oled.init();
  oled.clear();
  oled.setCursorXY(20, 17);
  oled.print("Meat:");
  oled.setCursorXY(84, 17);
  oled.print("Fire:");
  oled.update();

  Serial.begin(115200);

  WiFi.softAPConfig(local_IP, gateway, subnet);
  WiFi.softAP(ssid, password);
  Serial.printf("AP IP address: %s\n", WiFi.softAPIP().toString().c_str());
  server.begin();

}


String formatTemperature(float temp) {
    if (isinf(temp)) {
        return "\"NaN\"";
    } else {
        return String(temp, 1);
    }
}

void loop() {
  float temperature_1 = thermocouple_1.readFahrenheit(); // floats can be adjusted for calibration
  float rounded_temp_1 = round(temperature_1 * 10) / 10.0; // Round to one decimal place
  float temperature_2 = thermocouple_2.readFahrenheit();
  float rounded_temp_2 = round(temperature_2 * 10) / 10.0;

  String fireTemp = formatTemperature(rounded_temp_1);
  String meatTemp = formatTemperature(rounded_temp_2);
  
  oled.setCursorXY(90, 35);
  oled.print(rounded_temp_1, 1);
  oled.setCursorXY(23, 35);
  oled.print(rounded_temp_2, 1);
  oled.update();

  WiFiClient client = server.available();
  if (client) {
    Serial.println("New Client.");
    String currentLine = "";
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        if (c == '\n') {
          if (currentLine.length() == 0) {
              String response = String("{\"fire\": ") + fireTemp + ", \"meat\": " + meatTemp + "}";
              client.println("HTTP/1.1 200 OK");
              client.println("Content-Type: application/json");
              client.println("Connection: close");
              client.println("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
              client.println("Pragma: no-cache");
              client.println("Access-Control-Allow-Origin: *");
              client.println("Content-Security-Policy: default-src 'self'");
              client.println("X-Content-Type-Options: nosniff");
              client.print("Content-Length: ");
              client.println(response.length());
              client.println();
              client.print(response);
              client.flush();
              client.stop();

            break;
          } else {
            currentLine = "";
          }
        } else if (c != '\r') {
          currentLine += c;
        }
      }
    }
    client.stop();
    Serial.println("Client Disconnected.");
  }


  delay(2000);
}
