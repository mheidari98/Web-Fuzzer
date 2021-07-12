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
from SqlInjection import *
from CmdInjection import *
from BlindCmdInjection import *

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

def Session_Creator(login_url, payload={}, isDVWA = False):
    s = requests.session()
    # s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
    protected_url = Login(s, login_url, payload, isDVWA)
    return (s, protected_url)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Simple Web Fuzzer")
    parser.add_argument("--login", help="login page url")
    parser.add_argument('--avoid', nargs='*', help='avoid urls')
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
    avoidURL  = args.avoid
    thread = args.thread
    max_urls = args.maxUrl 

    if args.test :
        loginURL  = "http://127.0.0.1/login.php"
        avoidURL = ["http://127.0.0.1/logout.php", "http://127.0.0.1/security.php",
                    "http://127.0.0.1/setup.php", "http://127.0.0.1/vulnerabilities/csrf/",
                    'http://127.0.0.1/reset.php', 'http://127.0.0.1/security_level_set.php','http://127.0.0.1/password_change.php','http://127.0.0.1/user_extra.php'
                    ]

    username = args.username if args.username else 'admin'
    password = args.password if args.password else 'password'

    # Fill in your details here to be posted to the login form.
    payload = { 
        'username': username,
        'password': password,
        'Login': 'Login'
    }
    payload = {
        'login':'bee',
        'password':'bug',
        'security_level':'0',
        'form':'submit'
    }

    Session, protectedURL = Session_Creator(loginURL, payload, args.test)

    #internal_urls = Crawler(Session, protectedURL, loginURL, avoidURL).crawl(max_urls, DynamicSite=0, verbose=False)
    internal_urls =['http://127.0.0.1/xss_get.php', 'http://127.0.0.1/xss_post.php']

    #print(internal_urls)
    if args.XSSi :
        XssInjection(Session, args.XSSpayload, internal_urls).Fuzzer()
    if args.SQLi :
        SqlInjection(Session, args.SQLpayload, internal_urls).Fuzzer()
    if args.CMDi :
        BlindCmdInjection(Session, args.CMDpayload, internal_urls, 0.5).Fuzzer()

if __name__ == '__main__':
    main()
