from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db
from models.admin import Admin
from models.customers import Customer
from models.game import Game

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games_shop.db'
db.init_app(app)


@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    if not data['name'] or not data['email'] or not data['phone']:
        return jsonify({'error': 'All fields are required'}), 400

    new_customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data['phone']
    )
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully'}), 201


@app.route('/customers', methods=['GET'])
def get_customers():
    try:
        customers = Customer.query.all()
        customers_list = [{'id': c.id, 'name': c.name, 'email': c.email, 'phone': c.phone} for c in customers]
        return jsonify({'customers': customers_list}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve customers', 'message': str(e)}), 500


@app.route('/customers/<int:customer_id>', methods=['PUT'])
def edit_customer(customer_id):
    data = request.json
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    if 'name' in data:
        customer.name = data['name']
    if 'email' in data:
        customer.email = data['email']
    if 'phone' in data:
        customer.phone = data['phone']

    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'}), 200


@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'}), 200



@app.route('/games', methods=['POST'])
def add_game():
    data = request.json
    if not data['title'] or not data['genre'] or not data['price'] or not data['quantity']:
        return jsonify({'error': 'All fields are required'}), 400

    new_game = Game(
        title=data['title'],
        genre=data['genre'],
        price=data['price'],
        quantity=data['quantity']
    )
    db.session.add(new_game)
    db.session.commit()
    return jsonify({'message': 'Game added to database.'}), 201


@app.route('/games', methods=['GET'])
def get_games():
    try:
        games = Game.query.all()
        games_list = []

        for game in games:
            game_data = {
                'id': game.id,
                'title': game.title,
                'genre': game.genre,
                'price': game.price,
                'quantity': game.quantity,
                'loan_status': game.loan_status,
            }
            games_list.append(game_data)

        return jsonify({
            'message': 'Games retrieved successfully',
            'games': games_list
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve games',
            'message': str(e)
        }), 500


@app.route('/games/<int:game_id>', methods=['PUT'])
def edit_game(game_id):
    data = request.json
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    # Update fields
    if 'title' in data:
        game.title = data['title']
    if 'genre' in data:
        game.genre = data['genre']
    if 'price' in data:
        game.price = data['price']
    if 'quantity' in data:
        game.quantity = data['quantity']

    db.session.commit()
    return jsonify({'message': 'Game updated successfully'}), 200


@app.route('/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    db.session.delete(game)
    db.session.commit()
    return jsonify({'message': 'Game deleted successfully'}), 200


@app.route('/add_admin', methods=['POST'])
def add_admin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    new_admin = Admin(email=email, password=password)
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({'message': 'Admin added successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_email = data['email']
    user_password = data['password']
    user = Admin.query.filter_by(email=user_email, password=user_password).first()
    if user:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid email or password.'}), 401


@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'You are logged out.'}), 200



@app.route('/games/<int:game_id>/loan', methods=['PUT'])
def loan_game(game_id):
    data = request.json
    customer_id = data.get('customer_id')  # מזהה הלקוח שמשאיל את המשחק

    # מציאת המשחק
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    # אם המשחק כבר מושאל, לא ניתן לשאול אותו שוב
    if game.loan_status:
        return jsonify({'error': 'Game is already loaned out'}), 400

    # עדכון הסטטוס של המשחק
    game.loan_status = True  # המשחק מושאל
    game.customer_relationship = customer_id  # שמירה על מזהה הלקוח

    db.session.commit()
    return jsonify({'message': f'Game "{game.title}" loaned to customer with ID {customer_id} successfully'}), 200



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
