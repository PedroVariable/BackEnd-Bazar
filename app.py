from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
with open('products.json') as f:
    data = json.load(f)

@app.route('/api/items', methods=['GET'])
def get_items():
    query = request.args.get('q', '').lower()
    category = request.args.get('category', '').lower()
    filtered_items = [
        item for item in data['products']
        if (query in item['title'].lower() or
            query in item['category'].lower() or
            query in item['description'].lower() or
            any(query in tag.lower() for tag in item.get('tags', []))
            if query else True) and
           (category == item['category'].lower() if category else True)
    ]
    
    return jsonify(filtered_items)



@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in data['products'] if item['id'] == item_id), None)
    return jsonify(item) if item else ('', 404)

sales = []
@app.route('/api/addSale', methods=['POST'])
def add_sale():
    sale_data = request.get_json()
    sales.append(sale_data)
    return jsonify({'success': True}), 201

@app.route('/api/sales', methods=['GET'])
def get_sales():
    return jsonify(sales)

if __name__ == '__main__':
    app.run(port=5000)
