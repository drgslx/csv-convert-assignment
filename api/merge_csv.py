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
            sep = ',' if source != 'website' else ';' 
            df = pd.read_csv(csv_files[source], sep=sep, on_bad_lines='skip')

            # Add the source column
            df['source'] = source

            # Standardize the name column
            if source in ['google', 'facebook'] and 'name' in df.columns:
                df.rename(columns={'name': 'name'}, inplace=True)
            elif source == 'website' and 'legal_name' in df.columns:
                df.rename(columns={'legal_name': 'name'}, inplace=True)

            # Ensure phone numbers have a '+' prefix
            if 'phone' in df.columns:
                df['phone'] = df['phone'].apply(ensure_plus_prefix)

            # Standardize category column
            if source == 'google' and 'category' in df.columns:
                df.rename(columns={'category': 'category'}, inplace=True)
            elif source == 'website' and 's_category' in df.columns:
                df.rename(columns={'s_category': 'category'}, inplace=True)
            elif source == 'facebook' and 'categories' in df.columns:
                df.rename(columns={'categories': 'category'}, inplace=True)

            # Concatenate the current DataFrame to the combined DataFrame
            combined_df = pd.concat([combined_df, df[['name', 'phone', 'category', 'source']]], ignore_index=True)

        except FileNotFoundError:
            print(f"File not found: {csv_files[source]}")
        except Exception as e:
            print(f"Error reading {source} dataset: {str(e)}")

    # Define a custom aggregation function to prioritize Google > Facebook > Website
    def prioritize_entries(group):
        if 'google' in group['source'].values:
            return group[group['source'] == 'google'].iloc[0]
        elif 'facebook' in group['source'].values:
            return group[group['source'] == 'facebook'].iloc[0]
        return group.iloc[0]  # Default to first entry (website)

    # Group by phone and apply the custom function
    combined_df = combined_df.groupby('phone', as_index=False).apply(prioritize_entries)

    # Reset the index after grouping
    combined_df.reset_index(drop=True, inplace=True)

    try:
        address_df = pd.read_csv(csv_files['website_address'], sep=',', on_bad_lines='skip')
        if 'address' in address_df.columns:
            combined_df = combined_df.merge(address_df[['address']], left_index=True, right_index=True, how='left')
    except FileNotFoundError:
        print(f"File not found: {csv_files['website_address']}")
    except Exception as e:
        print(f"Error reading website address dataset: {str(e)}")

    combined_df.drop_duplicates(subset=['phone', 'name'], inplace=True)
    combined_df.to_csv(csv_files['merged'], index=False) 
    print(f"Merged dataset saved as: {csv_files['merged']}")

if __name__ == "__main__":
    merge_csvs()
