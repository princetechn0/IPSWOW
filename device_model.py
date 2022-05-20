from flask_sqlalchemy import SQLAlchemy
from app_setup import app, db

SQLALCHEMY_TRACK_MODIFICATIONS = False
# db_device = SQLAlchemy(app)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    firmware = db.Column(db.String(20), nullable=False)

    def __init__(self, url, name, firmware):
        self.url = url
        self.name = name
        self.firmware = firmware

    def __repr__(self) -> str:
        return "%s, %s, %s" % (self.url, self.name, self.firmware) 

    def dictRep(self):
        return {
            'url' : self.url,
            'name': self.name,
            'firmware': self.firmware
        }



def add_data(url, name, firmware):  
  try:
      db.session.add(Device(url, name, firmware))
      db.session.commit()
      print("Added")
  except:
    print("Add Device failed")

def initializeDB(incoming_data):
    for x in incoming_data:
        add_data(x[0], x[1], x[2])
    print("DEVICE DB initialized")

def clear_data():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
        db.session.commit()
    print("DEVICE DB Cleared")
