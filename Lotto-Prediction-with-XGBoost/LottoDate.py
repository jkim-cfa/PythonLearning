import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import xgboost as xgb

# Load data
df = pd.read_csv("../lotto_data.csv")

df = df.iloc[:, :8]
df['Date'] = pd.to_datetime(df['Date'])
first_date = df['Date'].min()

# Convert dates to numeric values (days since first draw)
df['Date_Numeric'] = (df['Date'] - first_date).dt.days

# Lottery numbers (target variables)
Y = df.iloc[:, 1:8].values

# Date as a feature (no need to scale)
X = df['Date_Numeric'].values.reshape(-1, 1)

# Split data into training and validation sets
X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.2, random_state=42)

# Train XGBoost model
xgb_model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=500)
xgb_model.fit(X_train, Y_train)

# Predict for the next draw (7 days after last recorded draw)
next_date_numeric = df['Date_Numeric'].max() + 7
next_date = np.array([[next_date_numeric]])

# Predict lottery numbers
predicted_numbers = xgb_model.predict(next_date)

# Convert predictions to integers
predicted_numbers = np.round(predicted_numbers).astype(int)

print("Predicted Next Lottery Numbers:", predicted_numbers)
