from flask import Flask, request


app = Flask(__name__)


@app.route("/get", methods=['GET'])
def get_products():
    return "get_products"


@app.route("/get", methods=['GET'])
def get_product_by_id(product_id):
    return "get_product_by_id"


@app.route("/post", methods=['POST'])
def add_product():
    return "add_product"


@app.route("/update_product", methods=['GET'])
def update_product():
    return "update_product"


@app.route("/delete_product", methods=['GET'])
def delete_product():
    return "delete_product"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
