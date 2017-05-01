from mongodb_queue import MogoQueue
from bs4 import BeautifulSoup
from Download import down
spider_queue = MogoQueue('meinvxiezhenji','crawl_queue')
def start(url):
		response = down.get(url,3)
		all_a = BeautifulSoup(response.text,'lxml').find('div',class_='all').find_all('a')
		for a in all_a:
			title = a.get_text()
			url = a['href']
			spider_queue.push(url,title)
if __name__ == "__main__":
	start('http://www.mzitu.com/all')
