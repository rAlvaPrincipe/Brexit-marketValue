from flask import Flask, render_template
from flask_mysqldb import MySQL
import subprocess

app = Flask(__name__)
mysql = MySQL(app)

#set up mysql options
app.config['MYSQL_HOST'] = 'db' # <-- db if docker
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'experiments'


#routes
@app.route('/')
def index():
    return render_template('index.html')

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
