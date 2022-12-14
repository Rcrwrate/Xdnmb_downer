from Lib.Network import Network
import os
import json


class XdnmbException(BaseException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Xdnmb():
    def __init__(self, cookie, s: Network = Network({})) -> None:
        self.s = s
        self.s.changeHeader({"cookie": cookie})

    def po(self, id, page):
        url = f"https://api.nmb.best/Api/po/id/{id}/page/{page}"
        r = self.s.get(url).json()
        self.success(r)
        return self.remove_tips(r)

    def defalut(self, id, page):
        url = f"https://api.nmb.best/Api/thread/id/{id}/page/{page}"
        r = self.s.get(url).json()
        self.success(r)
        return self.remove_tips(r)

    def subscribe(self, uuid):
        def single(page):
            url = f"https://api.nmb.best/Api/feed/uuid/{uuid}/page/{page}"
            r = self.s.get(url).json()
            self.success(r)
            return r
        fin = []
        i = 1
        t = single(i)
        c = self.cache("subscribe")
        if c:
            if c[0]["id"] == t[0]["id"]:
                return c
        while t != []:
            fin += t
            i += 1
            t = single(i)
        self.cache("subscribe", fin)
        return fin

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

    def get_by_id(self, id):
        url = f"https://api.nmb.best/Api/ref/id/{id}"
        r = self.s.get(url).json()
        self.success(r)
        return r

    def get_all(self, id, handle, p=1, fin=[]):
        try:
            r = handle(id, p)
            fin.append(r)
            p += 1
            while len(r["Replies"]) != 0:
                r = handle(id, p)
                fin.append(r)
                p += 1
        except Exception as e:
            self.err = self.transform(fin)
            raise Exception(e.args)
        return fin

    def get_with_cache(self, id, handle):
        c = self.cache(f"{id}_{handle.__name__}")
        if c:
            fin = self.get_all(id, handle, p=len(c)+1, fin=c)
            return self.transform(fin)
        else:
            fin = self.get_all(id, handle)
            self.cache(f"{id}_{handle.__name__}", fin[:-2])
            return self.transform(fin)

    @staticmethod
    def success(r):
        try:
            r["success"] == False
        except Exception:
            return r
        else:
            if r["error"] == "???????????????":
                raise XdnmbException("?????????????????????,???????????????,?????????????????????")
            elif r["error"] == "??????????????????????????????????????????":
                raise XdnmbException("???????????????????????????????,??????????????????????????????????????????,?????????????????????")
            else:
                raise XdnmbException("?????????,????????????????????????:"+r["error"])

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
        path = os.path.join(".log", f"{id}.json")
        if fin == {}:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    c = json.load(f)
                return c
            except:
                print("[INFO]:??????????????????")
                return False
        else:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(fin, f)
