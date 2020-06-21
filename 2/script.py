import pandas as pd
from plots import *
import os

class Charging:
    def __init__(self, ip):
        self._payment = 0
        self.init_df(ip)
        self.base_rule = None
        self.add_rule = None
    
    def init_df(self, abonent_ip):
        #load file
        df = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "file.csv"))
        #filter columns
        df = df[["ts", "te", "td", "sa", "ibyt"]]
        #filter source address
        df = df[df["sa"]==abonent_ip]
        self.df = df
        
    def init_rules(self, base, add):
        #base rule
        self.base_rule = dict(k=base)
        #add rule
        add = add[0]
        self.add_rule = dict(k=add[0], limit=add[1])
            
    def _get_amount(self):
        return self.df["ibyt"].sum()/1024/1024

    def calculate(self):
        a = self._get_amount()
        #apply addition rule
        if (self.add_rule):
            tmp = a - self.add_rule["limit"]
            if tmp <= 0:
                #change conditions (Mb to Kb(in Mb)
                a *= 1024
                tmp = a - self.add_rule["limit"]
                if tmp <= 0:
                    self._payment += a * self.add_rule["k"]
                    return
            a = tmp
            self._payment += self.add_rule["limit"] * self.add_rule["k"]
        #apply base rule
        self._payment += a * self.base_rule["k"]
    
    @property
    def payment(self):
        return round(self._payment, 2)




def prepare_charging():
    abonent_ip = "192.168.250.59"

    c = Charging(abonent_ip)
    c.init_rules(1, [(0, 1000)])
    return c
    
def get_payment(charging):
    charging.calculate()
    return charging.payment
    
def main():
    c = prepare_charging()
    print("Оплата услуги \"Интернет\":", get_payment(c), "руб.")

    print("График связи объема трафика и длительности обращения")
    make_duration_traffic_plot(c.df)
    print("График связи объема трафика и времени обращения")
    make_time_traffic_plot(c.df)

if __name__ == "__main__":
    main()