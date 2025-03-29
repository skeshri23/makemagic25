import torch
import torchaudio
import torch.nn as nn
import torch.optim as optim
from torchaudio.transforms import MelSpectrogram
from torch.utils.data import DataLoader, Dataset
import os

# Hyperparameters
EPOCHS = 10
BATCH_SIZE = 16
LEARNING_RATE = 0.001

# Define custom dataset
class AudioDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.audio_files = [f for f in os.listdir(data_dir) if f.endswith(".wav")]
        self.labels = [0 if "normal" in f else 1 for f in self.audio_files]  # 0 = Normal, 1 = Emergency

    def __len__(self):
        return len(self.audio_files)

    def __getitem__(self, idx):
        filepath = os.path.join(self.data_dir, self.audio_files[idx])
        waveform, sample_rate = torchaudio.load(filepath)
        
        if self.transform:
            waveform = self.transform(waveform)
        
        label = self.labels[idx]
        return waveform, torch.tensor(label, dtype=torch.long)

# Define neural network
class SoundClassifier(nn.Module):
    def __init__(self):
        super(SoundClassifier, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(32 * 32 * 32, 128)
        self.fc2 = nn.Linear(128, 2)  # Two classes: normal and emergency

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = x.view(-1, 32 * 32 * 32)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def train_model():
    # Prepare dataset
    transform = MelSpectrogram()
    dataset = AudioDataset(data_dir="data/train", transform=transform)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    # Initialize model, loss, optimizer
    model = SoundClassifier()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # Training loop
    for epoch in range(EPOCHS):
        for batch_idx, (inputs, labels) in enumerate(dataloader):
            optimizer.zero_grad()
            outputs = model(inputs.unsqueeze(1))  # Add channel dimension
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            if batch_idx % 5 == 0:
                print(f"Epoch [{epoch+1}/{EPOCHS}], Step [{batch_idx+1}/{len(dataloader)}], Loss: {loss.item():.4f}")

    # Save model
    torch.save(model.state_dict(), "sound_model.pth")
    print("Model training complete. Saved as sound_model.pth")

if __name__ == "__main__":
    train_model()
