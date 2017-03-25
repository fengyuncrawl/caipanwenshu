此文件夹内容为使用scrapy框架抓取中国裁判文书网的判决文书并存入mysql数据库。具体操作为：
1.利用caipan.sql在mysql中创建数据库:caipan和数据表panjueshu
2.在已安装python3.5以及scrapy框架的基础上，将caipanwenshu文件夹移植到C盘（或其他盘）某路径下
3.在cmd命令行下进入caipanwenshu根目录输入：scrapy crawl caipanwenshu 回车后程序运行
4.爬取的index在Panjueshu.py中parse方法的for index in range(?,?)中，理论上可以爬取上万页
5.注意Panjueshu.py中数据库连接的建立要以自己的用户名密码为准：conn = mysql.connector.connect(user='root', password='', database='caipan')
