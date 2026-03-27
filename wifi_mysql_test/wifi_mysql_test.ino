/*
  ESP32 WiFi + HTTP POST API 傳輸法
  將資料存入我們新建的 Flask + SQLite 即時儀表板
*/

#include <WiFi.h>
#include <HTTPClient.h>

const char ssid[] = "baba";
const char password[] = "77777777";

// 你的電腦 IP + Flask 伺服器路徑 (Port 5000, 路徑 /sensor)
String serverName = "http://172.20.10.3:5000/sensor";

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("\n================================");
  Serial.println("ESP32 to Flask Dashboard Test");
  Serial.println("================================\n");

  // === 第一步：連接 WiFi ===
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
}

void loop() {
  // === 第二步：透過 HTTP POST 發送感測器資料 (每 5 秒送一次) ===
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);

    // 設定為 JSON 格式
    http.addHeader("Content-Type", "application/json");

    // 這裡我們產生測試用的溫濕度資料 (可以改成接上 DHT11 讀取的數值)
    float temp = 28.5; 
    float humid = 55.2;

    // 將資料包裝成 JSON 字串
    String jsonPayload = "{\"temp\":" + String(temp) + 
                         ", \"humid\":" + String(humid) + 
                         ", \"metadata\":\"{\\\"device_id\\\":\\\"ESP32_硬件本體\\\"}\"}";

    Serial.print("\nSending POST request: ");
    Serial.println(jsonPayload);

    int httpResponseCode = http.POST(jsonPayload);   // 發送 POST 請求

    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);  // 201 代表寫入資料庫成功
      String payload = http.getString();
      Serial.println("Server reply: " + payload);
    } else {
      Serial.print("HTTP Error code: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }

  // 等待 5 秒再送下一筆
  delay(5000);
}
