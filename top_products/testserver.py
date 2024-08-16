from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Endpoint to provide top N products based on category
@app.route('/test/companies/<string:company>/categories/<string:category>/products', methods=['GET'])
def get_products(company, category):
    if category not in ['electronics', 'clothing', 'books']:  # Example categories
        return jsonify({"error": "Invalid category"}), 400
    
    # Generate random product data for demonstration purposes
    products = [
        {
            "id": f"{company}_{category}_{i}",
            "name": f"Product {i}",
            "price": round(random.uniform(10, 500), 2),
            "rating": round(random.uniform(1, 5), 1),
            "discount": round(random.uniform(0, 30), 2)
        } for i in range(1, 21)  # Generate 20 products
    ]
    
    # Sorting
    sort_by = request.args.get('sort_by', 'price')
    order = request.args.get('order', 'asc')
    if sort_by in ['price', 'rating', 'discount']:
        products = sorted(products, key=lambda x: x[sort_by], reverse=(order == 'desc'))

    # Pagination
    top = request.args.get('top', 10, type=int)
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * top
    end = start + top
    paginated_products = products[start:end]
    
    return jsonify({"products": paginated_products})

if __name__ == '__main__':
    app.run(port=5001)
