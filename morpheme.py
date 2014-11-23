# -*- coding: utf-8 -*-
import sys
sys.path.append('config')

import MeCab
import MySQLdb as mysql
import config
import collections

def main():
	# db接続
	con = mysql.connect(
		host    = config.db['host'],
		user    = config.db['user'],
		passwd  = config.db['passwd'],
		db      = config.db['db'],
		charset = 'utf8'
	)
	cur = con.cursor()

	mecab = MeCab.Tagger()

	cur.execute("SELECT body FROM favorites lIMIT 100")
	res = cur.fetchall()

	fav_nouns = collections.defaultdict(int)
	for r in res:
		text_s = r[0].split()
		for ts in text_s:
			if not (ts.startswith("http") or ts.startswith("RT") or ts.startswith("@")):
				node = mecab.parseToNode(ts.encode("utf-8"))
				while node:
					category = node.feature.split(",")[0]
					if category == "名詞" and len(unicode(node.surface, 'utf-8')) > 1:
						if config.stop_noun.find(node.surface) == -1:
							fav_nouns[node.surface] += 1

					node = node.next

	for k,v in sorted(fav_nouns.items(), key=lambda x: x[1]):
		print "%s: %d", k,v

if __name__ == '__main__':
	main()
