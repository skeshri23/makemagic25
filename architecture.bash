AI_Audio_Surveillance/
│── data/                           # Folder for storing training data
│    ├── normal/                        # Normal sounds dataset
│    ├── emergency/                     # Distress sounds dataset
│── models/                         # Folder for storing trained models
│    ├── sound_model.pth                # Trained PyTorch model
│── scripts/                        # Python scripts for different tasks
│    ├── train.py                       # Model training script
│    ├── raspi_ai.py                    # Main Raspberry Pi AI script for real-time processing
│    ├── wakeup_detection.py            # Smart wake-up system (low-power mode)
│    ├── offline_storage.py             # Stores logs in local DB when offline
│── arduino/                        # If Arduino is used for control
│    ├── arduino_code.ino               # Arduino firmware
│── esp32/                          # If ESP32 is used
│    ├── esp32_code.ino                 # ESP32 firmware
│── .env                            # Environment variables (Supabase API keys)
│── requirements.txt                # Python dependencies
│── README.md                       # Project documentation
