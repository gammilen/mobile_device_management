import pandas as pd
import os

file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.csv")

class DataManager:
    @classmethod
    def get_data(cls, f_name=file_name):
        data = pd.read_csv(f_name)
        data['msisdn_origin'] = data['msisdn_origin'].astype(str)
        data['msisdn_dest'] = data['msisdn_dest'].astype(str)
        return data

