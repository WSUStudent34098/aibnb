#!/usr/bin/env python3

import pandas as pd

# Read the cleaned data produced by clean.py
df = pd.read_csv("data/listings_clean.csv")

# Separate the target (price) from the predictors
y = df["price"]
X = df.drop(columns="price")
