from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from models import db
from models.game import Game
from models.admin import Admin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_COOKIE_NAME'] = 'admin_session'
app.config['SESSION_COOKIE_HTTPONLY'] = False  # מאפשר גישה לסשן דרך JS (אם צריך)
db.init_app(app)

@app.route('/admin', methods=['GET'])
def get_admins():
    admins = Admin.query.all()
    games_list = [{
        'id': admin.id,
        'username': admin.username,
        'password': admin.password
    } for admin in admins]
    return jsonify({'message:': 'successful','games': games_list}), 200
# יצירת המשתמש 'noam' אם הוא לא קיים
@app.before_request
def create_admin():
    admin = Admin.query.filter_by(username="noam").first()
    if not admin:
        # יצירת סיסמה מוצפנת
        hashed_password = generate_password_hash("290106Na", method='sha256')
        admin = Admin(username="noam", password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: noam")  # הודעה בקונסול אם נוצר משתמש


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    user_password = data['password']
    user = Admin.query.filter_by(username=username,password=user_password).first()  # חפש משתמש לפי שם משתמש
    if user:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password.'}), 401


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('admin', None)  # מחק את שם המשתמש מהסשן
    return jsonify({'message': 'Logged out successfully'}), 200


# הוספת משחק חדש
@app.route('/games', methods=['POST'])
def add_game():
    if 'admin' not in session:  # אם אין סשן לאדמין
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.json
    new_game = Game(
        title=data['title'],
        genre=data['genre'],
        price=data['price'],
        quantity=data['quantity']
    )
    db.session.add(new_game)
    db.session.commit()
    return jsonify({'message': 'Game added successfully'}), 201


# הצגת רשימת משחקים
@app.route('/games', methods=['GET'])
def get_games():
    if 'admin' not in session:
        return jsonify({'message': 'Unauthorized'}), 403
    games = Game.query.all()
    games_list = [
        {'id': game.id, 'title': game.title, 'genre': game.genre, 'price': game.price, 'quantity': game.quantity} for
        game in games]
    return jsonify({'games': games_list}), 200


# מחיקת משחק לפי ID
@app.route('/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    if 'admin' not in session:
        return jsonify({'message': 'Unauthorized'}), 403
    game = Game.query.get(game_id)
    if game:
        db.session.delete(game)
        db.session.commit()
        return jsonify({'message': 'Game deleted successfully'}), 200
    return jsonify({'message': 'Game not found'}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # יצירת כל הטבלאות במערכת
    app.run(debug=True)
