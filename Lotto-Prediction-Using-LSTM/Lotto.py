import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# Load data
df = pd.read_csv("../lotto_data.csv")

# Keep only the first 8 columns
df = df.iloc[:, 1:8]
# Rename columns
df.columns = ['Num1', 'Num2', 'Num3', 'Num4', 'Num5', 'Num6', 'BnusNo']

# Convert to NumPy array
data = df.values

# Normalize the data
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# Create sequences
sequence_length = 52
X, y = [], []

for i in range(sequence_length, len(data_scaled)):
    X.append(data_scaled[i - sequence_length:i])
    y.append(data_scaled[i])  # The next set to predict

# Convert to numpy arrays
X, y = np.array(X), np.array(y)

# Split into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the LSTM model
model = Sequential([
    LSTM(100, activation='relu', return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
    LSTM(50, activation='relu'),
    Dense(7)
])

# Compile the model
model.compile(optimizer='adam', loss='mse')

# Train the model
history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_val, y_val))

# Make prediction for the next set
last_sequence = X[-1].reshape(1, X.shape[1], X.shape[2])
predicted_scaled = model.predict(last_sequence)

# Convert back to original scale
predicted_numbers = scaler.inverse_transform(predicted_scaled).flatten()

# Round to nearest integers
predicted_numbers = np.round(predicted_numbers).astype(int)

print("Predicted Next Lottery Numbers:", predicted_numbers)
