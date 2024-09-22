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







if __name__ == "__main__":
    app.run(debug=True)
