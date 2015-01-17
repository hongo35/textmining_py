# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/config')

import MeCab
import MySQLdb as mysql
import config
import collections
import copy

from sklearn.svm import LinearSVC
import numpy as np

def main():
	data_training  = []
	label_training = []

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

	# ひな形作成
	cur.execute("SELECT body FROM public_timelines LIMIT 2000 OFFSET 100000")
	res = cur.fetchall()

	nouns = collections.defaultdict(int)
	for r in res:
		text_s = r[0].split()
		for ts in text_s:
			if not (ts.startswith("http") or ts.startswith("RT") or ts.startswith("@")):
				node = mecab.parseToNode(ts.encode("utf-8"))
				while node:
					category = node.feature.split(",")[0]
					if category == "名詞" and len(unicode(node.surface, 'utf-8')) > 1:
						if config.stop_noun.find(node.surface) == -1:
							nouns[node.surface] = 0

					node = node.next

	# Fav
	cur.execute("SELECT body FROM favorites LIMIT 1000")
	res = cur.fetchall()

	for r in res:
		nouns_copy = copy.deepcopy(nouns)
		text_s = r[0].split()
		for ts in text_s:
			if not (ts.startswith("http") or ts.startswith("RT") or ts.startswith("@")):
				node = mecab.parseToNode(ts.encode("utf-8"))
				while node:
					category = node.feature.split(",")[0]
					if category == "名詞" and len(unicode(node.surface, 'utf-8')) > 1:
						if config.stop_noun.find(node.surface) == -1:
							if node.surface in nouns_copy:
								nouns_copy[node.surface] += 1
					node = node.next
		data_training.append(nouns_copy.values())
		label_training.append(1)

	# Non-Fav
	cur.execute("SELECT body FROM public_timelines LIMIT 1500")
	res = cur.fetchall()

	for r in res:
		nouns_copy = copy.deepcopy(nouns)
		text_s = r[0].split()
		for ts in text_s:
			if not (ts.startswith("http") or ts.startswith("RT") or ts.startswith("@")):
				node = mecab.parseToNode(ts.encode("utf-8"))
				while node:
					category = node.feature.split(",")[0]
					if category == "名詞" and len(unicode(node.surface, 'utf-8')) > 1:
						if config.stop_noun.find(node.surface) == -1:
							if node.surface in nouns_copy:
								nouns_copy[node.surface] += 1
					node = node.next
		data_training.append(nouns_copy.values())
		label_training.append(-1)
	
	# 学習
	estimator = LinearSVC(C=1.0)
	estimator.fit(data_training, label_training)


	cur.execute("SELECT body FROM timelines LIMIT 100")
	res = cur.fetchall()

	for r in res:
		nouns_copy = copy.deepcopy(nouns)
		text_s = r[0].split()
		for ts in text_s:
			if not (ts.startswith("http") or ts.startswith("RT") or ts.startswith("@")):
				node = mecab.parseToNode(ts.encode("utf-8"))
				while node:
					category = node.feature.split(",")[0]
					if category == "名詞" and len(unicode(node.surface, 'utf-8')) > 1:
						if config.stop_noun.find(node.surface) == -1:
							if node.surface in nouns_copy:
								nouns_copy[node.surface] += 1
					node = node.next
		label_prediction = estimator.predict(nouns_copy.values())
		if label_prediction == 1:
			print "%s: %s", r[0], label_prediction

if __name__ == '__main__':
	main()
