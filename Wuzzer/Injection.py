import re
import time
from bs4.builder import FAST
import requests
import random
from bs4 import BeautifulSoup
import colorama
import pandas as pd
from json import dumps
try:
    from urllib import urlencode, unquote
    from urlparse import urlparse, parse_qsl, ParseResult
except ImportError:
    # Python 3 fallback
    from urllib.parse import urlunparse, urljoin, urlencode, unquote, urlparse, parse_qsl, ParseResult
    
# https://pypi.org/project/colorama/
colorama.init()     # init the colorama module
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
RED = colorama.Fore.RED
BLACK = colorama.Fore.BLACK
BLUE = colorama.Fore.BLUE
MAGENTA = colorama.Fore.MAGENTA
CYAN = colorama.Fore.CYAN
WHITE = colorama.Fore.WHITE


class Injection:

    def __init__(self, session, urls, attack):
        self.session = session
        self.urls = list(urls)
        self.attack = attack

    def PrintErr(self, err_msg, url, selected_input, payload):
        print( f"{RED}[+] Error :  {err_msg} at {url}{RESET}")
        print( f"{GRAY} \t InputName={GREEN}{selected_input}{GRAY} with value={GREEN}{payload} {RESET}")
        print()

    def addInputs(self, df, formInputs, tag):
        SubmitExistence = False
        for j, formInput in enumerate(formInputs):
            tmptype  = formInput.get('type') 
            tmpname  = formInput.get('name')
            tmpvalue = formInput.get('value')

            if tmptype == 'submit':
                if SubmitExistence == False:
                    # https://stackoverflow.com/questions/10715965/
                    df.loc[0 if pd.isnull(df.index.max()) else df.index.max() + 1] = [tmptype, tmpname, tmpvalue, tag]  
                    SubmitExistence = True
                else: 
                    continue
            elif tmptype == 'hidden':
                df.loc[0 if pd.isnull(df.index.max()) else df.index.max() + 1] = [tmptype, tmpname, tmpvalue, tag]

            elif tmpname != None:
                df.loc[0 if pd.isnull(df.index.max()) else df.index.max() + 1] = [tmptype, tmpname, '', tag]


    def fuzz(self, url, form):
        formMethod = form.get('method')    # post / GET  
        formAction = form.get('action')    # login.php  
        print(f"{CYAN}\tmethod = {formMethod}\taction = {formAction}{RESET}")

        href = urljoin(url, formAction) 

        params = pd.DataFrame(columns = ['type', 'name', 'value', 'tag'])
        
        formInputs = [i for i in form.find_all('input') if i.get('type')!='checkbox']
        self.addInputs(params, formInputs, 'input')

        formInputs = form.find_all('select')
        self.addInputs(params, formInputs, 'select')

        formInputs = form.find_all('textarea')
        self.addInputs(params, formInputs, 'textarea')

        formInputs = [i for i in form.find_all('button') if i.get('type').lower()=='submit']
        self.addInputs(params, formInputs, 'button')
        
        #print(params)
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
                print(f"{BLUE}[-] Form ({i}) in {url}{RESET}")
                self.fuzz(url, form)
                

    def send_request(self, url, payload, method):
        #self.session.cookies.set('security', 'medium', path='')
        #print(self.session.cookies.get_dict())
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

        s = ""
        for i, item in enumerate(query.items()):
            key, value = item
            if i :
                s += '&'
            s += f"{key}={value}"

        url_parts[4] = s # urlencode(query)
        return urlunparse(url_parts)

    def add_url_params_encoded(self, url, params={}):
        url_parts = list(urlparse(url))
        query = dict(parse_qsl(url_parts[4]))  # query = url_parts.query
        query.update(params)
        url_parts[4] = urlencode(query)
        return urlunparse(url_parts)

    def PayloadInjection(self, *arg):
        pass

    def CheckFault(self, *arg):
        pass

