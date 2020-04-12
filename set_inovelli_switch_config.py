#!/usr/bin/env python3

import configparser
import requests
import time

# load the config file
config = configparser.ConfigParser()
config.read('config.ini')

# load required home assistant configuration
HA_URL = config['homeassistant']['BASE_URL']
BEARER_TOKEN = config['homeassistant']['BEARER_TOKEN']


def set_config_param(node_id, parameter, value):
    '''Sets a Z-Wave configuration (parameter) to (value) for node (node_id)'''

    print(f"   Setting config parameter {parameter} to {value}: ", end='')
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "content-type": "application/json",
    }
    data = {"node_id": node_id, "parameter": parameter, "value": value}
    r = requests.post(
        f"{HA_URL}/api/services/zwave/set_config_parameter", json=data, headers=headers)
    if (r.ok):
        print("SUCCESS")
    else:
        print("FAILED")
    time.sleep(2)


def set_config_params(node_id, parameters):
    '''Sets a list of Z-Wave config parameters [{id,value}] for node (node_id)'''

    print(f"Node {node_id}: Setting {len(parameters)} parameters")

    for parameter in parameters:
        set_config_param(node_id, parameter['id'], parameter['value'])

all_inovelli_dimmers = [35, 19, 20, 18, 44, 45, 41, 24, 23, 37, 39,
                        38, 36, 16, 42, 22, 49, 17, 52, 7, 25, 40, 43, 47, 48]

three_way_inovelli = [44, 45]

def update_inovelli_dimmers():
    for node_id in all_inovelli_dimmers:
        parameters = []

        # set 1 (Dimming Speed - Z-Wave) to 3 (3 seconds)
        parameters.append({"id": 1, "value": 3})
        # set 2 (Dimming Speed - Switch) to 3 (3 seconds)
        parameters.append({"id": 2, "value": 3})

        # set 3 (Ramp Rate - Z-Wave) to 3 (3 seconds)
        parameters.append({"id": 3, "value": 3})
        # set 4 (Ramp Rate - Switch) to 0 (Instant On)
        parameters.append({"id": 4, "value": 0})

        # set 9 (Power On Level) to 99 (Full Brightness)
        parameters.append({"id": 9, "value": 99})
        # set 9 (Power On Level - Z-Wave) to 99 (Full Brightness)
        parameters.append({"id": 10, "value": 99})

        set_config_params(node_id, parameters)

def update_three_way_inovelli():
    for node_id in three_way_inovelli:
        parameters = []

        # set neutral wire, for some reason have to set no neutral first
        parameters.append({"id": 21, "value": 0})
        parameters.append({"id": 21, "value": 1})

        # set three way, for some reason have to set no three way first 
        parameters.append({"id": 22, "value": 0})
        parameters.append({"id": 22, "value": 2})

        set_config_params(node_id, parameters)

# update_inovelli_dimmers()
update_three_way_inovelli()
