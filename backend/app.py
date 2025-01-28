from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from models import db
from models.user import User
from models.game import Game
from models.loans import Loan

app = Flask(__name__)  # יצירת מופע Flask
CORS(app, resources={r"/*": {"origins": "*"}})  # לאפשר בקשות מכל מקור (לא מומלץ לאבטחה)

# הגדרת חיבור למסד הנתונים (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
db.init_app(app)  # חיבור Flask למסד הנתונים

@app.route('/games', methods=['POST'])
def add_game():
    data = request.json  # קריאת הנתונים מהבקשה
    new_game = Game(
        name=data['name'],
        creator=data['creator'],
        year_released=data['year_released'],
        genre=data['genre']
    )
    db.session.add(new_game)  # הוספת המשחק למסד הנתונים
    db.session.commit()  # שמירת השינויים
    return jsonify({'message': 'Game added to database.'}), 201

@app.route('/games', methods=['GET'])
def get_games():
    try:
        games = Game.query.all()  # שליפת כל המשחקים ממסד הנתונים
        games_list = []

        for game in games:
            game_data = {
                'id': game.id,
                'name': game.name,
                'creator': game.creator,
                'year_released': game.year_released,
                'genre': game.genre
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # יצירת כל הטבלאות המוגדרות במודלים

    app.run(debug=True)  # הפעלת האפליקציה במצב debug