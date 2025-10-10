import subprocess
import time
from PIL import ImageGrab

# Start the application
process = subprocess.Popen(["python3", "main.py"])

# Give the application time to load
time.sleep(5)

# Take a screenshot
screenshot = ImageGrab.grab()
screenshot.save("jules-scratch/verification/verification.png")

# Terminate the application
process.terminate()
process.wait()