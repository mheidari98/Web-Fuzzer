from Injection import *
import re

class CmdInjection(Injection):
    def __init__(self, session, payloadPath, urls):
        super().__init__(session, urls, "Cmd Injection")
        if payloadPath:
            self.payloads = self.Get_payloads(payloadPath)
        else : 
            self.payloads  = self.Get_payloads('payload/cmdi_min.txt')

    def CheckFault(self, payload, response_html_doc):
        injected_file = re.search(' (.*\.txt)', payload)
        return injected_file.group(1) in response_html_doc 

    def PayloadInjection(self, params, selected_input, url, href, formMethod):
        params_dict = {}
        for i in range(len(params)):
            params_dict[params.loc[i, 'name']] = params.loc[i, 'value']

        for payload in self.payloads:
            params_dict[params.loc[selected_input, 'name']] = payload
            response_html_doc = self.send_request(href, params_dict, formMethod)

            delimiters = [';', '&&', '|']
            for delm in delimiters:
                params_dict[params.loc[selected_input, 'name']] = delm + 'ls'
                response_html_doc = self.send_request(href, params_dict, formMethod)
                fault = self.CheckFault(payload, response_html_doc)
                if fault: 
                    self.PrintErr("Command Injection", href, params.loc[selected_input, 'name'], payload)
                    return True
        return False
