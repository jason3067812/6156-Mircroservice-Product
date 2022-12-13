from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields
from db import db


class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)


class Category:
    APPLIANCES = 'Appliances'
    ELECTRONICS = 'Electronics'
    SPORTS = 'Sports'
    CLOTHING = 'Clothing'
    OTHERS = 'Others'


class Product(Base):
    __tablename__ = 'product'
    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    image = Column(String(256), nullable=True)
    category = Column(String(64), nullable=False, default=Category.OTHERS)
    discount = Column(Float, nullable=False, default=1.0)
    provider_id = Column(Integer)


class ProductSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    price = fields.Float()
    stock = fields.Int()
    image = fields.Str()
    category = fields.Str()
    discount = fields.Float()
    provider_id = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class Cart(Base):
    user_id = Column(Integer, nullable=False)
    items = relationship("CartItem", back_populates="cart")

    @property
    def count(self):
        return sum([item.quantity for item in self.items])

    @property
    def total_price(self):
        price = 0.0
        for item in self.items:
            price += item.product.price * item.product.discount * item.quantity
        return round(price, 2)


class CartSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    total_price = fields.Float()


class CartItem(Base):
    quantity = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('product.id', ondelete='SET NULL'))
    product = relationship("Product")
    cart_id = Column(Integer, ForeignKey('cart.id', ondelete='SET NULL'))
    cart = relationship("Cart", back_populates="items")


class CartItemSchema(Schema):
    id = fields.Int()
    quantity = fields.Int()
    product_id = fields.Int()
    cart_id = fields.Int()


class OrderStatus:
    CANCELLED = 'Cancelled'
    PENDING = 'Pending'
    FINISHED = 'Finished'


class Order(Base):
    status = Column(String(64), nullable=False, default=OrderStatus.PENDING)
    user_id = Column(Integer, nullable=False)
    items = relationship("OrderItem", back_populates="order")
    address_id = Column(Integer)

    @property
    def total(self):
        t = 0.0
        for item in self.items:
            t += item.product.price * item.product.discount * item.quantity
        return round(t, 2)


class OrderItem(Base):
    quantity = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey('product.id', ondelete='SET NULL'))
    product = relationship("Product")
    order_id = Column(Integer, ForeignKey('order.id', ondelete='SET NULL'))
    order = relationship("Order", back_populates="items")


class OrderSchema(Schema):
    id = fields.Int()
    status = fields.Str()
    user_id = fields.Int()
    total = fields.Float()


class OrderItemSchema(Schema):
    id = fields.Int()
    quantity = fields.Int()
    product_id = fields.Int()
    cart_id = fields.Int()