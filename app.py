from flask import Flask, request, jsonify
import csv

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_file():
    data = request.get_json()
    file_path = f"/malav_PV_dir/{data['file']}"
    product = data['product']

    try:
        with open(file_path, 'r', newline='') as file:
            # Attempt to read the file using csv.reader
            reader = csv.reader(file)
            rows = list(reader)
            if len(rows) < 2:
                return jsonify({"file": data['file'], "error": "Input file not in CSV format."}), 400

            # Extract headers and validate column names (remove any leading/trailing spaces)
            headers = [header.strip() for header in rows[0]]
            if headers != ["product", "amount"]:
                return jsonify({"file": data['file'], "error": "Input file not in CSV format."}), 400

            total_sum = 0
            for row in rows[1:]:
                if len(row) != 2:  
                    return jsonify({"file": data['file'], "error": "Input file not in CSV format."}), 400

                try:
                    row_product, row_amount = row
                    if row_product == product:
                        total_sum += int(row_amount)
                except ValueError as e:  
                    return jsonify({"file": data['file'], "error": "Input file not in CSV format."}), 400

        return jsonify({"file": data['file'], "sum": total_sum})

    except FileNotFoundError as e:
        return jsonify({"file": data['file'], "error": "File not found."}), 404
    except Exception as e:
        return jsonify({"file": data['file'], "error": "Input file not in CSV format."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)