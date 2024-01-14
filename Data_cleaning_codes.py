#***Data cleaning***
import pandas as pd

df = pd.read_excel('C:\\Users\\ferid\\OneDrive\\Masaüstü\\Automobile_sales.xlsx')
df.head() #Show first 5 observation

# Assuming the first two rows are not part of the data, and actual column names start from the third row
df.columns = df.iloc[1]  # Set the second row as the header
df = df.drop(df.index[0:2])  # Drop the first two rows which are not part of the data

# Correct the column names for clarity
df.columns = [
    'Year', 'Month', 'Brand', 'Model', 'Type', 'Color',
    'Transmission', 'Fuel Type', 'Price', 'Kilometers', 'Units Sold'
]

# Apply string operations to string columns
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].astype(str).str.strip().str.title()

# Specifically strip spaces and remove quotes from 'Model' and 'Transmission'
df['Model'] = df['Model'].str.strip().str.replace('"', '')
df['Transmission'] = df['Transmission'].str.strip().str.replace('"', '')

# Convert 'Year' to numeric type and handle non-numeric values
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

# Convert 'Price', 'Kilometers', and 'Units Sold' to numeric types and handle missing values
for col in ['Price', 'Kilometers', 'Units Sold']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col].fillna(df[col].mean(), inplace=True)

# Replace negative values in 'Units Sold' with their absolute values
df['Units Sold'] = df['Units Sold'].apply(lambda x: abs(x) if x < 0 else x)

# Define a function to replace outliers with the mean
def replace_outliers_with_mean(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    mean_value = series.mean()
    return series.apply(lambda x: mean_value if x < lower_bound or x > upper_bound else x)

# Handle outliers in 'Price' and 'Kilometers'
df['Price'] = replace_outliers_with_mean(df['Price'])
df['Kilometers'] = replace_outliers_with_mean(df['Kilometers'])

# Create a date column from 'Year' and 'Month', if possible
df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'], format='%Y-%b', errors='coerce')

# Save the cleaned data to a new Excel file
df.to_excel('Project_data_set', index=False)

# Display the cleaned data
print(df.head())