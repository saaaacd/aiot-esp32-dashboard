from flask import Flask, request, jsonify
import sqlite3
import datetime

app = Flask(__name__)
DB_NAME = "aiotdb.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temp REAL,
            humid REAL,
            metadata TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/sensor", methods=["POST"])
def sensor_data():
    data = request.json
    if not data or 'temp' not in data or 'humid' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    temp = data['temp']
    humid = data['humid']
    metadata = data.get('metadata', '')
    
    # 忽略舊的模擬器產生的假資料，只接受實體開發板的新資料
    if "ESP32_WiFi_Link" in metadata:
        return jsonify({"status": "ignored"}), 200
        
    import datetime
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sensors (temp, humid, metadata, timestamp) VALUES (?, ?, ?, ?)",
        (temp, humid, metadata, current_time)
    )
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "Data inserted"}), 201

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
