# Lotto Prediction with XGBoost

## Overview
This project uses an XGBoost regression model to predict the next set of lottery numbers based on historical draw data. The model is trained using past lottery draw dates as the feature and the winning numbers as the target variables.

## Data Format
The historical 1162 lottery data is used. The project expects a CSV file named `lotto_data.csv` in the parent directory (`../lotto_data.csv`).

| Date       | Num1 | Num2 | Num3 | Num4 | Num5 | Num6 | BnusNo |
|------------|------|------|------|------|------|------|--------|
| 2023-01-01 |  5   | 12   | 23   | 34   | 35   | 45   |   8    |
| 2023-01-08 |  2   | 18   | 22   | 31   | 39   | 45   |   7    |


## How It Works
1. The script reads the historical lottery data from the CSV file.
2. It converts the draw date into a numeric format (days since the first draw).
3. The dataset is split into training and validation sets.
4. An XGBoost regressor model is trained to predict future lottery numbers based on past trends.
5. The model predicts the numbers for the next draw (7 days after the last recorded draw).
6. The predicted numbers are rounded to the nearest integers and displayed.

```bash
Predicted Next Lottery Numbers: [3 15 22 29 37 44 9]
```
