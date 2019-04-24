#!/usr/bin/python
import MySQLdb

# Opens database connection
db = MySQLdb.connect("localhost","root","deb0123","tweets", charset='utf8' )

cursor = db.cursor()
cursor.execute("SET session group_concat_max_len=240000")
#Query retrieving tweets grouped by userId and creationTime, for a range of two months
sql = "SELECT userId, DATE_FORMAT(creationTime, '%d %m %Y') AS datee, GROUP_CONCAT(replace(content,'\n',' ')) FROM tweets_sample where creationTime between '2010-11-01' and '2010-12-31' group by userId, datee"
file = open("tweets.txt", "w+")
try:
	# Execute the SQL command
	cursor.execute(sql)
except:
	print "Error: unable to fetch data"
for row in cursor:
		file.write(str(row).encode('utf-8'))
		file.write('\n')
file.close()
# disconnect from server
db.close()