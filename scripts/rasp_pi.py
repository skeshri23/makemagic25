import torch
import torchaudio
import torchaudio.transforms as transforms
import sounddevice as sd
import numpy as np
from supabase import create_client
import os

# Load the trained model
MODEL_PATH = "models/sound_model.pth"
model = torch.load(MODEL_PATH)
model.eval()

# Supabase credentials (stored in .env)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Audio recording parameters
SAMPLE_RATE = 16000
DURATION = 3  # 3 seconds per sample

# Define emergency categories based on AudioSet
LOW_EMERGENCY = ["alarm", "beep"]
MEDIUM_EMERGENCY = ["siren"]
HIGH_EMERGENCY = ["explosion", "gunshot"]

def record_audio():
    """Records audio for the given duration."""
    print("Listening for distress sounds...")
    audio = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1, dtype=np.float32)
    sd.wait()
    return torch.tensor(audio.T, dtype=torch.float32)

def process_audio(audio):
    """Converts audio to Mel Spectrogram."""
    transform = transforms.MelSpectrogram()
    return transform(audio.unsqueeze(0))

def classify_audio():
    """Records and classifies audio, sending an alert if necessary."""
    audio = record_audio()
    spectrogram = process_audio(audio)
    
    with torch.no_grad():
        output = model(spectrogram.unsqueeze(1))  # Add channel dimension
        prediction = torch.argmax(output).item()

    if prediction == 1:  # Detected emergency sound
        print("🚨 Emergency detected! Classifying severity...")
        classify_severity()
    else:
        print("✅ No emergency detected.")

def classify_severity():
    """Classify the severity of the emergency sound and send the appropriate alert."""
    audio = record_audio()
    spectrogram = process_audio(audio)
    
    with torch.no_grad():
        output = model(spectrogram.unsqueeze(1))
        predicted_labels = output.argmax(dim=1).item()
    
    if predicted_labels in LOW_EMERGENCY:
        print("🔰 Low Emergency detected! Sending alert...")
        send_alert("Low Emergency")
    elif predicted_labels in MEDIUM_EMERGENCY:
        print("⚠️ Medium Emergency detected! Sending alert...")
        send_alert("Medium Emergency")
    elif predicted_labels in HIGH_EMERGENCY:
        print("🔥 High Emergency detected! Sending alert...")
        send_alert("High Emergency")
    else:
        print("✅ No emergency sound detected.")

def send_alert(severity):
    """Sends an alert to Supabase."""
    alert_data = {
        "timestamp": str(pd.Timestamp.now()),
        "message": f"{severity} sound detected!",
        "status": "urgent"
    }
    supabase.table("alerts").insert(alert_data).execute()
    print("✅ Alert sent to Supabase!")

if __name__ == "__main__":
    while True:
        classify_audio()
