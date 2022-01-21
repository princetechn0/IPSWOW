#!/usr/bin/env python3
import os
import shutil
import requests
import json

from flask import Flask, render_template, url_for


app = Flask(__name__)


# Prints the devices in the server
all_devices_api = requests.get("https://api.ipsw.me/v4/devices").json()
# print(json.dumps(j, sort_keys=True, indent=4))


device_types = ["iOS", "iPadOS", "M1 Macs / Apple Watch"]

all_devices = [[x['name'], x['identifier']]
               for x in all_devices_api if "iBridge" not in x['name'] and "Developer Transition Kit" not in x["name"]]


# Name, ID, URL, FW Version
all_iPhones = [[x, requests.get(
    "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['url'], requests.get(
    "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['version']]
    for x in all_devices if "iPhone" in x[0]]

all_iPads = [[x, requests.get(
    "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['url'], requests.get(
    "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['version']]
    for x in all_devices if "iPad" in x[0]]


all_macs = [[x, requests.get(
    "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['url'], requests.get(
    "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['version']] for x in all_devices if "Mac" in x[0]]

all_ipods = [[x, requests.get(
    "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['url'], requests.get(
    "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['version']] for x in all_devices if "iPod" in x[0]]

all_watches = [[x, requests.get("https://api.ipsw.me/v4/device/{}?type=ota".format(x[1])).json()['firmwares'][0]['url'], requests.get(
    "https://api.ipsw.me/v4/device/{}?type=ota".format(x[1])).json()['firmwares'][0]['version']] for x in all_devices if "Watch" in x[0]]


@ app.route("/")
@ app.route("/home")
def home():
    return render_template('home.html', data=[device_types, all_iPhones, all_iPads, all_macs, all_ipods, all_watches])


@ app.route("/presets")
def presets():
    return render_template('presets.html')


@ app.route("/about")
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
