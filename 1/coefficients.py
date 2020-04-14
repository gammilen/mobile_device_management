from abc import ABC, abstractmethod

class Restriction:
    def __init__(self, *args, **kwargs):
        self.count = {
            "free finite": True,
            "free amount": 1,
        }
        self.period = {
            "free finite": False,
            "free amount": None, 
        }
        self.validation = {
            "free-count": self.free_count,
            "free-period": self.free_period,
            "non-free-count": self.non_free_count,
            "non-free-period": self.non_free_period,
        }

    #вызывается при добавлении non-free-count правила
    @staticmethod
    def non_free_count(period_num, free_period_num):
        if period_num != free_period_num:
            raise ValueError("Нарушен порядок сочетания правил")
    
    #вызывается при добавлении non-free-period правила
    @staticmethod
    def non_free_period(count_num, free_count_num):
        if count_num != free_count_num:
            raise ValueError("Нарушен порядок сочетания правил")
    
    def free_count(self, free_count_num):
        if self.count['free finite']:
            if free_count_num != self.count['free amount']:
                raise ValueError(
                    "Нарушен порядок использования"
                    "правил типа 'количество' с отсутствием платы")
    
    def free_period(self, free_period_num):
        if self.period['free finite']:
            if free_period_num != self.count['free amount']:
                raise ValueError(
                    "Нарушен порядок использования"
                    "правил типа 'количество' с отсутствием платы")
    
    #TODO Проверка на пересечение 
    # периоды в формате (начало, конец)
    def period(self, periods):
        pass


class Coefficient(ABC):
    def __init__(self, *args, **kwargs):
        self.restriction = Restriction()
        self.free_period_num = 0
        self.free_count_num = 0
        self.period = dict()
        self.count = dict()

    def set_base_rule(self, rule):
        self.base = rule


class CallingCoefficient(Coefficient):
    def __init__(self, *args, **kwargs):
        super(CallingCoefficient, self).__init__(*args, **kwargs)
        self.free_period_num = 0
        self.free_count_num = 0
        self.period = dict()
        self.count = dict()

    def add_period_rule(self, rule):
        if rule.k == 0:
            self.restriction.validation['free-period'](self.free_period_num+1)
            self.free_period_num += 1
            self.update_rules(rule, "period", True)
        else:
            self.restriction.validation['non-free-period'](
                len(self.count), self.free_count_num)
            self.update_rules(rule, "period", False)

    def add_count_rule(self, rule):
        if rule.k == 0:
            self.restriction.validation['free-count'](self.free_count_num+1)
            self.free_count_num += 1
            self.update_rules(rule, "count", True)
        else:
            self.restriction.validation['non-free-count'](
                len(self.period), self.free_period_num)
            self.update_rules(rule, "count", False)

    def has_free(self):
        return self.free_count_num > 0 or self.free_period_num > 0

    def update_rules(self, _rule, r_type, free):
        if r_type == "period":
            if free is True:
                self.period["free"].append(_rule)
            else:
                self.period["non-free"].append(_rule)
        elif r_type == "count":
            if free is True:
                self.count["free"].append(_rule)
            else:
                self.count["non-free"].append(_rule)    
    
    #TODO Учет прочих правил при расчете
    def calculate(self, recordset):
        # return self.base * (sum of out calling)
        return self.base.k * recordset["call_duration"].sum()
        
        
class IncomingCoefficient(CallingCoefficient):
    pass


class OutgoingCoefficient(CallingCoefficient):
    pass


class SMSCoefficient(Coefficient):
    def __init__(self, *args, **kwargs):
        super(SMSCoefficient, self).__init__(*args, **kwargs)
        self.free_count_num = 0
        self.count = dict()

    def add_count_rule(self, rule):
        if rule.k == 0:
            self.restriction.validation['free-count'](self.free_count_num+1)
            self.free_count_num += 1
            self.update_rules(rule, "count", True)
        else:
            self.restriction.validation['non-free-count'](
                len(self.period), self.free_period_num)
            self.update_rules(rule, "count", False)

    def has_free(self):
        return self.free_count_num > 0

    def update_rules(self, _rule, r_type, free):
        if r_type == "count":
            if free is True:
                self.count["free"].append(_rule)
            else:
                self.count["non-free"].append(_rule)
    
    #TODO Учет прочих правил при расчете
    def calculate(self, recordset):
        # return self.base * (sum of sms)
        return self.base.k * recordset["sms_number"].sum()
