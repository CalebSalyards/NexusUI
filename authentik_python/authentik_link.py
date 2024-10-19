from flask import Flask, request, jsonify, send_file
import requests
import pandas as pd
import os
import json

app = Flask(__name__)

# Configuration
AUTHENTIK_API_URL = "https://your-authentik-instance/api/v1/users/"  # Change to your Authentik API URL
DUPLICATES_CSV_FILE = "duplicates_not_created.csv"

@app.route('/register_users', methods=['POST'])
def register_users():
    try:
        data = request.json
        usernames_passwords = data.get('users', [])
        duplicates = []

        for user in usernames_passwords:
            username = user.get('username')
            password = user.get('password')
            
            # Check if the user exists
            response = requests.get(f"{AUTHENTIK_API_URL}{username}/")
            if response.status_code == 200:
                duplicates.append({'username': username, 'password': password})
            else:
                # Register the user
                register_response = requests.post(AUTHENTIK_API_URL, json={
                    'username': username,
                    'password': password,
                    # Add additional fields if required by your Authentik API
                })

                if register_response.status_code != 201:
                    return jsonify({'message': 'Error registering user', 'error': register_response.text}), 400
        
        if duplicates:
            # Save duplicates to CSV
            df = pd.DataFrame(duplicates)
            df.to_csv(DUPLICATES_CSV_FILE, index=False)

            return jsonify({
                'message': 'Successfully submitted with duplicates.',
                'duplicates_csv': DUPLICATES_CSV_FILE
            }), 200
        else:
            return jsonify({'message': 'Successfully submitted.'}), 200

    except Exception as e:
        return jsonify({'message': 'Error submitting.', 'error': str(e)}), 500


@app.route('/download_duplicates', methods=['GET'])
def download_duplicates():
    if os.path.exists(DUPLICATES_CSV_FILE):
        return send_file(DUPLICATES_CSV_FILE, as_attachment=True)
    else:
        return jsonify({'message': 'No duplicates found.'}), 404


if __name__ == '__main__':
    app.run(debug=True)
