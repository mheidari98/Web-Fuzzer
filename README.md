# Web-Fuzzer

## General info
> Web-Fuzzer

## Requirements
- python3
- use virtual environments & install requirements packages ([Link](https://gist.github.com/mheidari98/8ae29b88bd98f8f59828b0ec112811e7)) 
 
## Usage
  ```bash
  ./Wuzzer URL
  ```

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
  + XSS (Reflected)
    > http://127.0.0.1/vulnerabilities/xss_r/?name=payload#


## Related Link 
### Vulnerable Web Applications
* OWASP Vulnerable Web Applications Directory ([github](https://github.com/OWASP/OWASP-VWAD)) ([owasp](https://owasp.org/www-project-vulnerable-web-applications-directory/))
* Web vulnerability collection ([github](https://github.com/lotusirous/vulnwebcollection)) 

