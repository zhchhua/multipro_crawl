import os
import time
import threading
import multiprocessing
from mongodb_queue import MogoQueue
from Download import down
from bs4 import BeautifulSoup

SLEEP_TIME = 1

def mzitu_crawler(max_threads=10):
	crawl_queue = MogoQueue('meinvxiezhenji','crawl_queue')
	def pageurl_crawler():
		while True:
			try:
				url = crawl_queue.pop()
				print(url)
			except KeyError:
				print('队列没有数据')
				break
			else:
				img_urls = []
				req = down.get(url,3).text
				title = crawl_queue.pop_title(url)
				mkdir(title)
				os.chdir('/home/zch/py_dir/multi_pro/'+str(title))
				max_span = BeautifulSoup(req,'lxml').find('div',class_='pagenavi').find_all('span')[-2].get_text()
				for page in range(1,int(max_span)+1):
					page_url = url +'/'+ str(page)
					img_url =BeautifulSoup(down.get(page_url,3).text,'lxml').find('div',class_='main-image').find('img')['src']
					save(img_url)
				crawl_queue.complete(url)
	def save(img_url):
		name = img_url[-9:-4]
		print(u'开始保存：',img_url)
		img = down.get(img_url,3)
		f = open(name+'.jpg','ab')
		f.write(img.content)
		f.close()
	def mkdir(path):
		path = path.strip()
		isExists = os.path.exists(os.path.join("/home/zch/py_dir/multi_pro/",path))
		if not isExists:
			print(u'创建文件坚：',path)
			os.makedirs(os.path.join("/home/zch/py_dir/multi_pro/",path))
			return True
		else:
			print(u'文件夹',path,u'已经存在')
			return False
	threads = []
	while threads or crawl_queue:
		for thread in threads:
			if not thread.is_alive():
				threads.remove(thread)
		while len(threads) < max_threads or crawl_queue.peek():
			thread = threading.Thread(target=pageurl_crawler)
			thread.setDaemon(True)
			thread.start()
			threads.append(thread)
		time.sleep(SLEEP_TIME)
def process_crawler():
	process = []
	num_cpu = multiprocessing.cpu_count()
	print('将启动进程数目：',num_cpu)
	for i in range(num_cpu):
		p = multiprocessing.Process(target=mzitu_crawler)
		p.start()
		process.append(p)
	for p in process:
		p.join()
if __name__ =="__main__":
	process_crawler()
