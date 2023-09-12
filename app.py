from utils import convert_to_csvs
from utils import scrape_availability
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

def prepareData():
    scrape_availability.scrape_availability()
    convert_to_csvs.convert_json_to_csv()

app = Flask(__name__)
CORS(app)

@app.route('/api/availability', methods=['POST'])
def get_availability():
    magic_key_name = request.json.get('magic_key_name')
    if magic_key_name in ['inspire', 'believe', 'enchant', 'imagine', 'dream']:
        df = pd.read_csv(f'data/{magic_key_name}.csv')
        return jsonify(df.to_dict(orient='records'))
    else:
        return jsonify({'error': 'Invalid magic key name'})

#prepareData()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)