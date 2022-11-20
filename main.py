from flask import Flask, Response, request
import json
from product_db import Products
from flask_cors import CORS


# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)


@app.route("/get_products", methods=['GET'])
def get_products():
    print("get products")
    result = Products.get_products()
    if result:
        resp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        resp = Response("NOT FOUND", status=404, content_type="text/plain")
    return resp


@app.route("/get_product/<id>", methods=['GET'])
def get_product_by_id(id):
    print("get product by id")
    result = Products.get_product_by_id(id)
    if result:
        resp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        resp = Response("NOT FOUND", status=404, content_type="text/plain")
    return resp


@app.route("/add_product", methods=['POST'])
def add_product(name, description, price, inventory, image):
    print("add product")
    result = Products.add_product(name, description, price, inventory, image)
    if result:
        resp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        resp = Response("NOT FOUND", status=404, content_type="text/plain")
    return resp


@app.route("/update_product", methods=['POST'])
def update_product(product_id, name, description, price, inventory, image):
    print("update product")
    result = Products.update_product(product_id, name, description, price, inventory, image)
    if result:
        resp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        resp = Response("NOT FOUND", status=404, content_type="text/plain")
    return resp


@app.route("/delete_product", methods=['POST'])
def delete_product(id):
    print("delete product")
    result = Products.delete_product(id)
    if result:
        resp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        resp = Response("NOT FOUND", status=404, content_type="text/plain")
    return resp


if __name__ == "__main__":
    app.run(port=5011, debug=True)
