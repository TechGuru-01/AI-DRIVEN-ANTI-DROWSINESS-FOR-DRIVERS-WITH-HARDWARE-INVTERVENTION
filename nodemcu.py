import serial
import time

class NodeMCUStates:
    """
    pre-drive
        0: awake (OK)
        1: drowsy
        2: yawning
    drive
        3: drowsy
        4: yawning
    others
        5: reset
        6: normal
    """
    # change port !!
    def __init__(self, port="COM11", baudrate=115200):
        self.ser = None
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)
            self.ser.reset_input_buffer()

            print("Sending Jetson READY...")
            self.ser.write(b"JETSON_READY\n")

            while True:
                line = self.ser.readline().decode(errors='ignore').strip()
                if "READY" in line:
                    print("NodeMCU READY")
                    break
        except Exception as e:
            print(f"Serial error: {e}")

    def send_state(self, state: int):
        self.ser.write(f"{state}\n".encode())
        print(f"STATE SENT: {state}")
        try:
            resp = self.ser.readline().decode(errors='ignore').strip()
            if resp:
                    print(f"ESP: {resp}")
        except Exception as e:
            print(f"Error reading ESP: {e}")

    def close(self):
        if self.ser:
            self.ser.close()