import serial
import time

def test_st3215():
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
        
        print("Testing ST3215 servo communication...")
        
        # ST3215 protocol command to read position
        # Format: 0x55 0x55 ID CMD LEN DATA
        command = bytes([0x55, 0x55, 0x01, 0x02, 0x02, 0x00])
        print(f"Sending command: {command.hex()}")
        
        # Clear any existing data
        ser.reset_input_buffer()
        
        # Send command
        ser.write(command)
        time.sleep(0.1)
        
        # Read response
        if ser.in_waiting:
            response = ser.read(ser.in_waiting)
            print(f"Raw response: {response.hex()}")
            
            # Check if response is valid
            if len(response) >= 6:
                if response[0] == 0x55 and response[1] == 0x55:
                    print(f"Valid response header found")
                    if response[2] == 0x01:
                        print(f"Response from correct servo ID")
                        print(f"Command: {response[3]:02x}")
                        print(f"Length: {response[4]:02x}")
                        if len(response) > 5:
                            print(f"Data: {response[5:].hex()}")
        else:
            print("No response received")
        
        ser.close()
        
    except serial.SerialException as e:
        print(f"Error: Could not open serial port. {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_st3215() 