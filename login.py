from flask import Blueprint,session, Flask , render_template, url_for, request, redirect, send_from_directory

login_bp = Blueprint('login', __name__)

from db import db
from models import User

from sqlalchemy import and_

@login_bp.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if 'signinBtn' in request.form and request.form['signinBtn'] == 'Signin':        
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter(and_(User.password == password, User.email == email)).first()
            if user:
                session['user_id'] = user.id
                if user.admin == True:
                    admin_status = True
                    return redirect(url_for('dashboard', admin_status= admin_status))
                else:
                    alert_message = 'User is not Admin'
                return redirect(url_for('login', alert_message=alert_message))
            
            else:
                alert_message = 'Invalid Credentials'
                return redirect(url_for('login', alert_message=alert_message))
        
        if 'signupBtn' in request.form and request.form['signupBtn'] == 'Signup':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            
            # user = User.query.filter(and_(User.password == password, User.email == email)).first()
            user = User.query.filter(User.email == email).first()
            
            if not user:
                newUser = User(username=username, email=email, password=password, admin=True)   
                db.session.add(newUser)
                db.session.commit()
                
                session['user_id'] = newUser.id
                newUser.id = newUser.id
                return redirect(url_for('dashboard'))
            
            elif user:
                alert_message = "User Already Exist | Kindly Sign In"
                return redirect(url_for('admin_login', alert_message=alert_message))
    
    alert_message = request.args.get('alert_message', None)
    return render_template('login.html', alert_message=alert_message)



@login_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'signinBtn' in request.form and request.form['signinBtn'] == 'Signin':        
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter(and_(User.password == password, User.email == email)).first()
            if user:
                session['user_id'] = user.id
                if user.admin == True:
                    admin_status = True
                    return redirect(url_for('dashboard', admin_status=admin_status))
                else: 
                    return redirect(url_for('dashboard'))
            else:
                alert_message = 'Invalid Credentials'
                return redirect(url_for('login.login', alert_message=alert_message))
        
        if 'signupBtn' in request.form and request.form['signupBtn'] == 'Signup':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            
            # user = User.query.filter(and_(User.password == password, User.email == email)).first()
            user = User.query.filter(User.email == email).first()
            
            if not user:
                newUser = User(username=username, email=email)
                newUser = User(username=username, email=email, password=password)
                    
                db.session.add(newUser)
                db.session.commit()
                session['user_id'] = newUser.id
                newUser.id = newUser.id
                return redirect(url_for('dashboard'))
            else:
                alert_message = "User Already Exist | Kindly Sign In"
                return redirect(url_for('login', alert_message=alert_message))
    
    alert_message = request.args.get('alert_message', None)
    return render_template('login.html', alert_message=alert_message)

@login_bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))

