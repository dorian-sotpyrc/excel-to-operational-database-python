from __future__ import annotations

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    joined_date = Column(DateTime, nullable=True)

    orders = relationship("Order", back_populates="customer")


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    unit_price = Column(Float, nullable=True)

    orders = relationship("Order", back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    order_date = Column(DateTime, nullable=True)
    quantity = Column(Integer, nullable=True)

    customer = relationship("Customer", back_populates="orders")
    product = relationship("Product", back_populates="orders")
