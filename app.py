from utils import convert_to_csvs
from utils import scrape_availability
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import pandas as pd
from time import sleep

def prepareData():
    scrape_availability.scrape_availability()
    convert_to_csvs.convert_json_to_csv()

app = Flask(__name__)
CORS(app)

valid_magic_keys = ['inspire', 'believe', 'enchant', 'imagine', 'dream']

#curl -X POST http://localhost:5000/api/availability -H 'Content-Type: application/json' -d '{"magic_key_name": "inspire"}'
@app.route('/api/availability', methods=['GET'])
@app.route('/api/availability/<magic_key>', methods=['GET'])
def get_availability( *args, **kwargs ):
    prepareData()
    magic_key = None
    if 'magic_key' in kwargs:
        magic_key = kwargs['magic_key']

    if magic_key != None and magic_key in valid_magic_keys:
        magic_key_data = pd.read_csv(f'data/{magic_key}.csv')
        return jsonify(magic_key_data.to_dict(orient='records'))
    elif kwargs == {}:
        all_data = {}
        for magic_key in valid_magic_keys:
            magic_key_data = pd.read_csv(f'data/{magic_key}.csv')
            all_data[magic_key] = magic_key_data.to_dict(orient='records')
        return jsonify(all_data)
    else:
        return jsonify({'error': 'Invalid magic key name'})
    return jsonify({'error': 'Invalid magic key name'})

#prepareData()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)