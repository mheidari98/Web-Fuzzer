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
* Cheatsheet_XSS_Vectors.txt ([github](https://github.com/OlivierLaflamme/Cheatsheet-God/blob/master/Cheatsheet_XSS_Vectors.txt))

