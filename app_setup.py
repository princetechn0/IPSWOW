from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jsatwyoeevweno:c6da2df7ed6f7466b46efcab85110dfd8e865e7db7047ce676d906882cb10580@ec2-54-80-122-11.compute-1.amazonaws.com:5432/d8vusfpuh3n3cp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Corrected line

db = SQLAlchemy(app)
