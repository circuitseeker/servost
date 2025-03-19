#!/usr/bin/env python3

import serial
import time

def scan_servo():
    try:
        # Open serial port with lower baudrate
        ser = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=115200,  # Try lower baudrate
            timeout=0.1,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )
        
        print("Port opened successfully")
        
        # Try to read the current position (0x38 is the position address)
        # Header (0xFF 0xFF) + ID + Length + Instruction + Address + Data Length
        packet = bytearray([0xFF, 0xFF, 0x01, 0x04, 0x02, 0x38, 0x02])
        checksum = (~sum(packet[2:]) & 0xFF)
        packet.append(checksum)
        
        print(f"Sending position read packet: {' '.join([f'0x{x:02X}' for x in packet])}")
        
        # Clear input buffer
        ser.reset_input_buffer()
        
        # Send packet
        ser.write(packet)
        time.sleep(0.1)
        
        # Read response
        if ser.in_waiting:
            response = ser.read(ser.in_waiting)
            print(f"Received response: {' '.join([f'0x{x:02X}' for x in response])}")
            
            if len(response) >= 8:  # Position read response should be 8 bytes
                if response[0] == 0xFF and response[1] == 0xFF:
                    print("Valid header found")
                    print(f"Servo ID: {response[2]}")
                    if len(response) > 4:
                        print(f"Error byte: {response[4]}")
                    if len(response) >= 7:
                        position = (response[6] << 8) | response[5]
                        print(f"Current position: {position}")
        else:
            print("No response received")
            
            # Try sending a torque enable command
            print("\nTrying to enable torque...")
            torque_packet = bytearray([0xFF, 0xFF, 0x01, 0x04, 0x03, 0x28, 0x01])
            checksum = (~sum(torque_packet[2:]) & 0xFF)
            torque_packet.append(checksum)
            
            print(f"Sending torque enable packet: {' '.join([f'0x{x:02X}' for x in torque_packet])}")
            ser.write(torque_packet)
            time.sleep(0.1)
            
            if ser.in_waiting:
                response = ser.read(ser.in_waiting)
                print(f"Received response: {' '.join([f'0x{x:02X}' for x in response])}")
        
        ser.close()
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    scan_servo() 