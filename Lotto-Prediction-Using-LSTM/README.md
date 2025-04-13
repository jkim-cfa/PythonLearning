# Lottery Prediction Using LSTM

## Overview
This project utilizes a Long Short-Term Memory (LSTM) neural network to predict the next set of lottery numbers based on historical data. The model is trained on past winning numbers and attempts to identify patterns to forecast future results.

## Dataset Structure
The historical **1162** lottery data is stored in a CSV file named `lotto_data.csv`.

| Date       | Num1 | Num2 | Num3 | Num4 | Num5 | Num6 | BnusNo |
|------------|------|------|------|------|------|------|--------|
| 2023-01-01 |  5   | 12   | 23   | 34   | 35   | 45   |   8    |
| 2023-01-08 |  2   | 18   | 22   | 31   | 39   | 45   |   7    |

### Data Processing
1. Extract columns from the CSV.
2. Rename columns for consistency.
3. Sort the numbers in each row in ascending order to standardize the dataset.

## Preprocessing
1. The lottery numbers are **normalized** using `MinMaxScaler` to scale values between 0 and 1.
2. A sequence length of **52** is used to create input-output pairs for training. This is based on the assumption that one year consists of 52 weeks, making it a reasonable window for pattern detection.
3. The dataset is split into **80% training** and **20% validation** sets.

## Model Architecture
The model is built using TensorFlow's `Sequential` API with LSTM layers:

```md
| Layer   | Units | Activation | Additional Info |
|---------|-------|------------|----------------|
| LSTM    | 100   | ReLU       | Returns sequences |
| LSTM    | 50    | ReLU       | Final LSTM layer |
| Dense   | 7     | Linear     | Output layer |
```

The model is compiled with the **Adam** optimizer and **Mean Squared Error (MSE)** loss function.

## Training
- The model is trained for **20 epochs** with a batch size of **32**.
- Validation data is used to monitor performance.

## Prediction
- After training, the model makes a prediction based on the latest sequence of 52 draws.
- The output is transformed back to the original scale using `inverse_transform`.
- The predicted numbers are rounded to the nearest integers.

**The predicted next lottery numbers will be printed in the console:**
```
Predicted Next Lottery Numbers: [1 13 14 26 27 45 9]
```

