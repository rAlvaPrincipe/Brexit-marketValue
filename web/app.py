from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import sys, os, subprocess
# same as cd /web/ --> cd ../ --> cd src
lib_path = os.path.abspath(os.path.join('..', 'src'))
sys.path.append(lib_path)
from calculator import Calculator

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
	calc = Calculator()
	result = calc.start(str(request.form.get('dictionary')), str(request.form.get('typo')), float(request.form.get('tr-tollerance')), float(request.form.get('sm-tollerance')), int(request.form.get('discretization')))

	return render_template('demo.html', data=result)

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

# @app.route('/main')
# def main():
#     a = "subprocess?"
#     return str(a)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
