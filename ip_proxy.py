#coding:utf-8
from fake_useragent import UserAgent
import requests,threading,datetime
from lxml import etree
import random

# ------------------------------------------------------文档处理--------------------------------------------------------
# 写入文档
def write(path,text):
    with open(path,'a', encoding='utf-8') as f:
        f.writelines(text)
        f.write('\n')
# 清空文档
def truncatefile(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.truncate()
# 读取文档
def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        txt = []
        for s in f.readlines():
            txt.append(s.strip())
    return txt
# -----------------------------------------------------检查ip是否可用----------------------------------------------------
def checkip(targeturl,ip):
    ua = UserAgent()
    headers = {'User-Agent':ua.random}
    proxies = {"http": "http://"+ip, "https": "http://"+ip}  # 代理ip
    try:
        response=requests.get(url=targeturl,proxies=proxies,headers=headers,timeout=5).status_code
        if response == 200 :
            return True
        else:
            return False
    except:
        return False
#-------------------------------------------------------获取代理方法----------------------------------------------------
# 免费代理 XiciDaili
def findip(pagenum,targeturl,path): # ip类型,页码,目标url,存放ip的路径
    ip_url='http://www.xicidaili.com/nn/'  # xicidaili国内高匿代理
    url = r'{}/{}'.format(ip_url,pagenum) # 配置url
    ua = UserAgent()
    headers = {'User-Agent':ua.random}
    html=requests.get(url=url,headers=headers,timeout = 5).text
    selectors = etree.HTML(html)
    for tr in selectors.xpath('.//tr[@class="odd"]'):
        tds = tr.xpath('.//td/text()')
        ip = '%s:%s'%(tds[0],tds[1])
        is_avail = checkip(targeturl,ip)
        if is_avail == True:
            write(path=path,text=ip)
            print(ip)
#-----------------------------------------------------多线程抓取ip入口---------------------------------------------------
def getip(targeturl,path):
     truncatefile(path)             # 爬取前清空文档
     threads=[]
     for pagenum in range(11):
         t=threading.Thread(target=findip,args=(pagenum+1,targeturl,path))
         threads.append(t)
     print('开始爬取代理ip')
     for s in threads:              # 开启多线程爬取
         s.start()
     for e in threads:          # 等待所有线程结束
         e.join()
     print('爬取完成')
     ips = read(path)       # 读取爬到的ip数量
     print('一共爬取代理ip: %s 个' % (len(ips)))

#-------------------------------------------------------启动-----------------------------------------------------------
if __name__ == '__main__':
    path = 'ip.txt'                                 # 存放爬取ip的文档path
    targeturl = 'http://www.cnblogs.com/TurboWay/' # 验证ip有效性的指定url
    getip(targeturl,path)