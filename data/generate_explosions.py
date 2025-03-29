import pandas as pd
from pydub import AudioSegment
from pydub.generators import Sine, WhiteNoise
import random

# Load the CSV data
df = pd.read_csv('explosions.csv')

# Initialize an empty AudioSegment to hold the entire audio
final_audio = AudioSegment.silent(duration=0)

# Iterate through each row in the CSV
for _, row in df.iterrows():
    start_time = row['start_seconds'] * 1000  # Convert to milliseconds
    end_time = row['end_seconds'] * 1000  # Convert to milliseconds
    duration = end_time - start_time  # Explosion duration

    # Ensure that the duration is positive and above zero (in case of any zero-duration error)
    if duration > 0:
        # Generate a deep bass thud (low-frequency explosion)
        bass = Sine(random.randint(40, 60)).to_audio_segment(duration=duration).fade_in(50).fade_out(500)
        
        # Add a white noise burst to simulate the "blast" effect with random amplitude for more randomness
        blast_duration = duration // 2
        blast = WhiteNoise().to_audio_segment(duration=blast_duration).fade_in(30).fade_out(200)
        
        # Overlay the bass thud and the blast
        explosion = bass.overlay(blast - random.randint(5, 10))  # Add randomness to the blast volume
        
        # Increase the volume significantly for impact
        explosion = explosion + random.randint(10, 15)  # Randomly adjust volume for a varied impact

        # Append the explosion sound to the final audio with no crossfade (0ms)
        final_audio = final_audio.append(explosion, crossfade=0)

# Save the final audio to a .wav file
final_audio.export("explosions_louder.wav", format="wav")

print("💥 Explosion sounds saved as 'explosions_louder.wav'!")
