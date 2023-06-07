#!/usr/bin/env python3
from flask import render_template
from app_setup import app
from hash_model import checkForUpdate
from device_model import Device

checkForUpdate()

def convertToJSON(deviceList):
    return ([r.dictRep() for r in deviceList])

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
    return render_template('home.html', data=[column_headers, grouped_iPhones, grouped_iPads, grouped_Macs, grouped_iPods, grouped_Watches, latest_firmwares])

@ app.route("/presets")
def presets():
    return render_template('presets.html')


@ app.route("/about")
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=False)
