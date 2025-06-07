import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

# Load the CSV file
file_path = 'Symbols.csv'
data = pd.read_csv(file_path)

# Remove the image extensions

# One-Hot Encode the 'image_path_clean' column
encoder = OneHotEncoder(sparse_output=False)
image_path_encoded = encoder.fit_transform(data[['image_path']])

# Prepare the labels for causes and solutions
# Assuming the 'solution' column has categorical data to predict
solutions = data['solution'].astype('category')
solutions_encoded = solutions.cat.codes  # Convert to numeric codes

# Prepare labels for causes (if applicable, here we assume causes are in the 'label' column)
causes = to_categorical(data['label'])

# Train-Test Split (using causes for input and solutions for output)
X_train, X_test, y_train, y_test = train_test_split(image_path_encoded, solutions_encoded, test_size=0.2, random_state=42)

# Build a simple Neural Network
model = Sequential()
model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))  # Input layer
model.add(Dense(32, activation='relu'))  # Hidden layer
model.add(Dense(len(solutions.cat.categories), activation='softmax'))  # Output layer for solutions

# Compile the model
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=20, batch_size=8, validation_data=(X_test, y_test), verbose=2)

# Save the model
model.save("symbol_classifier_model.keras")
print("Model saved as 'symbol_classifier_model.keras'")
