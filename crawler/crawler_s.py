#coding:utf8

import Cookie
import cookielib

import urllib
import urllib2
import re

import random
import sqlite3

import database
import HttpTransport
#import requests
import os
import time

import logging

num = 0
num_ip = 1
changeIP = False


class Crawler(object):

    #def __init__(self, url):
    def __init__(self):
        #设定爬取翻页页面到url
        self.pageUrl = "http://www.baidu.com/page/"
        self.proxyip_db = database.DatabaseProxyIp()
        self.info_db = database.Database_capture()
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',                            filename = 'echo.log',
                            filemode = 'w')
        #self.url = ''
        #self.url = url

    #从db读取所有可用ip
    def read_proxyip(self):
        ip = self.proxyip_db.readDataOKIP()
        return ip

    #更新读取到的url,id位置
    def update_nextid(self, nextid):

        self.info_db.addNextTeacherID( nextid )

    def judge_info(self):
        nextid = self.info_db.readData()
        if nextid:
            return nextid[0][0]
        else:
            print 'no data'


    #判断剩余代理是否大于0,如果为0,退出,否则返回所剩代理ip数量
    def judge_ifProxyIP(self):
        ip = self.read_proxyip()

        if len(ip) == 0:
            print 'proxy 0 can available ,please wite 200 sencord .. .. '
            self.Database.close()
            self.DBC.close()
            return 0
            #exit()
        else:
            print '======> now available ip:',len(ip)
            return ip

    #获取id为n的代理ip地址,循环调用ip地址的使用
    def nextipid(self, id):
        return self.Database.readDataOKIP(id)

    def compiledata(self, html, key):
        pattern_1 = re.compile(r'link-person\\"\\u003e\\u003c/i\\u003e(.*?)\(.*?link-mobile\\\s*"\\u003e\\u003c/i\\u003e(.*?)\\u003cbr.*?link-qq\\"\\u003e\\u003c/i\\u003e(.*?)\\u003cbr.*?link-email\\"\\u003e\\u003c/i\\u003e(.*?)\\u.*?\s.*?link-weixin\\"\\u003e\\u003c/i\\u003e(.*?)\\u',re.S)
        pattern_2 = re.compile(r'link-mobile\\"\\u003e\\u003c/i\\u003e(.*?)\\u003cbr.*?link-qq\\"\\u003e\\u003c/i\\u003e(.*?)\\u.*?link-weixin\\"\\u003e\\u003c/i\\u003e(.*?)\\u')
        items1 = re.findall(pattern_1,html)
        items2 = re.findall(pattern_2,html)
        #print items,items1
        if items1:
            print '== TName:'+items1[0][0]+'  TPhone:'+items1[0][1]+'  TQQ:'+items1[0][2]+'  TEmail:'+items1[0][3]+'  TWeChat:'+items1[0][4]
            if items2[1]:
                print '== APhone:'+items2[1][0]+'  AQQ:'+items2[1][1]+'  AWeChat:'+items2[1][2]
                self.info_db.updateData(key,items1[0][0],items1[0][1],items1[0][2],items1[0][3],items1[0][4],items2[1][0],items2[1][1],items2[1][2])
            else:
                self.info_db.updateData(key,items1[0][0],items1[0][1],items1[0][2],items1[0][3],items1[0][4],'','','')
            return True
        else:
            #print 'this url not have data'
            return False

    #爬虫调用总函数
    def http_proxy(self ,proxyip):

        #获取下次要读取的id值,如果不存在设置此值为1
        if self.judge_info() == None:
            #self.DBC.addNextTeacherID( 2 )
            nextid = 1
        else:
            nextid = self.judge_info()
        print '===>  next find the id :',nextid

        for nnn in range(50):
            if nextid == 6000:
                break
            if nextid == nnn*200:
                print 'now sleep 30 minite'
                time.sleep(1200)

        #获取此次要爬取的url
        next_value = self.info_db.readDataKey(nextid)
        for value in next_value:
            key = value[0]
        print 'next the key:',key

        #enable_proxy = True
        #proxy_handler = urllib2.ProxyHandler({"http" : 'http://some-proxy.com:8080'})
        flag,html = HttpTransport.post_proxy(proxyip, key)

        if flag == 'ok':
            judge_lock = re.search('list-style-type:none;">',html)
            if judge_lock:
                self.proxyip_db.updateData(0, proxyip)
                print '////// proxy ip is lock /////////'
                logging.info('////// proxy ip is lock /////////')
                return 'fail'
            else:
                xx = self.compiledata(html, key)
                logging.info(html)
                if xx:
                    self.info_db.updateNextTeacherID(nextid+1)
                else:
                    print 'problem :',html
                    return 'fail'
        elif flag == 'fail':
            #self.proxyip_db.delData(proxyip)
            self.proxyip_db.delData(proxyip)
            return 'fail'


    def recontent(self, html, url):
        pattern = re.compile('class="logo-ps-name">(.*?)</a>',re.S)
        pattern1 = re.compile('<i class="link-icon link-mobile"></i>(.*?)<br />\s*<i class="link-icon link-qq"></i>(.*?)<br />\s*<i class="link-icon link-email"></i>(.*?)<br />\s*<i class="link-icon link-weixin"></i>(.*?)<br />.*?<i class="link-icon link-mobile"></i>(.*?)<br />\s*<i class="link-icon link-qq"></i>(.*?)<br />\s*<i class="link-icon link-weixin"></i>(.*?)<br />',re.S)
        #items = re.findall(pattern,html)
        items = re.findall(pattern,html)
        items1 = re.findall(pattern1,html)
        #print items,items1
        if items:
            print '== TName:'+items[0]+'  TPhone:'+items1[0][0]+'  TQQ:'+items1[0][1]+'  TEmail:'+items1[0][2]+'  TWeChat:'+items1[0][3]
            print '== APhone:'+items1[0][4]+'  AQQ:'+items1[0][5]+'  AWeChat:'+items1[0][6]
            self.DBC.updateData(url,items[0],items1[0][0],items1[0][1],items1[0][2],items1[0][3],items1[0][4],items1[0][5],items1[0][6])
        else:
            print 'this url not have data'

def main():
    crawler = Crawler()
    ip = crawler.read_proxyip()
    while 1:
        for x in range(len(ip)-1):
            print '===== now ip is ',ip[x][0],'  ipnum:',x
            for n in range(15):
                flag = crawler.http_proxy(ip[x][0])
                time.sleep(2)
                if flag == 'fail':
                    break

        ip = crawler.read_proxyip()
        print 'get ip num :',len(ip)
        if len(ip) < 2:
            print 'ip num et 2,please wait 5 minute'
            time.sleep(300)

if __name__ == '__main__':
    #main()
    #crawler = Crawler()
    #crawler.read_proxyip()
    #crawler.judge_info()
    main()