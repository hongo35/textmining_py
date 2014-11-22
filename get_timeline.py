# -*- coding: utf-8 -*-
import MySQLdb as mysql
import twitter
import config
import datetime
from datetime import datetime as dt
import re

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

	# twitter api
	api = twitter.Api(
		consumer_key        = config.tw['consumer_key'],
		consumer_secret     = config.tw['consumer_secret'],
		access_token_key    = config.tw['access_token_key'],
		access_token_secret = config.tw['access_token_secret']
	)

	statuses = api.GetHomeTimeline()
	for s in statuses:
		ts = dt.today().strftime("%Y-%m-%d %H:%M:%S")

		japan_flag = 0
		if s.lang == "ja" or s.user.time_zone == "Tokyo" or s.user.time_zone == "Osaka" or s.user.time_zone == "Sapporo":
			japan_flag = 1

		id = s.id
		user_id = s.user.id
		user_name = s.user.screen_name
		nickname = s.user.name
		body = s.text
		ts = dt.strptime(s.created_at, "%a %b %d %H:%M:%S +0000 %Y").strftime("%Y-%m-%d %H:%M:%S")
		timezone = s.user.utc_offset / 3600
		ts_japan = (dt.strptime(s.created_at, "%a %b %d %H:%M:%S +0000 %Y") + datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")
		ts_date_japan = (dt.strptime(s.created_at, "%a %b %d %H:%M:%S +0000 %Y") + datetime.timedelta(hours=9)).strftime("%Y-%m-%d")
		tool = re.compile(r'<.*?>').sub('', s.source)
		retweet_cnt = s.retweet_count
		fav_cnt = s.favorite_count
		cnt = s.user.statuses_count
		link_cnt = s.user.friends_count
		linked_cnt = s.user.followers_count
		listed_cnt = s.user.listed_count

		try:
			cur.execute("INSERT INTO timelines(id,user_id,user_name,nickname,body,ts,timezone,ts_japan,ts_date_japan,tool,retweet_cnt,fav_cnt,cnt,link_cnt,linked_cnt,listed_cnt,created_at,updated_at) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [id,user_id,user_name,nickname,body,ts,timezone,ts_japan,ts_date_japan,tool,retweet_cnt,fav_cnt,cnt,link_cnt,linked_cnt,listed_cnt,ts,ts])
			con.commit()
		except:
			pass

	cur.close()
	con.close()

if __name__ == '__main__':
	main()
