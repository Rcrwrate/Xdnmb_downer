from Network import Network
import logging


class Xdnmb():
    def __init__(self, cookie) -> None:
        self.s = Network(
            {"api.nmb.best": {"ip": "102.140.90.42"}}, log_level=logging.INFO)
        self.s.changeHeader({"cookie": cookie})

    def po(self, id, page):
        url = f"https://api.nmb.best/Api/po/id/{id}/page/{page}"
        r = self.s.get(url)
        return self.remove_tips(r.json())

    def defalut(self, id, page):
        url = f"https://api.nmb.best/Api/thread/id/{id}/page/{page}"
        r = self.s.get(url)
        return self.remove_tips(r.json())

    # def get_all(self, id):
    #     try:
    #         p = 1
    #         r = self.po(id, p)
    #         fin = r
    #         while len(r["Replies"]) != 0:
    #             p += 1
    #             r = self.po(id, p)
    #             fin["Replies"] += r["Replies"]
    #     except Exception as e:
    #         self.err = fin
    #         raise Exception(e.args)
    #     return fin

    def get_all(self, id, p=1, fin=[]):
        try:
            r = self.po(id, p)
            fin.append(r)
            p += 1
            while len(r["Replies"]) != 0:
                r = self.po(id, p)
                fin.append(r)
                p += 1
        except Exception as e:
            self.err = self.transform(fin)
            raise Exception(e.args)
        return fin

    def get_with_cache(self, id):
        c = self.cache(id)
        if c:
            fin = self.get_all(id, p=len(c)+1, fin=c)
            return self.transform(fin)
        else:
            fin = self.get_all(id)
            self.cache(id, fin[:-2])
            return self.transform(fin)

    @staticmethod
    def transform(fin):
        f = fin[0]
        i = 1
        while i < len(fin):
            f["Replies"] += fin[i]["Replies"]
            i += 1
        return f

    @staticmethod
    def remove_tips(fin):
        i = 0
        while i < len(fin["Replies"]):
            if fin["Replies"][i]["id"] == 9999999:
                del fin["Replies"][i]
            i += 1
        return fin

    @staticmethod
    def cache(id, fin={}):
        import json
        if fin == {}:
            try:
                with open(f".log/{id}.json", "r", encoding="utf-8") as f:
                    c = json.load(f)
                return c
            except:
                print("[INFO]:未检测到缓存")
                return False
        else:
            with open(f".log/{id}.json", "w", encoding="utf-8") as f:
                json.dump(fin, f)
