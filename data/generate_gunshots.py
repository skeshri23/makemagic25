import pandas as pd
from pydub import AudioSegment
from pydub.generators import Sine, WhiteNoise

# Load the CSV data
df = pd.read_csv('gunshots.csv')

# Initialize an empty AudioSegment to hold the entire audio
final_audio = AudioSegment.silent(duration=0)

# Iterate through each row in the CSV
for _, row in df.iterrows():
    start_time = row['start_seconds'] * 1000  # Convert to milliseconds
    end_time = row['end_seconds'] * 1000  # Convert to milliseconds
    duration = end_time - start_time  # Duration of the gunshot

    # Generate a sharp, loud gunshot sound (using a high-frequency sine wave for the impact)
    gunshot = Sine(1500).to_audio_segment(duration=100).fade_in(20).fade_out(150)

    # Add a burst of noise for the gunpowder effect (lower frequency white noise for a heavier sound)
    noise = WhiteNoise().to_audio_segment(duration=duration).fade_in(50).fade_out(200)
    noise = noise + 10  # Increase volume

    # Combine the gunshot with the noise for a more powerful, realistic effect
    shot = gunshot.overlay(noise)

    # If the shot is too short, extend it to ensure there are no crossfade issues
    if len(shot) < 100:  # Ensure the minimum shot length is 100ms
        shot = shot + (100 - len(shot))  # Extend it

    # Increase overall volume for a more impactful sound
    shot = shot + 20  # Increase the volume for better impact

    # Append shot to the final audio with 0ms crossfade (ensure no overlap)
    crossfade_duration = 0  # Set to 0ms crossfade for more clarity and to avoid overlap
    final_audio = final_audio.append(shot, crossfade=crossfade_duration)

# Save the final audio to a .wav file
final_audio.export("gunshots.wav", format="wav")

print("🔫 Gunshot sounds saved as 'gunshots.wav'!")
