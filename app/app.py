import requests, os
from flask import Flask, request, render_template, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "root"
app.config['MYSQL_DB'] = "users"
mysql = MySQL(app)
app.secret_key = os.urandom(32)



@app.route("/", methods = ["GET","POST"])
    
def index():
    if request.method == 'GET' or request.method == 'POST':
        return render_template('index.html')

@app.route("/admin", methods = ["GET","POST"])

def admin():
    if request.remote_addr != '127.0.0.1':
    	return render_template('admin_deny.html')
    else:
        return render_template('admin.html')
        
@app.route("/login", methods = ['GET','POST'])

def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user_id = request.form['id']
        user_password = request.form['password']
        if user_id and user_password:
                cur = mysql.connection.cursor()
                cur.execute(f"SELECT * FROM user WHERE uid='{user_id}' and upw='{user_password}'")
                result = cur.fetchone()
                if not result:
                    return render_template('login_fail.html')
                else:
                    session['id'] = user_id
                    return render_template('index.html')
        else:
            return render_template('login_fail.html') 

        
@app.route("/register", methods = ['GET'])

#TODO make register function..... but not now
def register():
    return render_template('register.html')

@app.route("/crawling", methods = ['GET','POST'])

def crawling():

    if request.method == 'GET':
        return render_template('crawling.html')
    else:
        try:
            if request.form['URL']:
                url = request.form['URL']
                res = requests.get(url = url)
                if res.status_code == 200:
                    return render_template('result.html', data= res.text)
                else:
                    return render_template('error.html')
            else:
                return render_template('crawling.html')
        except:
            return render_template('error.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=4000, debug = True)
