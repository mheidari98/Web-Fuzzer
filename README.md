# Web-Fuzzer

## General info
> simple Web Fuzzer
  1. **crawling** : colect all internal url ( [Crawler.py](https://github.com/mheidari98/Web-Fuzzer/blob/main/Wuzzer/Crawler.py) )
  2. use **selenium** and **BeautifulSoup** to detect form & input params for fuzzing
  3. inject payload
  4. Check responses to detect vulnerabilities
---

## Requirements
- python3
- use virtual environments & install requirements packages ([gist](https://gist.github.com/mheidari98/8ae29b88bd98f8f59828b0ec112811e7)) 
- Chrome web driver : Download it from the address below and put it in the **Wuzzer** folder
  ```
  Chrome:    https://sites.google.com/a/chromium.org/chromedriver/downloads
  ```

 ---

## Usage
  for test on DVWA :
  ```bash
  cd Wuzzer
  python Wuzzer.py --test --XSSi --SQLi --BSQLi --CMDi --BCMDi 
  ```
  for more options :
  ```bash
  python Wuzzer.py -h
  ```

---

## Test on [DVWA Docker](https://hub.docker.com/r/vulnerables/web-dvwa/)  
  + Run image
    ```bash
    docker run --rm -it -p 80:80 vulnerables/web-dvwa
    ```
  + Database Setup
    > http://127.0.0.1/setup.php
  + Login with default credentials
    - Username: **admin**
    - Password: **password**

---

## Task-Lists
- [x] Xss Injecyion attack
- [x] SQL Injecyion attack
- [x] Blind SQL Injecyion attack
- [x] Cmd Injecyion attack
- [x] Blind Cmd Injecyion attack
- [ ] complete Document
- [ ] threading support
- [ ] use proxy

---

## Related Link 
### Vulnerable Web Applications
* OWASP Vulnerable Web Applications Directory ([github](https://github.com/OWASP/OWASP-VWAD)) ([owasp](https://owasp.org/www-project-vulnerable-web-applications-directory/))
* Web vulnerability collection ([github](https://github.com/lotusirous/vulnwebcollection)) 

### Payloads
* Cheatsheet_XSS_Vectors.txt ([Cheatsheet-God github](https://github.com/OlivierLaflamme/Cheatsheet-God/blob/master/Cheatsheet_XSS_Vectors.txt))
* xss_alert.txt ([PayloadsAllTheThings github](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/Intruders/xss_alert.txt))
* SQL.txt ([wfuzz github](https://github.com/xmendez/wfuzz/blob/master/wordlist/Injections/SQL.txt))
* BlindSqli.txt ([sql-injection-payload-list github](https://github.com/payloadbox/sql-injection-payload-list/blob/master/Intruder/detect/Generic_TimeBased.txt))

### XSS
* Cross-site scripting (XSS) cheat sheet ([portswigger](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet))
* XSS Injection ([PayloadsAllTheThings github](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XSS%20Injection))
* Cross-Site Scripting (XSS) ([Resources-for-Beginner-Bug-Bounty-Hunters github](https://github.com/nahamsec/Resources-for-Beginner-Bug-Bounty-Hunters/blob/master/assets/vulns.md#cross-site-scripting-xss))

### Related work
* Most advanced XSS scanner ([XSStrike](https://github.com/s0md3v/XSStrike)) 
* Automatic SQL injection and database takeover tool ([sqlmap](https://github.com/sqlmapproject/sqlmap)) 
* Web fuzzers review ([pentestbook](https://pentestbook.six2dez.com/others/web-fuzzers-comparision))

### security game
* XSS Game By Google ([xss-game](https://xss-game.appspot.com))
* [xssgame](https://www.xssgame.com/)
* alert(1) to win ([alf.nu](https://alf.nu/alert1))
* prompt(1) to win ([prompt.ml](http://prompt.ml/0))
* prompt("sibears") to win ([xss school](http://xss.school.sibears.ru/easy/0))
