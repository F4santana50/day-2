from flask import *
import datetime 
import random 
import string 
import json 
import os

from flask_sqlalchemy import SQLAlchemy 

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend 
from cryptography.hazmat.primitives import hashes 
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64 



import colorama 
from colorama import Fore


# load_dotenv(find_dotenv())


class Config(object): 

    DEBUG = True
    TESTING = True
    CSRF_ENABLED = True_SQLAlchemy_TRACK_MODIFICATIONS = True
    apphost = os.getenv("Host")
    port = os.getenv("PORT")

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True 
    SESSION_COOKIE_SAMESITE = 'None'

    db_ip = os.getenv("dp_ip")
    db_name = os.getenv("db_name")
    db_username = os.getenv("username_db")
    db_password = os.getenv("password_db")


class Productionconfig(Config): 
    DEBUG = False
    AWS_SECRET_ACCESS_KEY = os.getenv("secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False 


class DevelopmentConfig(Config):
    ENV = "Development"
    DEVELOPMENT = True
    SECRET_KEY = os.getenv("secret_key_Two")

    OAUTHLIB_INSECURE_TRANSPOT = True 
    SQLALCHEMY_TRACK_MODIFICATIONS = False 


app = Flask(__name__)

colorama.init(autoreset=True)

success = Fore.GREEN
warning = Fore.YELLOW
error = Fore.RED

mysql_db_conn = f'mysql+pymysql://{Config.db_username}:{Config.db_password}@{Config.db_ip}/{Config.db_name}'

test_name_db = "Users"

temp_dp = f"sqlite:///{str(test_name_db)}.sqlite3"

format = "utf-8"
app.config["SQLALCHEMY_DATABASE_URI"] = temp_dp
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = "Users"
    _id = db.Column("id",db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    api_key = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self,username,password,email,api_key):
        self.username = username
        self.password = password
        self.email = email 
        self.api_key = api_key


@app.route("/")
def indexMain():
    return json.dumps(
        {
            "Server": "Online"
        }
    )

def run():
    try:
        db.create_all()
        app.run(
            threaded=True, 
            debug=Config.DEBUG, 
            port=Config.port,
            host=Config.apphost
        )
    except Exception as e:
        print(f"{error} {str(e)}")


if __name__ == '__main__':
    run()