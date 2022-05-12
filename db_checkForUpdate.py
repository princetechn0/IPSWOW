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

    def __init__(self, hashValue):
        self.hashValue = hashValue

    def __repr__(self) -> str:
        return "Current Hash Value: %s" % (self.hashValue) 


def checkForUpdate():
    try:
        all_devices_api = requests.get("https://api.ipsw.me/v4/devices").json()
        newHash = hashlib.md5(json.dumps(all_devices_api, sort_keys = True).encode("utf-8")).hexdigest()
        currentHash = CurrentApiHash.query.first().hashValue

        if(currentHash != newHash):
            print("API outdated. Running Update")
            updateAll()
            updateHash(newHash)
        else:
            print("API up to date")
            print("Running App without Update")

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
      clear_data()
      db.session.add(CurrentApiHash(newHashValue))
      db.session.commit()
      print("Hash Update Success")
  except:
    print("Hash Update Failed")


def clear_data():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
        db.session.commit()
    print("DB Cleared")