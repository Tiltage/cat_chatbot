from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import timedelta
import asyncio

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

import prompt as bot
from user import User

app = Flask(__name__)

app.secret_key = 'hello'
app.permanent_session_lifetime = timedelta(minutes=5) #Session persists for defined duration

@app.route('/') #Default domain
def home():
    return render_template('homepage.html')
 
@app.route('/user', methods=['POST','GET']) #References URL extension
def user():
    if 'email' in session:
        email = session['email']

        if request.method == 'POST':
            email = request.form['email']
            session['email'] = email
            flash('Email updated!', 'info')
            return render_template('user.html', email=email)
        else:
            return render_template('user.html')
    else:
        flash('You have not logged in!')
        return redirect(url_for('login'))

@app.route('/admin/') #Prevents unauthorised access, extra end slash to intialise new subfolder
def admin():
    flash('You do not have the required permissions to enter this site')
    return redirect(url_for('user')) #Name of function that we call to redirect

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        session['email'] = email
        if email:
            flash('Logged in successfully!', category='success')
            return redirect(url_for('user', email=email))
        else:
            flash('Incorrect password, try again.', category='error')
    else:
        flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@app.route('/logout')
def logout():
    if 'email' in session: #Already logged in
        email = session['email']
        flash(f'You have sucessfully logged out {email}', 'info')
    session.pop('email', None)
    session.pop('full_history', None)
    return redirect(url_for('login'))

@app.route('/catchatbot', methods=['GET', 'POST'])
def catchatbot():
    if not 'email' in session:
        flash('You have not logged in!')
        return redirect(url_for('login'))
    
    start_message = [
        {
            'sender': 'ChattyCat',
            'content': 'Meowllo! Ask me anything!'
        },
    ]
    print(session)

    if not 'full_history' in session: #First time entering the page
        print('Initialising message history')
        session['full_history'] = start_message
        session['image_url'] = bot.generate_image()
        print(session['image_url'])
    
    if request.method == 'POST':
        message_history = session['full_history']
        prompt = request.form.get('prompt')
        # request.form={} #Clear request form to prevent resubmission on page refresh

        message_history = bot.reply(prompt, message_history) #Instantiate image_url and keep it constant throughout a user's use.
        session['full_history'] = message_history
        
        if 'image_url' in session:
            image_url = session['image_url']
        else:
            image_url = None
        print(message_history)

    
    return render_template('catchatbot.html', messages=message_history, image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
