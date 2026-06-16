# Copyright (c) 2026, Ebi Emmrich-Adehor. All rights reserved.

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

# ==========================================
# SAMPLE TRAINING DATA
# ==========================================

# Features:
# 1. registered (0 or 1)
# 2. domain_age_days (int)
# 3. ssl (0 or 1)
# 4. reputation_score (0-100)
# 5. trust_score (0-100)
# Label: 0 (suspicious / high risk), 1 (trusted / safe)

training_data = [
    # Trusted / Safe Domains
    [1, 5000, 1, 100, 100, 1],
    [1, 2500, 1, 100, 100, 1],
    [1, 1200, 1, 100, 100, 1],
    [1, 365, 1, 100, 95, 1],
    [1, 500, 1, 90, 90, 1],
    [1, 720, 1, 100, 100, 1],
    [1, 4000, 1, 100, 100, 1],
    [1, 180, 1, 100, 90, 1],
    [1, 200, 1, 90, 85, 1],
    [1, 300, 1, 100, 95, 1],
    [1, 1500, 1, 100, 100, 1],
    [1, 2200, 1, 95, 95, 1],
    [1, 1800, 1, 100, 100, 1],
    [1, 3650, 1, 100, 100, 1],
    [1, 450, 1, 100, 95, 1],
    [1, 95, 1, 100, 90, 1],
    [1, 120, 1, 80, 80, 1],
    [1, 150, 0, 100, 70, 1], # Older domain, no SSL, but clean
    
    # Suspicious / Malicious Domains
    [1, 5, 0, 50, 15, 0],
    [1, 12, 1, 25, 30, 0],
    [1, 2, 0, 100, 45, 0],
    [1, 45, 1, 25, 40, 0],
    [1, 60, 0, 50, 30, 0],
    [1, 180, 1, 20, 45, 0],
    [1, 90, 0, 75, 45, 0],
    [1, 15, 1, 60, 40, 0],
    [1, 30, 1, 25, 30, 0],
    [1, 8, 0, 60, 20, 0],
    [1, 45, 0, 25, 20, 0],
    [1, 365, 0, 25, 40, 0],
    [1, 730, 0, 60, 55, 0],
    [1, 1000, 1, 20, 40, 0],
    
    # Unregistered Domains
    [0, 0, 0, 100, 10, 0],
    [0, 0, 0, 80, 10, 0],
    [0, 0, 1, 100, 10, 0],
    [0, 0, 0, 50, 10, 0]
]

data = pd.DataFrame(
    training_data,
    columns=[
        "registered",
        "domain_age_days",
        "ssl",
        "reputation_score",
        "trust_score",
        "label"
    ]
)

# ==========================================
# FEATURES
# ==========================================

X = data[
    [
        "registered",
        "domain_age_days",
        "ssl",
        "reputation_score",
        "trust_score"
    ]
]

y = data["label"]

# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
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

# Test with a trusted website: Registered, 10 years old, SSL, 100 reputation, 100 score
sample_prediction = model.predict([
    [1, 3650, 1, 100, 100]
])

print(
    f"Sample Trusted Domain Prediction: {sample_prediction[0]}"
)

# Test with a phishing website: Registered, 5 days old, SSL, 25 reputation, 30 score
phishing_prediction = model.predict([
    [1, 5, 1, 25, 30]
])

print(
    f"Sample Phishing Domain Prediction: {phishing_prediction[0]}"
)

print("=" * 50)
print("Training Complete")
print("=" * 50)

