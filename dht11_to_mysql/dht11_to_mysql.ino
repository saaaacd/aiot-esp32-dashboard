/*
  ESP32 + DHT11 溫濕度感測器 → 透過 WiFi HTTP API 上傳至 MySQL
  (使用 HTTPClient，不使用 MySQL_Connection，避免 crash)
  
  接線方式：
  DHT11 VCC  → ESP32 3.3V
  DHT11 DATA → ESP32 GPIO 4
  DHT11 GND  → ESP32 GND
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <SimpleDHT.h>       // DHT11 的標頭檔

// ===== WiFi 設定 =====
const char ssid[] = "baba";
const char password[] = "77777777";

// ===== 伺服器設定 =====
// 你的電腦 IP + Flask 伺服器端路徑 (5000 port)
String serverName = "http://172.20.10.3:5000/addData";

// ===== DHT11 設定 =====
int pinDHT11 = 15;           // DHT11 的 Data 腳位接在 GPIO 15
SimpleDHT11 dht11;

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("\n====================================");
  Serial.println("ESP32 + DHT11 → HTTP API → MySQL");
  Serial.println("====================================\n");

  // === 連接 WiFi ===
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  int retry = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    retry++;
    if (retry > 30) {
      Serial.println("\nWiFi connection timeout!");
      return;
    }
  }

  Serial.println("\nWiFi connected!");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
  Serial.println("Starting sensor readings...\n");
}

void loop() {
  // === 讀取 DHT11 感測器 ===
  byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;

  if ((err = dht11.read(pinDHT11, &temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT11 failed, err=");
    Serial.println(err);
    delay(2000);
    return;
  }

  int temp = (int)temperature;
  int humid = (int)humidity;

  Serial.print("DHT11 => Temp: ");
  Serial.print(temp);
  Serial.print("°C, Humidity: ");
  Serial.print(humid);
  Serial.println("%");

  // === 透過 HTTP 發送資料至 PHP ===
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // 將真實溫濕度資料塞進網址參數，並表明來源為 esp32
    String serverPath = serverName + "?temp=" + String(temp) + "&humid=" + String(humid) + "&source=esp32";

    Serial.print("Sending to: ");
    Serial.println(serverPath);

    http.begin(serverPath);
    int httpResponseCode = http.GET();

    if (httpResponseCode > 0) {
      Serial.print("HTTP ");
      Serial.print(httpResponseCode);
      Serial.print(" => ");
      Serial.println(http.getString());
    } else {
      Serial.print("HTTP Error: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("WiFi disconnected! Reconnecting...");
    WiFi.begin(ssid, password);
    delay(5000);
  }

  Serial.println("---");
  delay(2000);  // 每 2 秒讀取一次 (作業需求)
}
