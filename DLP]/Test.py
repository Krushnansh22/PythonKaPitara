import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import OneHotEncoder

# Load the saved model
model = load_model('symbol_classifier_model.keras')

# Load the original dataset for reference
file_path = 'Symbols.csv'
data = pd.read_csv(file_path)

# Remove the image extensions


# Recreate the OneHotEncoder with the same training data
encoder = OneHotEncoder(sparse_output=False)
encoder.fit(data[['image_path']])

# Create a mapping for solutions based on their encoded values
solution_mapping = data[['solution']].drop_duplicates().reset_index(drop=True)


# Function to get user input for image paths (without extension)
def get_user_input():
    print("Please input the clean image path (without extension):")
    image_input = input("Image path: ")

    # Prepare the input data for the model
    new_input_df = pd.DataFrame({'image_path_clean': [image_input]})
    new_input_encoded = encoder.transform(new_input_df)

    return new_input_encoded


# Get the input from the user
new_input = get_user_input()

# Use the model to predict the solution
prediction = model.predict(new_input)
predicted_solution_index = np.argmax(prediction, axis=1)[0]

# Display the predicted cause and solution
predicted_solution = solution_mapping.iloc[predicted_solution_index]['solution']
print(f"Predicted solution: {predicted_solution}")
