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


@app.route('/games', methods=['POST'])
def add_game():
    data = request.json
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
                'customer_relationship': game.customer_relationship
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


@app.route('/customer', methods=['GET'])
def is_user_exits():
    pass


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
    return jsonify({'message': 'You are logout.'}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
