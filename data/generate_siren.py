import pandas as pd
from pydub import AudioSegment
from pydub.generators import Sine

# Load the CSV file
df = pd.read_csv("siren.csv")

# Initialize an empty audio segment
final_audio = AudioSegment.silent(duration=0)

# Generate siren sound with rising and falling frequency
for index, row in df.iterrows():
    start_time = row["start_seconds"] * 1000  # Convert to milliseconds
    end_time = row["end_seconds"] * 1000  # Convert to milliseconds
    duration = end_time - start_time

    # Generate a siren effect with oscillating frequency
    siren_segment = AudioSegment.silent(duration=0)

    for i in range(0, duration, 500):  # Change frequency every 500ms
        freq = 500 + (i % 1000)  # Frequency oscillates between 500Hz and 1500Hz
        beep = Sine(freq).to_audio_segment(duration=500)
        siren_segment += beep

    # Append siren sound
    final_audio = final_audio.append(siren_segment, crossfade=0)

# Export the final siren sound as a WAV file
final_audio.export("siren.wav", format="wav")

print("✅ Siren sound file 'siren.wav' created successfully!")
