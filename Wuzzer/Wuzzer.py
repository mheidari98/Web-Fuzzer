#################################################################   
#								
# 								
# 	Creator Name:   Mahdi Heidari, Sara Baradaran		
# 	Create Date:    July 2021 				
# 	Module Name:    Wuzzer.py				
# 	Project Name:   Web Fuzzer	
#								
#								
#################################################################

#!/usr/bin/env python

from Crawler import *
from XssInjection import *

def Login(session, login_url, payload, isDVWA = False):
    r = session.get(login_url)

    if isDVWA :
        session.cookies.set('security', 'low', domain=urlparse(login_url).netloc, path='')
    
    signin = BeautifulSoup( r.content , "html5lib")
    loginforms = signin.find('form')
    try:
        hiddenInput = loginforms.find_all('input', attrs={"type" : "hidden"} )
        for hr in hiddenInput:
            payload[ hr['name'] ] = hr['value']
    except:
        pass

    p = session.post(login_url, data=payload)
    return p.url

def Session_Creator(login_url, payload={}):
    s = requests.session()
    # s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
    protected_url = Login(s, login_url, payload)
    return (s, protected_url)


def main():
    """import argparse
    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("url", help="The URL to extract links from.")
    parser.add_argument("-m", "--max-urls", help="Number of max URLs to crawl, default is 30.", default=30, type=int)
    
    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls """

    loginURL  = "http://127.0.0.1/login.php"
    logoutURL = "http://127.0.0.1/logout.php"

    # Fill in your details here to be posted to the login form.
    payload = { 
        'username': 'admin',
        'password': 'password',
        'Login': 'Login'
    }

    Session, protectedURL = Session_Creator(loginURL, payload)

    internal_urls = Crawler(Session, protectedURL, loginURL, logoutURL).crawl(max_urls=30, DynamicSite=0, verbose=False)

    XssInjection(Session, "./payload/xss-payload-list.txt", internal_urls)
    
if __name__ == '__main__':
    main()
