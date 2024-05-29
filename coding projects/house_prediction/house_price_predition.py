mport pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load dataset (assuming a CSV file with relevant data)
url = 'https://example-dataset-url.com/house_prices.csv'
data = pd.read_csv(url)

# Display the first few rows of the dataset
print("Dataset Preview:")
print(data.head())

# Define features and target variable
X = data[['num_rooms', 'lot_size', 'year_built']]  # Replace with actual feature column names
y = data['price']  # Replace with actual target column name

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Display actual vs predicted prices
results = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
print("\nActual vs Predicted Prices:")
print(results.head())

# Save the model for future use (optional)
import joblib
joblib.dump(model, 'house_price_model.pkl')
print("\nModel saved as house_price_model.pkl")