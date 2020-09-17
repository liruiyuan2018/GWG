import requests
from bs4 import BeautifulSoup
import time
import re
#import response
#from collections import OrderedDict
mdict = {}
for i in range(1000000):
    with open("hr.txt", "r") as frh:
        hr = frh.read().strip() #当前要抓的单词，词组的词词是用＋连接
    with open("word.txt", "r") as frw:
        word = frw.read().strip() #词条，词组的词词之间空格
    with open("wordlist.txt", "r") as frw: #存的所有已抓取词头＋
        words = frw.readlines()
    for w in words:  #把已经处理的单词表读入字典
        mdict[w] = w
     

    

    
    for c in range(5):
        try:
            c += 1
            r = requests.get('http://www.goodwordguide.com/define/'+hr, timeout=5)
        except:
            time.sleep(10*c)
            print("ERROR"+str(c))
        else:
            break
    if (r.status_code != 200):
        print("BREAK")
        break
    soup = BeautifulSoup(r.text, "html5lib")
    divsharetag = soup.find("div", class_="shareToolBox") #移除共享按键
    if divsharetag:
        divsharetag.extract()

    divfontResizetag = soup.find("div", class_="fontResize") #移除字体设置
    if divfontResizetag:
        divfontResizetag.extract()
    
    divpronuntag = soup.find("a",class_="pronun_speaker") #除去发音
    if divpronuntag:
        divpronuntag.extract()
    
    dt = soup.find("div", class_="trail")
    tc = dt.find("li", class_=re.compile("trail-current"))
    
    d = soup.find("div", id="page")    
    word_tag = soup.find("h1", id="page-title")
    wordtemp = word_tag.string.strip()
    
    
    with open("dict.txt", "a") as fa:
        fa.write(word+"\n"+'''<link rel="stylesheet" href="goodwordguide.css">'''+str(d)+"\n</>\n")
    # with open ("wordlist.txt","a") as faword:
       # faword.write(hr+"\n")  #记录已经处理的单词
    mdict[hr] = hr #将已处理的词头记录进字典
    print(hr)
    print(word)

    n1 = tc.find_next_sibling("li")
    if (n1 == None):
        print("END")
        break   #网站最后一条词条，结束任务
    while (n1.a == None):
        n1 = n1.find_next_sibling("li")
    while True:
        print("n1.a现在的值是：",n1.a)
        hr1 = n1.a.get('href')
        word1 = n1.a.get_text().strip()
        for c1 in range(5):
            try:
                c1 += 1
                r1 = requests.get('http://www.goodwordguide.com/define/'+hr1, timeout=5)
            except:
                time.sleep(10*c1)
                print("ERROR"+str(c1))
            else:
                break
        if (r1.status_code != 404):
            newword = r1.url.lstrip('http://www.goodwordguide.com/define/')
            if newword in mdict: #有无跳转判断,如是（跳转到别的词条）则，
                with open("dict.txt", "a") as fa:
                    fa.write(word1+"\n"+'''<link rel="stylesheet" href="goodwordguide.css">'''+
                    '''<a href="entry://">'''+newword+'''</a>'''+"\n</>\n") 
                mdict[hr1] = newword
                with open("hr.txt", "w") as fwh:
                    fwh.write(hr1)
                with open("word.txt", "w") as fw:
                    fw.write(word1)
                with open ("wordlist.text","a") as fww:
                    fww.write(word1+"\n")            
            break
        
        n1 = n1.find_next_sibling("li")

    with open("hr.txt", "w") as fwh:
        fwh.write(n1.a.get("href").strip())
    with open("wordlist.txt", "a") as fww:
        fww.write(n1.string.strip()+"\n")
    with open ("word.txt", "w") as fw:
        fw.write(n1.string.strip())