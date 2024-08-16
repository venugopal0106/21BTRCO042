from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Endpoint to provide numbers based on the number_id
@app.route('/test/numbers/<string:number_id>', methods=['GET'])
def get_numbers(number_id):
    if number_id == 'p':  # Prime numbers
        numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    elif number_id == 'f':  # Fibonacci numbers
        numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    elif number_id == 'e':  # Even numbers
        numbers = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    elif number_id == 'r':  # Random numbers
        numbers = [random.randint(1, 100) for _ in range(10)]
    else:
        return jsonify({"error": "Invalid number ID"}), 400

    return jsonify({"numbers": numbers})

if __name__ == '__main__':
    app.run(port=5001)  # Run on port 5001
