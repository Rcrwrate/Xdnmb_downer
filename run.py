import re
import os
from Xdnmb import Xdnmb, XdnmbException
from Lib.ini import CONF

conf = CONF("Xdnmb")


def get(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default


def setting(inputs=False, sec="", key=""):
    if inputs == False:
        try:
            return conf.load(sec, key)[0]
        except:
            return False
    else:
        conf.add(sec, key, inputs)
        conf.save()
        return inputs


def Cookie(inputs=[]):
    if inputs == []:
        return setting(sec="cookie", key="cookie").replace("_",r"%")
    else:
        if len(inputs) < 3:
            print("[ERR]:\t请按照如下进行输入\n>c PHPSESSID=*****; userhash=*****")
        else:
            c = f"{inputs[1]} {inputs[2]}"
            setting(sec="cookie", key="cookie", inputs=c.replace(r"%", "_"))
            return c


def cache(cache={}):
    import json
    if cache == {}:
        try:
            with open(os.path.join(".log", "cache.json"), "r", encoding="utf-8") as f:
                c = json.load(f)
            return c
        except:
            print("[ERR]:\t缓存不存在或缓存失效")
            return False
    else:
        with open(os.path.join(".log", "cache.json"), "w", encoding="utf-8") as f:
            json.dump(cache, f)


def out(fin, x):
    print("[OUT]:正在导出")
    from Epub import Epub
    from Epub import TXT
    e = Epub(fin["title"], f'''https://www.nmbxd1.com/t/{fin["id"]}''')
    e.plugin(x.s)
    e.cover(fin["content"])
    msg = fin["Replies"]
    e.add_text(
        f'''来自https://www.nmbxd1.com/t/{fin["id"]}<br />版权归属原作者及X岛匿名版<br />请勿用于违法用途，仅供学习交流使用，请在24小时内删除<br />本文档由https://github.com/Rcrwrate/Xdnmb_downer生成''', "来源声明")
    for i in msg:
        if i["img"] != "":
            e.add_text(i["content"], i["title"], [
                       "https://image.nmb.best/image/"+i["img"]+i["ext"]])
        else:
            e.add_text(i["content"], i["title"])
    e.finish()
    t = TXT(fin["title"])
    t.add(
        f'''来自https://www.nmbxd1.com/t/{fin["id"]}\n版权归属原作者及X岛匿名版\n请勿用于违法用途，仅供学习交流使用，请在24小时内删除\n本文档由https://github.com/Rcrwrate/Xdnmb_downer生成''')
    t.add(fin["content"])
    for i in fin["Replies"]:
        t.add(i["content"])
    del t
    print("[OUT]:导出完成")


def analysis(fin: dict):
    i = 0
    while i < len(fin["Replies"]):
        if len(fin["Replies"][i]["content"]) <= 25 and fin["Replies"][i]["img"] == "":
            print(
                f'''[ANALYSIS]:\t侦测到过短内容,请手动审核,从最终结果删除为d,其他为通过,以下为具体内容\n\t\t{fin["Replies"][i]["content"]}''')
            inputs = re.split('\\s+', input('>').strip())
            if inputs[0].startswith('d'):
                del fin["Replies"][i]
        i += 1
    print("[ANALYSIS]:\t优化完成")
    print(
        f'''[TIPS]:当前标题为"{fin["title"]}",是否需要修改,如需修改请直接键入修改后的标题,不需请按回车''')
    inputs = re.split('\\s+', input('>').strip())[0]
    if inputs != "":
        fin["title"] = inputs
    return fin


msg = '''
指令(指令输入字首即可):
h | help\t\t\t\t\t--- 显示说明 (显示此讯息)
r | read cache\t\t\t\t\t--- 读取上次缓存文件，并启用优化选项
q | quit\t\t\t\t\t--- 退出脚本
c <cookie> | cookie <cookie> \t\t\t--- 设置cookie
d <id> | download <id> \t\t\t\t--- 下载某个串，中间无视其他优化选项
i <id> | id <id> \t\t\t\t--- 下载某个串，并启用优化选项
'''
print(msg)


def main():
    try:
        cookie = Cookie()
        inputs = re.split('\\s+', get('>').strip())
        while True:
            if inputs[0].startswith('q'):
                import sys
                sys.exit()
            elif inputs[0].startswith('c'):
                Cookie(inputs)
            elif inputs[0].startswith('d'):
                if cookie:
                    if len(inputs) != 2:
                        print("[ERR]:\t缺少参数")
                    else:
                        x = Xdnmb(cookie)
                        try:
                            fin = x.get_with_cache(inputs[1], x.po)
                        except Exception as e:
                            print(f"[ERROR]:\t{e.args}")
                            fin = x.err
                        cache(fin)
                        out(fin, x)
                else:
                    print("[ERR]:\t请先设置cookie")
            elif inputs[0].startswith('r'):
                c = cache()
                if c:
                    fin = analysis(c)
                    x = Xdnmb("")
                    out(fin, x)
            elif inputs[0].startswith('i'):
                if cookie:
                    if len(inputs) != 2:
                        print("[ERR]:\t缺少参数")
                    else:
                        x = Xdnmb(cookie)
                        try:
                            fin = x.get_with_cache(inputs[1], x.po)
                        except Exception as e:
                            print(f"[ERROR]:\t{e.args}")
                            fin = x.err
                        cache(fin)
                        fin = analysis(fin)
                        out(fin, x)
                else:
                    print("[ERR]:\t请先设置cookie")
            elif inputs[0].startswith('s'):
                if len(inputs) == 2:
                    uuid = inputs[1]
                    setting(inputs=uuid, sec="subscribe", key="uuid")
                else:
                    uuid = setting(sec="subscribe", key="uuid")
                if uuid == False:
                    raise XdnmbException("虚空订阅?")
                x = Xdnmb(cookie)
                l = x.subscribe(uuid)
                print(f"订阅总数共{len(l)}个")
            else:
                print(msg)
            inputs = re.split('\\s+', get('>').strip())
    except XdnmbException as err:
        print("[ERR]:" + err.args[0])
        main()
    except Exception:
        import traceback
        print(traceback.format_exc())


if __name__ == "__main__":
    main()
