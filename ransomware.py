import streamlit as st
import numpy as np
import pandas as pd
import warnings
import joblib

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

warnings.filterwarnings(action="ignore")

# Load dataset
csv_path = r"C:\Users\salom\OneDrive\Desktop\ransomware\data_file.csv"
df = pd.read_csv(csv_path)

# Streamlit Title
st.markdown("<h1 style='text-align: center;'>Ransomware Attack Detection</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='background-color: black; text-align: center;'>Streamlit Ransomware Classifier</h2>", unsafe_allow_html=True)

# Drop unnecessary columns
cols_to_drop = ['FileName', 'md5Hash']
df = df.drop(columns=[col for col in cols_to_drop if col in df.columns], errors='ignore')

# Convert categorical features to numerical
categorical_columns = ["Machine", "DebugSize", "NumberOfSections", "SizeOfStackReserve", "MajorOSVersion", "BitcoinAddresses"]
for col in categorical_columns:
    if col in df.columns:
        df[col] = df[col].astype('category').cat.codes

# Drop duplicates and save the processed dataset
df.drop_duplicates(keep='last', inplace=True)
df.to_csv("df_clear.csv", index=False)

# Reload the cleaned dataset
df = pd.read_csv("df_clear.csv")

# Define selected features (all except the target column)
selected_feature_names = df.columns[:-1].tolist()  # Exclude the last column (target)

# Extract features (X) and labels (Y)
X = df[selected_feature_names].values  # Use all feature columns
Y = df.iloc[:, -1].values  # Use the last column as the target

# Split data: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

# Create and train an ANN classifier
ann = MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=0)
ann.fit(X_train, y_train)

# Save the trained model
joblib.dump(ann, "best_model.pkl")

# Malware Prediction Section
st.write("## Predict Malware Attack")

# Load Trained Best Model
model = joblib.load("best_model.pkl")

st.write("### Enter Feature Values for Prediction")

# Collect User Input for Features
user_inputs = {}
for col in selected_feature_names:
    user_inputs[col] = st.number_input(f"{col}", value=0.0)

# Convert User Inputs to NumPy Array
input_data = np.array(list(user_inputs.values())).reshape(1, -1)

# Predict Button
if st.button("Predict"):
    prediction = model.predict(input_data)
    st.success(f" The predicted malware category is: **{prediction[0]}**")

import sys
print(sys.executable)
print(sys.path)
