import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Dummy data for training
data = {
    'credit': [1000, 200, 3000, 50, 10000, 500, 70],
    'debit': [0, 500, 0, 60, 0, 700, 5000],
    'balance': [5000, 2000, 10000, 100, 20000, 1000, 100],
    'is_fraud': [0, 1, 0, 1, 0, 1, 1]
}

df = pd.DataFrame(data)

# Prepare training data
X = df[['credit', 'debit', 'balance']]
y = df['is_fraud']

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, 'ml_model.pkl')
print("✅ ML model saved as 'ml_model.pkl'")

