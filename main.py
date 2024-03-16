from flask import *
import mysql.connector

app = Flask(__name__)
app.secret_key = '1581'

@app.before_request
def connection():
    con=mysql.connector.connect(
        host='92.53.96.11',
        database='sch688_etobaza',
        user='sch688_etobaza',
        password='Qwerty123')
    g.conn=con

@app.teardown_request
def close_connection(er):
    g.conn.close()

def get_user_by_login(login):
    cursor=g.conn.cursor()
    cursor.execute('SELECT * FROM users WHERE sUserLogin=%s',(login,))
    data=cursor.fetchall()
    return {'user':data}

def add_user(user):
    cursor=g.conn.cursor()
    cursor.execute('INSERT INTO users(sUserName, sUserLogin, sUserPassword, sUserPhone, sUserMail, iUserStatus, sUserSurname) VALUES (%s,%s,%s,%s,%s,%s,%s)',(user['name'], user['login'], user['paswd'], user['phnumber'], user['mail'],0,user['surname']))
    g.conn.commit()
    data=cursor.lastrowid
    return {'lastid':data}

@app.route("/")
def reg():
    return render_template('main.html')

@app.route("/login")
def log():
    return render_template('login.html')
@app.route("/admin")
def adm():
    return render_template('admin.html')

@app.route("/ajax/registration",methods=["POST"])
def ajax_rega():
    req=request.get_json()
    user=get_user_by_login(req['login'])
    if user['user']:
        user['error']='Пользователь с таким логином уже существует, придумайте другой логин'
        user['result']=False
        return jsonify(user)
    user= add_user(req)
    user['result']=True
    return jsonify(user)

@app.route('/shop')
def shop():
    if session:
        return render_template('shop.html',session = session)
    else:
        return render_template('403.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/login')


@app.route("/ajax/login",methods=["POST"])
def ajax_login():
    req=request.get_json()
    user=get_user_by_login(req['login'])
    if not user['user']:
        user['error']='Неправильный логин или пароль'
        user['result']=False
        return jsonify(user)
    if req['paswd']==user['user'][0][4]:
        user['result'] = True
        session['id'] = user['user'][0][0]
        session['name'] = user['user'][0][1]
        session['surname'] = user['user'][0][2]
        session['status'] = user['user'][0][7]
        return jsonify(user)
    user['error']='Неправильный логин или пароль'
    user['result']=False
    return jsonify(user)


if __name__ == '__main__':
    app.run(debug=True,port=8000)

