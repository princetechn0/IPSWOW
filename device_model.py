from app_setup import db


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    firmware = db.Column(db.String, nullable=False)

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
    print(url, name, firmware)
    print("Add Device failed")

def initializeDB(incoming_data):
    for x in incoming_data:
        add_data(x[0], x[1], x[2])
    print("DEVICE DB initialized")

def clear_data():
    Device.query.delete()
    db.session.commit()
    print("DEVICE DB Cleared")
