class BaseBilling:
    def __init__(self, subscriber, *args, **kwargs):
        self.records = None
        self.tariff = None
        self.subscriber = subscriber
    
    def load_records(self, recordset):
        self.records = recordset
    
    def load_tariff(self, tariff):
        tariff.load_subscriber(self.subscriber)
        self.tariff = tariff

    def count(self):
        if not self.tariff:
            raise AttributeError("Отсутствует тариф для расчета")
        return self.tariff.calculate(self.records)

