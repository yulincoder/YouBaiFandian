# -*- coding: utf-8 -*-

# Copyright (c) 2016, Zhang Te
# All rights reserved.


import os
import json

def load(location,option = True):
    return mousedb(location, option)

class mousedb:
    
    def __init__(self,location,option = True):
        ''' Creates a database object with the location.If the file dose not exist
        it will be created on the frist update.If the option is True then the file 
        will be stored disk ,else it is still stay in memory.
        --------------------------------------------------------------------------
        根据输入的路径实例化一个数据库对象，如果路径不存在则在第一次实例化时新建文件
        否则只是打开文件。option参数如果是True则任何查询与更新数据都会发生一次磁盘数据读写
        (多个应用同时使用一个数据库可以保持应用之间数据的实时同步)，

        False则存储于数据只有在更新数据时发生一次磁盘读写，将数据存储与磁盘。        
        '''
        self.loco = location
        self.fsave = option
        self.abs_location = os.path.abspath(location)     
        self.KEY_VALUE = 0
        self.items = None
        
        if os.path.exists(self.abs_location):
            self._loaddb()
        else:   
            self.db = {}
            self.db[u'items'] = None       
            self._dumpdb()
        
    
    
    def createtable(self,items):
        ''' Create a table in database object,and a object will support only one table.
            The 0 of index in items is the key value.
        -------------------------------------------------------------------------------
            在一个数据库对象中建立一张表，并且一个对象管理只能是一张表。其中items第一个
            元素为主键条目。
        '''
        self.items = items
        self.db[u'items'] = items       #items is a tuple.
        self.db[items[self.KEY_VALUE]] = {}
        self._dumpdb()
        
    

    def intable(self,key):
    	if self.fsave:
        	self._loaddb()

        if key in self.db[self.items[self.KEY_VALUE]]:
            return True
        else:
            return False


        
    def insertrow(self,data):
        ''' Insetr a row data into table.And data is a tuple.
        ---------------------------------
            向表中插入一行数据,data是一个元组。
        '''
        if self.fsave:
        	self._loaddb()

        row = dict(zip(self.items[1:],data[1:]))
        self.db[self.items[self.KEY_VALUE]][data[0]] = row
        self._dumpdb()
        
        
        
    def update(self,key,item,value):
        ''' Update a value of the special key and item.
        ------------------------------------------------
            根据主键和索引更新数据。
        '''
        if self.fsave:
        	self._loaddb()

        if key in self.db[self.items[self.KEY_VALUE]]:
            #curr = self.db[self.items[self.KEY_VALUE]][key]
            if item in self.db[self.items[self.KEY_VALUE]][key]:
                self.db[self.items[self.KEY_VALUE]][key][item] = value
                self._dumpdb()
                return True
        return False
        
        
        
    def delrow(self,key):
        ''' Delete a row.
        -----------------
            删除一行。
        '''
        if self.fsave:
        	self._loaddb()

        if self.db[self.items[self.KEY_VALUE]].has_key(key): 
            self.db[self.items[self.KEY_VALUE]].pop(key)
            self._dumpdb()
            

    
    def findrow(self,key):
        ''' Find the special row.
        -------------------------
            查找指定行。
        '''
        if self.fsave:
        	self._loaddb()

        if key in self.db[self.items[self.KEY_VALUE]]:
            return {key:self.db[self.items[self.KEY_VALUE]][key]}

            
            
            
    def findvalue(self,key,item):
        ''' Find a value reply on key and item.
        ---------------------------------------
            根据主键值和表项查找值
        '''
        if self.fsave:
        	self._loaddb()

        if key in self.db[self.items[self.KEY_VALUE]] and item in self.db[self.items[self.KEY_VALUE]][key]:
            return self.db[self.items[self.KEY_VALUE]][key][item]
            
    



    def get_items(self):    # 返回所有主键值
        keys = []

        if self.fsave:
        	self._loaddb()

        date = self.db[self.items[self.KEY_VALUE]]

        for each in date:
            keys.append(each)

        return keys

                
        
    def printtable(self):
        ''' Print database with json fromat.
        ------------------------------------
            打印表。
        '''
        if self.fsave:
        	self._loaddb()

        if self.fsave:
            with open(self.abs_location,'r') as f:
                data = json.loads(f.read())
                print (data)
        
        
        
    def _loaddb(self):
        ''' Load or reload the json info from the file. 
        ----------------------------------------------
            从文件中以加载数据到内存中，并将json格式数据
            进行解析。
        '''
        with open(self.abs_location,'r') as f:    
            self.db = json.loads(f.read())
            self.items = self.db['items']

    
    
    def _dumpdb(self):
        ''' Write/save reload the json dump into the file.
        --------------------------------------------------
            将数据库数据生成json格式并存入磁盘文件。
        '''
        with open(self.abs_location, 'w') as f:
            f.write(json.dumps(self.db,ensure_ascii=True))
