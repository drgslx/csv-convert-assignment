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

def clean_phone(phone):
    if pd.isna(phone):
        return phone
    return ''.join(filter(str.isdigit, str(phone)))

def ensure_plus_prefix(phone):
    phone = clean_phone(phone)
    if pd.isna(phone) or len(phone) == 0:
        return phone 
    phone_str = str(phone).strip()
    if not phone_str.startswith('+'):
        return '+' + phone_str
    return phone_str

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
                df['phone'] = df['phone'].apply(ensure_plus_prefix)

            if source == 'google' and 'category' in df.columns:
                df.rename(columns={'category': 'category'}, inplace=True)
            elif source == 'website' and 's_category' in df.columns:
                df.rename(columns={'s_category': 'category'}, inplace=True)
            elif source == 'facebook' and 'categories' in df.columns:
                df.rename(columns={'categories': 'category'}, inplace=True)

            combined_df = pd.concat([combined_df, df[['name', 'phone', 'category', 'source']]], ignore_index=True)

        except FileNotFoundError:
            print(f"File not found: {csv_files[source]}")
        except Exception as e:
            print(f"Error reading {source} dataset: {str(e)}")

    def prioritize_entries(group):
        if 'google' in group['source'].values:
            return group[group['source'] == 'google'].iloc[0]
        elif 'facebook' in group['source'].values:
            return group[group['source'] == 'facebook'].iloc[0]
        return group.iloc[0]

    # Apply grouping with `include_group=False`
    combined_df = combined_df.groupby('phone', group_keys=False).apply(prioritize_entries)

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
