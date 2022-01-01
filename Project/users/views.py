from flask import Blueprint,render_template,redirect,url_for,flash,request,abort
from Project import db
from flask_login  import login_user,login_required,logout_user,current_user
from Project.models import User
from Project.users.forms import UserRegistrationForm,UserLoginForm
from Project.users.picture_handler import add_profile_pic
from flask_dance.contrib.google import make_google_blueprint,google
from flask_dance.contrib.twitter import make_twitter_blueprint,twitter
from flask_dance.contrib.facebook import make_facebook_blueprint,facebook
import datetime


users_blueprint = Blueprint('users',__name__, template_folder = 'templates/users')
# google_blueprint = make_google_blueprint(client_id='156026091265-u5tlf5srj1ron927kkpbs46913gtifsp.apps.googleusercontent.com',client_secret='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',offline=True,scope=['profile','email'])
# app.register_blueprint(google_blueprint,url_prefix='/login')
# twitter_blueprint = make_twitter_blueprint(api_key='yp8b1rMHabc4EMdGiALTxbwvR',api_secret='NeqHfrxBQkV4p6ai7SltAnlVmNz2UfG8IkiYFAv4t0tX9F5zGi')
# app.register_blueprint(twitter_blueprint,url_prefix='/login')


@users_blueprint.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out!")
    return redirect(url_for('index'))


@users_blueprint.route('/login',methods=['GET','POST'])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("Logged in Successfully!")
            next = request.args.get('next')
            if next is None or not next[0]=='/':
                next = url_for('users.welcome_user')
            return redirect(next)
    return render_template('user.html',form=form)

@users_blueprint.route('/register',methods=['GET','POST'])
def register():
    form = UserRegistrationForm()

    if form.validate_on_submit():
        user   = User(name=form.name.data,email=form.email.data,dob=form.dob.data,gender=form.gender.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        if form.picture.data:
            pic = add_profile_pic(form.picture.data,form.username.data)
            user.profile_image = pic
        db.session.commit()
        flash("Thanks for registration!")
        return redirect(url_for('users.login'))
    return render_template('user_register.html',form=form)

@users_blueprint.route('/account',methods=['GET','POST'])
@login_required
def account():
    profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html',profile_image=profile_image,form=form)


@users_blueprint.route('/welcome_google')
def google_welcome():
    #RETURN ERROR INTERNAL SERVER ERROR IF NOT LOGGED IN
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok,resp.text
    email = resp.json()['email']
    return render_template('welcome_google_user.html',email = email)


@users_blueprint.route('/login/google')
def login_google():
    if not google.authorized:
        return render_template(url_for('google.login'))
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok,resp.text
    email = resp.json()['email']
    picture = resp.json()["picture"]
    users_name = resp.json()["given_name"]

    user = User.query.filter_by(email=email).first()
    if user is None:
        x = datetime.datetime(1990, 10, 10)
        user   = User(name=users_name,email=email,dob=x,gender='NA',username=email,password='NA')
        db.session.add(user)
        db.session.commit()
        if picture:
            pic = add_profile_pic(picture,email)
            user.profile_image = pic
        db.session.commit()
    login_user(user)
    flash("Logged in Successfully!")
    #return render_template(url_for('users.google_welcome'),email = email,users_name=users_name)
    return render_template('welcome_google_user.html',email = email,users_name=users_name)

@users_blueprint.route('/welcome_twitter')
def twiter_welcome():
    #RETURN ERROR INTERNAL SERVER ERROR IF NOT LOGGED IN
    account_info = twitter.get('account/settings.json')
    # assert account_info.ok,account_info.text
    # account_info_json = account_info.json()
    # screen_name = account_info_json['screen_name']
    # return render_template('welcome_twitter_user.html',screen_name=screen_name)
    if account_info.ok:
        account_info_json = account_info.json()
        screen_name = account_info_json['screen_name']
        return render_template('welcome_twitter_user.html',screen_name=screen_name)


@users_blueprint.route('/login/twitter')
def login_twitter():
    if not twitter.authorized:
        return render_template(url_for('twitter.login'))
    account_info = twitter.get('account/settings.json')

    if account_info.ok:
        account_info_json = account_info.json()
        screen_name = account_info_json['screen_name']
        email = account_info_json['screen_name']
        user = User.query.filter_by(email=email).first()
        if user is None:
            x = datetime.datetime(1990, 10, 10)
            user   = User(name=screen_name,email=email,dob=x,gender='NA',username=email,password='NA')
            db.session.add(user)
            db.session.commit()
            if picture:
                pic = add_profile_pic(picture,email)
                user.profile_image = pic
            db.session.commit()
        login_user(user)
        flash("Logged in Successfully!")
        return render_template('welcome_twitter_user.html',screen_name=screen_name)





@users_blueprint.route('/welcome_facebook')
def facebook_welcome():
    #RETURN ERROR INTERNAL SERVER ERROR IF NOT LOGGED IN
    account_info = facebook.get('/me?fields=name,email')

    if account_info.ok:
        account_info_json = account_info.json()
        screen_name = account_info_json['name']
        email= account_info_json['email']
        return render_template('welcome_facebook_user.html',screen_name=screen_name,email=email)



@users_blueprint.route('/login/facebook')
def login_facebook():
    if not facebook.authorized:
        return render_template(url_for('facebook.login'))
    account_info = facebook.get('/me?fields=name,email')

    if account_info.ok:
        account_info_json = account_info.json()
        screen_name = account_info_json['name']
        email= account_info_json['email']
        user = User.query.filter_by(email=email).first()
        if user is None:
            x = datetime.datetime(1990, 10, 10)
            user   = User(name=screen_name,email=email,dob=x,gender='NA',username=email,password='NA')
            db.session.add(user)
            db.session.commit()
            if picture:
                pic = add_profile_pic(picture,email)
                user.profile_image = pic
            db.session.commit()
        login_user(user)
        flash("Logged in Successfully!")
        return render_template('welcome_facebook_user.html',screen_name=screen_name,email=email)
