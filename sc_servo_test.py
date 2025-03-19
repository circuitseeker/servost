import serial
import time

def test_sc_servo():
    try:
        # Open serial port with matching ESP32 settings
        ser = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=1000000,  # Match ESP32 baudrate
            timeout=0.1,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )
        
        print("Testing SCServo communication...")
        
        # First try to set servo mode (like in ESP32 setup)
        # Command format: 0xFF 0xFF ID CMD LEN DATA
        mode_command = bytes([0xFF, 0xFF, 0x01, 0x02, 0x01, 0x00])  # Set to Servo Mode
        print(f"Sending mode command: {mode_command.hex()}")
        ser.write(mode_command)
        time.sleep(0.1)
        
        if ser.in_waiting:
            response = ser.read(ser.in_waiting)
            print(f"Mode response: {response.hex()}")
        
        # Try to read position
        read_command = bytes([0xFF, 0xFF, 0x01, 0x02, 0x02, 0x00])
        print(f"\nSending read command: {read_command.hex()}")
        ser.write(read_command)
        time.sleep(0.1)
        
        if ser.in_waiting:
            response = ser.read(ser.in_waiting)
            print(f"Position response: {response.hex()}")
            
            # Parse position if response is valid
            if len(response) >= 6:
                if response[0] == 0xFF and response[1] == 0xFF:
                    print("Valid response header found")
                    if response[2] == 0x01:
                        print("Response from correct servo ID")
                        if len(response) >= 8:
                            position = (response[6] << 8) | response[5]  # Combine bytes for position
                            print(f"Current position: {position}")
        else:
            print("No response received")
        
        ser.close()
        
    except serial.SerialException as e:
        print(f"Error: Could not open serial port. {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_sc_servo() 