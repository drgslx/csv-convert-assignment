from flask import Flask, jsonify, request, json
import os
import pandas as pd

app = Flask(__name__)

csv_files = {
    'google': os.path.join('api', 'google_dataset.csv'),
    'website': os.path.join('api', 'website_dataset.csv'),
    'website_address': os.path.join('api', 'website_dataset_with_address.csv'),
    'facebook': os.path.join('api', 'facebook_dataset.csv'),
    'merged': os.path.join('api', 'merged_dataset.csv')
}

@app.route("/api/csv-convert")
def get_csv_as_json():
    dataset_type = request.args.get('dataset', 'google') 

    if dataset_type not in csv_files:
        return jsonify({"error": "Invalid dataset type"}), 400
    
    print("Loading dataset from:", csv_files[dataset_type])

    try:
        sep = ',' if dataset_type != 'website' else ';'
        df = pd.read_csv(csv_files[dataset_type], sep=sep, on_bad_lines='skip')
        df = df.fillna('')
        data = df.to_dict(orient='records')
        return jsonify(data)

    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/merge-csvs", methods=["POST"])
def merge_csvs():
    try:
        combined_df = pd.DataFrame()
        for source in ['google', 'website', 'facebook']:
            df = pd.read_csv(csv_files[source], sep=',' if source != 'website' else ';', on_bad_lines='skip')
            if 'phone' in df.columns:
                combined_df = pd.concat([combined_df, df[['phone']]], ignore_index=True)

        combined_df.drop_duplicates(subset='phone', inplace=True)
        combined_df.to_csv(csv_files['merged'], index=False)

        return jsonify({"message": "CSV files merged successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/get-json")
def get_json_data():
    json_path = os.path.join('data', 'sample_data.json')
    try:
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
