# app.py
from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from config import Config

# Extensions
mongo = PyMongo()
login_manager = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from flask import Blueprint
quiz_test = Blueprint('quiz_test', __name__)

@quiz_test.route('/quiz-test')
def quiz_test_route():
    return "✅ Quiz blueprint is reachable"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    mongo.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)

    from app.study.routes import study
    from app.models import User
    from app.users.routes import users
    from app.quiz.routes import quiz

    app.register_blueprint(study)
    app.register_blueprint(users)
    app.register_blueprint(quiz)
 


    from flask import render_template

    @app.route('/')
    def index():
        return render_template('index.html')
    import app.quiz.routes
    return app

from app import mongo, login_manager, bcrypt
