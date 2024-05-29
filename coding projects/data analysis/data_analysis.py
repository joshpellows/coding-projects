import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
url = 'https://example-dataset-url.com/data.csv'
data = pd.read_csv(url)

# Display basic information about the dataset
print("Dataset Information:")
print(data.info())

# Display basic statistics
print("\nDataset Statistics:")
print(data.describe())

# Visualization: Distribution of a feature
plt.figure(figsize=(10, 6))
sns.histplot(data['feature_column'], kde=True)
plt.title('Distribution of Feature Column')
plt.xlabel('Feature Column')
plt.ylabel('Frequency')
plt.show()

# Visualization: Correlation heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Heatmap')
plt.show()