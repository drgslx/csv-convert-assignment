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

# Function to clean strings
def clean_string(value):
    if isinstance(value, str):
        value = value.replace('"', ' ').replace('\\', ' ').strip()
        if value.endswith('\\""'):
            value = value[:-1]
    return value

# Function to merge datasets with prioritization
def merge_csvs():
    combined_df = pd.DataFrame()

    # Source priority: 'google' > 'website' > 'facebook'
    source_priority = ['google', 'website', 'facebook']

    for source in source_priority:
        try:
            sep = ',' if source != 'website' else ';'
            df = pd.read_csv(csv_files[source], sep=sep, on_bad_lines='skip', low_memory=False, quotechar='"', escapechar='\\')

            # Clean the 'name' or 'legal_name' column
            if 'name' in df.columns:
                df['name'] = df['name'].apply(clean_string)
            elif 'legal_name' in df.columns:
                df.rename(columns={'legal_name': 'name'}, inplace=True)
                df['name'] = df['name'].apply(clean_string)
            else:
                print(f"Warning: 'name' or 'legal_name' column not found in {source} dataset.")
                continue  

            # Add source information to the dataframe
            df['source'] = source

            # Clean the 'phone' column
            if 'phone' in df.columns:
                df['phone'] = df['phone'].astype(str)

            # Standardize category column names across datasets
            if source == 'google' and 'category' in df.columns:
                df.rename(columns={'category': 'category'}, inplace=True)
            elif source == 'website' and 's_category' in df.columns:
                df.rename(columns={'s_category': 'category'}, inplace=True)
            elif source == 'facebook' and 'categories' in df.columns:
                df.rename(columns={'categories': 'category'}, inplace=True)

            # Combine the dataframes
            combined_df = pd.concat([combined_df, df[['name', 'phone', 'category', 'source', 'address']]], ignore_index=True)

        except FileNotFoundError:
            print(f"File not found: {csv_files[source]}")
        except Exception as e:
            print(f"Error reading {source} dataset: {str(e)}")

    # Deduplicate based on phone and address, prioritizing by source
    combined_df['priority'] = combined_df['source'].apply(lambda x: source_priority.index(x))
    combined_df.sort_values(by=['phone', 'address', 'priority'], inplace=True)
    combined_df.drop_duplicates(subset=['phone', 'address'], keep='first', inplace=True)

    # Add '+' to phone numbers if it is missing
    if 'phone' in combined_df.columns:
        combined_df['phone'] = combined_df['phone'].str.replace('.0', '', regex=False)
        combined_df['phone'] = combined_df['phone'].apply(lambda x: x if x.startswith('+') else f'+{x}')

    # Drop unnecessary columns
    combined_df.dropna(how='all', inplace=True)

    # Save the merged dataset
    combined_df.to_csv(csv_files['merged'], index=False) 
    print(f"Merged dataset saved as: {csv_files['merged']}")

if __name__ == "__main__":
    merge_csvs()
