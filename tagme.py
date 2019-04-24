import gevent.monkey
gevent.monkey.patch_socket()
from gevent.pool import Pool
import gevent
gevent.monkey.patch_socket()
gevent.monkey.patch_ssl()
import requests
import json
import time
import sys


urls = []
def check_urls(urls):

	def fetch(url):
		id = url.split(" ")[0]
		try:
			resp = requests.request('POST', url.partition(' ')[2], timeout=10.0)
		except requests.exceptions.Timeout:
			print "Timeout - will not annotate this document.\n"
			return
		except requests.exceptions.ConnectionError:
			print "Couldn't connect - will not annotate this document.\n"
			return
		if resp.status_code == 200:
			
			try:
				if len(resp.json().get("annotations"))>0:
					entities.write(id.encode('utf-8') + ' ' + 'en' + ' ')
					for annotation in resp.json().get("annotations"):
						if "Hypertext" not in annotation.get('title'):
							entities.write(annotation.get('title').replace(" ","_").encode('utf-8') + ' ')
					entities.write('\n')
			except ValueError:
				print resp.content
				pass
			except AttributeError:
				e = sys.exc_info()[0]
				print(e)
				print(sys.exc_info()[1])
				print(sys.exc_info()[2])
				pass
			except:
				pass

	pool = Pool(500)
	for url in urls:
		pool.spawn(fetch, url)
	pool.join()

with open('annotatedEntities.txt', 'w+') as entities:
	with open('tweets.txt', 'rU') as f:
		for line in f:
			line = line.replace("(","")
			line = line.replace(")","")
			line = line.replace("RT", "")
			line = line.replace("\'", "")
			urls.append((line.partition(', ')[0] + '_' + line.partition(', ')[2].partition(', ')[0]).replace(" ","") + ' https://tagme.d4science.org/tagme/tag?lang=en&gcube-token=e5fa2022-3215-4878-a738-1606a67b9400-843339462&tweet=true&epsilon=0.5&text=' + line.partition(' ')[2].partition(' ')[2].partition(' ')[2].partition(' ')[2])
		check_urls(urls)