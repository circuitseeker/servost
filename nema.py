#!/usr/bin/env python3
import time
import Jetson.GPIO as GPIO

# Stepper Motor Pin Configuration
DIR_PIN = 7
STEP_PIN = 11

# Setup GPIO
GPIO.setmode(GPIO.BOARD)  # Use the board pin numbering
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)

# Main program
try:
    print("Stepper Motor Simple Movement Started")
    print(f"Using DIR_PIN: {DIR_PIN}, STEP_PIN: {STEP_PIN}")

    # Set direction pin high (clockwise)
    GPIO.output(DIR_PIN, GPIO.HIGH)
    print("Direction set to clockwise (PIN HIGH)")

    print("Starting continuous movement...")
    # Continuously pulse the step pin
    while True:
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(0.001)  # Short delay
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(0.001)  # Short delay

except KeyboardInterrupt:
    print("\nProgram stopped by user")

except Exception as e:
    print(f"\nAn error occurred: {e}")

finally:
    # Clean up GPIO
    GPIO.cleanup()
    print("GPIO cleanup completed")
