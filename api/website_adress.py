import os
import pandas as pd

file_path = os.path.join('api', 'website_dataset.csv')  
df = pd.read_csv(file_path, sep=';', on_bad_lines='skip') 

print("Column names in the dataset:", df.columns)

df.columns = df.columns.str.strip()

address_columns = ['main_city', 'main_region', 'main_country']
existing_columns = [col for col in address_columns if col in df.columns]

df['address'] = df[existing_columns].apply(lambda x: ', '.join(x.dropna()), axis=1)

df = df.drop(columns=existing_columns)

output_file_path = 'api/website_dataset_with_address.csv'
df.to_csv(output_file_path, index=False)

print(f"File saved as {output_file_path}")
