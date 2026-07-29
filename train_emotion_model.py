import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical

# -------------------
# Load dataset
# -------------------
print("Loading dataset...")
data = pd.read_csv("dataset/fer2013.csv")  # path to dataset

# Convert pixel strings to numpy arrays
pixels = data['pixels'].tolist()
X = []
for pixel_sequence in pixels:
    pixels_array = np.array([int(p) for p in pixel_sequence.split()], dtype='float32')
    X.append(pixels_array)

X = np.array(X).reshape(-1, 48, 48, 1) / 255.0
y = to_categorical(data['emotion'])

# Split by Usage column
train_idx = data['Usage'] == 'Training'
val_idx   = data['Usage'] == 'PublicTest'
test_idx  = data['Usage'] == 'PrivateTest'

X_train, y_train = X[train_idx], y[train_idx]
X_val, y_val     = X[val_idx], y[val_idx]
X_test, y_test   = X[test_idx], y[test_idx]

print("Train:", X_train.shape, y_train.shape)
print("Validation:", X_val.shape, y_val.shape)
print("Test:", X_test.shape, y_test.shape)

# -------------------
# Build CNN model
# -------------------
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(48,48,1)),
    MaxPooling2D((2,2)),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D((2,2)),
    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D((2,2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(7, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# -------------------
# Train model
# -------------------
print("Training model...")
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=10,          # start small, later you can increase
    batch_size=64
)

# -------------------
# Evaluate
# -------------------
test_loss, test_acc = model.evaluate(X_test, y_test)
print("Test Accuracy:", test_acc)

# -------------------
# Save model
# -------------------
model.save("emotion_model.h5")
print("✅ Model saved as emotion_model.h5")

