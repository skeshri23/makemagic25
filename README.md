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
