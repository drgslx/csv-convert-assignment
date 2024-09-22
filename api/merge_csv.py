import os
import pandas as pd

# Define file paths
csv_files = {
    'google': os.path.join('public', 'google_dataset.csv'),
    'website': os.path.join('public', 'website_dataset.csv'),
    'facebook': os.path.join('public', 'facebook_dataset.csv'),
    'website_address': os.path.join('public', 'website_dataset_with_address.csv'),  # Add this line
    'merged': os.path.join('public', 'merged_dataset.csv'),
}

def ensure_plus_prefix(phone):
    """Ensure that the phone number has a '+' prefix."""
    if pd.isna(phone):
        return phone  # Return NaN as is
    phone_str = str(phone).strip()
    if not phone_str.startswith('+'):
        return '+' + phone_str
    return phone_str

def merge_csvs():
    combined_df = pd.DataFrame()

    for source in ['google', 'website', 'facebook']:
        try:
            # Read each CSV file
            sep = ',' if source != 'website' else ';'  # Adjust separator for website dataset
            df = pd.read_csv(csv_files[source], sep=sep, on_bad_lines='skip')

            # Handle 'name' column
            if source in ['google', 'facebook'] and 'name' in df.columns:
                combined_df['name'] = df['name']
            elif source == 'website' and 'LEGAL_NAME' in df.columns:
                combined_df['name'] = df['LEGAL_NAME']
                combined_df.rename(columns={'LEGAL_NAME': 'name'}, inplace=True)

            # Handle 'phone' column and ensure it has a '+' prefix
            if 'phone' in df.columns:
                combined_df['phone'] = df['phone'].apply(ensure_plus_prefix)

            # Handle 'Category' column based on source
            if source == 'google' and 'Category' in df.columns:
                combined_df['Category'] = df['Category']
            elif source == 'website' and 's_category' in df.columns:
                combined_df['Category'] = df['s_category']
            elif source == 'facebook' and 'Categories' in df.columns:
                combined_df['Category'] = df['Categories']

        except FileNotFoundError:
            print(f"File not found: {csv_files[source]}")
        except Exception as e:
            print(f"Error reading {source} dataset: {str(e)}")

    # Read the address from the website dataset with address
    try:
        address_df = pd.read_csv(csv_files['website_address'], sep=',', on_bad_lines='skip')
        if 'address' in address_df.columns:
            combined_df['address'] = address_df['address']
    except FileNotFoundError:
        print(f"File not found: {csv_files['website_address']}")
    except Exception as e:
        print(f"Error reading website address dataset: {str(e)}")

    # Remove duplicates and save to merged CSV
    combined_df.drop_duplicates(subset=['phone', 'name'], inplace=True)
    combined_df.to_csv(csv_files['merged'], index=False)  # Save as CSV
    print(f"Merged dataset saved as: {csv_files['merged']}")

if __name__ == "__main__":
    merge_csvs()
