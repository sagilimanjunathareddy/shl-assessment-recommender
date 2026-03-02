import pandas as pd
import os

# Path to your uploaded Excel file
file_path = "Gen_AI Dataset.xlsx"

# Create folders if not exist
os.makedirs("data/train", exist_ok=True)
os.makedirs("data/test", exist_ok=True)

# Load sheets
train_df = pd.read_excel(file_path, sheet_name="Train-Set")
test_df = pd.read_excel(file_path, sheet_name="Test-Set")

# Save as CSV
train_df.to_csv("data/train/labeled_train.csv", index=False)
test_df.to_csv("data/test/unlabeled_test.csv", index=False)

print("Datasets successfully prepared.")