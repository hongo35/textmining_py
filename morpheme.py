# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/config')

import MeCab
import MySQLdb as mysql
import config

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

	cur.execute("SELECT body FROM favorites LIMIT 10")
	res = cur.fetchall()
	for r in res:
		node = mecab.parseToNode(r[0].encode("utf-8"))
		while node:
			print node.surface + '\t' + node.feature
			node = node.next

	#node = mecab.parseToNode("今日もしないとね")
	#print node

if __name__ == '__main__':
	main()
