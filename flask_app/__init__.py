from flask import Flask
from flask_bcrypt import Bcrypt


app = Flask(__name__)

DATABASE = "recipes_db"
BCRPYT = Bcrypt(app)

app.secret_key = "password"