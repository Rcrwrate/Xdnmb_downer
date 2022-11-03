import requests
import logging
import os
import ssl
ssl.HAS_SNI = False
requests.packages.urllib3.disable_warnings()

dfheader = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39",
    "sec-ch-ua": '''" Not A;Brand";v="99", "Chromium";v="101", "Microsoft Edge";v="101"''',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "dnt": "1",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "utf-8",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
}


def get_qs(qs, key):
    try:
        id = qs[key]
    except KeyError:
        return False
    else:
        return id


class Network():
    def __init__(self, hostTips: dict, log_path=".log", log_level=logging.INFO, proxies={"http": None, "https": None}) -> None:
        '''
        hostTips = {
            "office.com": {
                "ip": "0.0.0.0"
            },
            "office.com": {
                "ip": False
            }
        }
        '''

        if os.path.exists(log_path) != True:
            os.mkdir(log_path)
        self.LOG = logging.getLogger("Net")
        self.LOG.setLevel(log_level)
        F = logging.FileHandler(
            f"{log_path}\\Network.log", "a", encoding="utf-8")
        F.setFormatter(logging.Formatter('%(asctime)s:%(message)s'))
        self.LOG.addHandler(F)

        self.s = requests.session()
        self.s.trust_env = False
        self.s.keep_alive = False
        self.table = hostTips

    def get(self, url, headers=False, noDefaultHeader=False, changeDefaultHeader=False, verify=False, **kwargs):
        h = Header.headerchange(headers, noDefaultHeader, changeDefaultHeader)
        domain = url.split("/")[2]
        conf = get_qs(self.table, domain)
        if conf != False:
            ip = get_qs(conf, "ip")
            if ip:
                url = url.replace(domain, ip)
                h["host"] = domain
        try:
            r = self.s.get(url, headers=h, verify=False, **kwargs)
        except Exception as e:
            self.LOG.error(f"[GET][ERROR]\t\t{url}\t{domain}\t{e.args}")
            raise Exception(e.args)
        self.LOG.info(f"[GET][INFO]\t\t{r.status_code}\t{r.url}\t{domain}")
        try:
            self.LOG.debug(
                f"[GET][DEBUG]\t\t{h}\n"+"\t"*11 + f"{r.headers}\n" + "\t"*11 + f"{r.text}")
        except Exception:
            pass
        return r

    def changeHeader(self, header, noDefaultHeader=False):
        return Header.headerchange(header, noDefaultHeader, changeDefaultHeader=True)


class Header():
    @staticmethod
    def headerchange(header, noDefaultHeader=False, changeDefaultHeader=False):
        global dfheader
        if header:
            if noDefaultHeader:
                h = header
            else:
                h = Header.addheader(dfheader, header)
        else:
            h = dfheader.copy()
        if changeDefaultHeader:
            dfheader = h.copy()
        return h

    @staticmethod
    def addheader(d1: dict, d2: dict):
        d = d2.copy()
        for i in d1:
            d[i] = d1[i]
        return d
