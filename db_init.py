from device_model import clear_data, initializeDB
import requests
import itertools
import operator

def initDB():
    # Clearing Device table
    clear_data()

    # Gets the new set of devices from API
    all_devices_api = requests.get("https://api.ipsw.me/v4/devices").json()

    # Re-initializing DB 
    all_devices = [[x['name'], x['identifier'], all_devices_api.index(x)]
                for x in all_devices_api if "iBridge" not in x["name"] 
                and "Developer Transition Kit" not in x["name"] 
                and "Apple Virtual Machine 1" not in x["name"]]
    
    # Name, ID, URL, FW Version
    all_iPhones = [[x, requests.get(
        "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['url'], requests.get(
        "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['version'], x[2]]
        for x in all_devices if "iPhone" in x[0]]
    filterFunction(all_iPhones)


    all_iPads = [[x, requests.get(
        "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['url'], requests.get(
        "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['version'], x[2]]
        for x in all_devices if "iPad" in x[0]]
    filterFunction(all_iPads)

    all_macs = [[x, requests.get(
        "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['url'], requests.get(
        "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['version'], x[2]] 
        for x in all_devices if "Mac" in x[0]]
    filterFunction(all_macs)

    all_ipods = [[x, requests.get(
        "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['url'], requests.get(
        "https://api.ipsw.me/v4/device/{}?type=ipsw".format(x[1])).json()['firmwares'][0]['version'], x[2]] 
        for x in all_devices if "iPod" in x[0]]
    filterFunction(all_ipods)

    all_watches = [[x, requests.get("https://api.ipsw.me/v4/device/{}?type=ota".format(x[1])).json()['firmwares'][0]['url'], requests.get(
        "https://api.ipsw.me/v4/device/{}?type=ota".format(x[1])).json()['firmwares'][0]['version'], x[2]] 
        for x in all_devices if "Watch" in x[0]]
    filterFunction(all_watches)

def filterFunction(device_list):
    wordsToClean = ["(GSM)", "(Global)", "(WiFi)", "(Cellular)"]
    key_func = lambda x: x[1]
    group = itertools.groupby(sorted(device_list, key=key_func), key=key_func)
    to_clean = [[key, [[x[0][0], x[2], x[3]] for x in list(group)]] for key,group in group]
    cleaned  =  sorted([[x[0], '/'.join(sorted(set(' '.join(x for x in y[0].split(' ') if x not in wordsToClean)
    for y in x[1]))), x[1][0][1], x[1][0][2]] for x in to_clean], key=operator.itemgetter(3))

    initializeDB(cleaned)
    return cleaned
