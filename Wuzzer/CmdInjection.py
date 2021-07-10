from Injection import *
import re

class CmdInjection(Injection):
    def __init__(self, session, payloadPath, urls):
        super().__init__(session, urls, "Cmd Injection")
        self.payloads = self.Get_payloads(payloadPath)

    def CheckFault(self, payload, response_html_doc):
        injected_file = re.search(' (.*\.txt)', payload)
        return injected_file.group(1) in response_html_doc 

    def PayloadInjection(self, params, inputName, href, formMethod):

	for payload in self.payloads:
            paramsCopy = params
            paramsCopy[inputName] = payload
            #new_URL = add_url_params(href, params)
            response_html_doc = self.send_request(href, paramsCopy, formMethod)

            delimiters = [';', '&&', '|']
            for delm in delimiters:
                paramsCopy[inputName] = delm + 'ls'
                response_html_doc = self.send_request(href, paramsCopy, formMethod)
                fault = self.CheckFault(payload, response_html_doc)
                if fault: 
                    PrintErr(self, "Cmd Injection", payload, href)
                    return True
        return False
