#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

unsigned long startTime = millis();

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// Create display object using custom I2C pins
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

const char* ssid = "";
const char* password = "";

const char* pikudApiUrl = "https://www.oref.org.il/WarningMessages/alert/alerts.json";
const char* testApiUrl = "https://74ed6813-dbbe-4cc4-ab8d-21f818e58df1-00-2v81qhx301d8.janeway.replit.dev/"; 
const char* targetCity = ""; 

const int buzzerPin = 19;

void setup() {
  Wire.begin(21, 5);
  Serial.begin(115200);
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(buzzerPin, LOW);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("❌ OLED not found. Check wiring and address.");
    while (true);
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("Booting up [Success!]");
  display.println("Connecting to wifi");
  display.println("");
  display.println("Almost there!");
  display.display();

  Serial.println("Scanning Wi-Fi...");
  int n = WiFi.scanNetworks();
  for (int i = 0; i < n; ++i) {
    Serial.printf("%d: %s (%d dBm)\n", i + 1, WiFi.SSID(i).c_str(), WiFi.RSSI(i));
  }

  Serial.printf("Connecting to SSID: %s\n", ssid);
  WiFi.begin(ssid, password);
  int retries = 0;
  while (WiFi.status() != WL_CONNECTED && retries < 20) {
    delay(500);
    Serial.print(".");
    retries++;
  }
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("\n❌ Failed to connect to WiFi.");
    return;
  }
  Serial.println("\n✅ WiFi Connected!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    bool testAlert = checkTestAPI();
    bool realAlert = checkPikudAPI();

    if (testAlert || realAlert) {
      activateBuzzer();
    }
  } else {
    Serial.println("WiFi disconnected. Reconnecting...");
    WiFi.begin(ssid, password);
  }

  delay(10000); // Wait 10 seconds before checking again
}

bool checkTestAPI() {
  HTTPClient http;
  http.begin(testApiUrl);
  int httpCode = http.GET();
  if (httpCode == 200) {
    String payload = http.getString();
    return payload.indexOf("true") > 0;
  }
  http.end();
  return false;
}

bool checkPikudAPI() {
  HTTPClient http;
  http.begin(pikudApiUrl);
  http.addHeader("Referer", "https://www.oref.org.il/");
  http.addHeader("X-Requested-With", "XMLHttpRequest");

  int httpCode = http.GET();
  Serial.print("HTTP Status Code: ");
  Serial.println(httpCode);

  if (httpCode == 200) {
    String payload = http.getString();
    if (payload.startsWith("\xEF\xBB\xBF")) {
      payload = payload.substring(3);
    }

    Serial.println("=== RAW RESPONSE START ===");
    Serial.println(payload);
    Serial.println("=== RAW RESPONSE END ===");

    if (payload.length() < 10) {
      Serial.println("Waiting to receive alert! System is armed");
      display.clearDisplay();
      display.setTextSize(1);
      display.setTextColor(SSD1306_WHITE);
      display.setCursor(0, 0);
      display.println("System is waiting for alerts!");
      display.display();
      http.end();
      return false;
    }

    DynamicJsonDocument doc(2048);
    DeserializationError error = deserializeJson(doc, payload);
    if (!error) {
      JsonArray alerts = doc["data"].as<JsonArray>();
      for (JsonObject alert : alerts) {
        String data = alert["data"];
        Serial.print("Checking alert: ");
        Serial.println(data);
        if (data.indexOf(targetCity) != -1) {
          Serial.println("⚠️ Alert for your city detected!");
          http.end();
          return true;
        }
      }
    } else {
      Serial.print("❌ FATAL ERROR: SYSTEM IS IDLE!! ");
      Serial.println(error.c_str());
    }
  } else {
    Serial.print("HTTP error: ");
    Serial.println(httpCode);
  }

  http.end();
  return false;
}

void activateBuzzer() {
  unsigned long alertStart = millis();
  while (millis() - alertStart < 600000) { // Run for 10 minutes
    for (int j = 0; j < 3; j++) {
      digitalWrite(buzzerPin, HIGH);
      delay(200);  // 200ms ON
      digitalWrite(buzzerPin, LOW);
      delay(100);  // 100ms OFF
    }
    delay(0);

    Serial.println("ALERT RECEIVED!! IMMEDIATE DANGER");
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.println("!IMMEDIATE DANGER!");
    display.println("Please go to the shelter!!");
    display.println("System will restart once");
    display.println("Danger is eliminated");
    display.display();
  }
}
