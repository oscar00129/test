from flask import Flask, render_template, session, request, redirect
from flask_socketio import SocketIO, send
from datetime import datetime
import mysql.connector, json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

listaJSON = []

@app.route('/')
def index():
    if 'user' in session:
        return redirect('/chat')
    return render_template('index.html')

@app.route('/chat/')
def chat():
    if 'user' in session:
        return render_template('chat.html', user = session['user'])
    return redirect("/")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    u = request.form['user']
    u = u.lower()
    p = request.form['pass']
    p = p.lower()
    
    try:
        mydb = mysql.connector.connect( host="127.0.0.1", user="root", passwd="", database="pruebaFlask")
        mycursor = mydb.cursor()
        iniciado = False

        query = "select * from users where nombre = %s"
        tupla = (u, )

        mycursor.execute(query, tupla)
        rs = mycursor.fetchall()

        for row in rs:
            if row[2] == p:
                iniciado = True

        if iniciado:
            session['user'] = u
            return redirect('/chat')
        else:
            return redirect('/')
        
    except mysql.connector.Error as err:
        return "Something went wrong: {}".format(err)

    

    

@socketio.on('message')
def handleMsg(jsonString):
    listaJSON.append(jsonString)
    send(jsonString, broadcast = True)


if __name__ == '__main__':
    app.run(port = 3000, debug = True)