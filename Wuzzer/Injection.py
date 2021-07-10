import re
import time
from bs4.builder import FAST
import requests
import random
from bs4 import BeautifulSoup
import colorama
try:
    import urlparse
    from urllib import urlencode
except: # For Python 3
    import urllib
    from urllib.parse import urlparse, urlunparse, urljoin, urlencode, parse_qsl


class Injection:
    def __init__(self, session, payloadPath, urls, attack):
        self.session = session
        self.payloads = self.Get_payloads(payloadPath)
        self.urls = urls
        self.attack = attack

    def Fuzzer(self):
        for url in self.urls :
            html_doc = self.session.get(url).text
            soup = BeautifulSoup( html_doc , "html5lib")
            forms = soup.find_all('form')

            for i, form in enumerate(forms): 
                print(f"[-] Form ({i}) in {url}")

                formMethod = form.get('method')    # post / GET  
                formAction = form.get('action')    # login.php  
                print(f"\tmethod = {formMethod}")
                print(f"\taction = {formAction}")

                formInputs = form.find_all('input')
                formSelects = form.find_all('select')
                formInputs = formInputs + formSelects
                

                href = urljoin(url, formAction) 
                print('\t' + href)

                params={}
                for j, formInput in enumerate(formInputs):
                    inputType = formInput.get('type') 
                    inputName = formInput.get('name')
                    inputValue = formInput.get('value')

                    if inputType in ['submit', 'hidden']:
                        params[inputName] = inputValue
                    elif inputName != None:
                        params[inputName] = ''
                
                for inputName, inputValue in params.items():
                    if not inputValue:
                        for payload, NewParams in self.InjectedPayload(params, inputName):
                            if self.CheckFault(payload) :
                                print("YES!!!")


    def send_request(self, url, payload, method):
        if method.upper()  == "GET":
            #res = self.session.get( add_url_params(href, params) )
            res = self.session.get(url, params=payload, allow_redirects=False)
        elif method.upper()  == "POST":
            res = self.session.post(url, data=payload, allow_redirects=False)
        
        return res.text

    def MyReadFile(self, path, encoding=None):
        file = open( path, 'r', encoding=encoding)
        filecontent = file.readlines()
        file.close() 
        return filecontent

    def Get_payloads(self, filename):
        XSS_payloads = self.MyReadFile(filename, "ISO-8859-1")
        XSS_payloads_list = []
        for i in XSS_payloads:
            if i[:-1] != '\n':
                XSS_payloads_list.append(i[:-1])
                
        XSS_payloads = [x for x in XSS_payloads_list if x != '']
        return XSS_payloads
    
    # https://stackoverflow.com/questions/2506379/add-params-to-given-url-in-python
    def add_url_params(self, url, params={}):
        url_parts = list(urlparse(url))
        query = dict(parse_qsl(url_parts[4]))  # query = url_parts.query
        query.update(params)
        url_parts[4] = urlencode(query)
        return urlunparse(url_parts)

    def InjectedPayload(self, params, inputName):
        paramsCopy = params
        for payload in self.payloads:
            paramsCopy[inputName] = payload
            #new_URL = add_url_params(href, params)
            yield payload, paramsCopy

    def CheckFault(self, *arg):
        pass

