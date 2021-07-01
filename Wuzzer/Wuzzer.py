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

def login(session, loginURL, payload):
    r = session.get( loginURL )
    signin = BeautifulSoup( r.content , "html5lib")
    
    try:
        payload['user_token'] = signin.find('input', attrs={"name" : "user_token"} )['value']
    except:
        pass

    p = session.post( loginURL, data=payload )

def SessionCreator(loginURL, payload={}):
    s = requests.Session()
    # s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
    login( s, loginURL, payload )
    return s

def main():
    """import argparse
    parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
    parser.add_argument("url", help="The URL to extract links from.")
    parser.add_argument("-m", "--max-urls", help="Number of max URLs to crawl, default is 30.", default=30, type=int)
    
    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls """

    protectedURL = "http://127.0.0.1/index.php" 
    loginURL  = "http://127.0.0.1/login.php"
    logoutURL = "http://127.0.0.1/logout.php"

    # Fill in your details here to be posted to the login form.
    payload = { 
        'username': 'admin',
        'password': 'password',
        'Login': 'Login'
    }

    Session = SessionCreator(loginURL, payload)

    internal_urls = Crawler(Session, protectedURL, loginURL, logoutURL).crawl(max_urls=30, DynamicSite=0, verbose=False)

    
if __name__ == '__main__':
    main()
