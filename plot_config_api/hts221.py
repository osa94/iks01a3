import json


class HTS221Config:

    def __init__(self, json_path):
        self.__json_path = json_path
        self.__json_data = {}

        self.get_json_data()

    def get_json_data(self):
        with open(self.__json_path, 'r') as f:
            self.__json_data = json.load(f)

    def get_humidity_dict(self):
        return self.__json_data["humidity"]

    def get_humidity_xlim_dict(self):
        return self.get_humidity_dict()["xlim"]

    def get_humidity_ylim_dict(self):
        return self.get_humidity_dict()["ylim"]

    def get_humidity_title_dict(self):
        return self.get_humidity_dict()["title"]

    def get_humidity_xlabel_dict(self):
        return self.get_humidity_dict()["xlabel"]

    def get_humidity_ylabel_dict(self):
        return self.get_humidity_dict()["ylabel"]

    def get_humidity_grid_dict(self):
        return self.get_humidity_dict()["grid"]

    def get_temperature_dict(self):
        return self.__json_data["temperature"]

    def get_temperature_xlim_dict(self):
        return self.get_temperature_dict()["xlim"]

    def get_temperature_ylim_dict(self):
        return self.get_temperature_dict()["ylim"]

    def get_temperature_title_dict(self):
        return self.get_temperature_dict()["title"]

    def get_temperature_xlabel_dict(self):
        return self.get_temperature_dict()["xlabel"]

    def get_temperature_ylabel_dict(self):
        return self.get_temperature_dict()["ylabel"]

    def get_temperature_grid_dict(self):
        return self.get_temperature_dict()["grid"]

'''
hts221 = HTS221Config("./plot_config_json/hts221_config.json")
print(hts221.get_humidity_dict())
print(hts221.get_humidity_xlim_dict())'''
