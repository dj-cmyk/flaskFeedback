from flask import Flask, render_template, redirect, request, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback 
from forms import RegisterUserForm, LoginForm, FeedbackForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'aksdjf;iei9203kjaas'

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def display_home_page():
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def display_register_page():
    '''docstring'''
    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()
        
        session['username'] = new_user.username
        # flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def display_login_page():
    '''docstring'''
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
    
        user = User.authenticate(username, password)
        if user:
            # flash(f"Welcome Back, {user.username}!", "primary")
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    session.pop('username')
    # flash("Goodbye!", "info")
    return redirect('/')


@app.route('/users/<username>')
def display_secret_page(username):
    if ('username' in session) and (username == session['username']):
        user = User.query.get_or_404(username)
        return render_template('secret.html', user=user)
    else:
        return redirect('/login')


@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    if ('username' in session) and (username == session['username']):
        session.pop('username')
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/login')


@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_user_feedback(username):
    '''docstring'''
    if ('username' in session) and (username == session['username']):
        form = FeedbackForm()
        user = User.query.get_or_404(username)

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            new_feedback_entry = Feedback(title=title, content=content, username=username)

            db.session.add(new_feedback_entry)
            db.session.commit()   
            return redirect(f'/users/{user.username}') 

        return render_template('add-feedback.html', user=user, form=form)
    else:
        return redirect('/login')

@app.route('/feedback/<id>/update', methods=["GET", "POST"])
def edit_user_feedback(id):
    '''docstring'''
    feedback = Feedback.query.get_or_404(id)
    if ('username' in session) and (feedback.username == session['username']):
        form = FeedbackForm(obj=feedback)

        if form.validate_on_submit():
            feedback.title = request.form.get("title", feedback.title)
            feedback.content = request.form.get("content", feedback.content)

            db.session.commit()
            return redirect(f'/users/{feedback.username}')
        else:
            return render_template('edit-feedback.html', form=form)
    else:
        return redirect('/login')    


@app.route('/feedback/<id>/delete', methods=["POST"])
def delete_user_feedback(id):
    '''docstring'''
    if ('username' in session) and (feedback.username == session['username']):
        feedback = Feedback.query.get_or_404(id) 
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    else:
        return redirect('/login')    
