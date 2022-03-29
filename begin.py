#!/usr/bin/env python3
import os
import shutil
import requests
import json
import itertools
from flask import Flask, render_template, url_for
app = Flask(__name__)


# Prints the devices in the server
all_devices_api = requests.get("https://api.ipsw.me/v4/devices").json()
# print(json.dumps(j, sort_keys=True, indent=4))


device_types = ["iOS", "iPadOS", "MacOS / WatchOS"]
all_devices = [[x['name'], x['identifier']]
               for x in all_devices_api if "iBridge" not in x['name'] and "Developer Transition Kit" not in x["name"]]


def filterFunction(device_list):
    key_func = lambda x: x[1]
    group = itertools.groupby(sorted(device_list, key=key_func), key=key_func)
    to_clean = [[key, [[x[0][0], x[2]] for x in list(group)]] for key,group in group]
    cleaned  =  [[x[0], '/'.join(sorted(set(y[0] for y in x[1]))), x[1][0][1]] for x in to_clean]
    return cleaned

# Name, ID, URL, FW Version
all_iPhones = [[x, requests.get(
    "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['url'], requests.get(
    "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['version']]
    for x in all_devices if "iPhone" in x[0]]
grouped_iPhones = filterFunction(all_iPhones)
    

all_iPads = [[x, requests.get(
    "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['url'], requests.get(
    "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['version']]
    for x in all_devices if "iPad" in x[0]]
grouped_iPads = filterFunction(all_iPads)

all_macs = [[x, requests.get(
    "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['url'], requests.get(
    "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['version']] for x in all_devices if "Mac" in x[0]]

all_ipods = [[x, requests.get(
    "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['url'], requests.get(
    "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['version']] for x in all_devices if "iPod" in x[0]]

all_watches = [[x, requests.get("https://api.ipsw.me/v4/device/{}?type=ota".format(x[1])).json()['firmwares'][0]['url'], requests.get(
    "https://api.ipsw.me/v4/device/{}?type=ota".format(x[1])).json()['firmwares'][0]['version']] for x in all_devices if "Watch" in x[0]]

latest_firmwares = {
    "iOS": all_iPhones[-1][2],
    "iPadOS": all_iPads[-1][2],
    "MacOS": all_macs[-1][2],
    "WatchOS": all_watches[-1][2],
}


@ app.route("/")
@ app.route("/home")
def home():
    return render_template('home.html', data=[device_types, grouped_iPhones, grouped_iPads, all_macs, all_ipods, all_watches, latest_firmwares])


@ app.route("/presets")
def presets():
    return render_template('presets.html')


@ app.route("/about")
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
