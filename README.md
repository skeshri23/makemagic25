<<<<<<< HEAD
# **makemagic25**

## **AI Audio Surveillance for Public Safety 🚨**

This project is an AI-powered surveillance system designed to enhance campus safety while maintaining energy efficiency. It integrates **microphones, vibration sensors, and AI models** to detect abnormal sounds like screams, gunshots, and breaking glass. When an emergency is identified, the system **triggers LED alerts, sends SMS notifications, and calls emergency lines** to ensure a rapid response.

Built on **Raspberry Pi and Arduino**, the system processes real-time audio and vibration data using AI-based classification models like **DeepSpeech or Whisper**. It operates efficiently with a **Sleep Mode Display** to conserve energy, making it a **reliable and proactive security solution for public spaces**.

## **📂 Project Structure**
```plaintext
AI-Audio-Surveillance/
│── main.py                 # Runs the full system (entry point)
│── audio_capture.py        # Records & processes microphone input
│── sound_classification.py # AI model for sound classification
│── led_control.py          # Controls Raspberry Pi LEDs
│── alert_system.py         # (Optional) Sends SMS alerts
│── model/                  
│   ├── sound_model.h5      # Trained AI model (if using custom training)
│── requirements.txt        # Dependencies for easy setup
│── README.md               # Explanation of how to run your project
=======
**AI-based Audio Surveillence System**

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt


# How it works:
Wake-Up Mode (wakeup.py) runs to detect loud sounds.
Once activated, it triggers raspi_ai.py.
raspi_ai.py does real-time audio classification and anomaly detection.
Offline logs are handled by offline_storage.py and sync periodically.
>>>>>>> 59ac4157cd6eb39591c802821dee1e2c6a16612a
