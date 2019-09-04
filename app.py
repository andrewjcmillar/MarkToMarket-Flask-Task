import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['PORT'] = os.getenv('PORT', 5000)
app.config['HOST'] = os.getenv('HOST', 'localhost')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'SQLALCHEMY_DATABASE_URI', 'postgresql://postgres:password@localhost:5432/postgres'
)

db = SQLAlchemy(app)

from views import *

db.create_all()
