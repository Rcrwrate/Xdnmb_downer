import argparse
import os
import sys
parser = argparse.ArgumentParser(
    prog="Xdnmb Downloader",
    description='用于下载Xdnmb的串内容',
    epilog='Phantom-sea © limited',
)
parser.add_argument('-c', '--cookies', type=str,
                    dest="cookie", help='设置cookie,请用冒号包裹', default=False)
parser.add_argument('-t', '--title', type=str,
                    help='此参数将在标题为无标题的时候覆盖串标题', default=False)
parser.add_argument("-ft", "--forcetitle", type=str,
                    help='用此参数强制覆盖串标题', default=False)
parser.add_argument("-d", "--download", type=int,
                    help='下载某个串，中间无视其他优化选项', default=False)
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

    cookies = cookies(args.cookie)
    if cookies == False:
        print("[ERR]:请先设置Cookie或用-c传入")
        sys.exit(-1)


main(args)
