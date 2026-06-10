
import os
import pickle
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ==========================================
# START
# ==========================================

print("=" * 50)
print("Starting Omminsentiry AI Training")
print("=" * 50)

# ==========================================
# CREATE MODELS FOLDER
# ==========================================

os.makedirs("models", exist_ok=True)

# ==========================================
# SAMPLE TRAINING DATA
# ==========================================

data = pd.DataFrame({

    "domain_age_days": [
        5,
        30,
        60,
        180,
        365,
        1000,
        2000,
        5000,
        7000,
        9000
    ],

    "ssl": [
        0,
        0,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1
    ],

    "label": [
        0,  # suspicious
        0,
        0,
        1,  # trusted
        1,
        1,
        1,
        1,
        1,
        1
    ]
})

# ==========================================
# FEATURES
# ==========================================

X = data[
    [
        "domain_age_days",
        "ssl"
    ]
]

y = data["label"]

# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# ==========================================
# RANDOM FOREST MODEL
# ==========================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# ==========================================
# TRAIN MODEL
# ==========================================

model.fit(
    X_train,
    y_train
)

# ==========================================
# EVALUATE MODEL
# ==========================================

predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(f"Model Accuracy: {accuracy:.2f}")

# ==========================================
# SAVE MODEL
# ==========================================

model_path = "models/trust_model.pkl"

with open(model_path, "wb") as f:

    pickle.dump(
        model,
        f
    )

print(f"Model saved: {model_path}")

# ==========================================
# TEST MODEL
# ==========================================

sample_prediction = model.predict([
    [3650, 1]
])

print(
    f"Sample Prediction: {sample_prediction[0]}"
)

print("=" * 50)
print("Training Complete")
print("=" * 50)

