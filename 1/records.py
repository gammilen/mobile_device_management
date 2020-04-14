import pandas as pd

def prepare_data:
    data = pd.read_csv('crd.csv', delimiter=',')
    data['timestamp'] = pd.Datetime(data['timestamp'])

prepare_data()

class RecordSet:
    def __init__(self, *args, **kwargs):
        self.data = data
        
    def by_time(self, t_from, t_to):
        self.data[
            (self.data['timestamp'] > t_from ) &
            (self.data['timestamp'] < t_to)
        ]
        return self

    def by_count(self, start, finish):
        self.data.iloc[:, start:finish]
        return self
    
    def by_origin(self, origin):
        self.data[self.data.msisdn_origin == origin]
        return self

    def get_results(self):
        return self.data
    


