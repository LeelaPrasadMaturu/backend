from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')  # Adjust URI as needed
db = client['gethuman_db']  # Replace 'gethuman_db' with your database name
collection = db['companies']  # Replace 'companies' with your collection name

# Mock dataset resembling GetHuman data
mock_data = [
    {"id": 1, "name": "Amazon", "phone": "1-888-280-4331", "website": "https://www.amazon.com"},
    {"id": 2, "name": "Apple", "phone": "1-800-MY-APPLE", "website": "https://www.apple.com"},
    {"id": 3, "name": "Google", "phone": "1-866-246-6453", "website": "https://www.google.com"},
    # Add more rows as needed to make up 20–30 entries
]

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify([])  # Return an empty list if no query is provided

    # Filter mock data based on query
    results = [
        item for item in mock_data
        if query in item['name'].lower() or query in item['phone'] or query in item['website'].lower()
    ]
    return jsonify(results)

@app.route('/store', methods=['POST'])
def store():
    try:
        data = request.json  # Expect JSON data
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Insert data into MongoDB
        result = collection.insert_one(data)
        return jsonify({"message": "Data stored successfully", "id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
