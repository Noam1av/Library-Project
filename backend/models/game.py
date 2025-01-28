# create a __init__.py file in the models folder to make all the model act as a package if you dont have it already , also you can make one file with all the models just copy ythe all the code in the files into it

from . import db
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)  # שם המשחק
    creator = db.Column(db.String(200), nullable=False)  # שם היוצר
    year_released = db.Column(db.Integer, nullable=False)  # שנת ההוצאה
    genre = db.Column(db.String(100), nullable=False)  # סגנון המשחק
