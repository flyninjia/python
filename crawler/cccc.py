#coding:utf8

import urllib2
import re

import random
import sqlite3

import json
import database
#import requests
import proxy

num = 0
num_ip = 1
changeIP = False


class Crawler(object):

    #def __init__(self, url):
    def __init__(self):
        #设定爬取翻页页面到url
        self.pageUrl = "http://www.baidu.com/page/"
        self.Database = database.DatabaseProxyIp()
        self.DBC = database.Database_capture()
        #self.url = ''
        #self.url = url
        #

    def readNullUrl(self):
        values = self.DBC.readData_Null()
        #print values
        for value in values:
            print value[1]

    def readNullUrl_s(self):
        values = self.DBC.readData_Null()
        for value in values:
            print 'next find the url:',value[2]
            self.http_proxy(value[1])

    #判断剩余代理是否大于0,如果为0,退出,否则返回所剩代理ip数量
    def judge_ifProxyIP(self):
        ip = self.Database.readDataOK(1)

        if len(ip) == 0:
            print 'proxy 0 can available ,please anew get ip'
            self.Database.close()
            self.DBC.close()
            return True
            #exit()
        else:
            print '======> now available ip:',len(ip)
            return len(ip)

    #获取id为n的代理ip地址,循环调用ip地址的使用
    def nextipid(self,id):
        return self.Database.readDataOKIP(id)

    #爬虫调用总函数
    def http_proxy(self,url):

        #获取目前存活可使用代理ip数量,并输出
        count_ip = self.judge_ifProxyIP()


        #values_cate = cursor.fetchall()
        #调用全局变量,设置限定调用ip次数num为11次,num_ip为要使用代理ip  id
        global changeIP
        global num
        global num_ip


        #判断是否更改ip,如果更改,重新赋值调用次数num为0,调高num_ip + 1
        if changeIP:
            num = 0
            changeIP = False
            num_ip = num_ip + 1
        #否则增加一次此ip使用次数
        else:
            num = num + 1

        #提前判断,当前要获取到num_ip大于代理ip个数，大于则重新赋值为1
        ProxyIp = self.Database.readDataOK('*')
        if num_ip >= len(ProxyIp)-1:
            num_ip = 1

        #判断此ip是否存活状态,存活则跳出循环赋值到ip,否则继续读取下一条ip
        #在判断代理ip是否可用的try: except: 语句中增加判断条件
        #根据跳出错误条件判断代理是否可以继续使用
        while 1:
            nextip = self.nextipid(num_ip)
            #print 'now ip id:',nextip[0][1]
            if nextip[0][1] == 0:
                num_ip = num_ip + 1
            else:
                print "now ip id :",num_ip
                ip = nextip[0][2]
                break

        #代理ip使用11次后,设定更改changeIP为真,下次更改ip
        if num == 11:
            changeIP = True
        print 'count num:',num

        #ProxyIp = self.Database.readDataOK('*')

        #print ProxyIp
        #ip = ProxyIp[num_ip][0]

        print 'now ip:',ip

        enable_proxy = True
        #proxy_handler = urllib2.ProxyHandler({"http" : 'http://some-proxy.com:8080'})
        proxy_handler = urllib2.ProxyHandler({'http':ip})
        null_proxy_handler = urllib2.ProxyHandler({})
        if enable_proxy:
            opener = urllib2.build_opener(proxy_handler)
        else:
            opener = urllib2.build_opener(null_proxy_handler)
            #urllib2.install_opener(opener)

        try:
            response = opener.open(url,timeout=8)
            self.recontent(response.read().decode('utf-8'),url)
            #nextid = nextid + 1
            #print nextid
            #self.DBC.updateNextTeacherID( nextid )
        except Exception,e:
            print Exception,":",e
            print "timeout the ProxyIp is not work"
            self.Database.updateDataOK(0, ip)
            num_ip = num_ip + 1
            self.http_proxy(url)

        #cursor.close()
        #conn.close()

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
            #print html
            pattern_lock = re.compile('document.getElementById',re.S)
            item_lock = re.findall(pattern_lock,html)
            if item_lock:
                print '/////////////url lock////////////////'
                self.DBC.updateData(url,u'用户被锁定','','','','','','','')

            else:
                print '=====this url not have data======'

def main():
    try:
        f = open('sitemap_lect_1.xml','r')
        for line in f.readlines():
        #print(line.strip())
            m = re.match(r'^<loc>(.*)</loc>$',line.strip())
        #m = re.search(r'<loc>.*',line.strip())
            if m:
            #print "yse"
                contact = re.search(r'contact.html',m.group(1))
                if contact:
                    print m.group(1)
                    #getUrl(m.group(1))
                    http_proxy(m.group(1))
                    #m.group()
    finally:
        if f:
            f.close()


test = Crawler()
test.readNullUrl_s()
#test.readNullUrl()

