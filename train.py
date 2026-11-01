#!/usr/bin/env python3

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Fixed seed so every run produces the same split
SEED = 437

# Read the cleaned data produced by clean.py
df = pd.read_csv("data/listings_clean.csv")

# Separate the target (price) from the predictors
y = df["price"]
X = df.drop(columns="price")

# Hold out 20% for testing, stratified by room type so the rare
# hotel and shared rooms land in both sets
X_train, X_test, y_train, y_test = train_test_split(
	X, y, test_size=0.2, random_state=SEED, stratify=X["room_type"]
)

# Make sure every room type has at least 2 rows in both sets
room_types = X["room_type"].unique()
for name, part in (("train", X_train), ("test", X_test)):
	# reindex so a room type with no rows still shows up, as 0
	counts = part["room_type"].value_counts().reindex(room_types, fill_value=0)
	too_few = counts[counts < 2]
	assert too_few.empty, f"room types with fewer than 2 {name} rows: {too_few.to_dict()}"

# Every predictor except room type is numeric
numeric_columns = X.columns.drop("room_type")

# One-hot encode room type and scale the numeric columns. Dropping the
# first room type (entire home/apt) makes it the baseline the others
# are compared against
prep = ColumnTransformer([
	("encode", OneHotEncoder(drop="first"), ["room_type"]),
	("scale", StandardScaler(), numeric_columns),
])

# Preprocessing followed by linear regression
model = Pipeline([
	("prep", prep),
	("model", LinearRegression()),
])

# Train the model; the encoder and scaler learn only from the training rows
model.fit(X_train, y_train)
