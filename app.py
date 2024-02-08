#!/usr/bin/env python3
from app_setup import app
from hash_model import checkForUpdate
from device_model import Device
from flask_cors import CORS
from urllib.parse import unquote

CORS(app)
app.app_context().push()

checkForUpdate()


def convertToJSON(deviceList):
    return ([r.dictRep() for r in deviceList])

with app.app_context():
    grouped_iPhones = convertToJSON(Device.query.filter(Device.name.contains('iPhone')).order_by(Device.id).all())
    grouped_iPads = convertToJSON(Device.query.filter(Device.name.contains('iPad')).all())
    grouped_Macs = convertToJSON(Device.query.filter(Device.name.contains('Mac')).all())
    grouped_iPods = convertToJSON(Device.query.filter(Device.name.contains('iPod')).all())
    grouped_Watches = convertToJSON(Device.query.filter(Device.name.contains('Watch')).all())

column_headers = ["iOS", "iPadOS", "MacOS / WatchOS"]


# Get latest firmwares for each OS type
latest_firmwares = {
    "iOS": "",
    "iPadOS": "",
    "MacOS": "",
    "WatchOS": "",
}
try:
    if grouped_iPhones:
        latest_firmwares["iOS"] = grouped_iPhones[-1]['firmware']
except (IndexError, KeyError):
    pass

try:
    if grouped_iPads:
        latest_firmwares["iPadOS"] = grouped_iPads[-1]['firmware']
except (IndexError, KeyError):
    pass

try:
    if grouped_Macs:
        latest_firmwares["MacOS"] = grouped_Macs[-1]['firmware']
except (IndexError, KeyError):
    pass

try:
    if grouped_Watches:
        latest_firmwares["WatchOS"] = grouped_Watches[-1]['firmware']
except (IndexError, KeyError):
    pass


@ app.route("/")
@ app.route("/home")
def home():
    return { 'devices' : [{'name': 'iOS', 'data' : [*grouped_iPhones[::-1], *grouped_iPods[::-1]]}, {'name': 'iPadOS', 'data': grouped_iPads[::-1]}, {'name': 'MacOS/WatchOS', 'data': [*grouped_Macs, *grouped_Watches[::-1]]}], 'firmwares': latest_firmwares}

@app.route("/getDeviceByName/<device_name>")
def getDeviceByName(device_name):
    decoded_device_name = unquote(device_name)
    print("Searching for device with name:", decoded_device_name)

    first_entry = Device.query.filter(Device.name == decoded_device_name).first()
    print(first_entry)
    
    if first_entry:
        return first_entry.dictRep()
    else:
        return f"No device found with name: {decoded_device_name}", 404

if __name__ == "__main__":
    app.run(debug=False)
