from abc import ABC

class Rule(ABC):
    def __init__(self, k, *args, **kwargs):
        self.k = k

class BasicRule(Rule):
    #Просто стабильный множитель 
    pass

class PeriodRule(Rule):
    #Ограничения по времени 
    #Если не указано то 'до' с наименьшего времени, если 'после', то до наибольшего времени
    pass

class CountRule(Rule):
    #Множитель зависит от количества
    #Если не указано 'от', то с 0 , если не 'до', то бесконечности
    pass
