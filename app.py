from flask import Flask, jsonify, request
from models import db, User, Post, Follow, Customer, Product, Category, ProductCategoryMap, Order, OrderItem, Shipment, Warehouse, ShipmentItem, ProductReview

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

# ----- USERS -----
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'user_id': user.user_id, 'username': user.username, 'role': user.role, 'created_at': user.created_at} for user in users])

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(username=data['username'], role=data.get('role', ''))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Nuevo usuario creado'}), 201

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    user.username = data['username']
    user.role = data.get('role', user.role)
    db.session.commit()
    return jsonify({'message': 'Usuario actualizado'})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuario eliminado'})

# ----- POSTS -----
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{'post_id': post.post_id, 'title': post.title, 'body': post.body, 'user_id': post.user_id, 'status': post.status, 'created_at': post.created_at} for post in posts])

@app.route('/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    new_post = Post(title=data['title'], body=data['body'], user_id=data['user_id'], status=data['status'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Nueva publicación creada'}), 201

@app.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()
    post = Post.query.get(id)
    if not post:
        return jsonify({'message': 'Publicación no encontrada'}), 404

    post.title = data['title']
    post.body = data['body']
    post.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Publicación actualizada'})

@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    if not post:
        return jsonify({'message': 'Publicación no encontrada'}), 404

    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Publicación eliminada'})

# ----- FOLLOWS -----
@app.route('/follows', methods=['GET'])
def get_follows():
    follows = Follow.query.all()
    return jsonify([{'following_user_id': follow.following_user_id, 'followed_user_id': follow.followed_user_id, 'created_at': follow.created_at} for follow in follows])

@app.route('/follows', methods=['POST'])
def add_follow():
    data = request.get_json()
    new_follow = Follow(following_user_id=data['following_user_id'], followed_user_id=data['followed_user_id'])
    db.session.add(new_follow)
    db.session.commit()
    return jsonify({'message': 'Nuevo seguidor añadido'}), 201

@app.route('/follows/<int:following_user_id>/<int:followed_user_id>', methods=['DELETE'])
def delete_follow(following_user_id, followed_user_id):
    follow = Follow.query.filter_by(following_user_id=following_user_id, followed_user_id=followed_user_id).first()
    if not follow:
        return jsonify({'message': 'Relación no encontrada'}), 404

    db.session.delete(follow)
    db.session.commit()
    return jsonify({'message': 'Relación eliminada'})

# ----- CUSTOMERS -----
@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{'customer_id': customer.customer_id, 'username': customer.username, 'email': customer.email} for customer in customers])

@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    new_customer = Customer(customer_guid=data['customer_guid'], username=data['username'], email=data['email'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Nuevo cliente creado'}), 201

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({'message': 'Cliente no encontrado'}), 404

    customer.username = data['username']
    customer.email = data['email']
    db.session.commit()
    return jsonify({'message': 'Cliente actualizado'})

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return jsonify({'message': 'Cliente no encontrado'}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Cliente eliminado'})

# ----- PRODUCTS -----
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'product_id': product.product_id, 'name': product.name, 'short_description': product.short_description} for product in products])

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(product_type_id=data['product_type_id'], name=data['name'], short_description=data.get('short_description', ''))
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Nuevo producto creado'}), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Producto no encontrado'}), 404

    product.name = data['name']
    product.short_description = data.get('short_description', product.short_description)
    db.session.commit()
    return jsonify({'message': 'Producto actualizado'})

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Producto no encontrado'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Producto eliminado'})

# ----- CATEGORIES -----
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{'category_id': category.category_id, 'meta_title': category.meta_title, 'meta_description': category.meta_description} for category in categories])

@app.route('/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    new_category = Category(meta_title=data['meta_title'], meta_description=data['meta_description'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Nueva categoría creada'}), 201

@app.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.get_json()
    category = Category.query.get(id)
    if not category:
        return jsonify({'message': 'Categoría no encontrada'}), 404

    category.meta_title = data['meta_title']
    category.meta_description = data['meta_description']
    db.session.commit()
    return jsonify({'message': 'Categoría actualizada'})

@app.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({'message': 'Categoría no encontrada'}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Categoría eliminada'})

# ----- ORDERS -----
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{'order_id': order.order_id, 'customer_id': order.customer_id, 'order_guid': order.order_guid} for order in orders])

@app.route('/orders', methods=['POST'])
def add_order():
    data = request.get_json()
    new_order = Order(order_guid=data['order_guid'], store_id=data['store_id'], customer_id=data['customer_id'], billing_address_id=data['billing_address_id'], shipping_address_id=data['shipping_address_id'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Nuevo pedido creado'}), 201

@app.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    data = request.get_json()
    order = Order.query.get(id)
    if not order:
        return jsonify({'message': 'Pedido no encontrado'}), 404

    order.billing_address_id = data['billing_address_id']
    order.shipping_address_id = data['shipping_address_id']
    db.session.commit()
    return jsonify({'message': 'Pedido actualizado'})

@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get(id)
    if not order:
        return jsonify({'message': 'Pedido no encontrado'}), 404

    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Pedido eliminado'})

# ----- ORDER ITEMS -----
@app.route('/order_items', methods=['GET'])
def get_order_items():
    order_items = OrderItem.query.all()
    return jsonify([{'order_item_id': item.order_item_id, 'order_id': item.order_id, 'product_id': item.product_id, 'quantity': item.quantity} for item in order_items])

@app.route('/order_items', methods=['POST'])
def add_order_item():
    data = request.get_json()
    new_order_item = OrderItem(order_item_guid=data['order_item_guid'], order_id=data['order_id'], product_id=data['product_id'], quantity=data['quantity'])
    db.session.add(new_order_item)
    db.session.commit()
    return jsonify({'message': 'Nuevo item de pedido creado'}), 201

@app.route('/order_items/<int:id>', methods=['PUT'])
def update_order_item(id):
    data = request.get_json()
    order_item = OrderItem.query.get(id)
    if not order_item:
        return jsonify({'message': 'Item de pedido no encontrado'}), 404

    order_item.quantity = data['quantity']
    db.session.commit()
    return jsonify({'message': 'Item de pedido actualizado'})

@app.route('/order_items/<int:id>', methods=['DELETE'])
def delete_order_item(id):
    order_item = OrderItem.query.get(id)
    if not order_item:
        return jsonify({'message': 'Item de pedido no encontrado'}), 404

    db.session.delete(order_item)
    db.session.commit()
    return jsonify({'message': 'Item de pedido eliminado'})

# ----- SHIPMENTS -----
@app.route('/shipments', methods=['GET'])
def get_shipments():
    shipments = Shipment.query.all()
    return jsonify([{'shipment_id': shipment.shipment_id, 'order_id': shipment.order_id, 'tracking_number': shipment.tracking_number, 'total_weight': float(shipment.total_weight), 'shipped_date_utc': shipment.shipped_date_utc} for shipment in shipments])

@app.route('/shipments', methods=['POST'])
def add_shipment():
    data = request.get_json()
    new_shipment = Shipment(order_id=data['order_id'], tracking_number=data['tracking_number'], total_weight=data['total_weight'], shipped_date_utc=data['shipped_date_utc'])
    db.session.add(new_shipment)
    db.session.commit()
    return jsonify({'message': 'Nuevo envío creado'}), 201

@app.route('/shipments/<int:id>', methods=['PUT'])
def update_shipment(id):
    data = request.get_json()
    shipment = Shipment.query.get(id)
    if not shipment:
        return jsonify({'message': 'Envío no encontrado'}), 404

    shipment.tracking_number = data['tracking_number']
    shipment.total_weight = data['total_weight']
    shipment.shipped_date_utc = data['shipped_date_utc']
    db.session.commit()
    return jsonify({'message': 'Envío actualizado'})

@app.route('/shipments/<int:id>', methods=['DELETE'])
def delete_shipment(id):
    shipment = Shipment.query.get(id)
    if not shipment:
        return jsonify({'message': 'Envío no encontrado'}), 404

    db.session.delete(shipment)
    db.session.commit()
    return jsonify({'message': 'Envío eliminado'})

# ----- WAREHOUSES -----
@app.route('/warehouses', methods=['GET'])
def get_warehouses():
    warehouses = Warehouse.query.all()
    return jsonify([{'warehouse_id': warehouse.warehouse_id, 'name': warehouse.name, 'admin_comment': warehouse.admin_comment} for warehouse in warehouses])

@app.route('/warehouses', methods=['POST'])
def add_warehouse():
    data = request.get_json()
    new_warehouse = Warehouse(name=data['name'], admin_comment=data['admin_comment'])
    db.session.add(new_warehouse)
    db.session.commit()
    return jsonify({'message': 'Nuevo almacén creado'}), 201

@app.route('/warehouses/<int:id>', methods=['PUT'])
def update_warehouse(id):
    data = request.get_json()
    warehouse = Warehouse.query.get(id)
    if not warehouse:
        return jsonify({'message': 'Almacén no encontrado'}), 404

    warehouse.name = data['name']
    warehouse.admin_comment = data['admin_comment']
    db.session.commit()
    return jsonify({'message': 'Almacén actualizado'})

@app.route('/warehouses/<int:id>', methods=['DELETE'])
def delete_warehouse(id):
    warehouse = Warehouse.query.get(id)
    if not warehouse:
        return jsonify({'message': 'Almacén no encontrado'}), 404

    db.session.delete(warehouse)
    db.session.commit()
    return jsonify({'message': 'Almacén eliminado'})

# ----- SHIPMENT ITEMS -----
@app.route('/shipment_items', methods=['GET'])
def get_shipment_items():
    shipment_items = ShipmentItem.query.all()
    return jsonify([{'shipment_item_id': item.shipment_item_id, 'shipment_id': item.shipment_id, 'order_item_id': item.order_item_id, 'warehouse_id': item.warehouse_id} for item in shipment_items])

@app.route('/shipment_items', methods=['POST'])
def add_shipment_item():
    data = request.get_json()
    new_shipment_item = ShipmentItem(shipment_id=data['shipment_id'], order_item_id=data['order_item_id'], warehouse_id=data['warehouse_id'])
    db.session.add(new_shipment_item)
    db.session.commit()
    return jsonify({'message': 'Nuevo item de envío creado'}), 201

@app.route('/shipment_items/<int:id>', methods=['PUT'])
def update_shipment_item(id):
    data = request.get_json()
    shipment_item = ShipmentItem.query.get(id)
    if not shipment_item:
        return jsonify({'message': 'Item de envío no encontrado'}), 404

    shipment_item.order_item_id = data['order_item_id']
    shipment_item.warehouse_id = data['warehouse_id']
    db.session.commit()
    return jsonify({'message': 'Item de envío actualizado'})

@app.route('/shipment_items/<int:id>', methods=['DELETE'])
def delete_shipment_item(id):
    shipment_item = ShipmentItem.query.get(id)
    if not shipment_item:
        return jsonify({'message': 'Item de envío no encontrado'}), 404

    db.session.delete(shipment_item)
    db.session.commit()
    return jsonify({'message': 'Item de envío eliminado'})

# ----- PRODUCT REVIEWS -----
@app.route('/product_reviews', methods=['GET'])
def get_product_reviews():
    reviews = ProductReview.query.all()
    return jsonify([{'review_id': review.review_id, 'customer_id': review.customer_id, 'product_id': review.product_id, 'is_approved': review.is_approved, 'title': review.title, 'review_text': review.review_text} for review in reviews])

@app.route('/product_reviews', methods=['POST'])
def add_product_review():
    data = request.get_json()
    new_review = ProductReview(customer_id=data['customer_id'], product_id=data['product_id'], is_approved=data['is_approved'], title=data['title'], review_text=data['review_text'])
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Nueva reseña de producto creada'}), 201

@app.route('/product_reviews/<int:id>', methods=['PUT'])
def update_product_review(id):
    data = request.get_json()
    review = ProductReview.query.get(id)
    if not review:
        return jsonify({'message': 'Reseña no encontrada'}), 404

    review.is_approved = data['is_approved']
    review.title = data['title']
    review.review_text = data['review_text']
    db.session.commit()
    return jsonify({'message': 'Reseña actualizada'})

@app.route('/product_reviews/<int:id>', methods=['DELETE'])
def delete_product_review(id):
    review = ProductReview.query.get(id)
    if not review:
        return jsonify({'message': 'Reseña no encontrada'}), 404

    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Reseña eliminada'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
