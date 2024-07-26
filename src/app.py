import json
from flask import Flask, request, jsonify
from main import get_stock_values

app = Flask(__name__)

@app.route('/api/esg', methods=['GET'])
def get_esg_scores():
    stock = request.args.get('stock')
    if not stock:
        return jsonify({'error': 'Stock parameter is required'}), 400

    try:
        result = get_stock_values(stock)
        esg_scores = result["esg_scores"]
        sources = result["sources"]
        response = {
            "stock": stock,
            "esg_scores": esg_scores,
            "sources": sources
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
