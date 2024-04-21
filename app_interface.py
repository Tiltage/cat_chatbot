from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_login import current_user
from datetime import timedelta
import json

import prompt as bot
import catapi as cat
import radar

app = Flask(__name__)

app.secret_key = 'hello'
app.permanent_session_lifetime = timedelta(days=1) #Session persists for defined duration

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
            return redirect(url_for('catchatbot'))
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
    # if not 'email' in session:
    #     flash('You have not logged in!')
    #     return redirect(url_for('login'))
    
    start_message = [
        {
            'sender': 'Chatty Cat',
            'content': 'Meowllo! Ask me anything!'
        },
    ]

    if 'full_history' not in session: #First time entering the page
        session['full_history'] = start_message
    
    if request.method == 'POST':
        if request.form.get('generate_new_cat'):
            return redirect(url_for('viewcat'))
        
        message_history = session['full_history']
        prompt = request.form.get('prompt')

        message_history = bot.reply(prompt, message_history)
        session['full_history'] = message_history
        
        if 'image_url' in session:
            image_url = session['image_url']
        else:
            image_url = None
        
        real_cat = session['real_cat']

    else:
        if 'json_obj' in session:
            json_obj = session['json_obj']
        else:
            json_obj = cat.get_json_obj('Random', '1', [''], '1')

        session['json_obj'] = json_obj
        session['real_cat'] = json_obj[0]['url']
    
        message_history = session['full_history']
        real_cat = session['real_cat']
        
        if 'image_url' in session:
            image_url = session['image_url']
        else:
            image_url = None
        
    return render_template('catchatbot.html', messages=message_history, image_url=image_url, real_cat=real_cat)

@app.route('/viewcat', methods=['GET', 'POST'])
def viewcat():
    # if not 'email' in session:
    #     flash('You have not logged in!')
    #     return redirect(url_for('login'))
    user_prompt = request.form.get('catpictureprompt')

    if 'image_url' not in session:
        if user_prompt is None:
            session['image_url'] = None
        else:
            session['image_url'] = bot.generate_image(f'{user_prompt}')

    image_url = session['image_url']

    json_list = []
    if 'json_obj' in session:
        json_obj = session['json_obj']
    else:
        json_obj = cat.get_json_obj('Random', '1', [''], '1')

    session['json_obj'] = json_obj
    for obj in session['json_obj']:
        json_list.append(obj)
        radar_list = radar.generate_radar_charts(json_list)

    return render_template('viewcat.html', json_list=json_list, image_url=image_url, radar_list=radar_list)

@app.route('/submit', methods=['POST'])
def submit():
    order = request.form.get('order')
    breedinfo = request.form.get('breedinfo')
    breeds = request.form.get('breed').split(',')
    number_images = request.form.get('number')
    if number_images is None:
        number_images = 1
    json_obj = cat.get_json_obj(order, breedinfo, breeds, number_images)

    session['json_obj'] = json_obj
    json_list = []
    for obj in json_obj:
        json_list.append(obj)
    session['real_cat'] = json_list

    if 'image_url' in session:
        image_url = session['image_url']
    else:
        image_url = None

    radar_list = radar.generate_radar_charts(json_list)

    for obj in json_list:
        print(json.dumps(obj, indent=4))

    return render_template('viewcat.html', json_list=json_list, image_url=image_url, radar_list=radar_list)


if __name__ == '__main__':
    app.run(debug=True)
