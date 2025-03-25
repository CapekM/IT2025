import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Parameters for generating data
num_samples = 300
mean_height = 170
std_height = 10
noise_level = 2
slope = 0.6
intercept = -15

heights = np.random.normal(mean_height, std_height, num_samples)
heights.sort()
weights = slope * heights + intercept + np.random.normal(0, noise_level, num_samples)

data = pd.DataFrame({'Height (cm)': heights, 'Weight (kg)': weights})
data = data.round(2)

# Visualize data
data.plot.scatter(x='Height (cm)', y='Weight (kg)')
plt.show()

# Train linear regression
model = LinearRegression()
model.fit(heights.reshape(-1, 1), weights)

# Predict for a new height
new_height = np.array([[176]])
print(f"Prediction for {new_height} is {model.predict(new_height)}")

# Visualize data
data.plot.scatter(x='Height (cm)', y='Weight (kg)')
plt.plot(heights, model.predict(heights.reshape(-1, 1)), color='red')
plt.show()

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Train NN
model = Sequential([
    Dense(64, input_shape=(1,), activation='relu'),  # Input layer with 10 neurons
    Dense(64, input_shape=(1,), activation='softplus'),  # Input layer with 10 neurons
    Dense(1)  # Output layer
])
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(heights, weights, epochs=100, verbose=1)

# Test the model with new data
test_X = np.array([[185.0], [175.0], [160.0]], dtype=np.float32)
predictions = model.predict(test_X)
print("Predictions:", predictions)


# Plot the original data and the model predictions
data.plot.scatter(x='Height (cm)', y='Weight (kg)')
plt.plot(heights, model.predict(heights.reshape(-1, 1)), color='red')
plt.show()
