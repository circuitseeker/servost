#!/usr/bin/env python3

import serial
import time

class STServo:
    def __init__(self, port='/dev/ttyACM0', baudrate=1000000):
        """Initialize serial connection"""
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=0.1,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        )
        time.sleep(0.1)  # Wait for serial to initialize
        
    def writeByte(self, id, addr, value):
        """Write a byte value to servo"""
        buf = bytearray([0xFF, 0xFF, id, 0x04, 0x03, addr, value])
        checksum = (~sum(buf[2:]) & 0xFF)
        buf.append(checksum)
        
        print(f"Writing to ID {id}, addr {addr:02x}, value {value:02x}")
        print(f"Sending: {' '.join([f'0x{x:02X}' for x in buf])}")
        
        self.serial.write(buf)
        time.sleep(0.05)
        
        if self.serial.in_waiting:
            response = self.serial.read(self.serial.in_waiting)
            print(f"Response: {' '.join([f'0x{x:02X}' for x in response])}")
            return 1
        return 0
        
    def readByte(self, id, addr):
        """Read a byte value from servo"""
        buf = bytearray([0xFF, 0xFF, id, 0x04, 0x02, addr, 0x01])
        checksum = (~sum(buf[2:]) & 0xFF)
        buf.append(checksum)
        
        print(f"Reading from ID {id}, addr {addr:02x}")
        print(f"Sending: {' '.join([f'0x{x:02X}' for x in buf])}")
        
        self.serial.write(buf)
        time.sleep(0.05)
        
        if self.serial.in_waiting:
            response = self.serial.read(self.serial.in_waiting)
            print(f"Response: {' '.join([f'0x{x:02X}' for x in response])}")
            if len(response) >= 7:
                return response[5]
        return -1

    def WritePosEx(self, id, position, move_time, speed):
        """Write position with time and speed"""
        buf = bytearray([0xFF, 0xFF, id, 0x09, 0x03, 0x2A])
        
        # Add position bytes (2 bytes, little endian)
        buf.extend([position & 0xFF, (position >> 8) & 0xFF])
        
        # Add time bytes (2 bytes, little endian)
        buf.extend([move_time & 0xFF, (move_time >> 8) & 0xFF])
        
        # Add speed bytes (2 bytes, little endian)
        buf.extend([speed & 0xFF, (speed >> 8) & 0xFF])
        
        checksum = (~sum(buf[2:]) & 0xFF)
        buf.append(checksum)
        
        print(f"Setting ID {id} to position {position}, time {move_time}, speed {speed}")
        print(f"Sending: {' '.join([f'0x{x:02X}' for x in buf])}")
        
        self.serial.write(buf)
        time.sleep(0.05)
        
        if self.serial.in_waiting:
            response = self.serial.read(self.serial.in_waiting)
            print(f"Response: {' '.join([f'0x{x:02X}' for x in response])}")
            return 1
        return 0

def main():
    print("Initializing ST Servo test...")
    st = STServo()
    
    # Constants from your ESP32 code
    SMS_STS_MODE = 0x30
    SMS_STS_TORQUE_ENABLE = 0x28
    
    print("\nEnabling torque...")
    if st.writeByte(1, SMS_STS_TORQUE_ENABLE, 1) == 1:
        print("Successfully enabled torque")
    else:
        print("Failed to enable torque")
    
    print("\nTrying to set Servo Mode...")
    # Set to Servo Mode (0) for ID 1
    if st.writeByte(1, SMS_STS_MODE, 0) == 1:
        print("Successfully set to Servo Mode")
    else:
        print("Failed to set Servo Mode")
    
    print("\nTrying to read current mode...")
    mode = st.readByte(1, SMS_STS_MODE)
    if mode != -1:
        print(f"Current mode: {mode}")
    else:
        print("Failed to read mode")

    print("\nStarting continuous movement between 0 and 90 degrees...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            # Move to 90 degrees (position 1024)
            print("\nMoving to 90 degrees...")
            st.WritePosEx(1, 1024, 2000, 1000)
            time.sleep(2.5)
            
            # Move to 0 degrees (position 0)
            print("Moving to 0 degrees...")
            st.WritePosEx(1, 0, 2000, 1000)
            time.sleep(2.5)
            
    except KeyboardInterrupt:
        print("\nStopping movement...")
        # Move back to center before stopping
        st.WritePosEx(1, 2048, 2000, 1000)
        time.sleep(2.5)
    
    st.serial.close()

if __name__ == "__main__":
    main() 