from Injection import *

class BlindCmdInjection(Injection):
    def __init__(self, session, payloadPath, urls, threshold):
        super().__init__(session, urls, "Blind Cmd Injection")
        self.payloads = self.Get_payloads(payloadPath)
        self.threshold = threshold

    def CheckFault(self, start, end, random_time):

        t_time = end - start  
        return t_time > random_time and t_time < random_time + self.threshold

    def PayloadInjection(self, params, inputName, href, formMethod):

	random_time = random.uniform(10, 20)
        delimiters = [';', '&&', '|']
        for delm in delimiters:
            payload = delm + 'sleep ' + str(random_time)
            paramsCopy[inputName] = payload
            start = time.time() 
            response_html_doc = self.send_request(href, paramsCopy, formMethod)
            end = time.time()
            fault = self.CheckFault(start, end, random_time)
            if fault: 
                PrintErr(self, "Blind Cmd Injection", payload, href)
                return True
        return False