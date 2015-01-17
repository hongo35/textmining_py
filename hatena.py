# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/config')

import requests
import hashlib
from bs4 import BeautifulSoup
import MySQLdb
import config
from datetime import datetime as dt
import time

class Hatena:
	def __init__(self):
		self.con = MySQLdb.connect(
			host    = config.db['host'],
			db      = config.db['db'],
			user    = config.db['user'],
			passwd  = config.db['passwd'],
			charset = "utf8"
		)
		self.cursor = self.con.cursor()

	def parse(self):
		rss = [
			'http://b.hatena.ne.jp/hotentry.rss',
			'http://b.hatena.ne.jp/hotentry/social.rss',
			'http://b.hatena.ne.jp/hotentry/economics.rss',
			'http://b.hatena.ne.jp/hotentry/life.rss',
			'http://b.hatena.ne.jp/hotentry/knowledge.rss',
			'http://b.hatena.ne.jp/hotentry/entertainment.rss',
			'http://b.hatena.ne.jp/hotentry/game.rss',
			'http://b.hatena.ne.jp/hotentry/fun.rss',
			'http://b.hatena.ne.jp/hotentry/it.rss',
			'http://b.hatena.ne.jp/hotentry/entertainment.rss'
		]

		for r in rss:
			res = requests.get(r)
			soup = BeautifulSoup(res.text)

			items = soup.find_all("item")
			for item in items:
				title        = item.find("title").text.encode("utf-8")
				url          = item.find("link").text
				description  = item.find("description").text
				published_at = dt.strftime(dt.strptime(item.find("dc:date").text, "%Y-%m-%dT%H:%M:%S+09:00"), "%Y-%m-%d %H:%M:%S")
				genre        = item.find("dc:subject").text
				hatebu       = item.find("hatena:bookmarkcount").text

				id = hashlib.md5(title + published_at).hexdigest()[5:17]
				ts = dt.today().strftime("%Y-%m-%d %H:%M:%S")
	
				try:
					self.cursor.execute("INSERT INTO articles(id,title,url,description,published_at,genre,hatebu,created_at,updated_at) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE hatebu = %s", [id,title,url,description,published_at,genre,hatebu,ts,ts,hatebu])
					self.con.commit()
				except:
					pass

			time.sleep(5)

if __name__ == '__main__':
	h = Hatena()
	h.parse()
