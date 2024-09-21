import pandas as pd
import os

# Define a function to load datasets with error handling
def load_dataset(filepath):
    try:
        df = pd.read_csv(filepath, on_bad_lines='skip')  # Use on_bad_lines for handling bad lines
        print(f"Loaded {filepath} with columns: {df.columns.tolist()}")
        return df
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# Load datasets
google_df = load_dataset('public/google_dataset.csv')
facebook_df = load_dataset('public/facebook_dataset.csv')
website_df = load_dataset('public/website_dataset.csv')

# Normalize phone numbers
def normalize_phone(df):
    if 'phone' in df.columns:
        df['phone'] = df['phone'].str.replace(r'\D', '', regex=True)  # Keep only digits
    return df

google_df = normalize_phone(google_df)
facebook_df = normalize_phone(facebook_df)
website_df = normalize_phone(website_df)

# Merge on 'city'
merge_on_columns = ['city']  # Merging based on the 'city' column

# Check if the merging column exists in at least one DataFrame
if 'city' in google_df.columns or 'city' in facebook_df.columns or 'city' in website_df.columns:
    
    # Merging the datasets
    merged_df = google_df.merge(facebook_df, on=merge_on_columns, how='outer', suffixes=('_google', '_facebook'))
    merged_df = merged_df.merge(website_df, on=merge_on_columns, how='outer', suffixes=('', '_website'))

    # Conflict Resolution for phone numbers
    def resolve_conflicts(row):
        google_phone = row.get('phone_google')
        facebook_phone = row.get('phone_facebook')
        website_phone = row.get('phone')
        
        # Prioritize Google, then Facebook, then Website
        return google_phone if pd.notna(google_phone) else (facebook_phone if pd.notna(facebook_phone) else website_phone)

    merged_df['phone'] = merged_df.apply(resolve_conflicts, axis=1)

    # Select relevant columns for the final dataset
    final_columns = ['city', 'category', 'phone', 'country_name', 'zip_code']
    final_df = merged_df[final_columns]

    # Save the merged dataset to a CSV file
    output_path = os.path.join('public', 'merged_dataset.csv')
    final_df.to_csv(output_path, index=False)
    print("Merged dataset created at:", output_path)
else:
    print("No valid data available for merging.")
