class Tariff:
    def __init__(self, incoming, outgoing, sms):
        self.coeffs = {
            'incoming': incoming,
            'outgoing': outgoing,
            'sms': sms
        }
    
    def load_subscriber(self, sub):
        self.subscriber = sub

    def _filter_incoming(self, recordset):
        return recordset[recordset["msisdn_dest"] == self.subscriber][["timestamp","call_duration"]]

    def _filter_outgoing(self,recordset):
        return recordset[recordset["msisdn_origin"] == self.subscriber][["timestamp","call_duration"]]
        
    def _filter_sms(self, recordset):
        return recordset[recordset["msisdn_origin"] == self.subscriber][["timestamp","sms_number"]]

    def _calculate_incoming(self, recordset):
        return self.coeffs["incoming"].calculate(recordset)
    
    def _calculate_outgoing(self, recordset):
        return self.coeffs["outgoing"].calculate(recordset)

    def _calculate_sms(self, recordset):
        return self.coeffs["sms"].calculate(recordset)

    def calculate(self, recordset):        
        result = 0
        result += self._calculate_incoming(self._filter_incoming(recordset))
        result += self._calculate_outgoing(self._filter_outgoing(recordset))
        result += self._calculate_sms(self._filter_sms(recordset))
        return result
