from flask import Flask, Response
import json
from product_db import Products
from flask_cors import CORS
from flasgger import Swagger


app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)
Swagger(app)


@app.route("/get_products", methods=['GET'])
def get_products():
    """Example endpoint: get products
    This endpoint get all the product information.
    ---
    definitions:
      Products:
        type: array
        items:
          type: object
          properties:
            product_id:
              type: integer
              required: true
            name:
              type: string
              required: true
            description:
              type: string
              required: true
            price:
              type: number
              required: true
            inventory:
              type: integer
              required: true
            image:
              type: string
              required: true
    responses:
      200:
        description: The status of deletion
        schema:
          $ref: '#/definitions/Products'
        examples:
          success: true
    """
    result = Products.get_products()
    if result:
        resp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        resp = Response("NOT FOUND", status=404, content_type="text/plain")
    return resp


@app.route("/products/search", methods=['GET'])
def search_products():
    """Example endpoint: get products
    This endpoint get all the product information.
    ---
    definitions:
      Products:
        type: array
        items:
          type: object
          properties:
            product_id:
              type: integer
              required: true
            name:
              type: string
              required: true
            description:
              type: string
              required: true
            price:
              type: number
              required: true
            inventory:
              type: integer
              required: true
            image:
              type: string
              required: true
    responses:
      200:
        description: The status of deletion
        schema:
          $ref: '#/definitions/Products'
        examples:
          success: true
    """
    result = Products.get_products()
    if result:
        resp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        resp = Response("NOT FOUND", status=404, content_type="text/plain")
    return resp


@app.route("/get_product/<id>", methods=['GET'])
def get_product_by_id(id):
    """Example endpoint: get product by id
    This endpoint get product information by product_id.
    ---
    parameters:
      - name: Parameters
        in: body
        type: object
        schema:
            $ref: '#/definitions/GetProduct'
        required: true
    definitions:
      GetProduct:
        type: object
        properties:
          product_id:
            type: integer
            required: true
      Product:
        type: object
        properties:
          product_id:
            type: integer
            required: true
          name:
            type: string
            required: true
          description:
            type: string
            required: true
          price:
            type: number
            required: true
          inventory:
            type: integer
            required: true
          image:
            type: string
            required: true
    responses:
      200:
        description: The status of deletion
        schema:
          $ref: '#/definitions/Product'
        examples:
          success: true
    """
    result = Products.get_product_by_id(id)
    if result:
        resp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        resp = Response("NOT FOUND", status=404, content_type="text/plain")
    return resp


@app.route("/add_product", methods=['POST'])
def add_product(name, description, price, inventory, image):
    """Example endpoint: add product
    This endpoint add product by specifying the product information.
    ---
    parameters:
      - name: Parameters
        in: body
        type: object
        schema:
            $ref: '#/definitions/Add'
        required: true
    definitions:
      Add:
        type: object
        properties:
          name:
            type: string
            required: true
          description:
            type: string
            required: true
          price:
            type: number
            required: true
          inventory:
            type: integer
            required: true
          image:
            type: string
            required: true
      Status:
        type: object
        properties:
          success:
            type: boolean
            required: true
          product_id:
            type: integer
            required: true
    responses:
      200:
        description: The status of deletion
        schema:
          $ref: '#/definitions/Status'
        examples:
          success: true
    """
    result = Products.add_product(name, description, price, inventory, image)
    if result:
        resp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        resp = Response("NOT FOUND", status=404, content_type="text/plain")
    return resp


@app.route("/update_product", methods=['POST'])
def update_product(product_id, name, description, price, inventory, image):
    """Example endpoint: update product
    This endpoint updates product by inputting the information.
    ---
    parameters:
      - name: Parameters
        in: body
        type: object
        schema:
            $ref: '#/definitions/Update'
        required: true
    definitions:
      Update:
        type: object
        properties:
          product_id:
            type: integer
            required: true
          name:
            type: string
            required: true
          description:
            type: string
            required: true
          price:
            type: number
            required: true
          inventory:
            type: integer
            required: true
          image:
            type: string
            required: true
      Status:
        type: object
        properties:
          success:
            type: boolean
            required: true
    responses:
      200:
        description: The status of deletion
        schema:
          $ref: '#/definitions/Status'
        examples:
          success: true
    """
    result = Products.update_product(product_id, name, description, price, inventory, image)
    if result:
        resp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        resp = Response("NOT FOUND", status=404, content_type="text/plain")
    return resp


@app.route("/delete_product", methods=['POST'])
def delete_product(product_id):
    """Example endpoint: delete product
    This endpoint updates product by specifying the product id and the information.
    ---
    parameters:
      - name: Parameters
        in: body
        type: object
        schema:
            $ref: '#/definitions/Deletion'
        required: true
    definitions:
      Deletion:
        type: object
        properties:
          product_id:
            type: integer
            required: true
      Status:
        type: object
        properties:
          success:
            type: boolean
            required: true
    responses:
      200:
        description: The status of deletion
        schema:
          $ref: '#/definitions/Status'
        examples:
          success: true
    """
    result = Products.delete_product(product_id)
    if result:
        resp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        resp = Response("NOT FOUND", status=404, content_type="text/plain")
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5012, debug=True)
