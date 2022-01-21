from datetime import datetime
from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from datetime import datetime
import timeago
# api to compute time difference, took two datetime object as param
#pipenv install timeago to start 
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dash')
def dash():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    user = User.get_message(data)
    if user.count > 0:
        for i in user.message:
            
            now = datetime.now()
            i.time = timeago.format(i.created_at, now)
    return render_template('dash.html',user = user, users = User.get_all())

@app.route('/create', methods = ['POST'])
def create():
    if not User.validate(request.form):
        return redirect('/')
    
    password = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : password
    }
    
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dash')

@app.route('/login', methods = ['POST'])
def login():
    user = User.get_one(request.form)
    if not user:
        flash("Invalid Email/Password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect('/')
    
    session['user_id'] = user.id
    session['name'] = user.first_name
    return redirect('/dash')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
