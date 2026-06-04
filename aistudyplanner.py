import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import pickle

# Load dataset
df = pd.read_csv("study_planner_10k.csv")

print(df.head())
print(df.info())
print(df.isnull().sum())

# Encode study_type
df['study_type'] = df['study_type'].map({
    'Theory': 1,
    'Conceptual': 2,
    'Practical': 3
})

# Feature Engineering
df['priority_score'] = (df['difficulty'] * df['importance']) / df['deadline_days']

# Features
X = df[['difficulty', 'hours_available', 'deadline_days', 'importance', 'study_type', 'previous_score', 'priority_score']]
y = df['actual_hours_needed']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestRegressor(n_estimators=150, random_state=42)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print("MAE:", mean_absolute_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))

# Save model
pickle.dump(model, open("model.pkl", "wb"))
print("Model saved as model.pkl")
