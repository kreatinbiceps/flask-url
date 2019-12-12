
from flask import Flask, redirect, url_for, request, render_template, g
import random
import string
import sqlite3 as lite
import re
import os

app = Flask(__name__)

DATABASE = "./link.db"

if not os.path.exists(DATABASE):
    con = lite.connect(DATABASE)
    cursor = con.cursor()
    cursor.execute("CREATE TABLE url (ID INTEGER PRIMARY KEY AUTOINCREMENT, ORIGURL TEXT, SHORTURL TEXT UNIQUE);")
    con.commit()
    cur.execute("INSERT INTO url VALUES('', 'abc.com', 'xyzz');")
    con.commit()
    con.close

def randomString(stringLength=4):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range (stringLength))



def createNginx(url, shorturl):
	nginx = '\nlocation /'+ shorturl +' {return 301 ' + url + ';}'
	return nginx



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/url',methods = ['POST', 'GET'])
def index2():
    #connect to the database


    url = request.args.get('url')
    pattern = re.compile(r'(http|ftp|https)://([\w-]+(?:(?:.[\w-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', re.IGNORECASE)
    result = re.search(pattern, url)
    if result:
        shorturl = randomString()
        nginx = createNginx(url, shorturl)
        context = {'url': url, 'shorturl': shorturl, 'nginx': nginx}
        return render_template('url.html', **context)

    else:
        wrongurl = 'The URL provided was wrong.'
        context = {'wrongurl': wrongurl}
        return render_template('index.html', **context)



if __name__ == '__main__':
   app.run(host='192.168.1.5', port=42099, debug=True)
