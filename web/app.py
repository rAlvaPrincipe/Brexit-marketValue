from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import sys, os, subprocess
# same as cd /web/ --> cd ../ --> cd src
lib_path = os.path.abspath(os.path.join('..', 'src'))
sys.path.append(lib_path)
from interface import Interface
from sentiment import Sentiment

app = Flask(__name__)
mysql = MySQL(app)

#set up mysql options
app.config['MYSQL_HOST'] = '127.0.0.1' # <-- db if docker
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'experiments'


#routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo', methods=['GET','POST'])
def demo():
	return render_template('demo.html')
@app.route('/handle_data', methods=['GET','POST'])
def handle_data():
	interface = Interface()
	result = interface.compute(str(request.form.get('dictionary')), int(request.form.get('mk-discretization')), int(request.form.get('sm-discretization')), str(request.form.get('typo')), float(request.form.get('tr-tollerance')), float(request.form.get('sm-tollerance')))
	data=result[0]
	ti=[]
	ti.append(round(data[0],2))
	ti.append(round(data[1],2))
	ti.append(round(data[2],2))

	return render_template('demo.html', ti=result[0], tt=result[1] , to=result[2].transpose(), oss_row=result[2].__len__(), oss_col=len(result[2].columns), tr_row=result[1].__len__(), tr_col=len(result[1].columns), data=result)


#sentiment
@app.route('/sentiment', methods=['POST', 'GET'])
def sentiment():
    if request.method == 'POST':
        tweet = str(request.form['tweet'])
        dictionary = str(request.form['dictionary'])
        sentiment = "<here calculate sentiment!>"
        return render_template('sentiment.html', tweet=tweet, dictionary=dictionary, sentiment=sentiment)
    else:
        return render_template('sentiment.html')

#tweets
@app.route('/tweets')
@app.route('/tweets/<name>/<offset>/<limit>')
def tweets(offset=0,limit=10,name="tweets"):
    if int(offset) < 0:
        offset = 0
    if int(limit) < 0:
        limit=10

    cur = mysql.connection.cursor()
    cur.execute("SELECT id_tweet, tweet, tweet_date  FROM "+name+" LIMIT "+str(offset)+", "+str(limit))
    result = cur.fetchall()
    data = {}
    for row in result:
        data[str(row[0])] = (row[1],row[2])

    return render_template('tweets.html',data=data, name=name, offset=offset, limit=limit)


# dictionaries
@app.route('/dictionary')
@app.route('/dictionary/<name>/<offset>/<limit>')
def dictionary(offset=0,limit=10,name="bing"):
    if int(offset) < 0:
        offset = 0
    if int(limit) < 0:
        limit=10

    cur = mysql.connection.cursor()
    cur.execute("SELECT word, label FROM "+name+" LIMIT "+str(offset)+", "+str(limit))
    result = cur.fetchall()
    data = {}
    for row in result:
        data[str(row[0])] = row[1]

    return render_template('dictionary.html',data=data, name=name, offset=offset, limit=limit)

# 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0')
