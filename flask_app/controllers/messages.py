from flask_app import app 
from flask import render_template, redirect, request, session
from flask_app.models import user,message

@app.route("/sendMessage",methods = ['POST'])
def send():
    data = {
        'descrip' : request.form['descrip'],
        'name' : session['name'],
        'receiver_id' : request.form['receiver_id']
    }
    message.Message.save(data)
    return redirect("/dash")

@app.route('/delete/<int:id>')
def delete(id):
    data = {'id' : id}
    message.Message.delete(data)
    return redirect('/dash')