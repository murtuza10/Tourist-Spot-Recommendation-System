from Project import app,db
from Project.models import User
from flask import Blueprint,render_template,redirect,url_for,flash,request,abort
from flask_login  import login_user,login_required,logout_user,current_user
from flask_dance.contrib.google import make_google_blueprint,google
from flask_dance.contrib.twitter import make_twitter_blueprint,twitter
from flask_dance.contrib.facebook import make_facebook_blueprint,facebook

from Project.users.views import users_blueprint
from Project.admins.views import admins_blueprint

# google_blueprint = make_google_blueprint(client_id='156026091265-u5tlf5srj1ron927kkpbs46913gtifsp.apps.googleusercontent.com',client_secret='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',offline=True,scope=['profile','email'])
# users_blueprint.register_blueprint(google_blueprint,url_prefix='/login')
# twitter_blueprint = make_twitter_blueprint(api_key='yp8b1rMHabc4EMdGiALTxbwvR',api_secret='NeqHfrxBQkV4p6ai7SltAnlVmNz2UfG8IkiYFAv4t0tX9F5zGi')
# users_blueprint.register_blueprint(twitter_blueprint,url_prefix='/login')

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/google_welcome')
def google_welcome():
    #RETURN ERROR INTERNAL SERVER ERROR IF NOT LOGGED IN
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok,resp.text
    email = resp.json()['email']
    return render_template('welcome_google_user.html',email = email)


@app.route('/login/google')
def login_google():
    if not google.authorized:
        return render_template(url_for('google.login'))
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok,resp.text
    email = resp.json()['email']
    picture = resp.json()["picture"]
    users_name = resp.json()["given_name"]


    user   = User(name=users_name,email=email,username=email)
    db.session.add(user)
    db.session.commit()
    if form.picture.data:
        pic = add_profile_pic(picture,email)
        user.profile_image = pic
    db.session.commit()
    login_user(user)
    flash("Logged in Successfully!")
    return render_template(url_for('google_welcome'),email = email,users_name=users_name)


@app.route('/welcome_twitter')
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


@app.route('/login/twitter')
def login_twitter():
    if not twitter.authorized:
        return render_template(url_for('twitter.login'))
    account_info = twitter.get('account/settings.json')

    if account_info.ok:
        account_info_json = account_info.json()
        screen_name = account_info_json['screen_name']
        return render_template('welcome_twitter_user.html',screen_name=screen_name)


@app.route('/welcome_facebook')
def facebook_welcome():
    #RETURN ERROR INTERNAL SERVER ERROR IF NOT LOGGED IN
    account_info = facebook.get('/me?fields=name,email')

    if account_info.ok:
        account_info_json = account_info.json()
        screen_name = account_info_json['name']
        email= account_info_json['email']
        return render_template('welcome_facebook_user.html',screen_name=screen_name,email=email)



@app.route('/login/facebook')
def login_facebook():
    if not facebook.authorized:
        return render_template(url_for('facebook.login'))
    account_info = facebook.get('/me?fields=name,email')

    if account_info.ok:
        account_info_json = account_info.json()
        screen_name = account_info_json['name']
        email= account_info_json['email']
        return render_template('welcome_facebook_user.html',screen_name=screen_name,email=email)

#



if __name__ =='__main__':
    app.run(debug=True,ssl_context='adhoc')
