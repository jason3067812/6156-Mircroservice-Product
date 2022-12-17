from flask import Flask, jsonify, request, render_template
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy import desc, asc
import os
from db import db
from models import Product, Order, OrderItem, Cart, CartItem
from models import ProductSchema, CartSchema, CartItemSchema, OrderSchema, OrderItemSchema

application = Flask(__name__)
application.secret_key = 'cc6156-ms-product'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# development
# DB_HOST, DB_PORT = 'localhost', 3306
# DB_NAME = 'ms_product'
# DB_USERNAME, DB_PASSWORD = 'root', 'root'
DB_HOST, DB_PORT = "test.cvwwgxdyhdlt.us-east-2.rds.amazonaws.com", 3306
DB_NAME = 'project'
DB_USERNAME, DB_PASSWORD = 'admin', 'eric30678'

# production
# DB_HOST = os.environ['DB_HOST']
# DB_PORT = os.environ['DB_PORT']
# DB_NAME = os.environ['DB_NAME']
# DB_USERNAME = os.environ['DB_USERNAME']
# DB_PASSWORD = os.environ['DB_PASSWORD']


application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
)


db.init_app(application)
migrate = Migrate(application, db)


CORS(application)

productSchema = ProductSchema()
cartSchema = CartSchema()
cartItemSchema = CartItemSchema()
orderSchema = OrderSchema()
orderItemSchema = OrderItemSchema()

@application.route('/api/docs', methods=['GET'])
def get_docs():
    return render_template('/swaggerui.html')

@application.route("/api", methods=['GET'])
def index():
    return "product service"

@application.route("/api/products", methods=['GET'])
def products():
    args = request.args
    products = Product.query
    if 'category' in args:
        products = products.filter(Product.category == args['category'])
    if 'onsale' in args and args['onsale'] == 'true':
        products = products.filter(Product.discount < 1.0)
    if 'sort_by' in args:
        if 'ordering' in args and args['ordering'] == 'desc':
            products = products.order_by(desc(getattr(Product, args['sort_by'])))
        products = products.order_by(asc(getattr(Product, args['sort_by'])))
    if 'limit' in args:
        products = products.limit(int(args['limit']))
    products = products.all()
    return jsonify(
        message=f"list all products",
        data=productSchema.dump(obj=products, many=True),
        count=len(products),
        status=200
    )


@application.route("/api/products", methods=['POST'])
def create_product():
    data = request.json
    name = data['name']
    description = data['description']
    price = data['price']
    stock = data['stock']
    image = data['image']
    category = data['category']
    discount = data['discount']
    provider_id = int(data['provider_id'])
    p = Product(name=name, description=description, price=price, stock=stock,
                image=image, category=category, discount=discount, provider_id=provider_id)
    db.session.add(p)
    db.session.commit()
    return jsonify(
        message=f"create a product",
        data=productSchema.dump(obj=p),
        status=200
    )

@application.route('/api/products/<int:id>', methods=['DELETE'])
def delete(id):
    product = Product.query.filter_by(id=id).first()
    if product:
        db.session.delete(product)
        db.session.commit()

    return jsonify(
        message=f"delete product",
        status=200
    )

@application.route('/api/products/<int:id>', methods=['POST'])
def update(id):
    data = request.json
    product = Product.query.filter_by(id=id).first()
    for key, value in data.items():
        setattr(product, key, value)
    db.session.commit()

    return jsonify(
        message=f"update product",
        data=productSchema.dump(obj=product),
        status=200
    )



@application.route("/api/products/<category>", methods=['GET'])
def search_by_category(category):
    products = Product.query.filter(Product.category == category).all()
    return jsonify(
        message=f"list products",
        data=productSchema.dump(obj=products, many=True),
        count=products.count(),
        status=200
    )

@application.route("/api/products/search", methods=['GET'])
def search():
    args = request.args
    print(args)
    products = Product.query
    if 'category' in args:
        categories = args['category'].split(',')
        products = products.filter(Product.category.in_(categories))
    if 'discount' in args:
        products = products.filter(Product.discount < 1.0)
    if 'stock' in args:
        products = products.filter(Product.stock > 0)
    if 'ordering' in args:
        if args['ordering'] == 'desc':
            products = products.order_by(Product.price.desc())
        elif args['ordering'] == 'asc':
            products = products.order_by(Product.price.asc())

    count = products.count()
    if 'page' in args:
        # page = args.get('page', type=int, default=1)
        # products = products.paginate(page=int(args['page']), per_page=5, error_out=False)
        products = products.offset((int(args['page'])-1) * 5).limit(5)
    products = products.all()
    return jsonify(
        message=f"list products",
        data=productSchema.dump(obj=products, many=True),
        count=count,
        status=200
    )

@application.route("/api/cart", methods=['POST'])
def createCart():
    data = request.json
    user_id = data['user_id']
    if Cart.query.filter_by(user_id=user_id).count() == 0:
        c = Cart(user_id=user_id)
        db.session.add(c)
        db.session.commit()
        return jsonify(
            message=f"create a cart",
            data=cartSchema.dump(obj=c),
            status=201
        )
    return jsonify(
        message=f"existing cart",
        status=201
    )

@application.route("/api/cart/<user_id>", methods=['GET'])
def getCart(user_id):
    cart = Cart.query.filter_by(user_id=user_id).first()
    items = []
    for item in cart.items:
        items.append({'id': item.id, 'name': item.product.name, 'price': item.product.price,
                      'quantity': item.quantity})
    total_price = cart.total_price
    return jsonify(
        message=f"cart info",
        data={
            'items': items,
            'count': cart.count,
            'total_price': total_price
        },
        status=200
    )


@application.route("/api/cart/item", methods=['POST'])
def createCartItem():
    data = request.json
    product_id = data['product_id']
    quantity = data['quantity']
    cart_id = Cart.query.filter_by(user_id=data['user_id']).first().id
    item = CartItem.query.filter_by(product_id=product_id, cart_id=cart_id).first()
    if item:
        item.quantity += 1
    else:
        item = CartItem(product_id=product_id, quantity=quantity, cart_id=cart_id)
        db.session.add(item)
    db.session.commit()
    return jsonify(
        message=f"create a cart item",
        data=cartSchema.dump(obj=item),
        status=200
    )

@application.route("/api/cart/item/<id>", methods=['POST'])
def updateCartItem(id):
    data = request.json
    item = CartItem.query.filter_by(id=id).first()
    item.quantity = data['quantity']
    db.session.commit()

    return jsonify(
        message=f"update cart item",
        data=cartItemSchema.dump(obj=item),
        status=200
    )

@application.route('/api/cart/item/<int:id>', methods=['DELETE'])
def deleteCartItem(id):
    item = CartItem.query.filter_by(id=id).first()
    db.session.delete(item)
    db.session.commit()

    return jsonify(
        message=f"Delete cart item",
        status=200
    )

@application.route("/api/orders", methods=['POST'])
def createOrder():
    data = request.json
    user_id = data['user_id']
    cart = Cart.query.filter_by(user_id=user_id).first()
    o = Order(user_id=user_id)
    db.session.add(o)
    for item in cart.items:
        it = OrderItem(product_id=item.product_id, quantity=item.quantity, order_id=o.id)
        db.session.add(it)
    CartItem.query.filter_by(cart_id=cart.id).delete()
    db.session.commit()
    return jsonify(
        message=f"create a order",
        data=cartSchema.dump(obj=o),
        status=200
    )

@application.route("/api/orders/<id>", methods=['GET'])
def getOrder(id):
    order = Order.query.filter_by(id=id).first()
    items = []
    for item in order.items:
        items.append({'id': item.id, 'name': item.product.name, 'price': round(item.product.price * item.product.discount, 2),
                      'image': item.product.image, 'quantity': item.quantity})
    return jsonify(
        message=f"order info",
        data={
            'items': items,
            'status': order.status,
            'total': order.total
        },
        status=200
    )

@application.route("/api/orders/<id>", methods=['POST'])
def updateOrder(id):
    data = request.json
    order = Order.query.filter_by(id=id).first()
    order.status = data['status']
    order.address_id = data['address_id'] if 'address_id' in data else None
    db.session.commit()

    return jsonify(
        message=f"update order",
        data=cartItemSchema.dump(obj=order),
        status=200
    )

@application.route("/api/orders", methods=['GET'])
def orders():
    user_id = request.args['user_id']
    os = Order.query.filter_by(user_id=user_id).all()
    orders_list = []
    for order in os:
        order_formatted = {'created_at': order.created_at.strftime("%b %d, %Y"), 'id': order.id, 'status': order.status, 'images': []}
        for item in order.items:
            order_formatted['images'].append(item.product.image)
        orders_list.append(order_formatted)

    return jsonify(
        message=f"orders",
        data=orders_list,
        status=200
    )


@application.route("/api/orders/item/<id>", methods=['POST'])
def updateOrderItem(id):
    data = request.json
    item = OrderItem.query.filter_by(id=id).first()
    item.quantity = data['quantity']
    db.session.commit()

    return jsonify(
        message=f"update order item",
        data=cartItemSchema.dump(obj=item),
        status=200
    )

@application.route('/api/orders/item/<int:id>', methods=['DELETE'])
def deleteOrdertem(id):
    item = OrderItem.query.filter_by(id=id).first()
    db.session.delete(item)
    db.session.commit()

    return jsonify(
        message=f"Delete order item",
        status=200
    )

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5001)
