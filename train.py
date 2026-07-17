import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# 1. Load the dataset you generated
df = pd.read_csv('hostel_laundry_data.csv')

# 2. Select Features (Inputs) and Target (Output)
# We want to predict 'ActualDuration' based on the time and day
X = df[['DayOfWeek', 'Hour', 'CurrentQueueLength']]
y = df['ActualDuration']

# 3. Split data into Training (80%) and Testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Initialize and Train the Model
# Random Forest is great for catching non-linear patterns (like evening rushes)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Check accuracy
predictions = model.predict(X_test)
error = mean_absolute_error(y_test, predictions)
print(f"Model Training Complete!")
print(f"Average Prediction Error: {round(error, 2)} minutes")

# 6. Save the trained model to a file (Pickle)
# This allows our App to use the 'brain' without retraining it every time
with open('laundry_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model saved as 'laundry_model.pkl'")