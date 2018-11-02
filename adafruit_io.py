import urllib.request
import time
import json

class AdafruitIO:
    
    def __init__(self,user,key):
        '''Create an adafruit-io connector object.
        
        Args:
            user (string): the adafruit-io user name
            key (string): the X-AIO key for the user (only needed for non-public actions)
        '''
        
        self._user = user
        self._key = key           
    
    def add_data(self,feed,value):
        '''Post a new data value to the feed.
        
        Args:
            feed (string): the name of the feed
            value: the value to post to the feed
            
        Returns:
            json: the JSON object in response to the POST
        '''
        
        post_headers = {
            'X-AIO-Key': key, 
            'Content-Type':'application/json'
        }
        data = {'value' : value}
        url = 'https://io.adafruit.com/api/v2/{user}/feeds/{feed}/data'.format(user=self._user,feed=feed)
        d = json.dumps(data).encode()
        req = urllib.request.Request(url=url,headers=post_headers,method='POST',data=d)
        f = urllib.request.urlopen(req)
        ret =  json.loads(f.read().decode())
        return ret
    
    def add_data_retry(self,feed,value,retries=4,retry_wait=0.25):
        '''Post a new data value to the feed with retries.
        
        This attempts to recover from transient errors.
        
        Args:
            feed (string): the name of the feed
            value: the value to post to the feed
            retries (int): number of times to try the POST
            retry_wait (float): seconds to wait before a retry
        '''
        
        for x in range(retries-1):
            try:
                return self.add_data(feed,value)
            except:
                time.sleep(retry_wait)
        return self.add_data(feed,value)
