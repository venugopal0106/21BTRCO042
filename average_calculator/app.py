from flask import Flask, jsonify, request
import requests
import time

app = Flask(__name__)

# Configuration
ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzIzNzg5NTkzLCJpYXQiOjE3MjM3ODkyOTMsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjkxODYyZDMzLWI5MzctNDEzZS1iY2E1LTZjNDhiYTI3NzIzNSIsInN1YiI6IjIxYnRyY28wNDJAamFpbnVuaXZlcnNpdHkuYWMuaW4ifSwiY29tcGFueU5hbWUiOiJhZmZvcmRtZWQiLCJjbGllbnRJRCI6IjkxODYyZDMzLWI5MzctNDEzZS1iY2E1LTZjNDhiYTI3NzIzNSIsImNsaWVudFNlY3JldCI6IkhFZlB3a3FKbUhmWUlEZUwiLCJvd25lck5hbWUiOiJ2ZW51X2dvcGFsIiwib3duZXJFbWFpbCI6IjIxYnRyY28wNDJAamFpbnVuaXZlcnNpdHkuYWMuaW4iLCJyb2xsTm8iOiIyMWJ0cmNvMDQyIn0.Ap9hhxBDGLERsKtiUS6C5NuPKNK_A3zeSjvZd_v6MTQ'
WINDOW_SIZE = 10

# Initialize sliding window and fetch cache
sliding_window = []
cache = {}

# Function to fetch numbers from the test server
def fetch_numbers(number_id):
    url = f"http://127.0.0.1:5001/test/numbers/{number_id}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    try:
        response = requests.get(url, headers=headers, timeout=0.5)  # Timeout of 500ms
        if response.status_code == 200:
            data = response.json()
            return data.get('numbers', [])
        else:
            print(f"Failed to fetch numbers: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    return []


# Route to get numbers and calculate average
@app.route('/numbers/<string:number_id>', methods=['GET'])
def get_numbers(number_id):
    global sliding_window, cache

    # Validate number_id
    if number_id not in ['p', 'f', 'e', 'r']:
        return jsonify({"error": "Invalid number ID"}), 400

    # Fetch numbers from cache or test server
    if number_id in cache and time.time() - cache[number_id]['timestamp'] < 0.5:
        numbers = cache[number_id]['numbers']
    else:
        numbers = fetch_numbers(number_id)
        cache[number_id] = {'numbers': numbers, 'timestamp': time.time()}

    if not numbers:
        return jsonify({"error": "Could not fetch numbers"}), 400

    # Maintain sliding window of unique numbers
    new_numbers = [num for num in numbers if num not in sliding_window]
    sliding_window.extend(new_numbers)
    if len(sliding_window) > WINDOW_SIZE:
        sliding_window = sliding_window[-WINDOW_SIZE:]

    # Calculate average
    if sliding_window:
        average = sum(sliding_window) / len(sliding_window)
    else:
        average = 0

    # Create response
    response = {
        "numbers": new_numbers,
        "windowPrevState": list(sliding_window[:-len(new_numbers)]),
        "windowCurState": sliding_window,
        "avg": round(average, 2)
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
