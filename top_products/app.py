from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

COMPANIES = ['company1', 'company2', 'company3', 'company4', 'company5']
BASE_URL = "http://127.0.0.1:5001/test/companies"

def fetch_products_from_server(company, category, top, page, sort_by, order):
    url = f"{BASE_URL}/{company}/categories/{category}/products"
    params = {
        'top': top,
        'page': page,
        'sort_by': sort_by,
        'order': order
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('products', [])
    return []

@app.route('/categories/<string:category>/products', methods=['GET'])
def get_products(category):
    top = request.args.get('top', 10, type=int)
    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort_by', 'price')
    order = request.args.get('order', 'asc')

    all_products = []
    for company in COMPANIES:
        products = fetch_products_from_server(company, category, top, page, sort_by, order)
        all_products.extend(products)
    
    # Sorting the aggregated list
    if sort_by in ['price', 'rating', 'discount']:
        all_products = sorted(all_products, key=lambda x: x[sort_by], reverse=(order == 'desc'))

    # Pagination
    start = (page - 1) * top
    end = start + top
    paginated_products = all_products[start:end]
    
    return jsonify({"products": paginated_products})

if __name__ == '__main__':
    app.run(port=5000)

