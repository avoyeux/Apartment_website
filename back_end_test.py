import pandas as pd
import numpy as np
import csv

from flask import Flask, request, jsonify
from flask_cors import CORS


# Initialisation of a flask application
app = Flask(__name__)
CORS(app)

@app.route('/save-log', methods=['POST'])
def save_log():
    """
    To save the log from the front end for further analysis if needed.
    Also used as a data base.
    """

    data = request.json
    newlog = data['logString']

    with open('data.csv', mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([newlog])

    return jsonify({'message': 'String saved successfully'}), 200

@app.route('/get-logs', methods=['GET'])
def get_logs():
    """
    Function to get the log values to display in the past transactions html box.
    """

    df = pd.read_csv('data.csv', header=None)
    return df.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)