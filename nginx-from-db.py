import os
import subprocess
import sqlite3 as lite
import texttable as tt

#Connect to the DB
con = lite.connect('link.db')
cursor = con.cursor()

def createNginx():
	saveFile = open('/etc/nginx/ownfiles/location-url.conf', 'a')
	saveFile.write('\nlocation /'+ str(row[2]) +' {return 301 ' + row[1] + ';}')
	saveFile.close()


def showSQL():
	tab = tt.Texttable()
	col_name = ['ID', 'ORIGURL', 'SHORTURL']
	tab.header(col_name)
	cursor.execute('SELECT ID, ORIGURL, SHORTURL FROM url')
	for row in cursor.fetchall():
		tab.add_row(row)
	s = tab.draw()
	print (s)



#showSQL()
saveFile = open('/etc/nginx/ownfiles/location-url.conf', 'w').close()

cursor.execute('SELECT * from url')
for row in cursor.fetchall():
	createNginx()

subprocess.call(["sudo", "service", "nginx", "reload"])


con.close()
