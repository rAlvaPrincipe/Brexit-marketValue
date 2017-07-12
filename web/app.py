from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import subprocess
import sys
from decimal import Decimal
sys.path.insert(0, 'D:\Dropbox\Git_Projects\Brexit-marketValue\scripts\python')
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
	data=result[0]
	ti=[]
	ti.append(round(data[0],2))
	ti.append(round(data[1],2))
	ti.append(round(data[2],2))
	return render_template('demo.html', ti=ti, tt=result[1] , to=result[1] , filtering = result[2], data=result)

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
