import pandas as pd
import skops.io as sio
import os
import subprocess
import sys

# Check for saved model. If there's no model, run clean.py and train.py

modelPath = "data/model.skops"
cleanPath = "data/listings_clean.csv"

if not os.path.exists(modelPath):
    print("No saved model found.", flush=True)

    if not os.path.exists(cleanPath):
        print("\nCleaning data...\n", flush=True)
        subprocess.run([sys.executable, "clean.py"], check=True)

    print("Training model...\n", flush=True)

    subprocess.run([sys.executable, "train.py"], check=True)

    print("Model training complete!\n", flush=True)

model = sio.load(modelPath, trusted=[])

# Prompt user for and validate 5 input values

latitude = 0
longitude = 0
roomType = ""
minNights = 0
numOfReviews = 0

latitude = float(input("Latitude: "))

while latitude < 47.4 or latitude > 47.8:
    latitude = float(input("Input latitude between 47.4 and 47.8: "))

longitude = float(input("Longitude: "))

while longitude < -122.5 or longitude > -122.2:
    longitude = float(input("Input longitude between -122.5 and -122.2: "))

print("Room Types:")
print("1. Entire home/apt")
print("2. Hotel room")
print("3. Private room")
print("4. Shared room")

roomType = int(input("Room Type (1-4): "))

while roomType < 1 or roomType > 4:
    roomType = int(input("Input room type between 1 and 4: "))

if roomType == 1:
    roomType = "Entire home/apt"
elif roomType == 2:
    roomType = "Hotel room"
elif roomType == 3:
    roomType = "Private room"
else:
    roomType = "Shared room"

minNights = int(input("Minimum Nights: "))

while minNights < 1:
    minNights = int(input("Minimum Nights must be at least 1: "))

numOfReviews = int(input("Number of Reviews: "))

while numOfReviews < 0:
    numOfReviews = int(input("Number of Reviews cannot be negative: "))

# Convert the inputs into a pandas DataFrame with the exact column names expected by the model

listing = pd.DataFrame([{
    "latitude": latitude,
    "longitude": longitude,
    "room_type": roomType,
    "minimum_nights": minNights,
    "number_of_reviews": numOfReviews
}])

# Call model.predict() and print the estimated nightly price

prediction = model.predict(listing)[0]

print(f"Predicted Price: ${prediction:.2f}")
