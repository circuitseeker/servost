import serial
import time

def test_servo():
    try:
        # Open serial port
        ser = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=115200,
            timeout=0.1,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )
        
        print("Testing communication with servo ID 1...")
        
        # Try to read servo position
        command = bytes([0x55, 0x55, 0x01, 0x02, 0x02, 0x00])
        print(f"Sending command: {command.hex()}")
        ser.write(command)
        time.sleep(0.1)
        
        if ser.in_waiting:
            response = ser.read(ser.in_waiting)
            print(f"Received response: {response.hex()}")
        else:
            print("No response received")
        
        ser.close()
        
    except serial.SerialException as e:
        print(f"Error: Could not open serial port. {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_servo() 