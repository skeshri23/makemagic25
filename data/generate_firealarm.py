import pandas as pd
from pydub import AudioSegment
from pydub.generators import Sine

# Load the CSV data
df = pd.read_csv('fire_alarm.csv')

# Initialize an empty AudioSegment to hold the entire audio
final_audio = AudioSegment.silent(duration=0)

# Iterate through each row in the CSV
for _, row in df.iterrows():
    start_time = row['start_seconds'] * 1000  # Convert to milliseconds
    end_time = row['end_seconds'] * 1000  # Convert to milliseconds

    # Create a high-pitched fire alarm beep (3000 Hz)
    beep = Sine(3000).to_audio_segment(duration=(end_time - start_time))  
    beep = beep.set_frame_rate(44100)  # Standard audio sample rate

    # Append the beep sound to the final audio
    final_audio = final_audio.append(beep, crossfade=0)

# Save the final audio to a .wav file
final_audio.export("fire_alarm.wav", format="wav")

print("🔥 Fire alarm sound saved as 'fire_alarm.wav'!")
