from torpy.http.requests import TorRequests
from bs4 import BeautifulSoup
from utils import logger 
import time
import random

class TorpyManager:
    def __init__(self, rate_limit=5):
        self.tor_requests = None
        self.session = None
        self.request_counter = 0
        self.tokens = rate_limit
        self.last_check = time.time()

    def _refill_tokens(self):
        now = time.time()
        elapsed_time = now - self.last_check
        self.tokens += elapsed_time
        self.last_check = now

    def _consume_token(self):
        if self.tokens < 1:
            self._refill_tokens()
        while self.tokens < 1:
            time.sleep(0.1)
            self._refill_tokens()
        self.tokens -= 1

    @logger
    def create_session(self, sess):
       
        self.tor_requests = TorRequests()
        self.session = sess
        self.request_counter = 0  

    @logger
    def close_session(self):
      
        if hasattr(self.session, 'close'):
            self.session.close()
        self.session = None  
        self.request_counter = 0  

    @logger
    def rotate_session(self, sess):
      
        self.close_session()  
        self.create_session(sess)

    @logger
    def check_and_rotate_session(self, sess):
     
        if self.request_counter >= 3:
            self.rotate_session(sess)
            print("Session Refreshed")

    @logger
    def request_handler(self, url, AGENT_LIST):
        self._consume_token() 

        for tries in range(3):
            print(f"Try: {tries + 1}")
            random_agent = random.choice(AGENT_LIST)
            HEADERS = {"User-Agent": random_agent}
            
            try:
                response = self._send_request(url, HEADERS)
            except Exception as e:
                print(e)
            else:
                return response

        print("Max retries reached.")
        return None


    @logger
    def _send_request(self, url, HEADERS):

        print(self.session.get("http://httpbin.org/ip").json())
        response = self.session.get(url, headers=HEADERS, timeout=5)
        print(HEADERS["User-Agent"])
        
        self.request_counter += 1  # Update the request counter
        
        return response
    
    @logger
    def check_for_captcha(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        captcha_present = soup.find("div", {"id": "az_captcha_container"}) is not None
        return captcha_present
