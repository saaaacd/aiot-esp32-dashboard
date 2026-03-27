<?php
/**
 * DIC3-1: PHP & MySQL Implementation
 * This script receives sensor readings via HTTP GET requests and inserts them into MySQL.
 * 
 * Usage: http://localhost/aiot/addData.php?temp=25&humid=60
 */

$servername = "localhost";
$username = "root";
$password = "";
$dbname = "aiot_db";

// Create connection
$conn = new mysqli($servername, $username, $password);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Create database if not exists
$sql = "CREATE DATABASE IF NOT EXISTS $dbname";
if ($conn->query($sql) === TRUE) {
    $conn->select_db($dbname);
}
else {
    die("Error creating database: " . $conn->error);
}

// Create table if not exists as per homework requirements
$sql = "CREATE TABLE IF NOT EXISTS sensors (
    id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    temp FLOAT NOT NULL,
    humid FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)";

if ($conn->query($sql) !== TRUE) {
    die("Error creating table: " . $conn->error);
}

// Get data from GET request
$temp = isset($_GET['temp']) ? $_GET['temp'] : null;
$humid = isset($_GET['humid']) ? $_GET['humid'] : null;

if ($temp !== null && $humid !== null) {
    // Validate inputs
    if (is_numeric($temp) && is_numeric($humid)) {
        // Prepare and bind
        $stmt = $conn->prepare("INSERT INTO sensors (temp, humid) VALUES (?, ?)");
        $stmt->bind_param("dd", $temp, $humid);

        if ($stmt->execute()) {
            echo "New record created successfully. Temp: $temp, Humid: $humid";
        }
        else {
            echo "Error: " . $stmt->error;
        }
        $stmt->close();
    }
    else {
        echo "Invalid input. Temp and Humid must be numeric.";
    }
}
else {
    echo "No data received. Usage: addData.php?temp=value&humid=value";
}

$conn->close();
?>
