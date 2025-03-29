from flask import Flask
import os

app = Flask(__name__)

@app.route("/wakeup", methods=["GET"])
def wakeup():
    print("🚀 Wake-up signal received! Activating AI processing...")
    os.system("python3 raspi_ai.py &")  # Runs AI script in the background
    return "AI Activated", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Raspberry Pi listens on port 5000
