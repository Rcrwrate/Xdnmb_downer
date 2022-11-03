from Xdnmb import Xdnmb
from Epub import Epub
from Epub import TXT

x = Xdnmb(r"PHPSESSID=*****; userhash=*****")
DID = 51340998
fin = x.get_with_cache(DID)
fin["title"] = "魔王勇者二三事"#作品标题,这里是原文标题不合适所以进行修改

e = Epub(fin["title"],f"https://www.nmbxd1.com/t/{DID}")
e.plugin(x.s)

e.cover(fin["content"])
msg = fin["Replies"]
e.add_text(f"来自https://www.nmbxd1.com/t/{DID}\n版权归属原作者及X岛匿名版","来源声明")
for i in msg:
    if i["img"] != "":
        e.add_text(i["content"],i["title"],["https://image.nmb.best/image/"+i["img"]+i["ext"]])
    else:
        e.add_text(i["content"],i["title"])
e.finish()

t = TXT(fin["title"])
t.add(f"来自https://www.nmbxd1.com/t/{DID}\n版权归属原作者及X岛匿名版")
t.add(fin["content"])
for i in fin["Replies"]:
    t.add(i["content"])