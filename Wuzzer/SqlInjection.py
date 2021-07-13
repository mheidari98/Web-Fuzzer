from Injection import *
import re

class SqlInjection(Injection):
    def __init__(self, session, payloadPath, urls):
        super().__init__(session, urls, "SQL Injection")
        if payloadPath:
            self.payloads = self.Get_payloads(payloadPath)
        else : 
            self.payloads  = self.Get_payloads('payload/sqli_min.txt')

    def CheckFault(self, payload, response_html_doc):
        err_list = ['You have an error in your SQL syntax']
        for err in err_list:
            if err in response_html_doc: return True
        return False

    def PayloadInjection(self, params, selected_input, url, href, formMethod):
        params_dict = {}
        for i in range(len(params)):
            params_dict[params.loc[i, 'name']] = params.loc[i, 'value']

        for payload in self.payloads:
            params_dict[params.loc[selected_input, 'name']] = payload
            
            response_html_doc = self.send_request(href, params_dict, formMethod)

            fault = self.CheckFault(payload, response_html_doc)
            if fault: 
                self.PrintErr("SQL Injection", href, params.loc[selected_input, 'name'], payload)
                return True
        return False
