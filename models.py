from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ----- USERS -----
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50))
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

# ----- POSTS -----
class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    status = db.Column(db.String(50))
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('posts', lazy=True))

# ----- FOLLOWS -----
class Follow(db.Model):
    __tablename__ = 'follows'
    following_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    followed_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

# ----- CUSTOMERS -----
class Customer(db.Model):
    __tablename__ = 'customers'
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_guid = db.Column(db.String(36))
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

# ----- PRODUCTS -----
class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_type_id = db.Column(db.Integer)
    parent_grouped_product_id = db.Column(db.Integer)
    visible_individually = db.Column(db.Boolean)
    name = db.Column(db.String(255), nullable=False)
    short_description = db.Column(db.String(1000))

# ----- CATEGORIES -----
class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meta_description = db.Column(db.String(1000))
    meta_title = db.Column(db.String(255))
    parent_category_id = db.Column(db.Integer)
    picture_id = db.Column(db.Integer)
    page_size = db.Column(db.Integer)

# ----- PRODUCT CATEGORY MAP -----
class ProductCategoryMap(db.Model):
    __tablename__ = 'product_category_map'
    map_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    is_featured_product = db.Column(db.Boolean)
    display_order = db.Column(db.Integer)

    product = db.relationship('Product', backref=db.backref('product_categories', lazy=True))
    category = db.relationship('Category', backref=db.backref('product_categories', lazy=True))

# ----- ORDERS -----
class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_guid = db.Column(db.String(36))
    store_id = db.Column(db.Integer, unique=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    billing_address_id = db.Column(db.Integer)
    shipping_address_id = db.Column(db.Integer)

    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))

# ----- ORDER ITEMS -----
class OrderItem(db.Model):
    __tablename__ = 'order_items'
    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_item_guid = db.Column(db.String(36))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer)

    order = db.relationship('Order', backref=db.backref('order_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('order_items', lazy=True))

# ----- SHIPMENTS -----
class Shipment(db.Model):
    __tablename__ = 'shipments'
    shipment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    tracking_number = db.Column(db.String(255))
    total_weight = db.Column(db.Numeric(18, 2))
    shipped_date_utc = db.Column(db.DateTime)

    order = db.relationship('Order', backref=db.backref('shipments', lazy=True))

# ----- WAREHOUSES -----
class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    warehouse_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    admin_comment = db.Column(db.String(1000))
    address_id = db.Column(db.Integer)

# ----- SHIPMENT ITEMS -----
class ShipmentItem(db.Model):
    __tablename__ = 'shipment_items'
    shipment_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shipment_id = db.Column(db.Integer, db.ForeignKey('shipments.shipment_id'), nullable=False)
    order_item_id = db.Column(db.Integer, db.ForeignKey('order_items.order_item_id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.warehouse_id'), nullable=False)

    shipment = db.relationship('Shipment', backref=db.backref('shipment_items', lazy=True))
    order_item = db.relationship('OrderItem', backref=db.backref('shipment_items', lazy=True))
    warehouse = db.relationship('Warehouse', backref=db.backref('shipment_items', lazy=True))

# ----- PRODUCT REVIEWS -----
class ProductReview(db.Model):
    __tablename__ = 'product_reviews'
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    is_approved = db.Column(db.Boolean)
    title = db.Column(db.String(255))
    review_text = db.Column(db.String(2000))

    customer = db.relationship('Customer', backref=db.backref('product_reviews', lazy=True))
    product = db.relationship('Product', backref=db.backref('product_reviews', lazy=True))
