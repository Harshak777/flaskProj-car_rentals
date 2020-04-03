from flask import *

from flask_mysqldb import MySQL

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_DB'] = 'MyDB'

mysql = MySQL(app)



@app.route('/', methods=['POST','GET'])
def mai():
    return render_template('welcome___1.html')


@app.route('/signup', methods=['POST','GET'])
def index():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        password = details['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO MyUsers(firstName, password) VALUES (%s, %s)", (firstName, password))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('signup.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        password = details['password']
        cur = mysql.connection.cursor()
        qwe=cur.execute("SELECT * FROM MyUsers where firstname=%s AND password = %s",[firstName,password])
        if qwe == 1:
            resp = make_response(render_template('user.html')) 
            resp.set_cookie('name', firstName)
            session['currentuser'] = firstName
            return resp
        else:
            return 'wrong password. Go back and try again'
    return render_template('login.html')    

@app.route('/user', methods=['POST','GET'])
def user():
    return render_template('user.html')


@app.route('/book', methods=['POST','GET'])
def book():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM car")
    data = cur.fetchall()
    return render_template('book.html',name=session['currentuser'], data=data)

@app.route('/success/<name>', methods=['POST','GET'])
def suc(name):
    cur = mysql.connection.cursor()
    cur.execute("delete from car where carname = %s",[name])
    mysql.connection.commit()
    cur.close()
    return "Booking Successfull"

@app.route('/c',methods=['POST','GET'])
def cook():
    name = request.cookies.get('name')
    return '<h1>welcome '+name+'</h1>'

if __name__ == '__main__':
    app.run(debug=True)