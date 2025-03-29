import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import librosa
import numpy as np
from sklearn.model_selection import train_test_split

# Ensure the models directory exists
os.makedirs('models', exist_ok=True)

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

class SoundDataset(Dataset): #error
    def __init__(self, audio_files, labels, max_length=3000):
        self.audio_files = audio_files
        self.labels = labels
        self.max_length = max_length  # Maximum length for padding/truncating

    def __len__(self):
        return len(self.audio_files)

    def __getitem__(self, idx):
        audio_file = self.audio_files[idx]
        label = self.labels[idx]

        # Load audio file using librosa
        audio, sr = librosa.load(audio_file, sr=None)
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        
        # Ensure the shape is (1, 13, time_steps) for the Conv1d layer
        mfcc = np.expand_dims(mfcc, axis=0)  # Shape becomes (1, 13, time_steps)

        # Padding or truncating the MFCC to a fixed size
        if mfcc.shape[2] < self.max_length:
            # Pad with zeros
            padding = self.max_length - mfcc.shape[2]
            mfcc = np.pad(mfcc, ((0, 0), (0, 0), (0, padding)), mode='constant')
        else:
            # Truncate
            mfcc = mfcc[:, :, :self.max_length]

        return torch.tensor(mfcc).float().to(device), torch.tensor(label).long().to(device)




# Function to load dataset
def load_data(data_dir):
    audio_files = []
    labels = []
    categories = ['green', 'red', 'yellow']

    # Iterate through the main folders (green, red, yellow)
    for label, category in enumerate(categories):
        folder_path = os.path.join(data_dir, category)
        print(f"Checking folder: {folder_path}")  # This helps verify the folder structure

        if os.path.exists(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.wav'):  # Make sure it's a .wav file
                    audio_files.append(os.path.join(folder_path, file_name))
                    labels.append(label)

    return audio_files, labels


# Load data
data_dir = 'data'  # Assuming all the folders (green, red, yellow) are under '/data'
audio_files, labels = load_data(data_dir)

# Check if any files were loaded
if not audio_files:
    print("No audio files found in the specified directories.")
    exit()

# Split dataset
train_files, val_files, train_labels, val_labels = train_test_split(audio_files, labels, test_size=0.2, random_state=42)

# Create dataset objects
train_dataset = SoundDataset(train_files, train_labels)
val_dataset = SoundDataset(val_files, val_labels)

# Create DataLoader objects
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Define model (using the same model as earlier)
class SoundClassifier(nn.Module):
    def __init__(self):
        super(SoundClassifier, self).__init__()
        self.conv1 = nn.Conv1d(13, 64, kernel_size=3)
        self.conv2 = nn.Conv1d(64, 128, kernel_size=3)
        self.fc1 = nn.Linear(128 * 9, 256)
        self.fc2 = nn.Linear(256, 3)  # Output 3 classes (green, red, yellow)

    def forward(self, x):
        x = x.unsqueeze(1)  # Add channel dimension for 1D conv
        x = nn.functional.relu(self.conv1(x))
        x = nn.functional.max_pool1d(x, 2)
        x = nn.functional.relu(self.conv2(x))
        x = nn.functional.max_pool1d(x, 2)
        x = x.view(x.size(0), -1)  # Flatten for fully connected layers
        x = nn.functional.relu(self.fc1(x))
        x = self.fc2(x)
        return x


# Initialize model, move to device
model = SoundClassifier().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    correct_preds = 0
    total_preds = 0
    
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        
        outputs = model(inputs)
        
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        
        _, predicted = torch.max(outputs, 1)
        correct_preds += (predicted == labels).sum().item()
        total_preds += labels.size(0)
    
    train_loss = running_loss / len(train_loader)
    train_accuracy = correct_preds / total_preds * 100
    
    # Validation
    model.eval()
    val_loss = 0.0
    correct_preds = 0
    total_preds = 0
    
    with torch.no_grad():
        for inputs, labels in val_loader:
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            val_loss += loss.item()
            
            _, predicted = torch.max(outputs, 1)
            correct_preds += (predicted == labels).sum().item()
            total_preds += labels.size(0)
    
    val_loss = val_loss / len(val_loader)
    val_accuracy = correct_preds / total_preds * 100
    
    print(f'Epoch {epoch+1}/{num_epochs}, '
          f'Train Loss: {train_loss:.4f}, Train Accuracy: {train_accuracy:.2f}%, '
          f'Val Loss: {val_loss:.4f}, Val Accuracy: {val_accuracy:.2f}%')

# Save trained model
model_path = 'models/sound_model.pth'
torch.save(model.state_dict(), model_path)
print(f"Model saved to {model_path}")
