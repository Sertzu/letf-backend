from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
CORS(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["20 per minute"]
)

df = pd.read_csv('data/data.csv', sep=';')
df['Date'] = pd.to_datetime(df['Date'])

@app.route('/api/data', methods=['GET'])
@limiter.limit("20 per minute")
def get_data():
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    if not start_date or not end_date:
        return jsonify({'error': 'Please provide both start and end dates!'}), 400

    try:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please provide valid dates!'}), 400

    if start_date > end_date:
        return jsonify({'error': 'Start date cannot be after end date.'}), 400

    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    data = filtered_df.to_dict(orient='records')
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")