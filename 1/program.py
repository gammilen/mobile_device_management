from billing import BaseBilling
from tariffs import Tariff
from coefficients import IncomingCoefficient, OutgoingCoefficient, SMSCoefficient
from rules import BasicRule
from data_manager import DataManager

def calculate_tel():
    i = IncomingCoefficient()
    i.set_base_rule(BasicRule(1))
    o = OutgoingCoefficient()
    o.set_base_rule(BasicRule(3))
    s = SMSCoefficient()
    s.set_base_rule(BasicRule(1))
    t = Tariff(i, o, s)
    b = BaseBilling("968247916")
    b.load_tariff(t)
    b.load_records(DataManager.get_data())
    return b.count()

def main():
    print("Результат: ", calculate_tel())
    
if __name__ == "__main__":
    main()