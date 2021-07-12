#################################################################   
#								
# 								
# 	Creator Name:   Mahdi Heidari, Sara Baradaran		
# 	Create Date:    July 2021 				
# 	Module Name:    Crawler.py				
# 	Project Name:   Web Fuzzer	
#								
#								
#################################################################

import re
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import urllib
from urllib.parse import urlparse, urljoin
import colorama
import random
from stem.control import Controller
from stem import Signal
import sys
import os

# init the colorama module
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

class Crawler:

    def __init__(self, Session, url, loginURL, avoidURLS):
        self.Session = Session

        self.url = url
        self.loginURL = loginURL
        self.avoidURLS = avoidURLS

        # initialize the set of links (unique links)
        self.internal_urls = set()
        self.external_urls = set()
        self.total_urls_visited = 0
        
        self.internal_urls.add(loginURL)
        for avoid_url in self.avoidURLS:
            self.internal_urls.add(avoid_url)
        os.system('mkdir Crawled')

    def is_valid(self, url):
        """
        Checks whether `url` is a valid URL.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def get_all_website_links(self, url, DynamicSite=0, verbose=False):
        """
        Returns all URLs that is found on `url` in which it belongs to the same website
        """
        
        urls = set()     # all URLs of `url`
        
        domain_name = urlparse(url).netloc     # domain name of the URL without the protocol

        if DynamicSite:
            session = HTMLSession()   # initialize an HTTP session
            
            response = session.get(url)  # make HTTP request & retrieve response
            
            # execute Javascript
            try:
                response.html.render()
            except:
                pass
            
            html_doc = response.html.html
            
        else :
            r =  self.Session.get(url, allow_redirects=True)
            html_doc = r.text  # r.content    r.text
       
        soup = BeautifulSoup( html_doc , "html5lib")  # 'html5lib' , 'html.parser'  'lxml'

        #for link in soup.find_all(attrs={'href': re.compile("http")}):
        for link in soup.find_all('a', href=True):
            
            href = link.get('href')     #  link.attrs.get("href")   
            
            if href == "" or href is None:   
                continue   # href empty tag
                
            href = urljoin(url, href)      # join the URL if it's relative (not absolute link)
            
            parsed_href = urlparse(href)
            
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path  # remove URL GET parameters, URL fragments, etc.
            
            if not self.is_valid(href):     # not a valid URL
                continue      
                
            if href in self.internal_urls:  # already in the set
                continue       
                
            if domain_name not in href:  # external link
                if href not in self.external_urls:
                    if verbose :
                        print(f"{GRAY}[!] External link: {href}{RESET}")
                    self.external_urls.add(href)
                continue
                
            # https://stackoverflow.com/questions/16778435/python-check-if-website-exists
            if self.Session.get(href).status_code >= 400: 
                continue
            if verbose :
                print(f"{GREEN}[*] Internal link: {href}{RESET}")
            self.internal_urls.add(href)
            
            urls.add(href)
            
        return urls

    def RecCrawl(self, url, max_urls=30, DynamicSite=0, verbose=False):
        """
        Crawls a web page and extracts all links.
        You'll find all links in `external_urls` and `internal_urls` global set variables.
        params:
            max_urls (int): number of max urls to crawl, default is 30.
        """
        self.total_urls_visited += 1
        
        print(f"{YELLOW}[*] Crawling: {url}{RESET}")
        links = self.get_all_website_links(url, DynamicSite, verbose)
        for link in links:
            if self.total_urls_visited > max_urls:
                break
            self.RecCrawl(link, max_urls, DynamicSite, verbose )

    def crawl(self, max_urls=30, DynamicSite=0, verbose=False):
        self.RecCrawl(self.url, max_urls, DynamicSite, verbose)

        print("[+] Total Internal links:", len(self.internal_urls))
        print("[+] Total External links:", len(self.external_urls))
        print("[+] Total URLs:", len(self.external_urls) + len(self.internal_urls))
        print("[+] Total crawled URLs:", max_urls)
        print()
        
        domain_name = urlparse(self.url).netloc
        # save the internal links to a file
        with open(f"Crawled/{domain_name}_internal_links.txt", "w") as f:
            for internal_link in self.internal_urls:
                print(internal_link.strip(), file=f)

        # save the external links to a file
        with open(f"Crawled/{domain_name}_external_links.txt", "w") as f:
            for external_link in self.external_urls:
                print(external_link.strip(), file=f)

        self.internal_urls.remove(self.loginURL)
        for avoid_url in self.avoidURLS:
            self.internal_urls.remove(avoid_url)
        return self.internal_urls
