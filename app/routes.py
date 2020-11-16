from flask import render_template, flash, redirect, url_for, request, session, json as flask_json
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db, socketio
from app.forms import LoginForm, RegistrationForm
from app.models import User


# server socket io stuff
import json
import eventlet
from flask_socketio import SocketIO, send, emit, join_room, leave_room, \
    Namespace, disconnect

disconnect = None


@app.route('/')
@app.route('/index')
@login_required
def index():
    '''
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    '''
    # create namespace for user here
    # also create session?
    print(current_user.username)
    print(current_user.email)

    # remove spaces and add forward slash to create namespace
    temp_namespace = "/" + (current_user.username).replace(" ", "")
    print(temp_namespace)

    # create a namespace for a user profile
    socketio.on_namespace(MyNamespace(temp_namespace))

    return render_template('index.html', title='Home')#, posts=posts)

    #return render_template('session.html', title='Home')

"""
@app.route('/session')
def login():
    return render_template('session.html', title='Sign In')
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


class MyNamespace(Namespace):

    def __init__(self, namespace):
        super(Namespace, self).__init__(namespace)
        self.ns = namespace
        self.passcode = 'XXXXXX'
        self.master = False
        self.m = 0
        self.primarySid = ""
        self.sidList = []

    def connect(self):
        print('connect before authenticate')
        if not self.authenticate(request.args):
            print('not authenticate')
        else:
            print('authenticate')

    def on_connect(self):
        print(current_user)
        if self.master is False:                # checks if namespace has a master
            #if current_user.is_authenticated:   # if no master incomming connection must be authenticated 
            if request.args.get('fail'):
                return False
            print('authenticated sid: ' + request.sid)
            # send ns and master
            data = {"namespace":self.ns, "sid":request.sid, "master":self.master}
            #data = {"namespace":self.ns, "sid":request.sid, "m":self.m}
            socketio.emit('on_web_connect', data, namespace=self.ns)
        else:
            if request.args.get('fail'):
                    return False
            print('connecting sid: ' + request.sid)
            # send ns and master
            data = {"namespace":self.ns, "sid":request.sid, "master":self.master}
            #data = {"namespace":self.ns, "sid":request.sid, "m":self.m}
            socketio.emit('on_connect', data, namespace=self.ns)
    
    def on_disconnect(self):
        global disconnected
        disconnected = Namespace
        #disconnected = '/ns'

    def on_message(self, message):
        send(message)
        print(message)

    def on_event(self, data):
        print(data)

    def on_toServer(self, data):
        print(data)
        socketio.emit('server response', 'got your message')

    def on_establishWebMaster(self, data):
        print(data)
        retData = json.loads(data)
        # this sid will become primary sid and have control over namespace
        if retData["master"] is True:
            self.master = True
            self.passcode = retData["passcode"]
            self.primarySid = retData["masterSid"]
            self.sidList.append(retData["masterSid"])
            confData = {"sid":request.sid}
            #socketio.emit('webMasterConfirmation', confData, namespace=self.ns)

    def on_espTryVerify(self, data):
        # check if passcode is correct
        if (self.passcode) == (data["passcode"]) and (self.ns) == (data["namespace"]):
            # add sid to registered sid list and send confirmation of verification
            self.sidList.append(data["sid"])
            confData = {"verified":True, "sid":request.sid}
            socketio.emit('espClientVerified', confData, namespace=self.ns)

    def on_esp_to_server(self, msg):
        print(' server transfer server -> web')
        # check if esp sending message is registered with namespace
        if request.sid in self.sidList:
            emit('server_to_web', msg, namespace=self.ns, broadcast=True)
            print(msg)

    def on_web_to_server(self, msg):
        print(' server transfer server -> esp')
        # check if web sending message is registered as master of namespace
        if request.sid in self.sidList and request.sid == self.primarySid:
            emit('server_to_esp', msg, namespace=self.ns, broadcast=True)
            print(msg)

    def on_exit(self, data):
        disconnect()
