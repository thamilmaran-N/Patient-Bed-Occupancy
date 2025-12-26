# Patient Bed Occupancy 

## Project Overview
This project focuses on **detecting patient presence in hospital beds** by integrating **IoT technology** with existing (legacy) hospital infrastructure. Instead of replacing beds with expensive smart beds, the proposed system retrofits them using low-cost sensors, wireless communication, and cloud connectivity. The solution improves patient safety and enables real-time monitoring using a **Bed Unit** and a **Wrist Band Unit**.

---

## Main Objective
To **detect patient presence, absence, and abnormal conditions** in hospital beds using sensor data and Bluetooth signal strength, and to store this information in the cloud for future monitoring and enhancement.

---

## System Architecture
The system is divided into **two main units**:

### 1️.Bed Unit  
The Bed Unit is responsible for detecting patient weight and movement, processing data, and communicating with the cloud.

**Components Used:**
- ESP32  
- Load Cell  
- HX711 Amplifier  
- MPU6050 (Accelerometer & Gyroscope)  
- 16×2 I2C LCD Display  
- 3.7V Li-ion Battery  

**Functions:**
- Load cell placed under the bed detects patient weight  
- MPU6050 detects motion or abnormal movement  
- ESP32 processes sensor data  
- Bed status is displayed on the LCD  
- Data is sent to Firebase via Wi-Fi  

---

### 2️.Wrist Band Unit  
The Wrist Band Unit is a wearable device used to verify patient presence using Bluetooth signal strength.

**Components Used:**
- BM-10 Bluetooth Module  
- 3.3V Voltage Regulator  
- 3.7V Li-ion Battery  
- Slide Switch  
- LED  
- Resistors  

**Functions:**
- Worn by the patient  
- Continuously transmits Bluetooth signal  
- ESP32 in the Bed Unit reads signal strength (RSSI)  
- Helps identify patient presence and avoid false alerts  

---

## Working Principle
1. The **load cell** placed under the bed detects whether patient weight is present.  
2. The **wrist band** sends Bluetooth signals to the ESP32 in the Bed Unit.  
3. The ESP32 evaluates both **weight detection** and **Bluetooth signal strength** to determine patient status:

### Patient States
- **Patient Present**  
  - Bluetooth signal strength: High  
  - Patient weight: Detected  

- **Patient Absent**  
  - Bluetooth signal strength: Low  
  - Patient weight: Not detected  

- **Abnormal Condition**  
  - Bluetooth signal strength: High but patient weight not detected  
  - Bluetooth signal strength: Low but patient weight detected  

4. The processed data is sent to **Firebase** using Wi-Fi connectivity.  
5. Stored data can be used for **future enhancements** such as mobile or web-based monitoring.

---

## Tools Used
- Thonny IDE  
- Firebase Realtime Database  
- VS Code (for future enhancement and development)  

---

## Cloud Integration
- ESP32 connects to Firebase using Wi-Fi  
- Patient presence status is stored in real time  
- Enables future features such as mobile apps, dashboards, and analytics  

---

## Output
- Accurate detection of patient presence and absence  
- Identification of abnormal bed conditions  
- Real-time data storage in Firebase  
- Reduced manual monitoring by hospital staff  

---

## Applications
- Hospital bed monitoring  
- Elderly and critical care patient monitoring  
- Fall prevention systems  
- Smart healthcare and IoT-based hospitals  

---

## Conclusion
This project provides a **low-cost and effective IoT-based solution** for monitoring patient presence in hospital beds. By combining weight sensing, Bluetooth-based verification, and cloud storage, the system enhances patient safety while minimizing the need for expensive infrastructure upgrades.
