from flask import Flask, Response, request
from datetime import datetime
import json
from columbia_student_resource import ColumbiaStudentResource
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)

#########################################################################################
# sample code

@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "F22-Starter-Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result


@app.route("/api/students/<uni>", methods=["GET"])
def get_student_by_uni(uni):

    result = ColumbiaStudentResource.get_by_key(uni)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp
######################################################################################################
# start here

@app.route("/get_product", methods=['GET'])
def get_products():
    print("get product pass")
    return "get_products"


@app.route("/get_product/<id>", methods=['GET'])
def get_product_by_id(id):
    print(f"get product by id: {id} pass")
    return f"get_product_by_id: {id}"


@app.route("/post_product", methods=['POST'])
def add_product():
    print("add product pass")
    return "add_product"


@app.route("/update_product", methods=['GET'])
def update_product():
    print("update product pass")
    return "update_product"


@app.route("/delete_product", methods=['GET'])
def delete_product():
    print("delete product pass")
    return "delete_product"

if __name__ == "__main__":
    app.run(port=5000, debug=True)
    
