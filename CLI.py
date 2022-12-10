import argparse
import os
import sys
from Xdnmb import Xdnmb, XdnmbException
from Epub import Epub, TXT

parser = argparse.ArgumentParser(
    prog="Xdnmb Downloader",
    description='用于下载Xdnmb的串内容',
    epilog='Phantom-sea © limited |∀` )',
)
parser.add_argument('-c', '--cookies', type=str,
                    dest="cookie", help='设置cookie,请用冒号包裹', default=False)
parser.add_argument('-t', '--title', type=str,
                    help='此参数将在标题为无标题的时候覆盖串标题', default=False)
parser.add_argument("-ft", "--forcetitle", type=str,
                    help='用此参数强制覆盖串标题', default=False)
parser.add_argument("-d", "--download", "-i", "--id", type=int,
                    help='下载某个串，中间无视其他优化选项', default=False)
parser.add_argument("-o", "--output", type=str, nargs="?",
                    help='输出选择,可选项:epub,txt,默认全部', default=["epub", "txt"])
args = parser.parse_args()

print(args)


def main(args):
    def cookies(inputs=False):
        if inputs == False:
            try:
                with open(os.path.join(".log", "cookies"), "r", encoding="utf-8") as f:
                    return f.readlines()[0]
            except:
                return False
        else:
            inputs = inputs.split(" ")
            if len(inputs) < 3:
                print("[ERR]:\t请按照如下进行输入\n\t-c \"PHPSESSID=***** userhash=*****\"")
                sys.exit(-1)
            else:
                with open(os.path.join(".log", "cookies"), "w", encoding="utf-8") as f:
                    f.write(f"{inputs[0]} {inputs[1]}")
                return f"{inputs[0]} {inputs[1]}"

    def out(fin, x):
        print("[OUT]:正在导出")
        if "epub" in args.output:
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

        if "txt" in args.output:
            t = TXT(fin["title"])
            t.add(
                f'''来自https://www.nmbxd1.com/t/{fin["id"]}\n版权归属原作者及X岛匿名版\n请勿用于违法用途，仅供学习交流使用，请在24小时内删除\n本文档由https://github.com/Rcrwrate/Xdnmb_downer生成''')
            t.add(fin["content"])
            for i in fin["Replies"]:
                t.add(i["content"])
            del t
            print("[OUT]:导出完成")

    cookies = cookies(args.cookie)
    if cookies == False:
        print("[ERR]:请先设置Cookie或用-c传入")
        sys.exit(-1)
    if args.download == False:
        print("[ERR]:虚空下载不可取")
        sys.exit(0)
    x = Xdnmb(cookies)
    try:
        fin = x.get_with_cache(args.download, x.po)
    except XdnmbException as err:
        print("[ERR]:" + err.args[0])
        sys.exit(-1)
    except Exception as err:
        print("[ERR]:" + err.args[0])
        sys.exit(-1)
    if args.forcetitle:
        fin["title"] = args.forcetitle
    else:
        if args.title and fin["title"] == "无标题":
            fin["title"] = args.title

    out(fin, x=x)


main(args)
