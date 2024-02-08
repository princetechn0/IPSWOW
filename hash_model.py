import requests
import hashlib
import json
from db_init import initDB
from app_setup import db


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
        currentHash = CurrentApiHash.query.first()

        print("New Hash from Server", newHash)
        print("Current Hash in DB", currentHash)


        if(currentHash is None or currentHash.hashValue != newHash):
            print("API outdated. Running Update")
            updateAll()
            updateHash(newHash)
        else:
            print("API up to date")
            print("Running App without Update")
    except Exception as e:
        print(f"Check Hash Failed: {e}")


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
    CurrentApiHash.query.delete()
    db.session.commit()
    print("HASH DB Cleared")