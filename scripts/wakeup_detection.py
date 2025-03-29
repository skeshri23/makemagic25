import sounddevice as sd
import numpy as np
import os

THRESHOLD = 0.5  # Adjust sensitivity

def detect_loud_noise(indata, frames, time, status):
    """Trigger wake-up if loud sound is detected."""
    volume = np.linalg.norm(indata)  # Calculate volume level
    if volume > THRESHOLD:
        print("🔊 Loud noise detected! Waking up system...")
        os.system("python raspi_ai.py")  # Start AI processing

# Activate wake-up mode
with sd.InputStream(callback=detect_loud_noise):
    print("🔋 Low-power mode active. Listening for loud noises...")
    sd.sleep(1000000)  # Keep running
