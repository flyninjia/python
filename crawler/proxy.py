#coding:utf8

"""
proxiex.py
~~~~~~~~~~~~~

该模块包含所有代理服务器列表，提供代理选择功能。
爬取 xicidaili 高匿代理 判断可用代理 存储avaiable 1 ,否则为 0
"""

from threadPool import ThreadPool
import requests
import re
import urllib2
import sys
import database
import os

import time


class Proxy(object):

    def __init__(self):
        self.url = 'http://www.jiangshi.org'
        self.proxyurl = 'http://www.xicidaili.com/nn/'
        self.proxyip_db = database.DatabaseProxyIp()

    #循环读取列表页
    def HttpIP_get(self):

        for x in range(2):
            url = self.proxyurl+str(x+1)
            print 'get the url proxy ip: ',url
            self.frist_loop(url,x)

    #获取页面内容
    def getHtml(self,url):
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        req = urllib2.Request(url, headers = headers)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        unicodePage = myPage.decode("utf-8")
        #print unicodePage
        return unicodePage

    #页面内容正则匹配,返回获取ip,port及time
    def regularinfo(self,proxyurl):
        pattern_iport = re.compile('<td>([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})</td>\s*<td>([0-9]*)</td>',re.S)
        pattern_time = re.compile('<td>([0-9]{2})-([0-9]{2})-([0-9]{2})\s*([0-9]{2}):([0-9]{2})</td>')
        #获取所有匹配内容
        items_iport = re.findall(pattern_iport,self.getHtml(proxyurl))
        items_time = re.findall(pattern_time,self.getHtml(proxyurl))
        return items_iport, items_time

    #第一次获取前2页数据,并进行保存到数据库
    def frist_loop(self, proxyurl, x):
        items_iport,items_time = self.regularinfo(proxyurl)
        #loop regular get http://www.xicidaili.com ip,prot time write in database
        for n in range(0,len(items_iport)-1):

            iport = items_iport[n][0]+':'+items_iport[n][1]
            time  = items_time[n][0]+items_time[n][1]+items_time[n][2]+items_time[n][3]+items_time[n][4]
            if n == 0 and x == 0:
                self.proxyip_db.saveDatatime(time)

            self.proxyip_db.saveData(0, iport, time)

    #及时获取数据,并判断时间时候大于endtime 时间,保存到数据库中
    def for_loop(self):
        items_iport,items_time = self.regularinfo(self.proxyurl)
        endtime = self.proxyip_db.readendtime()
        num = 0
        for n in range(0,len(items_iport)-1):

            iport = items_iport[n][0]+':'+items_iport[n][1]
            time  = items_time[n][0]+items_time[n][1]+items_time[n][2]+items_time[n][3]+items_time[n][4]
            if time > endtime[0][0]:
                num = num + 1
                print 'get new ip: ',iport
                if n == 0:
                    self.proxyip_db.updateendtime(time)
                self.proxyip_db.saveData(0, iport, time)
        print '=====> add new ',num,' ip'

    #测试代理可连接性
    def checkProxy(self,proxy):
        try:
            response = requests.get('http://www.baidu.com',timeout=10, proxies={'http':proxy})
            if '030173' in response.text:
                return 'ok',proxy
        except Exception,e:
            return 'fail',proxy

    def checkclientUrl(self,proxy):
        try:
            response = requests.get(self.url,timeout=10)
            #print response.text.decode('utf-8')
            if '.goback a:hover,' in response.text:
                #print 'url are lock ,please wait some times ===='
                #return 'lock',proxy
                return 'lock',proxy
            elif 'ff5146bd3e0db147ced120c6c2c9bcb2' in response.text:
                #print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                return 'ok',proxy
            else:
                #print 'cant client the url'
                return 'fail',proxy
        except Exception,e:
            #print e
            return 'fail',proxy

    #保存测试成功代理到proxyipok表中
    def saveProxies(self):
        #创建线程30个,并开启线程
        threadPool = ThreadPool(30)
        threadPool.startThreads()

        #调用类 读取数据
        #databases = database.DatabaseProxyIp()

        proxyip = self.proxyip_db.readData()
        #x循环读取数据进行匹配
        for proxy in proxyip:
            #把测试函数放入线程中
            threadPool.putTask(self.checkclientUrl, proxy[0])
            #threadPool.putTask(self.checkProxy, proxy[0])
            #flag,proxy = checkProxy(proxy[0])
        #循环获取测试结果,成功写入数据库,失败修改available为0
        ip_fail = 0
        ip_ok = 0
        ip_lock = 0
        while threadPool.getTaskLeft():
            flag, proxy = threadPool.getTaskResult()
            print flag, proxy
            if flag == 'ok':
                #print 'ok ', proxy
                self.proxyip_db.updateData(1, proxy)
                ip_ok = ip_ok + 1
            elif flag == 'lock':
                self.proxyip_db.updateData(0, proxy)
                ip_lock = ip_lock + 1
            else:
                self.proxyip_db.delData(proxy)
                ip_fail = ip_fail + 1

        print '====> available ip: ',ip_ok,' , lock ip: ',ip_lock,' , fail ip: ',ip_fail,' <===='
        threadPool.stopThreads()

    def help():
        print 'Usage: pyhon proxy.py [options]'
        print 'Option:'
        print '   -h  help'
        print '   -f  frist get proxyip for HttpProxyIp.db'
        print '   -c  Check the proxyip to new table'

def main():
    if os.path.isfile('proxyip.db'):
        os.remove('proxyip.db')
    proxy = Proxy()
    #proxy.getProxy()
    proxy.HttpIP_get()
    proxy.saveProxies()
    while True:
        print 'please wait some 200 second .. .. '
        time.sleep(200)
        proxy.for_loop()
        proxy.saveProxies()

if __name__ == '__main__':
    main()

    '''
    proxyip_db = database.DatabaseProxyIp()
    try:
        f = open('ip.txt','r')
        for line in f.readlines():
            proxyip_db.saveData(1,line.strip(),'')
    finally:
        if f:
            f.close()
    '''
    #proxy = Proxy()
    #while True:
    #    proxy.checkclientUrl('101.201.235.141:8000')
    #    time.sleep(1)