import pandas as pd
from pydub import AudioSegment
from pydub.generators import Sine

# Load the CSV file
df = pd.read_csv("beeps.csv")

# Initialize an empty audio segment
final_audio = AudioSegment.silent(duration=0)

# Generate beep sound for each time interval
for index, row in df.iterrows():
    start_time = row["start_seconds"] * 1000  # Convert to milliseconds
    end_time = row["end_seconds"] * 1000  # Convert to milliseconds
    duration = end_time - start_time

    # Generate a beep sound (1000 Hz frequency)
    beep = Sine(1000).to_audio_segment(duration=duration)
    beep = beep.set_frame_rate(44100)  # Set standard sample rate

    # Append beep sound
    final_audio = final_audio.append(beep, crossfade=0)

# Export the final beeps sound as a WAV file
final_audio.export("beeps.wav", format="wav")

print("✅ Beeps sound file 'beeps.wav' created successfully!")
