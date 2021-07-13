from Injection import *
import re

class BlindSqlInjection(Injection):
    def __init__(self, session, payloadPath, urls, random_time):
        super().__init__(session, urls, "Blind SQL Injection")
        if payloadPath:
            self.payloads = self.Get_payloads(payloadPath)
        else : 
            self.payloads  = self.Get_payloads('payload/sqli_timebased.txt')
        self.random_time = random_time

    def CheckFault(self, start, end):

        t_time = end - start  
        return t_time > self.random_time

    def PayloadInjection(self, params, selected_input, url, href, formMethod):
        params_dict = {}
        for i in range(len(params)):
            params_dict[params.loc[i, 'name']] = params.loc[i, 'value']

        for payload in self.payloads:
            params_dict[params.loc[selected_input, 'name']] = payload
            start = time.time() 
            response_html_doc = self.send_request(href, params_dict, formMethod)
            end = time.time()
            fault = self.CheckFault(start, end)
            if fault: 
                self.PrintErr("Blind SQL Injection", href, params.loc[selected_input, 'name'], payload)
                return True
        return False