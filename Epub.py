import os
from Lib.Network import Network


def mkdir(path):
    if os.path.exists(path) != True:
        os.mkdir(path)


class Epub():
    def __init__(self, name, url) -> None:
        self.name = name
        self.url = url
        self.forder_init()
        self.list = []
        self.id = 1
        self.pics = []

    def forder_init(self):
        mkdir(".tmp")
        mkdir(f".tmp/{self.name}")
        mkdir(f".tmp/{self.name}/META-INF")
        with open(f".tmp/{self.name}/META-INF/container.xml", "w", encoding="utf-8") as f:
            f.write('''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
   </rootfiles>
</container>''')
        with open(f".tmp/{self.name}/mimetype", "w", encoding="utf-8") as f:
            f.write('''application/epub+zip''')
        mkdir(f".tmp/{self.name}/OEBPS")
        mkdir(f".tmp/{self.name}/OEBPS/Images")
        mkdir(f".tmp/{self.name}/OEBPS/Styles")
        mkdir(f".tmp/{self.name}/OEBPS/Text")
        with open("cover.jpg","rb") as f:
            b = f.read()
        with open(f'.tmp/{self.name}/OEBPS/Images/cover.jpg',"wb") as f:
            f.write(b)

    def plugin(self, Net: Network):
        self.s = Net
    
    def download(self,url:list):
        fin = []
        for i in url:
            try:
                r = self.s.get(i)
                if r.status_code == 200:
                    with open(f'''.tmp/{self.name}/OEBPS/Images/{i.split("/")[-1]}''',"wb") as f:
                        f.write(r.content)
                    self.pics.append(i)
                    fin.append(i)
            except:
                print(f"[ERR]:\t{i}\t下载失败,是否将文件正常加入EPUB图片清单和插入章节Y/N")
                inputs = input('>')
                if inputs == "Y":
                    print(f'''[TIPS]:您需要手动下载该文件置于.tmp/{self.name}/OEBPS/Images/{i.split("/")[-1]}''')
                    self.pics.append(i)
                    fin.append(i)
        return fin

    def cover(self, text):
        with open(f".tmp/{self.name}/OEBPS/Text/cover.xhtml", "w", encoding="utf-8") as f:
            f.write(f'''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>书籍封面</title>
</head>
<body>
<div style="text-align: center; padding: 0pt; margin: 0pt;">
<svg xmlns="http://www.w3.org/2000/svg" height="100%" preserveAspectRatio="xMidYMid meet" version="1.1" viewBox="0 0 179 248" width="100%" xmlns:xlink="http://www.w3.org/1999/xlink">
<image height="248" width="179" xlink:href="../Images/cover.jpg"></image>
</svg>
</div>
<h1>{self.name}</h1>
<h2>{self.url}</h2>
<h3>更新時間: 我不知道</h3>
<h3>簡介:</h3>
''')
            o = text.replace("\n", "").split("<br />")
            for i in o:
                if i != "":
                    f.write(f"<p>　　{i}</p>\n")
            f.write("</body>\n</html>\n")
        self.list.append({
            "id": "cover",
            "url": "Text/cover.xhtml",
            "title": "书籍封面"
        })

    def add_text(self, text, title, pics=[]):
        pics = self.download(pics)
        o = text.replace("\n", "").split("<br />")
        with open(f".tmp/{self.name}/OEBPS/Text/{self.id:06d}.xhtml", "w", encoding="utf-8") as f:
            f.write(f'''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>{title}</title>
</head>
<body>
<h3>{title}</h3>\n''')
            for i in o:
                if i != "":
                    f.write(f"<p>　　{i}</p>\n")
            for i in pics:
                f.write(
                    f'''<p>　　<img src="../Images/{i.split("/")[-1]}" alt=""/></p>\n''')
            f.write("</body></html>")
        self.list.append({
            "id": f"{self.id:06d}",
            "url": f"Text/{self.id:06d}.xhtml",
            "title": title
        })
        self.id += 1

    def finish(self):
        with open(f".tmp/{self.name}/OEBPS/toc.ncx", "w", encoding="utf-8") as f:
            f.write(f'''<?xml version="1.0" encoding="utf-8" standalone="no" ?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head>
<meta content="hbooker:100012892" name="dtb:uid"/>
<meta content="2" name="dtb:depth"/>
<meta content="0" name="dtb:totalPageCount"/>
<meta content="0" name="dtb:maxPageNumber"/>
</head>
<docTitle>
<text>{self.name}</text>
</docTitle>
<docAuthor>
<text>{self.url}</text>
</docAuthor>
<navMap>\n''')
            i = 1
            while i <= len(self.list):
                f.write(
                    f'''<navPoint id="{self.list[i-1]["id"]}" playOrder="{i}"><navLabel><text>{self.list[i-1]["title"]}</text></navLabel><content src="{self.list[i-1]["url"]}" /></navPoint>\n''')
                i += 1
            f.write("</navMap>\n</ncx>\n")
        with open(f".tmp/{self.name}/OEBPS/content.opf", "w", encoding="utf-8") as f:
            f.write(f'''<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId" version="2.0">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
<dc:identifier id="BookId">{self.url}</dc:identifier>
<dc:title>{self.name}</dc:title>
<dc:creator opf:role="aut">{self.url}</dc:creator>
<dc:language>zh-CN</dc:language>
<dc:publisher></dc:publisher>
</metadata>
<manifest>
<item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml" />
<item href="Images/cover.jpg" id="cover.jpg" media-type="image/jpeg" />
''')
#可以在此处</metadata>之前加入<meta name="cover" content="cover.jpg"/>,加入后QQ的epub插件会出现异常，移除后正常，但封面章节内的文字依旧不显示
            for i in self.list:
                f.write(
                    f'''<item href="{i["url"]}" id="{i["url"].replace("Text/", "")}" media-type="application/xhtml+xml" />\n''')
            for i in self.pics:
                f.write(
                    f'''<item href="Images/{i.split("/")[-1]}" id="{i.split("/")[-1]}" media-type="image/jpeg" />\n''')
            f.write('''</manifest>\n<spine toc="ncx">\n''')
            for i in self.list:
                f.write(
                    '''<itemref idref="{}" />\n'''.format(i["url"].replace("Text/", "")))
            f.write(
                '''</spine>\n<guide>\n<reference href="Text/cover.xhtml" title="书籍封面" type="cover" />\n</guide>\n</package>''')

class TXT():
    def __init__(self,name) -> None:
        self.f = open(f".tmp/{name}.txt","w",encoding="utf-8")
    
    def add(self,text):
        self.f.write(text.replace("<br />",""))
        self.f.write("\n")

    def __del__(self):
        self.f.close()

if __name__ == '__main__':
    e = Epub("test", "adw")
    e.cover("ABABA")
    n = Network({})
    e.plugin(n)
    e.add_text("aaa", "wuti", [
               "https://image.nmb.best/image/2022-09-13/6320726e73bd9.jpg"])
    
    e.finish()
