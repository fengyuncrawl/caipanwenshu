import scrapy,re,random
from panjueshu.items import PanjueshuItem
import mysql.connector
class PanjueshuSpider(scrapy.Spider):
    name='caipanwenshu'
    allowed_domains=['wenshu.court.gov.cn']
    start_urls=['http://wenshu.court.gov.cn/Index']
    user_agents=['Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
                 'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95'
        ]
    #def start_requests(self):
        #return [scrapy.FormRequest('http://wenshu.court.gov.cn/List/ListContent',formdata={'Param':'裁判年份:2016','Page':'20','Order':'法院层级','Index':'1','Direction':'asc'},headers={'X-Requested-With': 'XMLHttpRequest','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','User-Agent': 'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0','Connection': 'keep-alive','Host': 'wenshu.court.gov.cn'},callback=self.parse_id)]
    def parse(self,response):
        return scrapy.FormRequest('http://wenshu.court.gov.cn/List/ListContent',formdata={'Param':'裁判年份:2016','Page':'20','Order':'法院层级','Index':'4','Direction':'asc'},headers={'X-Requested-With': 'XMLHttpRequest','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','User-Agent': random.choice(self.user_agents),'Connection': 'keep-alive','Host': 'wenshu.court.gov.cn'},callback=self.parse_id)

    def parse_id(self,response):
        #print(response.body)
        pattern=re.compile(r'"文书ID\\":\\"(.*?)\\"')
        id_list=re.findall(pattern,response.body.decode('utf-8'))
        #print(id_list)
        for ids in id_list:
            url_next='http://wenshu.court.gov.cn/content/content?DocID=%s'%ids
            yield scrapy.Request(url_next,callback=self.parse_next,meta={'url_next':url_next})

    def parse_next(self,response):
        item=PanjueshuItem()
        caseinfo=response.xpath('//input[@id="hidCaseInfo"]/@value')
        item['name']=caseinfo.re(r'"案件名称":"(.*?)"')[0]
        item['docid']=caseinfo.re(r'"文书ID":"(.*?)"')[0]
        item['proced']=caseinfo.re(r'"审判程序":"(.*?)"')[0]
        item['types']=caseinfo.re(r'"案件类型":"(.*?)"')[0]
        item['url']=response.meta['url_next']
        item['num']=caseinfo.re(r'"案号":"(.*?)"')[0]
        item['court']=caseinfo.re(r'"法院名称":"(.*?)"')[0]
        item['dates']=caseinfo.re(r'"裁判日期":(.*?)')[0]
        item['cause']=caseinfo.re(r'"诉讼记录段原文":"(.*?)"')[0]
        #item['area']=caseinfo.re(r'')
        url_content=r'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID=%s'%item['docid']
        
        return scrapy.Request(url_content,callback=self.parse_content,meta={'item':item})

    def parse_content(self,response):
        item=response.meta['item']
        list_content=response.xpath("//div[@style='LINE-HEIGHT: 25pt;TEXT-ALIGN:justify;TEXT-JUSTIFY:inter-ideograph; TEXT-INDENT: 30pt; MARGIN: 0.5pt 0cm;FONT-FAMILY: 仿宋; FONT-SIZE: 16pt;']/text()").extract()
        item['content'] = ''.join(list_content)
        conn = mysql.connector.connect(user='root', password='', database='caipan')
        cursor = conn.cursor()
        cursor.execute('insert into panjueshu (name,docid,proced,types,url,num,court,dates,cause,content) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', [item['name'],item['docid'],item['proced'],item['types'],item['url'],item['num'],item['court'],item['dates'],item['cause'],item['content']])
        conn.commit()
        cursor.close()
        conn.close()
        return item



