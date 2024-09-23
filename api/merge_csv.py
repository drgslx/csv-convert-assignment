import os
import pandas as pd

# Define file paths
csv_files = {
    'google': os.path.join('api', 'google_dataset.csv'),
    'website': os.path.join('api', 'website_dataset.csv'),
    'facebook': os.path.join('api', 'facebook_dataset.csv'),
    'website_address': os.path.join('api', 'website_dataset_with_address.csv'),
    'merged': os.path.join('api', 'merged_dataset.csv'),
}

def clean_string(value):
    if isinstance(value, str):
        value = value.replace('"', ' ').replace('\\', ' ').strip()
        if value.endswith('\\""'):
            value = value[:-1]
    return value

def merge_csvs():
    combined_df = pd.DataFrame()

    for source in ['google', 'website', 'facebook']:
        try:
            sep = ',' if source != 'website' else ';' 
            df = pd.read_csv(csv_files[source], sep=sep, on_bad_lines='skip', low_memory=False, quotechar='"', escapechar='\\')

            if 'name' in df.columns:
                df['name'] = df['name'].apply(clean_string)
            elif 'legal_name' in df.columns:
                df.rename(columns={'legal_name': 'name'}, inplace=True)
                df['name'] = df['name'].apply(clean_string)
            else:
                print(f"Warning: 'name' or 'legal_name' column not found in {source} dataset.")
                continue  

            df['source'] = source

            if 'phone' in df.columns:
                df['phone'] = df['phone']

            # Rename category columns based on the source
            if source == 'google' and 'category' in df.columns:
                df.rename(columns={'category': 'category'}, inplace=True)
            elif source == 'website' and 's_category' in df.columns:
                df.rename(columns={'s_category': 'category'}, inplace=True)
            elif source == 'facebook' and 'categories' in df.columns:
                df.rename(columns={'categories': 'category'}, inplace=True)

            combined_df = pd.concat([combined_df, df[['name', 'phone', 'category', 'source', 'address']]], ignore_index=True)

        except FileNotFoundError:
            print(f"File not found: {csv_files[source]}")
        except Exception as e:
            print(f"Error reading {source} dataset: {str(e)}")

    # Prioritize entries based on source, including names and addresses
    combined_df = combined_df.groupby('phone', as_index=False).agg({
        'name': lambda x: x.bfill().iloc[0],  # Backfill to prioritize names
        'category': lambda x: x.bfill().iloc[0],  # Backfill to prioritize categories
        'source': 'first',  # Keep the source of the prioritized entry
        'address': lambda x: x.bfill().iloc[0]  # Prioritize addresses
    })

    # Remove rows where all values are empty
    combined_df.dropna(how='all', inplace=True)

    # Remove .0 from phone numbers
    if 'phone' in combined_df.columns:
        combined_df['phone'] = combined_df['phone'].astype(str).str.replace('.0', '', regex=False)

    # Ensure that the address prioritizes Google > Facebook > Website
    if 'address' in combined_df.columns:
        # Prioritize Google and Facebook addresses, if available
        combined_df['address'] = combined_df['address'].fillna(method='bfill')

    combined_df.drop_duplicates(subset=['phone'], inplace=True)

    # Add '+' sign to phone numbers
    if 'phone' in combined_df.columns:
        combined_df['phone'] = '+' + combined_df['phone']

    combined_df.to_csv(csv_files['merged'], index=False) 
    print(f"Merged dataset saved as: {csv_files['merged']}")

if __name__ == "__main__":
    merge_csvs()
