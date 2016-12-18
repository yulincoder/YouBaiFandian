# -*- coding: utf-8 -*-
'''
@brief 只能英->汉
'''
import urllib2
import os
import random
import re
import json

import httplib
import md5
import urllib
import color

import mousedb


#from demo import *

def url_open(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36')
    try:
    	response = urllib2.urlopen(req)
    	html = response.read()
    	return html
    except Exception, e:
        print 'error: No connected to Internet.'
        return ''



def get_result_word(word):
    content =  url_open('http://dict.youdao.com/w/eng/' + word + '/#keyfrom=dict2.index')

    content = content.replace(' ', '') # 去掉所有空格
    content = content.replace('\n', '') # 去掉所有换行
    content = content.replace('\t', '') # 去掉所有制表符
    content = content.replace('\t', '') # 去掉所有制表符

    result_string = re.findall('"trans-container"><ul><li>(.*?)</li></ul>', content)
    ''' 音标功能有问题，日后再加S
    pronounce = re.findall('<spanclass="pronounce">英<spanclass="phonetic">(.*?)</span><ahref="#"title="真人发音"\
class="spdictvoicevoice-jslog-js"data-rel="hello&type=1"data-4log="dict.basic.ec.uk.voice"></a></span><spanclass\
="pronounce">美<spanclass="phonetic">(.*?)</span>', content)
    '''
    
    if result_string != []:
        result_string[0] = result_string[0].replace('</li>', '')
        result_string[0] = result_string[0].replace('<li>', '\n      ')
        return result_string[0]
    else:
    	return '...'



def get_result_sentence(sentence = 'hello, word'):
    appid = '20161213000033948'
    secretKey = 'lWJS35DTzSvPFT8shGue'

     
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = sentence
    fromLang = 'en'
    toLang = 'zh'
    salt = random.randint(32768, 65536)

    sign = appid+q+str(salt)+secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    
    result = ''
    try:
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
     
        #response是HTTPResponse对象
        response = httpClient.getresponse()

        info_from_baidu = json.loads(response.read())
        
        result =  info_from_baidu[u'trans_result'][0][u'dst']

        if sentence == result:		#翻译结果与查询的句子一致，则是胡乱输入的一个句子
        	result = '...'
    except Exception, e:
        print 'error: No connected to Internet.'
        result = '...'
    finally:
        if httpClient:
            httpClient.close()

        return result



def db_update(db, word, interpert):       # 向数据库更新查词的数据
    items = db.get_items()                # 这个可以优化，设置成全局变量就不用每次都从数据库取键值集合了
    
    if word in items:
        count = db.findvalue(word, 'Counter')
        db.update(word, 'Counter', count + 1)
    else:
        db.insertrow((word, interpert, 1))



def print_db(db):           # 打印历史记录详细信息
    items = db.get_items()
    tmp_for_sort = {}       # 新dict用来排序之用   = item
    
    for item in items:
        index = db.findvalue(item, 'Counter')
        if index not in tmp_for_sort:           # 统计次数一样不同的单词放在一个list里面
            tmp_for_sort[index] = [item]
        else:
            tmp_for_sort[index].append(item)

    sorted_count = sorted(tmp_for_sort)         # 对统计的次数进行排序
    for each in sorted_count:                   # 根据排序输出查询历史记录
        
        for item in tmp_for_sort[each]:         # 统计次数一样的不同单词都在list里面
            print '>>>   ' +  item ,            # 输出单词
            clr_control.set_print_red_text()
            print '\t[' + str(db.findvalue(item, 'Counter')) + ']'   # 输出单词历史查询次数
            clr_control.set_print_yellow_text()         # 黄色输出
            print '...  ',
            print db.findvalue(item, 'interpert').decode('utf-8').encode('gbk')   # 输出解释
            clr_control.set_print_green_text()  	# 输出还原为绿色
            print ''
                

def print_summary_db(db, amount_word_a_row = 3):                       # 打印历史记录简单信息
        items = db.get_items()
        tmp_for_sort = {}       # 新dict用来排序之用   
        row_cnt = 0             # 输出行数计数
        words_cnt = 0           # 输出单词个数计数
        
        for item in items:      # 按照历史查询频率对单词分类
            index = db.findvalue(item, 'Counter')
            if index not in tmp_for_sort:
                    tmp_for_sort[index] = [item]        # 将字典的键设置为查询次数，值设置为单词本身，这样可以用sorted函数根据历史查询次数对单词排序
            else:
                    tmp_for_sort[index].append(item)


        sorted_count = sorted(tmp_for_sort)             # 对统计的次数进行排序
        
        clr_control.set_print_gray_text()               # 灰(hui)色输出
        print '%-5s\t' % (str(1) + ':'),
        clr_control.set_print_yellow_text()             # 黄色输出
        for each in sorted_count:                       # 根据排序输出查询历史记录
                
            for word in tmp_for_sort[each]:             # 统计次数一样的不同单词都在list里面
                
                    clr_control.set_print_red_text()
                    print '%6s' % ('[' + str(db.findvalue(word, 'Counter')) + ']'),   # 历史查询频率显示
                    clr_control.set_print_yellow_text() if row_cnt % 2 == 0 else clr_control.set_print_green_text()
                    
                    print  '%-15s' % (word),       # 输出单词
                    words_cnt += 1
                   
                    if words_cnt % amount_word_a_row == 0:         # 换行处理及与换行有关的颜色处理
                        row_cnt += 1
                        clr_control.set_print_gray_text()               # 灰(hui)色输出
                        print '\n\n%-5s\t' % (str(row_cnt+1) + ':'),   
                        if row_cnt % 2 == 0:
                            clr_control.set_print_yellow_text()  	# 黄色输出
                        else:
                            clr_control.set_print_green_text()          # 输出为绿色


        clr_control.set_print_green_text()  	# 输出还原为绿色


def rm_word_from_db(db, word):   # 从数据库删除元素
        db.delrow(word)
    
                        



        


if __name__ == '__main__':
	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')  # 设置默认编码为utf-8
	
	db = mousedb.load('YouBai.db', True) # 连接数据库，数据库不存在会自己建立

        # 建立一张表，建立就完注释掉
	#db.createtable(('Word', 'interpert', 'Counter'))

        launch_gui_msg = '\n\n\n\n\n				有百翻典\n\n\
                 只能查询从英语 -> 汉语，不能 从汉语 -> 英语\n\n\
                           句子翻译来自百度翻译\n\
		           单词查询来自有道词典\n\n\
			  行行无别语，只道早还乡！'.decode('utf-8').encode('gbk')
	
	

	help_msg =  '命令 -- <:q> or <:Q> 退出\n\
		<:h> or <:H> 帮助信息\n\
		<:c> or <:C> 清空屏幕\n\
		<:his> 历史信息  <-s> 历史信息概要 <-xx> 一行展示单词数量(默认为3)\n\
		<:rm xxx> 删除一条历史记录 \n\n'.decode('utf-8').encode('gbk')
	
	topbar_msg = 'YouBai [0.0.0.1] \nType ":q", ":c", ":h" or ":his" for more information.'.decode('utf-8').encode('gbk')

	clr_control = color.Color()	    # 控制台颜色控制
	clr_control.set_print_green_text()  # 初始化输出为绿色

	import os
	os.system("cls")
	print launch_gui_msg,
	raw_input()
	os.system("cls")


	print topbar_msg
	while True:
		needs = raw_input('>>>   '.decode('utf-8').encode('gbk'))

		if needs == ':q' or needs == ':Q':		# 退出
			break
		if needs == ':h' or needs == ':H':		# 帮助
			print help_msg
			continue

		if needs == ':c' or needs == ':C':		# 清屏
			os.system("cls")
			print topbar_msg
			continue

		if needs == ':his':                     # 查询历史记录
			print_db(db)
			continue

		if ':his -s' in needs:                  # 查询历史记录（只显示单词和历史查询次数）
			
			tmp_cmd = needs.split()
			if len(tmp_cmd) == 2:
                            print_summary_db(db)
                        else:
                            print_summary_db(db, int(tmp_cmd[2][1:]))  # 一行输出单词数量
			print ''
			continue

		if needs == "":		                # 无输入，只敲回车
			continue


		if ':rm' in needs:                      # 删除一个历史单词
                    rm_word_from_db(db, needs.split()[1])
                    continue
                    

		
		clr_control.set_print_yellow_text()             # 黄色输出
		print '...  '.decode('utf-8').encode('gbk'),	

		# 当输入不在结尾的位置有空格则按照句子翻译，否则就按照单词查字典
		if len(needs) == 1 or (len(needs) > 1 and ' ' in needs[:-1]):	
			result =  get_result_sentence(needs)	# 百度翻译
			print result.decode('utf-8').encode('gbk')
		else:
			result = get_result_word(needs)			# 有道词典
			print result.decode('utf-8').encode('gbk')
			if result != '...':                     # 将有效的单词存入数据库
				db_update(db, needs, result)
		
		print ''
		clr_control.set_print_green_text()  	        # 初始化输出为绿色
