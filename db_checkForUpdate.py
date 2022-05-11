from turtle import update
from flask_sqlalchemy import SQLAlchemy
import requests
import hashlib
import json
from application import app
from db_init import initDB

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)

class CurrentApiHash(db.Model):
    hashValue = db.Column(db.String(32), nullable=False, primary_key=True)

    def __repr__(self):
        return '<Currently Saved Hash: %r>' % self.hashValue


def checkForUpdate():
    try:
        all_devices_api = requests.get("https://api.ipsw.me/v4/devices").json()
        newHash = hashlib.md5(json.dumps(all_devices_api, sort_keys = True).encode("utf-8")).hexdigest()
        currentHash = CurrentApiHash.query.first().hashValue

        print(newHash)
        print(CurrentApiHash.query.first().hashValue)
        
        if(currentHash != newHash):
            print("rinning")
            updateAll()
            updateHash(newHash)
        else:
            print("API up to date")

    except:
        print("Check Hash Failed")


def updateAll():  
  try:
      initDB()
      print("New table data finished")
  except:
    print("Add Device failed")


def updateHash(newHashValue):  
  try:
      db.session.add(CurrentApiHash(newHashValue))
      db.session.commit()
      print("Hash Update Success")
  except:
    print("Hash Update Failed")