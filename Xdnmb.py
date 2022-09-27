from Epub import TXT
from Epub import Epub
from Network import Network
import logging

class Xdnmb():
    def __init__(self,cookie) -> None:
        self.s = Network({"api.nmb.best":{"ip":"102.140.90.42"}},log_level=logging.INFO)
        self.s.changeHeader({"cookie":cookie})
    
    def po(self,id,page):
        url = f"https://api.nmb.best/Api/po/id/{id}/page/{page}"
        r = self.s.get(url)
        return r.json()
    
    def defalut(self,id,page):
        url = f"https://api.nmb.best/Api/thread/id/{id}/page/{page}"
        r = self.s.get(url)
        return r.json()
    
    def get_all(self,id):
        p = 1
        r = self.po(id,p)
        fin = r
        while len(r["Replies"]) != 0:
            p += 1
            r = self.po(id,p)
            fin["Replies"] += r["Replies"]
        return fin
    
    



    