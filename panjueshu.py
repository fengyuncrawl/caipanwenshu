# -*- coding: utf-8 -*-

from urllib import request,parse
import gzip,re，requests,time,random
import orm_panjueshu
import myproxy
import asyncio
from model_panjueshu import panjueshu
loop=asyncio.get_event_loop()

def create(loop):
	yield from orm_panjueshu.create_pool(loop,user='root',password='password',db='caipan')

def ungzip(data):
    try:        # 尝试解压
        print('正在解压.....')
        data = gzip.decompress(data)
        print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data
	
@asyncio.coroutine
def test(name,types,num,court,dates,url,docid,proced='null',cause='null',area='null',yiju='null',content='null'):
	p=panjueshu(name=name,cause=cause,docid=docid,area=area,proced=proced,types=types,num=num,court=court,dates=dates,yiju=yiju,content=content,url=url)
	yield from p.save()

loop.run_until_complete(create(loop))
def getcontent(num_index):
	global ip_time,proxy_ip
	str_index=str(num_index)
	url='http://wenshu.court.gov.cn/List/ListContent'

	data={'Param':'裁判年份:2016',
	'Page':'20',
	'Order':'法院层级',
	'Index':str_index,
	'Direction':'asc'

	}
	#send_data=parse.urlencode(data).encode('utf-8')
	headers={'X-Requested-With': 'XMLHttpRequest',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	#'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
	'User-Agent': 'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
	#'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
	#'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 ',
	'Connection': 'keep-alive','Host': 'wenshu.court.gov.cn'
	}
	if not proxy_ip or (int(time.time())-ip_time) > 300:
		proxy_ip={'http':'http://%s'%random.choice(myproxy.get_ip())}
		ip_time=int(time.time())
	resp=requests.post(url,data=data,headers=headers,proxies=proxy_ip,time_out=60)
	respons=resp.text

	#response=dict(response)
	#print(response)
	with open('wenjian.txt','w') as f:
		f.write(respons)
	pattern=re.compile(r'"文书ID\\":\\"(.*?)\\"')
	id_list=re.findall(pattern,respons)
	print(id_list)
	for id in id_list:
		try:		
			url_content='http://wenshu.court.gov.cn/content/content?DocID=%s'%id
			resp_content=requests.get(url_content).text
			
			#resp_content=request.urlopen(req_content).read().decode('utf-8')
			#print(resp_content)
			pattern_docid=re.compile(r'"文书ID":"(.*?)"')
			docid=re.findall(pattern_docid,resp_content)
			pattern_name=re.compile(r'"案件名称":"(.*?)"')
			name=re.findall(pattern_name,resp_content)
			pattern_proced=re.compile(r'"审判程序":"(.*?)"')
			proced=re.findall(pattern_proced,resp_content)
			pattern_types=re.compile(r'"案件类型":"(.*?)"')
			types=re.findall(pattern_types,resp_content)
			pattern_num=re.compile(r'"案号":"(.*?)"')
			num=re.findall(pattern_num,resp_content)
			pattern_court=re.compile(r'"法院名称":"(.*?)"')
			court=re.findall(pattern_court,resp_content)
			pattern_dates=re.compile(r'"裁判日期":(.*?)')
			dates=re.findall(pattern_dates,resp_content)
			loop.run_until_complete(test(name,types,num,court,dates,url_content,docid,proced))
		except:
			print('%s爬取失败'%name)

if __name__=='__main__':
	proxy_ip=None
	ip_time=0
	for i in range(1,1000):
		Index(i)
		
		



