
import os
from datetime import timedelta
from dotenv import load_dotenv


config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.env')
if os.path.exists(config_path):
    load_dotenv(config_path)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '1234')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://manasa:1234@studybuddy.azclr1h.mongodb.net/studybuddy?retryWrites=true&w=majority&appName=studyBuddy')
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    SESSION_PROTECTION = 'strong'
    

    MONGO_DBNAME = 'studybuddy'
    

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'manasavinodkumar@gmail.com')
