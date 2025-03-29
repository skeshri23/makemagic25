import pandas as pd
import os
import librosa
import soundfile as sf
from tqdm import tqdm

# Function to convert audio from CSV to WAV format
def convert_csv_to_wav(csv_file, output_dir):
    # Read the CSV file
    try:
        print(f"Processing CSV file: {csv_file}")
        data = pd.read_csv(csv_file, comment='#', on_bad_lines='skip')  # Updated argument here

        # Check the column names to debug
        print("CSV Columns:", data.columns)

        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Iterate over rows to extract and process audio data
        for index, row in tqdm(data.iterrows(), total=data.shape[0]):
            yt_id = row['YTID']  # Check if 'YTID' exists or if it needs to be renamed
            start_time = row['start_seconds']
            end_time = row['end_seconds']
            labels = row['positive_labels'].split(',')  # Labels might be separated by commas
            print(f"Processing audio for YTID: {yt_id} from {start_time}s to {end_time}s")

            # Placeholder URL (replace this with actual YouTube API URL or download method)
            audio_url = f"http://path_to_audio/{yt_id}.mp3"  # Replace with actual URL or downloading method

            # Download the audio if it is not already downloaded
            audio_file = os.path.join(output_dir, f"{yt_id}.mp3")
            if not os.path.exists(audio_file):
                download_audio(audio_url, audio_file)

            # Load the audio file
            try:
                audio, sr = librosa.load(audio_file, sr=None, offset=start_time, duration=end_time - start_time)
                
                # Define the WAV file name based on YTID
                wav_file = os.path.join(output_dir, f"{yt_id}_{start_time}_{end_time}.wav")

                # Save the extracted audio as WAV
                sf.write(wav_file, audio, sr)
                print(f"Saved {wav_file}")

            except Exception as e:
                print(f"Error processing {yt_id}: {e}")

    except Exception as e:
        print(f"Error reading CSV: {e}")

# Example usage
csv_files = [
    "data/green/beeps.csv",
    "data/green/firealarms.csv",
    "data/yellow/sirens.csv",
    "data/red/explosions.csv",
    "data/red/gunshots.csv"
]

output_dir = "data/converted_audio"  # Change this as needed

# Loop over CSV files
for csv_file in csv_files:
    convert_csv_to_wav(csv_file, output_dir)
