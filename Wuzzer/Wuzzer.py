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
from CmdInjection import *
from BlindCmdInjection import *
from SqlInjection import *

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
    import argparse
    parser = argparse.ArgumentParser(description="Simple Web Fuzzer")
    parser.add_argument("-i", "--login", help="login page url")
    parser.add_argument("-o", "--logout", help="logout page url")
    parser.add_argument("-u", "--username", help="username")
    parser.add_argument("-p", "--password", help="password")
    parser.add_argument("-t", "--thread", help="Number of thread", default=1, type=int)
    parser.add_argument("-mu", "--maxUrl", help="Number of max URLs to crawl, default is 30.", default=30, type=int)
    parser.add_argument('-x', '--XSSi', help="Xss injecyion attack", action='store_true', default=False)
    parser.add_argument('-xp', '--XSSpayload', help="Xss injecyion payload path")
    parser.add_argument('-s', '--SQLi', help="SQL injecyion attack", action='store_true', default=False)
    parser.add_argument('-sp', '--SQLpayload', help="SQL injecyion payload path")
    parser.add_argument('-c', '--CMDi', help="Command injecyion attack", action='store_true', default=False)
    parser.add_argument('-cp', '--CMDpayload', help="Command injecyion payload path")
    parser.add_argument('--test', help="test on DVWA", action='store_true', default=False)
    args = parser.parse_args()

    loginURL  = args.login
    logoutURL  = args.logout
    thread = args.thread
    max_urls = args.maxUrl 

    if args.test :
        loginURL  = "http://127.0.0.1/login.php"
        logoutURL = "http://127.0.0.1/logout.php"

    username = args.username if args.username else 'admin'
    password = args.password if args.password else 'password'

    # Fill in your details here to be posted to the login form.
    payload = { 
        'username': username,
        'password': password,
        'Login': 'Login'
    }

    Session, protectedURL = Session_Creator(loginURL, payload)

    internal_urls = Crawler(Session, protectedURL, loginURL, logoutURL).crawl(max_urls, DynamicSite=0, verbose=False)

    #print(internal_urls)
    if args.XSSi :
        XssInjection(Session, args.XSSpayload, internal_urls).Fuzzer()
    if args.SQLi :
        XssInjection(Session, args.SQLpayload, internal_urls).Fuzzer()
    if args.CMDi :
        XssInjection(Session, args.CMDpayload, internal_urls).Fuzzer()
    
if __name__ == '__main__':
    main()
