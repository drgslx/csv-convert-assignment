from flask import Flask, jsonify, request, json
import os
import pandas as pd

app = Flask(__name__)

# MySQL Database Configuration


@app.route("/api/csv-convert")
def get_csv_as_json():
    dataset_type = request.args.get('dataset', 'google')  # Default to 'google'

    if dataset_type == 'google':
        csv_path = os.path.join('public', 'google_dataset.csv')
        sep = ','
    elif dataset_type == 'website':
        csv_path = os.path.join('public', 'website_dataset.csv')
        sep = ';'
    elif dataset_type == 'facebook':
        csv_path = os.path.join('public', 'facebook_dataset.csv')
        sep = ','
    elif dataset_type == 'combined':
        csv_path = os.path.join('public', 'merged_dataset.csv')  # Path to the combined dataset
        sep = ','
    else:
        return jsonify({"error": "Invalid dataset type"}), 400
    
    print("Loading dataset from:", csv_path)

    try:
        # Read the CSV file with the appropriate separator
        df = pd.read_csv(csv_path, sep=sep, on_bad_lines='skip')
        df = df.fillna('')  # Replace NaN values with empty strings
        data = df.to_dict(orient='records')
        return jsonify(data)

    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    



@app.route("/api/get-json")
def get_json_data():
    json_path = os.path.join('data', 'sample_data.json')
    try:
        # Open and read the JSON file
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)

        # Return JSON data as response
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



if __name__ == "__main__":
    app.run(debug=True)
