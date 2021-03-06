#!/usr/bin/env python3
from tokenize import group
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from app_setup import app
from hash_model import checkForUpdate
from device_model import Device


checkForUpdate()

device_types = ["iOS", "iPadOS", "MacOS / WatchOS"]


def convertToJSON(deviceList):
    return ([r.dictRep() for r in deviceList])

grouped_iPhones = convertToJSON(Device.query.filter(Device.name.contains('iPhone')).order_by(Device.id).all())
grouped_iPads = convertToJSON(Device.query.filter(Device.name.contains('iPad')).all())
grouped_Macs = convertToJSON(Device.query.filter(Device.name.contains('Mac')).all())
grouped_iPods = convertToJSON(Device.query.filter(Device.name.contains('iPod')).all())
grouped_Watches = convertToJSON(Device.query.filter(Device.name.contains('Watch')).all())


latest_firmwares = {
    "iOS": grouped_iPhones[-1]['firmware'],
    "iPadOS": grouped_iPads[-1]['firmware'],
    "MacOS": grouped_Macs[-1]['firmware'],
    "WatchOS":grouped_Watches[-1]['firmware'],
}


@ app.route("/")
@ app.route("/home")
def home():
    return render_template('home.html', data=[device_types, grouped_iPhones, grouped_iPads, grouped_Macs, grouped_iPods, grouped_Watches, latest_firmwares])

@ app.route("/presets")
def presets():
    return render_template('presets.html')


@ app.route("/about")
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=False)
