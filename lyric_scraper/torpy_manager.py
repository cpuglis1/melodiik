from torpy.http.requests import TorRequests
from utils import logger 
import random

class TorpyManager:
    def __init__(self):
        self.tor_requests = None 
        self.session = None 
        self.request_counter = 0 

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
    
        for tries in range(3):
            print(f"Try: {tries + 1}")
            HEADERS = {"User-Agent": random.choice(AGENT_LIST)}
            
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
