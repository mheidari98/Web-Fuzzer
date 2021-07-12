from Injection import *
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from seleniumrequests import Chrome	

class XssInjection(Injection):
    def __init__(self, session, payloadPath, urls):
        super().__init__(session, urls, "XSS Injection")
        self.payloads = self.Get_payloads(payloadPath)
        self.default_payloads = ['<script>alert(123);</script>', 
				 '<ScRipT>alert("XSS");</ScRipT>', 
				 '<script>alert(123)</script']
        self.driver = self.CreateDriver()

    def CheckFault(self):    
        # this is just to ensure that the page is loaded
        # time.sleep(0.5)
        try: 
            html_doc = self.driver.page_source        
        except UnexpectedAlertPresentException:
            self.driver.close()
            self.driver = self.CreateDriver()
            return True
        return False

    def CreateDriver(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        # options.set_capability("UnexpectedAlertPresentException", "accept")
        options.add_argument("--enable-javascript")

        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(3)

        driver.get(self.urls[0])
            
        cookie_dict = self.session.cookies.get_dict()
        for key, value in cookie_dict.items():
            driver.add_cookie({'name' : key, 'value' : value})
        return driver

    def PayloadInjection(self, params, selected_input, url, href, formMethod):
        for payload in self.payloads:
            params_dict = {}
            for i in range(len(params)):
                params_dict[params.loc[i, 'name']] = params.loc[i, 'value']
            
            self.driver.get(url) 

            if formMethod.upper() == 'GET':
                params_dict[params.loc[selected_input, 'name']] = payload
                new_url = self.add_url_params(href, params_dict)
                self.driver.get(new_url)
 
            elif formMethod.upper() == 'POST':
                inputname = params.loc[selected_input, 'name']
                inputbox = self.driver.find_element_by_name(inputname)
                
                if params.loc[selected_input, 'type'] in ['text']:
                    inputbox.send_keys(payload)
                    
                    try:  
                        submitBtns = params[params['type'] == 'submit']
                        submitBtn_name = submitBtns.iloc[0]['name']
                        
                        if submitBtn_name:
                            self.driver.find_element_by_name(submitBtn_name).click()
                    except UnexpectedAlertPresentException:
                        self.PrintErr("Xss Injection", payload, href)
                        self.driver.close()
                        self.driver = self.CreateDriver()

            fault = self.CheckFault()
            if fault: 
                self.PrintErr("Xss Injection", payload, href)
                return True

        return False
