import pandas as pd
from pydub import AudioSegment
from pydub.generators import Sine, WhiteNoise

# Load the CSV data
df = pd.read_csv('explosions.csv')

# Initialize an empty AudioSegment to hold the entire audio
final_audio = AudioSegment.silent(duration=0)

# Iterate through each row in the CSV
for _, row in df.iterrows():
    start_time = row['start_seconds'] * 1000  # Convert to milliseconds
    end_time = row['end_seconds'] * 1000  # Convert to milliseconds
    duration = end_time - start_time  # Explosion duration

    # Generate a deep bass thud (low-frequency explosion)
    bass = Sine(50).to_audio_segment(duration=duration).fade_in(50).fade_out(300)
    
    # Add a white noise burst to simulate the "blast" effect
    blast = WhiteNoise().to_audio_segment(duration=duration // 2).fade_in(30).fade_out(200)
    
    # Combine the bass thud and the blast
    explosion = bass.overlay(blast - 10)  # Reduce noise volume slightly

    # Increase volume for impact
    explosion = explosion + 5

    # Append the explosion sound to the final audio
    final_audio = final_audio.append(explosion, crossfade=0)

# Save the final audio to a .wav file
final_audio.export("explosions.wav", format="wav")

print("💥 Explosion sounds saved as 'explosions.wav'!")
