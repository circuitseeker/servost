import serial
import time

def scan_servos():
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
        
        print("Scanning for ST3215 servos...")
        
        # ST3215 servo ping command
        for servo_id in range(1, 254):
            # ST3215 protocol ping command
            command = bytes([0x55, 0x55, servo_id, 0x02, 0x01, 0x00])
            ser.write(command)
            time.sleep(0.01)
            
            if ser.in_waiting:
                response = ser.read(ser.in_waiting)
                print(f"Response for ID {servo_id}: {response.hex()}")
                if len(response) >= 6 and response[2] == servo_id:
                    print(f"Found ST3215 servo with ID: {servo_id}")
        
        ser.close()
        
    except serial.SerialException as e:
        print(f"Error: Could not open serial port. {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    scan_servos() 