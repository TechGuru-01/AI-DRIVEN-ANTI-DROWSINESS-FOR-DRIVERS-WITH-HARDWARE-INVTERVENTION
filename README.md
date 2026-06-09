# Lumina Alert: A YOLOv11n-Based Embedded System for Real-Time Driver Drowsiness Detection and Multi-Modal Intervention

---

## System Architecture & Signal Workflow

The system operates via an automated, distributed network topology that bridges local high-speed computer vision with deterministic embedded hardware response loops. The complete computational and mechanical process is executed through the following distinct operating phases:

### 1. Pre-Drive Security Check and Lockout State Machine

Before the vehicle's ignition relay can be closed, the system initiates an obligatory safety verification state:

* **The Monitoring Baseline:** The driver faces the vehicle's A-pillar mounted camera while the software evaluates baseline drowsiness indicators directly from face detection bounding boxes.
* **The Punsihment Mechanism:** If the initialization routine registers an immediate fatigue state (prolonged eye closure or frequent yawning signatures), the application flags a verification failure. The script registers the failure count to a local cache file and initiates a hard software lockout, forcing the operator to wait before trying again:
* **Failure 1:** Activates an unbypassable 5-minute cooldown timer.
* **Failure 2:** Escalates to an unbypassable 10-minute cooldown timer.
* **Failure 3:** Imposes a maximum 15-minute cooldown timer.


* **Persistent Session Token:** To maximize efficiency and ensure user convenience, passing the check generates a secure session token that remains valid in the background for a 2-hour window. This ensures that brief stops, such as fueling or loading luggage, do not require the driver to repeat the validation test upon turning the vehicle back on.

### 2. High-Frequency Video Capture and Streaming Pipeline

Once the driver is authorized and the vehicle is in operation, the dynamic tracking loop initializes:

* **Ergonomic Camera Placement:** A standard USB webcam is physically positioned on the driver-side **A-pillar** of the Toyota Avanza. This specific mounting location ensures the optical sensor captures an optimal angular profile of the driver's face while remaining completely non-intrusive, preserving an unobstructed field of view during operation.
* **Native Ultralytics Stream Processing:** The video frame ingestion, buffering, and frame management are handled directly through native **Ultralytics execution pipelines** running within an isolated Docker container. This maps the physical video device straight to the ML frame-handler, keeping data pathways streamlined and minimizing conversion overhead.

### 3. TensorRT Edge Inference and Single-Target Tracking

The computational core on the Nvidia Jetson Orin Nano processes incoming video streams utilizing advanced machine learning acceleration graphs and strict object tracking constraints:

* Raw image matrices are forwarded directly into the YOLOv11n engine model, which has been compiled down to a specialized TensorRT format to squeeze maximum efficiency out of the Jetson's CUDA cores.
* Because the system utilizes a pure YOLO object detection architecture rather than landmark estimation, it detects and isolates targeted facial feature classes (such as the face, open/closed eyes, and mouth state) using high-precision bounding boxes.
* To guarantee system stability and eliminate noise from passenger movement, the application integrates the **ByteTrack** tracking algorithm via the Ultralytics API. The tracking configuration is explicitly restricted to a maximum of **one target**, locking the tracking frame strictly onto the primary driver.
* **Continuous Drive Mode Monitoring:** Once the pre-drive evaluation is cleared, the driver is permitted to navigate continuously. The system transitions into an active driving assessment loop, using mathematical evaluations of bounding boxes over time to constantly parse fatigue levels.

### 4. Escalated Severity Alert Logic

When drowsiness profiles are captured mid-transit, the system executes a real-time tiered escalation routine based on anomaly duration and severity:

* **Early Fatigue Warning:** Upon detecting initial micro-sleep indicators or early-stage yawning trends, the system triggers localized audio warnings, utilizing the core application interface to prompt the driver to adjust focus.
* **Severe Fatigue Intervention:** If the vision pipeline flags severe, sustained drowsiness anomalies (e.g., critical extended eye closure times), the automation logic immediately escalates the response. The platform plays high-priority voice prompts specifically alerting passengers within the vehicle cabin to step in and take immediate action. Simultaneously, an unrelenting **3000 Hz high-frequency distress alarm** is activated, piercing through the vehicle to interrupt the micro-sleep state. This multi-channel alert loop runs continuously and will remain engaged until the driver demonstrates full visual alertness and normal tracking metrics.

### 5. Low-Latency Microcontroller Signal Offloading

To protect core operating threads and ensure immediate reaction times, heavy edge inference processing is completely decoupled from the physical alert hardware execution:

* When a persistent drowsiness state is confirmed by the TensorRT engine, the main Python application thread constructs a lightweight, single-byte serial interrupt trigger packet.
* This execution code is instantly transmitted down an automated hardware abstraction layer via the PySerial communication module, communicating over a hardwired USB-to-TTL UART serial bridge connected directly to the ESP8266 (NodeMCU) microcontroller.

### 6. Multi-Channel Safety Countermeasure Actuation

The ESP8266 acts as a dedicated real-time hardware handler, listening continuously for incoming interrupt commands from the Jetson:

* **Acoustic Warning Intervention:** The moment the ESP8266 decodes the serial alarm byte, it routes a high-priority sound signal straight into the auxiliary/USB audio interface of the Toyota Avanza. This forces high-decibel, high-frequency alert tracks—and the severe 3000 Hz critical buzzer alarm—to blare directly over the car speakers, cutting through driver disorientation.
* **Mechanical Countermeasures:** Simultaneously, the microcontroller shifts its onboard GPIO pins from low to high states. This voltage spike triggers mechanical relay boards linked to physical cabin alerts, completing a secure, closed-loop safety intervention that keeps operating conditions safe.

---

## Model Training & Performance Optimization

The core intelligence relies on an optimized YOLOv11n network profile trained extensively on dense facial datasets under erratic in-cabin conditions, balancing heavy backlight variation, nighttime driving angles, and optical obstructions like glasses. The custom-trained model achieved a high-accuracy baseline performance with a **93% evaluation score** during validation testing.

Maximizing performance on edge hardware required three key architectural steps:

* **Weight Quantization & Calibration:** Translating standard `.pt` PyTorch weights directly into localized TensorRT execution plans to exploit the hardware's deep learning accelerators. During compilation, the TensorRT engine was rigorously calibrated using a dedicated subset of **1,000 calibration images** to optimize quantization precision, lower latency, and preserve edge accuracy.
* **Memory Management:** Allocating a 50 GB local swap partition on the Jetson Orin Nano to seamlessly process sudden processing bursts without kernel panic or out-of-memory overhead.
* **Containerization:** Enclosing the entire runtime, CUDA toolkit variants, and dependency packages within an isolated Docker environment to ensure constant execution parameters on any host setup.

---

## Local Installation & Hardware Deployment

1. Clone this repository onto your Nvidia Jetson Orin Nano.
2. Ensure your Jetson environment has a 50 GB swap file allocated and that the Docker daemon is active.
3. Build and launch the provided container configuration using the setup scripts to compile the local environment with TensorRT dependencies.
4. Open the Arduino IDE, load the provided `.ino` firmware file from the firmware directory, and flash it onto your ESP8266 hardware.
5. Interface the ESP8266 with your vehicle relays, connect your webcam mounted on the vehicle's A-pillar to the Jetson via USB, and map the Jetson's audio output into the auxiliary/USB input of the Toyota Avanza's sound system.
6. Identify the active USB/serial port binding between the Jetson and the ESP8266, update the matching parameters inside the core Python configuration, and run the system container to initialize driver protection.

---

## References & Source Publication

* **Research Paper:** *Lumina Alert: A YOLOv11n-Based Embedded System for Real-Time Driver Drowsiness Detection and Multi-Modal Intervention*
* **Full Publication PDF:** https://www.researchgate.net/profile/Grazielle-Nychole-Dela-Cruz/publication/401350914_Lumina_Alert_A_YOLOv11n-Based_Embedded_System_for_Real-Time_Driver_Drowsiness_Detection_and_Multi-Modal_Intervention/links/69afdb1ba91b826e4348be2c/Lumina-Alert-A-YOLOv11n-Based-Embedded-System-for-Real-Time-Driver-Drowsiness-Detection-and-Multi-Modal-Intervention.pdf
