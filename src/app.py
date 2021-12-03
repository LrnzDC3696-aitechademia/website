from flask import Flask, render_template, redirect, url_for, session, request
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I am a website' 
socketio = SocketIO(app)

NAME_KEY = 'name'


@app.route('/login', methods = ['POST', 'GET'])
def login():

    if request.method == 'GET' and NAME_KEY in session:
        return redirect(url_for("home"))

    # if user input a name
    elif request.method == "POST":
        name = request.form["username"]
        if len(name) == 0:
            name = 'di mo sure' 
        session[NAME_KEY] = name
        return redirect(url_for("home"))

    return render_template("login.html")


@app.route('/logout', methods = ['POST', 'GET'])
def logout():
    session.pop(NAME_KEY)
    return redirect(url_for('login'))


@app.route('/')
@app.route('/home', methods=['POST', 'GET'])
def home():
    if NAME_KEY not in session:
        return redirect(url_for('login'))

    return render_template('home.html', username=session[NAME_KEY])


@app.route('/chat', methods=['POST', 'GET'])
def chat():
    return render_template('chat.html')



@socketio.on('message')
def handleMessage(msg):
    print('Message:' + msg)
    send(msg, broadcast=True)

