import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# Reproducible random data
np.random.seed(42)

# Generate synthetic student dataset
number_of_students = 1000

study_hours = np.random.uniform(0, 10, number_of_students)
attendance = np.random.uniform(40, 100, number_of_students)
previous_marks = np.random.uniform(30, 100, number_of_students)
assignments = np.random.uniform(0, 10, number_of_students)
sleep_hours = np.random.uniform(4, 10, number_of_students)

X = np.column_stack([
    study_hours,
    attendance,
    previous_marks,
    assignments,
    sleep_hours
])

# Generate realistic target marks
marks = (
    study_hours * 3 +
    attendance * 0.20 +
    previous_marks * 0.45 +
    assignments * 1.5 +
    sleep_hours * 1.2 +
    np.random.normal(0, 4, number_of_students)
)

marks = np.clip(marks, 0, 100)

# Train model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, marks)

# Create model folder
os.makedirs("model", exist_ok=True)

# Save model
joblib.dump(model, "model/student_model.pkl")

print("Model trained successfully!")
print("Model saved to model/student_model.pkl")
