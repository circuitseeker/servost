import serial
import time

class SCServo:
    def __init__(self, port='/dev/ttyACM0', baudrate=1000000):
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=0.1,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )
        
    def write_byte(self, servo_id, cmd, data):
        command = bytes([0xFF, 0xFF, servo_id, cmd, 0x01, data])
        self.ser.write(command)
        time.sleep(0.01)
        return self.read_response()
    
    def read_pos(self, servo_id):
        command = bytes([0xFF, 0xFF, servo_id, 0x02, 0x02, 0x00])
        self.ser.write(command)
        time.sleep(0.01)
        response = self.read_response()
        if response and len(response) >= 8:
            return (response[6] << 8) | response[5]
        return -1
    
    def read_response(self):
        if self.ser.in_waiting:
            return self.ser.read(self.ser.in_waiting)
        return None
    
    def close(self):
        self.ser.close()

def main():
    try:
        print("Initializing SCServo communication...")
        servo = SCServo()
        
        # Initialize servo to Servo Mode (like in ESP32 setup)
        print("\nSetting servo to Servo Mode...")
        response = servo.write_byte(1, 0x02, 0x00)  # Set to Servo Mode
        if response:
            print(f"Mode response: {response.hex()}")
        
        # Read current position
        print("\nReading current position...")
        position = servo.read_pos(1)
        if position != -1:
            print(f"Current position: {position}")
        else:
            print("Failed to read position")
        
        servo.close()
        
    except serial.SerialException as e:
        print(f"Error: Could not open serial port. {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 