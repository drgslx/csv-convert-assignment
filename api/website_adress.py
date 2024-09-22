import os
import pandas as pd

# Load the CSV file with the correct path, using the correct separator
file_path = os.path.join('public', 'website_dataset.csv')  # Adjust the path to your CSV file
df = pd.read_csv(file_path, sep=';', on_bad_lines='skip')  # Adjusting separator to semicolon

# Print the column names to check what's available in the dataset
print("Column names in the dataset:", df.columns)

# Clean column names by stripping whitespace
df.columns = df.columns.str.strip()

# Combine 'main_city', 'main_region', and 'main_country' into a new column called 'address', keeping blanks if missing
address_columns = ['main_city', 'main_region', 'main_country']
# Check which columns exist in the DataFrame
existing_columns = [col for col in address_columns if col in df.columns]

# Create the 'address' column only from existing columns
df['address'] = df[existing_columns].apply(lambda x: ', '.join(x.dropna()), axis=1)

# Drop the original columns that were combined into 'address'
df = df.drop(columns=existing_columns)

# Save the updated CSV file
output_file_path = 'public/website_dataset_with_address.csv'
df.to_csv(output_file_path, index=False)

print(f"File saved as {output_file_path}")
