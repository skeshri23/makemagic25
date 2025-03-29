import pandas as pd
from pydub import AudioSegment
from pydub.generators import Sine, WhiteNoise

# Load the CSV data
df = pd.read_csv('gunshots.csv')

# Print the column names to ensure the CSV file has the correct headers
print("Columns in CSV:", df.columns)

# Initialize an empty AudioSegment to hold the entire audio
final_audio = AudioSegment.silent(duration=0)

# Iterate through each row in the CSV
for _, row in df.iterrows():
    start_time = row['start_seconds'] * 1000  # Convert to milliseconds
    end_time = row['end_seconds'] * 1000  # Convert to milliseconds
    duration = end_time - start_time  # Duration of the gunshot

    # Generate a sharp, loud gunshot sound (using a high-frequency sine wave for the impact)
    gunshot = Sine(1000).to_audio_segment(duration=100).fade_in(10).fade_out(50)

    # Add a burst of noise for the gunpowder effect
    noise = WhiteNoise().to_audio_segment(duration=duration // 2).fade_in(10).fade_out(150)
    noise = noise + 10  # Increase volume

    # Combine the gunshot with the noise for a realistic effect
    shot = gunshot.overlay(noise)

    # Increase overall volume for a more impactful sound
    shot = shot + 15  

    # Check if crossfade is larger than the shot duration and modify it accordingly
    crossfade_duration = 50
    if len(shot) < crossfade_duration:
        crossfade_duration = 0  # Disable crossfade if the audio segment is too short

    # Append shot to the final audio with an adjusted crossfade duration
    final_audio = final_audio.append(shot, crossfade=crossfade_duration)

# Save the final audio to a .wav file
final_audio.export("gunshots.wav", format="wav")

print("🔫 Gunshot sounds saved as 'gunshots.wav'!")
