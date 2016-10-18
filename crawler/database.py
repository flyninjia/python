#coding:utf8

"""
database.py
~~~~~~~~~~~~~

该模块提供爬虫所需的sqlite数据库的创建、连接、断开，以及数据的存储功能。
"""

import sqlite3

class Database(object):
    def __init__(self, dbFile):
        try:
            self.conn = sqlite3.connect(dbFile, isolation_level=None, check_same_thread = False) #让它自动commit，效率也有所提升. 多线程共用
            self.conn.execute('''CREATE TABLE IF NOT EXISTS
                            Webpage (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            url TEXT, 
                            pageSource TEXT,
                            keyword TEXT)''')
        except Exception, e:
            self.conn = None

    def isConn(self):
        if self.conn:
            return True
        else:
            return False

    def saveData(self, url, pageSource, keyword=''):
        if self.conn:
            sql='''INSERT INTO Webpage (url, pageSource, keyword) VALUES (?, ?, ?);'''
            self.conn.execute(sql, (url, pageSource, keyword) )
        else :
            raise sqlite3.OperationalError,'Database is not connected. Can not save Data!'

    def close(self):
        if self.conn:
            self.conn.close()
        else :
            raise sqlite3.OperationalError, 'Database is not connected.'

class DatabaseProxyIp(object):
    #调用类时自动即执行,连接HttpProxyIP.db,如果表ProxyIp没有创建则创建
    def __init__(self):
        #try: except: 是首先执行try:后语句,抛出错误时执行except后语句
        try:
            self.conn = sqlite3.connect('proxyip.db', isolation_level=None, check_same_thread = False)
            self.conn.execute('''CREATE TABLE IF NOT EXISTS ProxyIp(
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             available int(2),
                             ip VARCHAR(100),
                             addtime VARCHAR(50)) ''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS endtime(
                             endtime VARCHAR(50)) ''')
        except Exception, e:
            print e
            self.conn = None

    #判断是否连接数据库
    def isConn(self):
        if self.conn:
            return True
        else:
            return False

    #保存数据
    def saveData(self, available, ip, addtime):
        if self.conn:
            sql = '''INSERT INTO ProxyIp (available, ip, addtime) VALUES (?, ?, ?);'''
            self.conn.execute(sql, (available, ip, addtime) )
        else:
            raise sqlite3.OperationalError,'Database is not connected. not save data!'
    #保存数据到proxyipok表中
    def saveDatatime(self, endtime ):
        if self.conn:
            sql = '''INSERT INTO endtime (endtime) VALUES (?);'''
            self.conn.execute(sql, (endtime,) )
        else:
            raise sqlite3.OperationalError,'Database is not connected. not save data!'

    #delete data from proxyip tables
    def delData(self, ip):
        if self.conn:
            sql = '''DELETE FROM ProxyIp WHERE ip = ?'''
            self.conn.execute(sql, (ip,))
        else:
            raise sqlite3.OperationalError,'Database is not connected.not delData'
    #更新数据
    def updateData(self, available, ip):
        if self.conn:
            sql = '''UPDATE ProxyIp SET available = ? WHERE ip = ?;'''
            self.conn.execute(sql, (available, ip))
        else:
            raise sqlite3.OperationalError,'Database is not connected. not save data!'
    def updateendtime(self, endtime):
        if self.conn:
            sql = '''UPDATE endtime SET endtime = ?'''
            self.conn.execute(sql, (endtime,))
        else:
            raise sqlite3.OperationalError,'Database is not connected. not save data!'
    #读取数据
    def readData(self):
        if self.conn:
            return self.conn.execute("SELECT ip from ProxyIp")
        else:
            raise sqlite3.OperationalError,'Database is not connected. not save data!'
    #读取最后获取的验证ip时间
    def readendtime(self):
        if self.conn:
            return self.conn.execute("SELECT endtime from endtime").fetchall()
        else:
            raise sqlite3.OperationalError,'Database is not connected. not save data!'
    #获取id为 n的ip,记录ip防止重复使用
    def readDataOKIP(self):
        if self.conn:
            #sql = '''SELECT ip from ProxyIp where available = 1;'''
            #return self.conn.execute(sql, (id, )).fetchall()
            return self.conn.execute("SELECT ip from ProxyIp where available = 1").fetchall()
        else:
            raise sqlite3.OperationalError,'Database is not connected. not save data!'


    #关闭数据库
    def close(self):
        if self.conn:
            self.conn.close()
        else:
            raise sqlite3.OperationalError, 'Database is not connectd .'

class Database_capture(object):
    #调用类时自动即执行,连接HttpProxyIP.db,如果表ProxyIp没有创建则创建
    def __init__(self):
        #try: except: 是首先执行try:后语句,抛出错误时执行except后语句
        try:
            self.conn = sqlite3.connect('Crawler.db', isolation_level=None, check_same_thread = False)
            self.conn.execute('''CREATE TABLE IF NOT EXISTS information (
                             id INTEGER PRIMARY KEY AUTOINCREMENT ,
                             url text,
                             key text,
                             TName text,
                             TPhone text,
                             TQQ text,
                             TEmail text,
                             TWeChat text,
                             APhone text,
                             AQQ text,
                             AWeChat text )''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS NextTeacher
                             (nextid int(10) )''')

        except Exception, e:
            print e
            self.conn = None

    #判断是否连接数据库
    def isConn(self):
        if self.conn:
            return True
        else:
            return False

    #保存数据
    def saveData(self, url, TName, TPhone, TQQ, TEmail, TWeChat, APhone, AQQ, AWeChat):
        if self.conn:
            sql='''INSERT INTO information (url, TName, TPhone, TQQ, TEmail, TWeChat, APhone, AQQ, AWeChat) VALUES (?,?,?,?,?,?,?,?,?)'''
            self.conn.execute(sql, (url, TName, TPhone, TQQ, TEmail, TWeChat, APhone, AQQ, AWeChat) )
        else:
            raise sqlite3.OperationalError,'Database is not connected. not save data!'

    #首先保存url到
    def saveDataUrl(self, url, key):
        if self.conn:
            sql='''INSERT INTO information (url,key) VALUES (?,?)'''
            self.conn.execute(sql, (url,key) )
        else:
            raise sqlite3.OperationalError,'Database is not connected. not save data!'

    #更新数据
    def updateData(self, key, TName, TPhone, TQQ, TEmail, TWeChat, APhone, AQQ, AWeChat):
        if self.conn:
            sql = '''UPDATE information SET TName = ?, TPhone = ?, TQQ = ?, TEmail = ?, TWeChat = ?, APhone = ?, AQQ = ?, AWeChat = ? WHERE key = ?;'''
            self.conn.execute(sql, (TName, TPhone, TQQ, TEmail, TWeChat, APhone, AQQ, AWeChat, key) )
        else:
            raise sqlite3.OperationalError,'Database is not connected. not save data!'
    def addNextTeacherID(self, nextid):
        if self.conn:
            sql='''INSERT INTO NextTeacher (nextid) VALUES (?);'''
            self.conn.execute(sql, (nextid,) )
        else :
            raise sqlite3.OperationalError,'Database is not connected. Can not save Data!'


    def updateNextTeacherID(self, nextid):
        if self.conn:
            sql = '''UPDATE NextTeacher SET nextid = ?;'''
            print nextid
            self.conn.execute(sql, (nextid,))
            #self.conn.execute('update NextTeacher set nextid =?', ('1' ))
            #selconn.execute((UPDATE NextTeacher SET nextid = ?), (nextid,))
        else:
            raise sqlite3.OperationalError,'Database is not connected. not save data!'
    #读取下次要获取网址的url
    def readDataKey(self, nextid):
        if self.conn:
            sql = '''SELECT key from information where id = ?;'''
            return self.conn.execute(sql, (nextid,))
        else:
            raise sqlite3.OperationalError,'Database is not connected. not save data!'

    #读取数据
    def readData(self):
        if self.conn:
            return self.conn.execute("SELECT nextid from NextTeacher").fetchall()
        else:
            raise sqlite3.OperationalError,'Database is not connected. not save data!'
    #读取没有读取到的数据的列表
    def readData_Null(self):
        if self.conn:
            return self.conn.execute("SELECT * from information where TName is null ").fetchall()
        else:
            raise sqlite3.OperationalError,'Database is not connected. not save data!'

    #关闭数据库
    def close(self):
        if self.conn:
            self.conn.close()
        else:
            raise sqlite3.OperationalError, 'Database is not connectd .'