import re
import time
from bs4.builder import FAST
import requests
import random
from bs4 import BeautifulSoup
import colorama
import pandas 
try:
    import urlparse
    from urllib import urlencode
except: # For Python 3
    import urllib
    from urllib.parse import urlparse, urlunparse, urljoin, urlencode, parse_qsl

# init the colorama module
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
RED = colorama.Fore.RED

class Injection:

    def __init__(self, session, urls, attack):
        self.session = session
        self.urls = list(urls)
        self.attack = attack

    def PrintErr(self, err_msg, payload, url):
        print( f"{RED} \tError :  {err_msg} {RESET}")
        print( f"{GRAY} \tVulnerable Input :  {payload} {RESET}")
        print( f"{YELLOW} \t{url} {RESET}")

    def fuzz(self, url, form):
        formMethod = form.get('method')    # post / GET  
        formAction = form.get('action')    # login.php  
        print(f"\tmethod = {formMethod}")
        print(f"\taction = {formAction}")

        formInputs = form.find_all('input')
        formSelects = form.find_all('select')
        formTextarea = form.find_all('textarea')
        formInputs = formInputs + formSelects + formTextarea

        href = urljoin(url, formAction) 
        print(f"\thref = {href}")

        params = pandas.DataFrame(columns = ['type', 'name', 'value'])
                        
        SubmitExistence = False
        Cnt = 0
        for j, formInput in enumerate(formInputs):
            
            tmptype  = formInput.get('type') 
            tmpname  = formInput.get('name')
            tmpvalue = formInput.get('value')

            if tmptype == 'submit':
                if SubmitExistence == False:
                    params.loc[Cnt] = [tmptype, tmpname, tmpvalue]
                    SubmitExistence = True
                    Cnt += 1

                else: continue

            elif tmptype == 'hidden':
                params.loc[Cnt] = [tmptype, tmpname, tmpvalue]
                Cnt += 1

            elif tmpname != None:
                params.loc[Cnt] = [tmptype, tmpname, '']
                Cnt += 1

        for i in range(len(params)):
            if not params.loc[i, 'value']:
                fault = self.PayloadInjection(params, i, url, href, formMethod)
                if fault: return

    def Fuzzer(self):
        for url in self.urls :
            html_doc = self.session.get(url).text
            soup = BeautifulSoup( html_doc , "html5lib")
            forms = soup.find_all('form')

            for i, form in enumerate(forms): 
                print(f"[-] Form ({i}) in {url}")
                self.fuzz(url, form)
                

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

    def PayloadInjection(self, *arg):
        pass

    def CheckFault(self, *arg):
        pass

