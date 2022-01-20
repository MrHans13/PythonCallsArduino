#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <stdio.h>
#include <string.h>

#define SSID1 "UPC2CE7432"
#define SSID2 "HUAWEI P smart+ 2019"
#define PWORD1 "5vuvNk2dbwbc"
#define PWORD2 "da11d05b814b"
#define BUTTONDELAY 200

ESP8266WebServer server(80);

const char* ssid = SSID2;
const char* password = PWORD2;

int selectPins[3] = {5, 4, 0};                  //pin 12 = S1, 13 = S2, 15 = S3
int relaisPins[3] = {12, 13, 15};
int relState[3] = {0, 0, 0};

int inputWerte[8] = {0, 0, 0, 0, 0, 0, 0, 0};
int buttonState[4] = {0, 0, 0, 0};
int buttonStateOld[4] = {0, 0, 0, 0};

int counter = 0;
int bits[3] = {0, 0, 0};

int ledPin = 16;
int ledState = 0;
int serialDataCounter = 0;
int wifiDataCounter = 0;

void setup() {
  Serial.begin(115200);
  PinModes();
  for (int i = 0; i < 3; i++) {
    relFunc(i, 1);
  }
  wifiFunc();
}
void loop() {
  server.handleClient();
  IC_4051();
  ButtonFunc();
  relaisFunc();
  SerialRead();
  ledFunc(1);
}
void PinModes() {
  for (int selectPinNr = 0; selectPinNr < 3; selectPinNr++) {
    pinMode(selectPins[selectPinNr], OUTPUT);
  }
  for (int relaisPinNr = 0; relaisPinNr < 4; relaisPinNr++) {
    pinMode(relaisPins[relaisPinNr], OUTPUT);
  }
  pinMode(ledPin, OUTPUT);
}
void serialSendState(int x) {
  Serial.print(x);
}
void SerialPrint() {
  String SensorBez[8] = {"Taster 4",
                         "Taster 3",
                         "Taster 1",
                         "Taster 2",
                         "Sensor 1",
                         "Sensor 2",
                         "Sensor 3",
                         "Sensor 4"
                        };
  serialDataCounter += 1;
  Serial.printf("Statusdaten ESP8266:\n"
                "Messung Nr. %d\n"
                "IP-Address: ", serialDataCounter);
  Serial.println(WiFi.localIP());
  Serial.printf("Led Status:         %d\n", ledState);
  Serial.printf("Tasterstaten:\n");
  for (int i = 0; i < 4; i++) {
    Serial.printf("Taster %d: %d\t", i + 1, buttonState[i]);
  }
  Serial.printf("\nRelais Staten:\nR1: %d\tR2: %d\tR3: %d\n", relState[0], relState[1], relState[2]);
  Serial.printf("Sensorwerte:\n");
  for (int i = 0; i < 8; i++) {
    Serial.printf("%s:\t%d\n", SensorBez[i], inputWerte[i]);
  }
  Serial.printf("\n-----------\nEnd of File\n-----------\n\n");
}
void SerialRead() {
  if (Serial.available() > 0) {
    int inByte = Serial.read();
    switch (inByte) {
      case 'a':
        if (relState[0] == 0) {
          relFunc(0, 1);
        } else {
          relFunc(0, 0);
        }
        break;
      case 'b':
        if (relState[1] == 0) {
          relFunc(1, 1);
        } else {
          relFunc(1, 0);
        }
        break;
      case 'c':
        if (relState[2] == 0) {
          relFunc(2, 1);
        } else {
          relFunc(2, 0);
        }
        break;
      case 's':
        SerialPrint();
        break;
      default:
        ;
    }
  }
}
void relaisFunc() {
  relaisMan();
}
void relaisMan() {
  for (int i = 0; i < 3; i++) {
    if (buttonState[i + 1] != buttonStateOld[i + 1]) {
      if (relState[i] == 0) {
        relFunc(i, 1);
        delay(BUTTONDELAY);
      } else {
        relFunc(i, 0);
        delay(BUTTONDELAY);
      }
    }
    buttonState[i + 1] = buttonStateOld[i + 1];
  }
}
void ButtonFunc() {
  ButtonOne();
  ButtonTwo();
  ButtonThree();
  ButtonFour();
}
void ButtonOne() {
  if (inputWerte[2] >= 512) {
    buttonState[0] = 1;
  } else {
    buttonState[0] = 0;
  }
  if (buttonState[0] != buttonStateOld[0]) {
    if (buttonState[0] == 1) {
      SerialPrint();
    }
  }
}
int ButtonTwo() {
  if (inputWerte[3] >= 512) {
    buttonState[1] = 1;
  } else {
    buttonState[1] = 0;
  }
  return buttonState[1];
}
void ButtonThree() {
  if (inputWerte[1] >= 512) {
    buttonState[2] = 1;
  } else {
    buttonState[2] = 0;
  }
}
void ButtonFour() {
  if (inputWerte[0] >= 512) {
    buttonState[3] = 1;
  } else {
    buttonState[3] = 0;
  }
}
void relFunc(int relaisNumber, int relaisStat) {
  digitalWrite(relaisPins[relaisNumber], relaisStat);
  relState[relaisNumber] = relaisStat;
}
void wifiFunc() {
  Serial.println("ESP Gestartet");
  WiFi.begin(ssid, password);
  WiFi.hostname("NoStandBy");
  Serial.print("Verbindung wird hergestellt ...");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Verbunden! IP-Adresse: ");
  Serial.println(WiFi.localIP());
  server.onNotFound([]() {
    server.send(404, "text/plain", "Link wurde nicht gefunden!");
  });
  server.on("/", []() {
    server.send(200, "text/plain", "Startseite");
  });
  server.on("/R1", []() {
    if (relState[0] == 1) {
      server.send(200, "text/plain", "Relais 1 wurde ausgeschalten.");
      relFunc(0, 0);
    } else {
      server.send(200, "text/plain", "Relais 1 wurde angeschaltet.");
      relFunc(0, 1);
    }
  });
  server.on("/R2", []() {
    if (relState[1] == 1) {
      server.send(200, "text/plain", "0");
      relFunc(1, 0);
    } else {
      server.send(200, "text/plain", "1");
      relFunc(1, 1);
    }
  });
  server.on("/R3", []() {
    if (relState[2] == 1) {
      server.send(200, "text/plain", "Relais 3 wurde ausgeschalten.");
      relFunc(2, 0);
    } else {
      server.send(200, "text/plain", "Relais 3 wurde angeschaltet.");
      relFunc(2, 1);
    }
  });
  server.on("/alles", []() {
    for (int i = 0; i < 4; i++) {
      if (relState[i] == 0) {
        relFunc(i, 1);
        server.send(200, "text/plain", "Relais wurden ausgeschalten.");
      }
    }
  });
  server.on("/bs1", []() {
    server.send(200, "text/plain",
                String(buttonState[0])
               );
  });
  server.on("/data", []() {
    wifiDataCounter += 1;
    server.send(200, "text/plain",
                "Messung Nr. " + String(wifiDataCounter) +
                "\nIP-Address: " + ip2Str(WiFi.localIP()) +
                "\n\nLed Status:\t" + String(ledState) +
                "\n\nTasterstaten:"
                "\nTaster 1: " + String(buttonState[0]) +
                "\tTaster 2: " + String(buttonState[1]) +
                "\tTaster 3: " + String(buttonState[2]) +
                "\tTaster 4: " + String(buttonState[3]) +
                "\n\nrelStaten:"
                "\nRelais 1: " + String(relState[0]) +
                "\tRelais 2: " + String(relState[1]) +
                "\tRelais 3: " + String(relState[2]) +
                "\n\nSteckdosenstaten:"
                "\nSteckdose 1 ist " + stateSign(0) +
                "\nSteckdose 2 ist " + stateSign(1) +
                "\nSteckdose 3 ist " + stateSign(2) +
                "\n\nSensorwerte:"
                "\nTaster 1:\t" + String(inputWerte[2]) +
                "\tSensor 1:\t" + String(inputWerte[4]) +
                "\nTaster 2:\t" + String(inputWerte[3]) +
                "\tSensor 2:\t" + String(inputWerte[5]) +
                "\nTaster 3:\t" + String(inputWerte[1]) +
                "\tSensor 3:\t" + String(inputWerte[6]) +
                "\nTaster 4:\t" + String(inputWerte[0]) +
                "\tSensor 4:\t" + String(inputWerte[7]) +
                "\n\n"
                "---EoF---"
               );
  });
  server.begin();
  Serial.println("Webserver gestartet.\n\n");
}
void IC_4051() {
  for ( counter = 0 ; counter <= 7; counter++ ) {
    for (int i = 0; i < 3; i++) {
      bits[i] = bitRead(counter, i);
    }
    for (int i = 0; i < 3; i++) {
      digitalWrite(selectPins[i], bits[i]);
    }
    inputWerte[counter] = analogRead(A0);
    delay(25);
    if (inputWerte[counter] < 20) {
      inputWerte[counter] = 0;
    }
  }
}
void ledFunc(int x) {
  digitalWrite(ledPin, x);
  ledState = digitalRead(ledPin);
}
String ip2Str(IPAddress ip) {
  String s = "";
  for (int i = 0; i < 4; i++) {
    s += i  ? "." + String(ip[i]) : String(ip[i]);
  }
  return s;
}
String stateSign(int x) {
  String plugOn = "an";
  String plugOff = "aus";
  if (relState[x] == 0) {
    return plugOn;
  }
  if (relState[x] == 1) {
    return plugOff;
  }
}
