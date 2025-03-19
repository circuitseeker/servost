#!/usr/bin/env python3

import os
import sys
import time
from STservo_sdk.port_handler import *
from STservo_sdk.protocol_packet_handler import *
from STservo_sdk.stservo_def import *

# Default setting
BAUDRATES = [115200, 1000000, 500000, 250000]  # Try different baudrates
DEVICENAME = '/dev/ttyACM0'    # Check which port is being used on your controller

# Protocol constants
PKT_HEADER0 = 0xFF
PKT_HEADER1 = 0xFF

def scan_servos():
    # Initialize PortHandler instance
    portHandler = PortHandler(DEVICENAME)

    # Open port
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        quit()

    for baudrate in BAUDRATES:
        print(f"\nTrying baudrate: {baudrate}")
        # Set port baudrate
        if portHandler.setBaudRate(baudrate):
            print(f"Succeeded to change the baudrate to {baudrate}")
        else:
            print("Failed to change the baudrate")
            continue

        # Try to ping servos with IDs from 0 to 253
        print("\nScanning for servos...")
        for servo_id in range(254):
            print(f"\rChecking ID: {servo_id}", end='', flush=True)
            
            # Create ping packet
            # Header (0xFF 0xFF) + ID + Length + Instruction + Param + Checksum
            packet = bytearray([PKT_HEADER0, PKT_HEADER1, servo_id, 0x02, 0x01, 0x00])
            checksum = (~sum(packet[2:]) & 0xFF)
            packet.append(checksum)
            
            # Clear any existing data
            portHandler.clearPort()
            
            # Send packet
            portHandler.writePort(packet)
            time.sleep(0.05)  # Increased delay
            
            # Read response
            if portHandler.getBytesAvailable() >= 6:
                response = portHandler.readPort(portHandler.getBytesAvailable())
                if len(response) >= 6 and response[0] == PKT_HEADER0 and response[1] == PKT_HEADER1:
                    if response[2] == servo_id:  # Check if response is from the servo we pinged
                        print(f"\nFound servo at ID {servo_id} at baudrate {baudrate}")
                        
                        # Try to read position
                        pos_packet = bytearray([PKT_HEADER0, PKT_HEADER1, servo_id, 0x04, 0x02, 0x38, 0x02])
                        checksum = (~sum(pos_packet[2:]) & 0xFF)
                        pos_packet.append(checksum)
                        
                        portHandler.clearPort()
                        portHandler.writePort(pos_packet)
                        time.sleep(0.05)  # Increased delay
                        
                        if portHandler.getBytesAvailable() >= 8:
                            pos_response = portHandler.readPort(portHandler.getBytesAvailable())
                            if len(pos_response) >= 8:
                                position = (pos_response[6] << 8) | pos_response[5]
                                print(f"Current position: {position}")
    
    print("\n\nScan complete!")
    
    # Close port
    portHandler.closePort()

if __name__ == '__main__':
    scan_servos() 