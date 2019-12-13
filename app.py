
from flask import Flask, redirect, url_for, request, render_template, g
import random
import string
import sqlite3 as lite
import re
import os
import subprocess

app = Flask(__name__)

DATABASE = "./link.db"


# If the Database does not exist, create one and just insert something
if not os.path.exists(DATABASE):
	con = lite.connect(DATABASE)
	cursor = con.cursor()
	cursor.execute("CREATE TABLE url (ID INTEGER PRIMARY KEY AUTOINCREMENT, ORIGURL TEXT, SHORTURL TEXT UNIQUE);")
	con.commit()
	cursor.execute("INSERT INTO url VALUES('1', 'abc.com', 'xyzz');")
	con.commit()
	con.close()

# Writing the generated 4-char string and the original URL to the database. Calling "nginx-from-db.py which creates the nginx files from the database
def writeToDB(longurl, shorturl):
	con = lite.connect(DATABASE)
	cursor = con.cursor()
	cursor.execute("INSERT INTO url (ID, ORIGURL, SHORTURL) VALUES(?,?,?)", (None, longurl, shorturl) )

	con.commit()
	con.close()

	subprocess.call(["sudo", "python3", "nginx-from-db.py"])

# Creating the random string
def randomString(stringLength=4):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range (stringLength))


# Creates the nginx string needed but I changed this to read from the DB instead in "nginx-from-db.py"
#def createNginx(url, shorturl):
#	nginx = '\nlocation /'+ shorturl +' {return 301 ' + url + ';}'
#	return nginx



@app.route('/')
def index():
	return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')




@app.route('/url',methods = ['POST', 'GET'])
def index2():

        url = request.args.get('url')
        longurl = url
        pattern = re.compile(r'(http|ftp|https)://([\w-]+(?:(?:.[\w-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', re.IGNORECASE)
        result = re.search(pattern, url)
        if result:
                shorturl = randomString()
               # nginx = createNginx(url, shorturl)

                writeToDB(longurl, shorturl)

                con = lite.connect(DATABASE)
                cursor = con.cursor()
                cursor.execute("SELECT * FROM url;")
                urldata = cursor.fetchall()

                context = {'url': url, 'shorturl': shorturl}
                return render_template('url.html', **context, urldata=urldata)

        else:
                wrongurl = 'The URL provided was wrong.'
                context = {'wrongurl': wrongurl}
                return render_template('index.html', **context)



if __name__ == '__main__':
	app.run(host='192.168.1.5', port=42099, debug=True)
