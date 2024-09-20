from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Load CSV and preprocess
df = pd.read_csv('data/data.csv', sep=';')
df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime

@app.route('/api/data', methods=['GET'])
def get_data():
    # Get the start and end dates from query parameters
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    # Check if both start and end dates are provided
    if not start_date or not end_date:
        return jsonify({'error': 'Please provide both start and end dates!'}), 400

    # Convert query params to datetime
    try:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please provide valid dates!'}), 400

    # Check if start_date is before end_date
    if start_date > end_date:
        return jsonify({'error': 'Start date cannot be after end date.'}), 400

    # Filter the DataFrame by the date range
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    # Convert the filtered DataFrame to JSON format
    data = filtered_df.to_dict(orient='records')
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")