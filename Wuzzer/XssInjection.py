from Injection import *

class XssInjection(Injection):
    def __init__(self, session, payloadPath, urls):
        super().__init__(session, payloadPath, urls, "XSS")

    def CheckFault(self, href, NewParams, formMethod, payload):
        html_doc = self.send_request(href, NewParams, formMethod)
        return payload in html_doc 