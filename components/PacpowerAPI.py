import json
import growattServer
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class PacpowerAPI:
    def __init__(self, username, password, storage_id, maxVolt):
        self.username = username
        self.password = password
        self.storage_id = storage_id
        self.maxVolt = maxVolt
        self.api = None
        self.user_id = None
        self.plant_id = None


    def initAPI(self):
        # Growatt Login
        api = growattServer.GrowattApi()
        login_response = api.login(self.username, self.password)

        # Firebaes Login
        cred = credentials.Certificate("fKey.json")
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://pacapi-ada92.firebaseio.com/'})

        #  Assign to instance variable
        self.api = api
        self.user_id = login_response['userId']
        plantInfo = self.api.plant_list(self.user_id)
        self.plant_id = plantInfo['data'][0]['plantId']


    # def get_remain_battery(self):
    #     raw_vbat = float(self.get_voltage())
    #     percent = int((raw_vbat / self.maxVolt) * 100)
    #     if percent > 100:
    #         percent = 100

    #     return percent

    def get_remain_battery(self):
        battery_cap = self.api.storage_detail(self.storage_id)['capacity']
        print('===== Storage Detail =====')
        print(self.api.storage_detail(self.storage_id))
        print('===== Storage Overview=====')
        print(self.api.storage_energy_overview(self.plant_id, self.storage_id))
        print('===== Storage params=====')
        print(self.api.storage_params(self.storage_id))
        print('===== Device List =====')
        print(self.api.inverter_list(self.plant_id))

        return battery_cap


    def get_voltage(self):
        voltage = self.api.storage_detail(self.storage_id)['vbat']
        # print(self.api.storage_detail(self.storage_id))

        return voltage

    def get_temp(self):
        voltage = self.api.storage_detail(self.storage_id)['vbat']

        return voltage





    def get_data_pack(self):
        package = {
            'energyLevel': self.get_remain_battery(),
            'voltage': self.get_voltage(),
            'patternNo': 5,
            'remainTime': '4 h 30 m',
            'temp': '36 °C',
            'kWatt': '250 kW-hr',
            'ampere': '20,000 A',
            'capacity': '35,000 mAh'
        }

        return package


    def send_to_cloud(self, node_name):
        ref = db.reference(node_name)
        ref.push(self.get_data_pack())
        print("=== Saved ===")
