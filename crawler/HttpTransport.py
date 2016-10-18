#coding:utf8
import cookielib
import Cookie
import urllib2
import urllib

import time
import re

def build_opener_with_cookie_str(cookie_str, domain, path='/'):
    simple_cookie = Cookie.SimpleCookie(cookie_str)    # Parse Cookie from str
    cookiejar = cookielib.CookieJar()    # No cookies stored yet

    for c in simple_cookie:
        cookie_item = cookielib.Cookie(
            version=0, name=c, value=str(simple_cookie[c].value),
                     port=None, port_specified=None,
                     domain=domain, domain_specified=None, domain_initial_dot=None,
                     path=path, path_specified=None,
                     secure=None,
                     expires=None,
                     discard=None,
                     comment=None,
                     comment_url=None,
                     rest=None,
                     rfc2109=False,
            )
        cookiejar.set_cookie(cookie_item)    # Apply each cookie_item to cookiejar
    return urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))    # Return opener

def post():
    #cookie_str = 'js_clientid=54cc4e18-983f-4260-828c-9d01861c6490;Hm_lvt_ff5146bd3e0db147ced120c6c2c9bcb2=1469672173;Hm_lpvt_ff5146bd3e0db147ced120c6c2c9bcb2=1469694067;ASP.NET_SessionId=mjjmo0koc3woq0xvaoq5cnii;js.userName=7DFB410B7FD820DC0231003100330038003900330038000000460CEBFAA8E8D10101464CCF2329EED10100002F0000005BBB4B92631C0A1A2CE2A09F3E429DE5406D554A'
    cookie_str = 'js_clientid=b23c4184-7479-4779-b457-caea66fdf027;ASP.NET_SessionId=vwvijvgsgvaxokpxexwnjbkz;uaid=68bec0a5e2168980fcb913b97c3d585a;Hm_lvt_ff5146bd3e0db147ced120c6c2c9bcb2=1470194822;Hm_lpvt_ff5146bd3e0db147ced120c6c2c9bcb2=1470194976;js.userName=5FD3BF3365D1A50002310031003700390039003600300000000B48334237EDD101010B88176BB7F2D10100002F00000052E914236DBA32454971A1DC81D624BA405984DA'
    #ip = '120.25.171.183:8080'
    #proxy_handler = urllib2.ProxyHandler({'http':ip})
    #opener = urllib2.build_opener(proxy_handler)
    url = 'http://www.jiangshi.org/space/space_lectview_submit'
    opener = build_opener_with_cookie_str(cookie_str, domain='www.jiangshi.org')
    values = {'lectuserid':'523562','position':'2'}
    data = urllib.urlencode(values)
    print data
    req = urllib2.Request(url, data)
    #response = urllib2.urlopen(req)
    response = opener.open(req)
    the_page = response.read().decode('utf-8')
    #print the_page
    judge_lock = re.search('list-style-type:none;">',the_page)

    print the_page
    pattern_1 = re.compile(r'link-mobile\\"\\u003e\\u003c/i\\u003e(.*?)\\u003cbr.*?link-qq\\"\\u003e\\u003c/i\\u003e(.*?)\\u.*?link-weixin\\"\\u003e\\u003c/i\\u003e(.*?)\\u',re.S)
    #pattern_2 = re.compile(r'\([\u4e00-\u9fa5]{4}\)\\u003cbr\s/\\u003e\\r\\n\s*\\u003ci\sclass=\\"link-icon\slink-mobile\\"\\u003e\\u003c/i\\u003e(.*?)\\u003cbr.*?link-qq\\"\\u003e\\u003c/i\\u003e(.*?)\\u.*?link-weixin\\"\\u003e\\u003c/i\\u003e(.*?)\\u')
    items1 = re.findall(pattern_1,the_page)
    #items2 = re.findall(pattern_2,the_page)
    print items1[1]
    if items1[1]:
        print 'have the assistant the information'
    else:
        print 'dont have aasistant data'
    
    
    #print items2
    if judge_lock:
        print 'now ip is lock ... wait some times ...'
    else:
        print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

def post_proxy(ip, key):
    #cookie_str = 'js_clientid=54cc4e18-983f-4260-828c-9d01861c6490;Hm_lvt_ff5146bd3e0db147ced120c6c2c9bcb2=1469672173;Hm_lpvt_ff5146bd3e0db147ced120c6c2c9bcb2=1469694067;ASP.NET_SessionId=mjjmo0koc3woq0xvaoq5cnii;js.userName=7DFB410B7FD820DC0231003100330038003900330038000000460CEBFAA8E8D10101464CCF2329EED10100002F0000005BBB4B92631C0A1A2CE2A09F3E429DE5406D554A'
    #cookie_str = 'js_clientid=b23c4184-7479-4779-b457-caea66fdf027;ASP.NET_SessionId=vwvijvgsgvaxokpxexwnjbkz;uaid=68bec0a5e2168980fcb913b97c3d585a;Hm_lvt_ff5146bd3e0db147ced120c6c2c9bcb2=1470194822;Hm_lpvt_ff5146bd3e0db147ced120c6c2c9bcb2=1470194976;js.userName=5FD3BF3365D1A50002310031003700390039003600300000000B48334237EDD101010B88176BB7F2D10100002F00000052E914236DBA32454971A1DC81D624BA405984DA'
    cookie_str = 'js_clientid=b23c4184-7479-4779-b457-caea66fdf027;ASP.NET_SessionId=vwvijvgsgvaxokpxexwnjbkz;uaid=68bec0a5e2168980fcb913b97c3d585a;js.userName=5FD3BF3365D1A50002310031003700390039003600300000000B48334237EDD101010B88176BB7F2D10100002F00000052E914236DBA32454971A1DC81D624BA405984DA'
    #url = 'http://www.jiangshi.org/space/space_lectview_submit'
    #ip = '210.72.14.142:80'
    proxy_handler = urllib2.ProxyHandler({'http':ip})
    opener = urllib2.build_opener(proxy_handler)
    url = 'http://www.jiangshi.org/space/space_lectview_submit'
    #url = 'http://www.jiangshi.org'
    opener = build_opener_with_cookie_str(cookie_str, domain='www.jiangshi.org')
    #proxy_handler = urllib2.ProxyHandler({'http':ip})
    #values = {'lectuserid':'1173372','position':'2'}
    #values = {'lectuserid':key,'position':'2'}
    values = {'position':'2','lectuserid':key}
    data = urllib.urlencode(values)
    #print data
    #头部
    #user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    #user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
    #headers = {'Host':'www.jiangshi.org','Referer':'http://www.jiangshi.org/'+key+'/contact.html','User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1'}
    #headers = {'Host':'www.jiangshi.org','User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1','Accept':'*/*','Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3','Accept-Encoding':'gzip, deflate','DNT':'1','Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','X-Request-With':'XMLHttpRequest','Referer':'http://www.jiangshi.org/'+key+'/contact.html','Content-Length':'28','Connection':'keep-alive'}
    #headers = { 'User-Agent' : user_agent }

    #req = urllib2.Request(url, data, headers)
    req = urllib2.Request(url, data)
    #response = urllib2.urlopen(req)
    try:
        response = opener.open(req, timeout=10)
        the_page = response.read().decode('utf-8')
        #the_page = response.read()
        #print the_page
        return 'ok',the_page
    except Exception,e:
        print Exception,":",e
        return 'fail',e
    #print the_page

def geturl():
    cookie_str = 'js_clientid=54cc4e18-983f-4260-828c-9d01861c6490;Hm_lvt_ff5146bd3e0db147ced120c6c2c9bcb2=1469672173;Hm_lpvt_ff5146bd3e0db147ced120c6c2c9bcb2=1469694067;ASP.NET_SessionId=mjjmo0koc3woq0xvaoq5cnii;js.userName=7DFB410B7FD820DC0231003100330038003900330038000000460CEBFAA8E8D10101464CCF2329EED10100002F0000005BBB4B92631C0A1A2CE2A09F3E429DE5406D554A'
    url = 'http://www.jiangshi.org/home'
    opener = build_opener_with_cookie_str(cookie_str, domain='www.jiangshi.org')
    html_doc = opener.open('http://www.jiangshi.org/home').read()
    print html_doc
    #import re
    #print 'Open With Cookie:', re.search('<title>(.*?)</title>', html_doc, re.IGNORECASE).group(1)

    #html_doc = urllib2.urlopen('http://192.168.1.253').read()
    #print 'Open Without Cookie:', re.search('<title>(.*?)</title>', html_doc, re.IGNORECASE).group(1)

def proxy_tarns():
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
        nextid = nextid + 1
        print nextid
        self.DBC.updateNextTeacherID( nextid )
    except Exception,e:
        print Exception,":",e
        print "timeout the ProxyIp is not work"
        self.Database.updateDataOK(0, ip)
        num_ip = num_ip + 1
        self.http_proxy()

if __name__ == '__main__':
    #geturl()
    #post_proxy('117.239.20.24:8080','1090155')
    #while True:
    post()
    time.sleep(1)